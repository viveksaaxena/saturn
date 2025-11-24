document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("https://saturn-101.onrender.com/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
        // Save user session in browser
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("email", data.email);

        document.getElementById("message").innerText = "Login successful!";
    } else {
        document.getElementById("message").innerText = data.detail;
    }
});
