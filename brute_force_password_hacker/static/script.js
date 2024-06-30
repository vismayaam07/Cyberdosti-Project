document.getElementById('passwordForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const password = document.getElementById('password').value;
    const response = await fetch('/crack_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password })
    });

    const result = await response.json();
    document.getElementById('result').textContent = result.result;
});
