$(window).on('load',function(){
    var UserID = $('#session_user_id').attr("UserID");
    var qurl = "/get_ticket_history/"+UserID;
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        dataType: "json",
        success: function (data) {
            console.log(data.success);
            var ticket;
            for( ticket = 0; ticket < data.success.length; ticket++){
                console.log(data.success[ticket]);
                $("#all_tickets").append("<div class='ticket_div'>" + "<span class='ticket_id'>" + data.success[ticket][2] + "</span> |" + "<span class='ticket_date'>" + data.success[ticket][7] + "</span>" + "<div>");
            }    
        },
        error: function (jqXHR) {
            console.log("error");
        }
    });
})