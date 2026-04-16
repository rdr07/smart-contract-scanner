import re

def run_slither(solidity_code):
    return basic_check(solidity_code)

def basic_check(code):
    vulnerabilities = []
    code_lower = code.lower()

    checks = [
        {
            "name": "Reentrancy Attack",
            "pattern": ".call{value:",
            "severity": "HIGH",
            "description": "External call before state update — classic reentrancy vulnerability. Use checks-effects-interactions pattern."
        },
        {
            "name": "Integer Overflow/Underflow",
            "pattern": "uint",
            "severity": "MEDIUM",
            "description": "Unprotected arithmetic may overflow. Use SafeMath or Solidity 0.8+ built-in overflow checks."
        },
        {
            "name": "Unchecked Return Value",
            "pattern": ".send(",
            "severity": "MEDIUM",
            "description": "Return value of send() not checked. Use transfer() or check return value."
        },
        {
            "name": "tx.origin Authentication",
            "pattern": "tx.origin",
            "severity": "HIGH",
            "description": "tx.origin used for authentication — vulnerable to phishing attacks. Use msg.sender instead."
        },
        {
            "name": "Timestamp Dependence",
            "pattern": "block.timestamp",
            "severity": "LOW",
            "description": "Block timestamp can be manipulated by miners within ~15 seconds."
        },
        {
            "name": "Delegatecall Risk",
            "pattern": "delegatecall",
            "severity": "HIGH",
            "description": "delegatecall executes code in caller's context — can overwrite storage if misused."
        },
        {
            "name": "Selfdestruct Risk",
            "pattern": "selfdestruct",
            "severity": "HIGH",
            "description": "Contract can be destroyed and ETH forcibly sent. Ensure proper access control."
        },
        {
            "name": "Inline Assembly",
            "pattern": "assembly",
            "severity": "MEDIUM",
            "description": "Inline assembly bypasses Solidity safety checks. Review carefully."
        },
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