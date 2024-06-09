$(document).ready(function() {
    	$('#redirectButton').click(function() {
		const city = $('#city').val();
		if (city) {
			window.location.href = "http://127.0.0.1:5000/weather/" + city;
		} else {
			alert('Please enter a city name.');
		}
	});
});
