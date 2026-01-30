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

const tailorForm = document.getElementById('tailor-form');

if (tailorForm) {
    tailorForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const resume = document.getElementById('resume-upload').files[0];
        const jd = document.getElementById('jd-upload').files[0];
        
        if(!resume || !jd) return alert("Please upload both files!");

        const formData = new FormData();
        formData.append('resume', resume);
        formData.append('jd', jd);

        // UI Feedback
        const btn = tailorForm.querySelector('button');
        btn.innerText = "Processing...";

        const response = await fetch('/tailor', { method: 'POST', body: formData });
        const result = await response.json();

        if (result.success) {
            document.getElementById('ai-results').style.display = 'block';
            document.getElementById('display-summary').innerText = result.summary;
            document.getElementById('display-analysis').innerText = result.analysis;
        } else {
            alert("Error: " + result.error);
        }
        btn.innerText = "Tailor Resume";
    });
}
