$(document).on('click', '#Contest', function () {
    remove_active_state();
    $('#Contest').addClass("active");
    $('#iframe').attr('src', '/superuser_admin/dashboard/contest')
});
$(document).on('click', '#Questions', function () {
    remove_active_state();
    $('#Questions').addClass("active");
    $('#iframe').attr('src', '/superuser_admin/dashboard/Questions')
});
$(document).on('click', '#Users', function () {
    remove_active_state();
    $('#Users').addClass("active");
    $('#iframe').attr('src', '/superuser_admin/dashboard/Users')
});


function remove_active_state(){
    $('#Contest').removeClass("active");
    $('#Questions').removeClass("active");
    $('#Users').removeClass("active");
}