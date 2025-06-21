const baseFontSize = window.innerHeight * 0.015; // vh units (1.5vh)




// -------------------------------------
// Time Chart


function drawTimeChart(timeChart) {

    const ctx = document.getElementById('time-chart');

    var gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 250);
    gradient.addColorStop(0, 'rgba(133, 61, 67, .4)');
    gradient.addColorStop(1, 'rgba(133, 61, 67, 0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeChart['labels'],
            datasets: [{
                data: timeChart['data'],
                borderWidth: baseFontSize / 8,
                borderColor: '#E8545F',
                fill: true,
                backgroundColor: gradient,
                tension: 0.4
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'NOMBRE DE BUT PAR SAISON',
                    font: {
                        size: baseFontSize,
                        family: 'Montserrat'
                    },
                    color: 'white',
                    padding: {
                        bottom: 40
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        font: {
                            size: baseFontSize
                        }
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: baseFontSize
                        }
                    }
                }
            }
        }
    });
}







// -------------------------------------
// Type of Goals Chart


function drawTypeChart(typeChart) {

    const ctx = document.getElementById('goals-type-chart');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: typeChart['labels'],
            datasets: [{
                data: typeChart['data'],
                borderWidth: baseFontSize / 8,
                borderColor: '#E8545F',
                backgroundColor: '#853D43'
            }]
        },
        options: {
            indexAxis: 'y',
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'TYPE DE BUT',
                    font: {
                        size: baseFontSize,
                        family: 'Montserrat'
                    },
                    color: 'white',
                    padding: {
                        bottom: 40
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        font: {
                            size: baseFontSize
                        }
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: baseFontSize
                        }
                    }
                }
            }
        }
    });
}








// -------------------------------------
// CUSTOM POSITION CHART


function updatePositionChart(positionChart) {

    container = document.querySelector('.position-chart-container');
    const custom_ctx = document.getElementById('position-custom-chart');

    for (position in positionChart) {

        const percent = positionChart[position]['percent'];
        const position_element = custom_ctx.querySelector('#' + position);
        const size = (.5 + percent) * 6 + 'vh';

        position_element.style.height = size;
        position_element.style.width = size;

        position_element.dataset.count = positionChart[position]['count']
    }

    custom_ctx.querySelectorAll('.position-points > li').forEach(item => {
        item.addEventListener('mouseenter', function () {
            // Store the original text in a data attribute so it can be restored on mouseleave
            item.dataset.originalText = item.textContent;
            // Set textContent to the value of data-count attribute
            item.textContent = item.dataset.count;
        });

        item.addEventListener('mouseleave', function () {
            // Restore the original text
            item.textContent = item.dataset.originalText;
        });
    });

    // Show chart
    container.classList.remove('masked');

}