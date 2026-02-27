document.getElementById("loginForm").addEventListener("submit", function(event) {

    event.preventDefault();

    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();

    let emailError = document.getElementById("emailError");
    let passwordError = document.getElementById("passwordError");

    let valid = true;

    // Reset errors
    emailError.classList.add("hidden");
    passwordError.classList.add("hidden");

    // Email check
    if (email === "") {
        emailError.innerText = "Email is required";
        emailError.classList.remove("hidden");
        valid = false;
    } 
    else if (!email.includes("@")) {
        emailError.innerText = "Enter valid email";
        emailError.classList.remove("hidden");
        valid = false;
    }

    // Password check
    if (password === "") {
        passwordError.innerText = "Password is required";
        passwordError.classList.remove("hidden");
        valid = false;
    } 
    else if (password.length < 6) {
        passwordError.innerText = "Password must be at least 6 characters";
        passwordError.classList.remove("hidden");
        valid = false;
    }

    if (valid) {
       window.location.href = "dashboard.html";
    }
});