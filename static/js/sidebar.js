$(document).ready(function() {
    $(".ion-ios-navicon").click(function () {

            $(".sidebar").toggleClass("active"),
                $(".sidebar .sidebar-overlay").removeClass("fadeOut animated").addClass("fadeIn animated");
        });
    $(".sidebar .sidebar-overlay").on("touchstart click", function(e) {
        e.preventDefault(), 
        $(".ion-ios-navicon").click()
    });
});