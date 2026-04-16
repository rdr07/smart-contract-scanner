const API_URL = 'https://smart-contract-scanner.onrender.com';

async function scanCode() {
    const code = document.getElementById('solidityCode').value;
    
    if (!code.trim()) {
        alert('Please paste your Solidity code first!');
        return;
    }

    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('scanBtn').disabled = true;

    try {
        const response = await fetch(`${API_URL}/scan`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        alert('Error connecting to scanner. Make sure backend is running!');
        console.error(error);
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('scanBtn').disabled = false;
    }
}

function displayResults(data) {
    const results = document.getElementById('results');
    results.classList.remove('hidden');

    // Count severities
    let high = 0, medium = 0, low = 0;
    data.vulnerabilities.forEach(v => {
        if (v.severity === 'High') high++;
        else if (v.severity === 'Medium') medium++;
        else low++;
    });

    // Show stats
    document.getElementById('summaryStats').innerHTML = `
        <div class="stat-box stat-total">Total: ${data.total_found}</div>
        <div class="stat-box stat-high">🔴 High: ${high}</div>
        <div class="stat-box stat-medium">🟠 Medium: ${medium}</div>
        <div class="stat-box stat-low">🟡 Low: ${low}</div>
    `;

    // Show vulnerability cards
    const vulnList = document.getElementById('vulnList');
    if (data.vulnerabilities.length === 0) {
        vulnList.innerHTML = `
            <div style="text-align:center; padding:30px; color:#00ff88; font-size:1.2rem">
                ✅ No vulnerabilities found! Your contract looks safe.
            </div>`;
    } else {
        vulnList.innerHTML = data.vulnerabilities.map(v => `
            <div class="vuln-card ${v.severity}">
                <div class="vuln-header">
                    <span class="vuln-name">⚠️ ${v.name}</span>
                    <span class="severity-badge badge-${v.severity}">${v.severity}</span>
                </div>
                <p class="vuln-desc">${v.description}</p>
            </div>
        `).join('');
    }

    // Show AI report
    document.getElementById('aiReport').textContent = data.ai_report;
}

function clearAll() {
    document.getElementById('solidityCode').value = '';
    document.getElementById('results').classList.add('hidden');
}

function loadSample() {
    document.getElementById('solidityCode').value = `pragma solidity ^0.8.0;

contract VulnerableBank {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint amount = balances[msg.sender];
        require(amount > 0);
        
        // VULNERABLE: Reentrancy attack possible here!
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
        
        balances[msg.sender] = 0;
    }
}`;
}