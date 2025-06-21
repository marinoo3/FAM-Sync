function updateNumbers(stats) {

    // Set goals to 0 and run count up
    const goalElement = document.querySelector('#goals');
    goalElement.textContent = 0;
    countUp(goalElement, stats['player']['goals']);
    // Set progress bar label
    const percentElement = document.querySelector('.progress-label');
    percentElement.textContent = stats['player']['progress'] + '%';
    // Set progress
    const progressBar = document.querySelector('.progress-slider');
    progressBar.style.width = stats['player']['progress'] + '%';

    // Set prediction date
    const predictedDate = document.querySelector('#prediction');
    predictedDate.textContent = stats['player']['prediction'];

    // Set season
    const playedGames = document.querySelector('#played-games');
    playedGames.textContent = stats['player']['seasons'];

    // Set average goals
    const averageGoals = document.querySelector('#average-goals');
    averageGoals.textContent = stats['player']['goalsPerSeason'];

}


document.addEventListener('DOMContentLoaded', async function () {

	// Show popup

	const popup = document.querySelector('#loading-popup');
	popup.classList.remove('hidden');

	// Requests stats to python API

	const response = await fetch('/api/get_dashboard_data/', {
		method: 'GET',
		headers: { 'Content-Type': 'application/json' }
	});

	if (!response.ok) {
		throw new Error('Network response was not ok');
	}

	const stats = await response.json();

	// Update GUI and draw charts

	updateNumbers(stats);

	drawTimeChart(stats['timeChart']);
	drawTypeChart(stats['typeChart']);
	updatePositionChart(stats['positionChart']);


	// Hide popup

	popup.classList.add('hidden');

});