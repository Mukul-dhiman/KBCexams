$(document).ready(function () {
    $(".ion-ios-navicon").on("touchstart click", function(e) {
        console.log("click")
        e.preventDefault(), 
        $(".sidebar").toggleClass("active"), 
        $(".sidebar .sidebar-overlay").removeClass("fadeOut animated").addClass("fadeIn animated")
    }),
    $(".sidebar .sidebar-overlay").on("touchstart click", function(e) {
        e.preventDefault(), 
        $(".ion-ios-navicon").click()
    })
    
});
$(".ion-ios-navicon").on("touchstart click", function(e) {
    console.log("click")
    e.preventDefault(), 
    $(".sidebar").toggleClass("active"), 
    $(".sidebar .sidebar-overlay").removeClass("fadeOut animated").addClass("fadeIn animated")
}),
$(".sidebar .sidebar-overlay").on("touchstart click", function(e) {
    e.preventDefault(), 
    $(".ion-ios-navicon").click()
})