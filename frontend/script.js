async function getRecommendation() {
    const movie = document.getElementById("movieInput").value;
    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = "Loading...";

    const response = await fetch(`http://127.0.0.1:5000/recommend?movie=${movie}`);
    const data = await response.json();

    if (data.error) {
        resultDiv.innerHTML = `<p style="color:red">${data.error}</p>`;
        return;
    }

    let html = "<ul>";

    data.recommendations.forEach(movie => {
        html += `<li>
            <b>${movie.title}</b><br>
            <small>${movie.genres}</small>
        </li><br>`;
    });

    html += "</ul>";
    resultDiv.innerHTML = html;
}
