$(document).on('click', '#Wallet_ticket_button', function () {
    document.getElementById("myModal").style.display = "block";
});

$(document).on('click', '#model-close', function () {
    document.getElementById("myModal").style.display = "none";
});


$(window).on('click', function(event){
    model = document.getElementById("myModal");
    if (event.target == model) {
        model.style.display = "none";
    }
});

$(document).on('click', '#confirm_ticket', function () {
    var contestID = $('#required-info-for-ticket').attr("contestID");
    var UserID = $('#required-info-for-ticket').attr("UserID");
    var qurl = "/get_ticket/"+contestID+"/"+UserID;
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        dataType: "json",
        success: function (data) {
            console.log(data);
        },
        error: function (jqXHR) {
            alert("error: " + jqXHR.status);
            console.log(jqXHR);
        }
    });
});