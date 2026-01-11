const LoginSignup = document.getElementById("LoginSignup");
const GetStarted = document.getElementById("GetStarted");
const login = document.getElementById("login");
const signup = document.getElementById("signup");

if (LoginSignup) {
    LoginSignup.addEventListener("click", function(event) {
        event.preventDefault();
        console.log("Clicked on 3 dots")
        window.location.href = "/login_or_signup"
    });
}

if (GetStarted) {
    GetStarted.addEventListener("click", function(event) {
        event.preventDefault();
        console.log("Clicked on Get Started");
        // to be implemented because need to do routing
    });
}

if (login) {
    login.addEventListener("click", function(event) {
        event.preventDefault();
        console.log("Chose Login");
        window.location.href = "/login";
    });
}

if (signup) {
    signup.addEventListener("click", function(event) {
        event.preventDefault();
        console.log("Chose Signup");
        window.location.href = "/signup";
    });
}