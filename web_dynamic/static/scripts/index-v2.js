$(document).ready(function() {
            $(".button-cr").click(function() {
                window.location.href = "/create";
            });
        });
$(document).ready(function() {
    // Redirect to the main page when the logo is clicked
    $('.header').on('click', function() {
        window.location.href = "http://127.0.0.1:5000/";
    });
});
