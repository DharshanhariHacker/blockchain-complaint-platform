async function submitComplaint() {
    const encryptedData = document.getElementById('encryptedData').value;
    
    const response = await fetch('/submit_complaint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ encrypted_data: encryptedData })
    });
    
    const result = await response.json();
    alert(result.status);
}

async function getComplaint() {
    const complaintId = document.getElementById('complaintId').value;

    const response = await fetch(`/get_complaint/${complaintId}`);
    const result = await response.json();
    
    const display = document.getElementById('result');
    display.innerHTML = `<p>Encrypted Data: ${result.encrypted_data}</p><p>Status: ${result.status}</p>`;
}
