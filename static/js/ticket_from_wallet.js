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
            get_Current_Wallet_Balance(UserID, '#Current_Wallet_Balance');
            if(data.success=="false"){
                document.getElementById("ticket_status").style.color="Red";
                document.getElementById("ticket_status").innerText="No Spots Left!!!";
            }
            else if(data.success=="complete"){
                document.getElementById("ticket_status").style.color="Green";
                document.getElementById("ticket_status").innerText="You get the Ticket!!!";
            }
            else{
                document.getElementById("ticket_status").style.color="Red";
                document.getElementById("ticket_status").innerText="Not enough money in Wallet";
            }
        },
        error: function (jqXHR) {
            document.getElementById("ticket_status").style.color="Red";
            document.getElementById("ticket_status").innerText="Something went Wrong! Try Again";
        }
    });
});