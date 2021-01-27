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

$(document).on('submit', '#CreateContestForm', function () {
    var qurl = "/superuser_admin/api/CreateContest";
    var form = $(this);
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        data: form.serialize(),
        success: function (data) {
            console.log("done");
        },
        error: function (jqXHR) {
            console.log("error");
        }
    });
});