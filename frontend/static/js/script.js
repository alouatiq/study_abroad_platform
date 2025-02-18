function loadContent(page) {
    if (page === "index.html") {
        window.location.href = "index.html"; // Reloads the main page
    } else {
        fetch(page)
            .then(response => response.text())
            .then(data => {
                document.getElementById("main-content").innerHTML = data;
            })
            .catch(error => console.error("Error loading page:", error));
    }
}
