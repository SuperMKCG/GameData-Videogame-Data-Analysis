/* ===================================
   GameData Analytics - Dashboard Charts
   =================================== */

document.addEventListener('DOMContentLoaded', function () {

  // Initialize all charts after DOM is ready
  loadTopGames();
  loadGenres();
  loadPublishers();
  loadRegions();

});

//Translations
//---Genre---
function translateGenre(genre) {

  const genres = {
    "Role-Playing": "Juego de rol",
    "Action": "Acción",
    "Sports": "Deportes",
    "Adventure" : "Aventura",
    "Role-Playing": "Rol",
    "Shooter": "Disparos",
    "Platform": "Plataformas",
    "Racing": "Carreras",
    "Simulation": "Simulación",
    "Fighting": "Peleas",
    "Strategy": "Estrategia",
    "Puzzle": "Puzzle",
    "Misc": "Misceláneo"
  };

  return genres[genre] || genre;
}

//---Places---
function translatePlaces(place) {
  const places = {
    "North America": "Norteamérica",
    "Europe": "Europa",
    "Japan": "Japón",
    "Other": "Otras regiones"
  };

  return places[place] || place;
}


// Colors for graphics
function generateColors(total) {

    const palette = [
        '#0d6efd',
        '#20c997',
        '#ffc107',
        '#dc3545',
        '#6f42c1',
        '#fd7e14',
        '#198754',
        '#0dcaf0',
        '#adb5bd',
        '#6610f2'
    ];

    return palette.sort(() => Math.random() - 0.5).slice(0, total);
}


/* ===================================
   Obtencion de top juegos con mejores ventas globales
   =================================== */
function loadTopGames() {

  fetch("http://127.0.0.1:5000/api/top-global-sales/")
  .then(response => response.json())
  .then(data => {

    // Map API response to Chart.js format
    const labels = data.map(item => item.Name);
    const values = data.map(item => item.Global_Sales);

    const ctx = document.getElementById('chartRevenue').getContext('2d');

    new Chart(ctx, {

      type: 'bar',

      data: {
        labels: labels,
        datasets: [{
          label: 'Ventas globales',
          data: values,
          backgroundColor: generateColors(values.length),
          borderRadius: 6,
          maxBarThickness: 48
        }]
      },

      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            title: {
              display: true,
              text:'Videojuegos',
              font: {
                size: 14,
                weight: 'bold'
              }
            }
          },
          y: {
            title:{
              display: true,
              text: 'Ventas globales (millones de unidades)',
              font: {
                size: 14,
                weight: 'bold'
              }
            },


            beginAtZero: true
          }
        }
      }

    });

  })
  .catch(error => console.error("Top Games API error:", error));

}


/* ===================================
   Sales by Genre Chart
   =================================== */
function loadGenres() {

  fetch("http://127.0.0.1:5000/api/sales-by-genre/")
  .then(response => response.json())
  .then(data => {

    const labels = data.map(item => translateGenre(item.Genre));
    const values = data.map(item => item.Global_Sales);

    const ctx = document.getElementById('chartGenres').getContext('2d');

    new Chart(ctx, {

      type: 'bar',

      data: {
        labels: labels,
        datasets: [{
          label: 'Ventas globales',
          data: values,
          backgroundColor: generateColors(values.length),
          borderRadius: 6,
          maxBarThickness: 48
        }]
      },

      options: {
        indexAxis: 'y', // grafica horizontal para mejor lectura
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            title:{
              display: true,
              text: 'Géneros de videojuegos',
              font:{
                size: 14,
                weight: 'bold'
              }
            },
            beginAtZero: true
          },

          x: {
            title:{
              display: true,
              text: 'Copias vendidas (Millones)',
              font: {
                size: 14,
                weight: 'bold'
              }
            }
          }



        }
      }

    });

  })
  .catch(error => console.error("Genre API error:", error));

}


/* ===================================
   Obtencion de top publishers
   =================================== */
function loadPublishers() {

  fetch("http://127.0.0.1:5000/api/top-publishers/")
  .then(response => response.json())
  .then(data => {

    const labels = data.map(item => item.Publisher);
    const values = data.map(item => item.Global_Sales);

    const ctx = document.getElementById('chartPublishers').getContext('2d');

    new Chart(ctx, {

      type: 'bar',

      data: {
        labels: labels,
        datasets: [{
          label: 'Ventas globales',
          data: values,
          backgroundColor: generateColors(values.length),
          borderRadius: 6,
          maxBarThickness: 48
        }]
      },

      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x:{
            title: {
              display: true,
              text: 'Publishers',
              font:{
                size: 14,
                weight: 'bold'
              }
            }
          },

          y: {
            title: {
              display: true,
              text: 'Unidades vendidas (millones)',
              font: {
                size: 14,
                weight: 'bold'
              }
            },
            beginAtZero: true
          }
        }
      }

    });

  })
  .catch(error => console.error("Publishers API error:", error));

}


/* ===================================
   Obtencion de ventas por region
   =================================== */
function loadRegions() {

  fetch("http://127.0.0.1:5000/api/sales-by-region/")
  .then(response => response.json())
  .then(data => {

    const labels = data.map(item => translatePlaces(item.Region));
    const values = data.map(item => item.Sales);

    const ctx = document.getElementById('chartRegion').getContext('2d');

    new Chart(ctx, {

      type: 'pie',

      data: {
        labels: labels,
        datasets: [{
          label: 'Venta por region (millones de unidades)',
          data: values,
          backgroundColor: generateColors(values.length),
        }]
      },

      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            title: {
              display: true,
              text: "Regiones",
              font: {
                size: 14,
                weight: 'bold'
              },
              padding: {
                top: 20
              }
            },
            labels: {
              pointStyle: 'circle',
              usePointStyle: true,
              padding: 20
            }
          },
        }
      }

    });

  })
  .catch(error => console.error("Region API error:", error));

}