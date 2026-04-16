import subprocess
import tempfile
import os
import json

def run_slither(solidity_code):
    vulnerabilities = []

    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.sol',
        delete=False,
        dir=tempfile.gettempdir()
    ) as f:
        f.write(solidity_code)
        temp_path = f.name

    try:
        result = subprocess.run(
            ['slither', temp_path, '--json', '-', '--solc-remaps', '@=@'],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Try to parse stdout
        output = result.stdout.strip()
        if output:
            try:
                data = json.loads(output)
                detectors = data.get('results', {}).get('detectors', [])
                for item in detectors:
                    vulnerabilities.append({
                        "name": item.get('check', 'Unknown'),
                        "severity": item.get('impact', 'Unknown'),
                        "description": item.get('description', ''),
                        "lines": []
                    })
            except json.JSONDecodeError:
                pass

        # If no results from stdout, check stderr
        if not vulnerabilities and result.stderr:
            lines = result.stderr.strip().split('\n')
            for line in lines:
                if 'Reference:' in line:
                    continue
                if any(x in line for x in [
                    'reentrancy', 'Reentrancy',
                    'suicidal', 'Suicidal',
                    'uninitialized', 'Uninitialized',
                    'locked-ether', 'arbitrary-send',
                    'controlled-delegatecall',
                    'msg-value-loop', 'tautology'
                ]):
                    vulnerabilities.append({
                        "name": line.split('(')[0].strip(),
                        "severity": get_severity(line),
                        "description": line.strip(),
                        "lines": []
                    })

        # If still nothing — run basic check
        if not vulnerabilities:
            vulnerabilities = basic_check(solidity_code)

    except FileNotFoundError:
        vulnerabilities = basic_check(solidity_code)
    except Exception as e:
        vulnerabilities = basic_check(solidity_code)
    finally:
        try:
            os.unlink(temp_path)
        except:
            pass

    return vulnerabilities


def get_severity(line):
    line_lower = line.lower()
    if any(x in line_lower for x in ['high', 'critical']):
        return 'High'
    elif 'medium' in line_lower:
        return 'Medium'
    else:
        return 'Low'


def basic_check(code):
    """Manual pattern detection as fallback"""
    vulnerabilities = []
    code_lower = code.lower()

    checks = [
        {
            "pattern": ".call{value",
            "name": "reentrancy",
            "severity": "High",
            "description": "Reentrancy vulnerability detected. The contract sends ETH with .call{value} before updating state. A malicious contract could repeatedly call withdraw() and drain funds."
        },
        {
            "pattern": "tx.origin",
            "name": "tx-origin",
            "severity": "High",
            "description": "Use of tx.origin for authorization. This can be exploited by phishing attacks. Use msg.sender instead."
        },
        {
            "pattern": "selfdestruct",
            "name": "suicidal",
            "severity": "High",
            "description": "Contract contains selfdestruct. If not properly protected, anyone could destroy the contract."
        },
        {
            "pattern": "block.timestamp",
            "name": "timestamp-dependence",
            "severity": "Medium",
            "description": "Contract relies on block.timestamp which can be manipulated by miners within a small range."
        },
        {
            "pattern": "assembly",
            "name": "assembly-usage",
            "severity": "Low",
            "description": "Contract uses inline assembly which bypasses Solidity safety checks."
        }
    ]

    for check in checks:
        if check["pattern"].lower() in code_lower:
            vulnerabilities.append({
                "name": check["name"],
                "severity": check["severity"],
                "description": check["description"],
                "lines": []
            })

    return vulnerabilities