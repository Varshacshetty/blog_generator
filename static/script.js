document.getElementById('generate-btn').addEventListener('click', function () {
    const prompt = document.getElementById('prompt').value.trim();
    const loading = document.getElementById('loading');
    const output = document.getElementById('blog-output');

    if (!prompt) {
        alert("Please enter a prompt.");
        return;
    }

    loading.style.display = "block";
    output.innerHTML = "";

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
    })
    .then(res => res.json())
    .then(data => {

        console.log("BACKEND RESPONSE:", data); 

        loading.style.display = "none";

        if (data.blog) {
            output.innerHTML = data.blog.replace(/\n/g, "<br><br>");
        } else {
            output.innerHTML = "<p>Error generating blog.</p>";
        }
    })
    .catch(err => {
        loading.style.display = "none";
        output.innerHTML = `<p style="color:red;">${err}</p>`;
    });
});
