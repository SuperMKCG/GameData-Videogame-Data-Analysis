/*========================
  Recommendations System
========================*/

//Cargar contenido al darle clic en el boton de analisis
document.addEventListener('DOMContentLoaded', function () {

    const btn = document.getElementById("btnRecommend");

    btn.addEventListener("click", function () {

        const genre = document.getElementById("genre").value;
        const score = document.getElementById("user_score").value;
        const rating = document.getElementById("rating").value;

        // VALIDACION
        if (!genre || !score || !rating) {

            document.getElementById("recommendationResults").innerHTML = `
                <div class="alert alert-warning text-center">
                    <i class="bi bi-exclamation-triangle-fill"></i>
                    Debes seleccionar género, calificación y clasificación.
                </div>
            `;

            return;
        }

        recommendGames(genre, score, rating);

    });

});

//Funcion para cargar juegos recomendados por medio de metricas
function recommendGames(genre, score, rating) {

    const resultsDiv = document.getElementById("recommendationResults");

    resultsDiv.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-info"></div>
            <p class="mt-2">Analizando datos...</p>
        </div>
    `;


    fetch(`http://127.0.0.1:5000/api/best-games-users/?genre=${genre}&rating=${rating}&min_score=${score}`)
    .then(response => response.json())
    .then(data => {

        displayResults(data);

    })
    .catch(error => {

        console.error("Recommendation API error:", error);

        resultsDiv.innerHTML = `
            <div class="alert alert-danger">
                Error al obtener recomendaciones
            </div>
        `;

    });
}

//Funcion que muestra los resultados del analisis
function displayResults(games) {
    const resultsDiv = document.getElementById("recommendationResults");

    if (games.length === 0) {
        resultsDiv.innerHTML = `
            <div class="alert alert-warning text-center">
                No se encontraron resultados
            </div>
        `;
        return;
    }


    let html = `
        <h3 class="mb-4 text-center section-title">
            Juegos recomendados
        </h3>
        <div class="row g-4">
    `;


    games.forEach(game => {
        html += `
            <div class="col-md-6 col-lg-4">
                <div class="card shadow-sm border-0 h-100">
                    <img src="${game.Image}" class="card-img-top" alt="${game.Name}">

                    <div class="card-body">
                        <h5 class="card-title fw-bold">
                            ${game.Name}
                        </h5>

                        <p class="card-text">
                            <i class="bi bi-controller text-primary"></i> Género: ${game.Genre} <br>
                            <i class="bi bi-star-fill text-warning"></i> Calificación de usuario: ${game.User_Score} <br>
                            <i class="bi bi-building text-secondary"></i> Publisher: ${game.Publisher} <br>
                            <i class="bi bi-patch-check-fill text-primary"></i> Clasificación: ${game.Rating}
                        </p>
                    </div>
                </div>
            </div>
        `;
    });

    html += `</div>`;

    resultsDiv.innerHTML = html;
}
