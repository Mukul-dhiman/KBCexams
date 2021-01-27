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


var only_one_load_contest_details={};
$(document).on('click', '#accordion1', function () {
    var contestid = $(this).attr('contestid');
    if(only_one_load_contest_details[contestid]){
        return null;
    }
    only_one_load_contest_details[contestid]=1;
    var qurl = "/superuser_admin/api/Contest_details/"+contestid;
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        success: function (data) {
            for (let i = 0; i < data.success.length; i++) { // iteration over input
                var range = data.success[i][1]+'-'+data.success[i][2];
                $('#'+contestid+'_list').append('<div class="row"><div class="col-4">'+range+'</div><div class="col-3">'+data.success[i][3]+'</div></div>');
            }
        },
        error: function (jqXHR) {
            console.log("error");
        }
    });
});



$(document).on('submit', '#contestPrize', function () {
    var contestid = $(this).attr('contestid');
    var qurl = "/superuser_admin/api/change_contest_details/"+contestid;
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
