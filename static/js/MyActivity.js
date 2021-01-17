$(window).on('load',function(){
    var UserID = $('#session_user_id').attr("UserID");
    var contestID = $('#session_user_id').attr("contestID");
    var qurl = "/get_ticket_history/"+UserID+"/"+contestID;
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        dataType: "json",
        success: function (data) {
            var ticket;
            for( ticket = 0; ticket < data.success.length; ticket++){
                $("#all_tickets").append("<a href='/ticket/"+data.success[ticket][0]+
                "'>"+
                " <div class='ticket_div' id='"+
                data.success[ticket][0]+"'>" + 
                "<span class='ticket_id'>" + 
                data.success[ticket][2] + 
                "</span> " + "<span class='ticket_date'>" + 
                data.success[ticket][7] + "</span>" + "<div></a>");
                let color = "red";
                if(data.success[ticket][10]==0){
                    color = "rgba(255,255,0,0.2)";
                }
                else if(data.success[ticket][10]==1){
                    color = "rgba(173,255,47,0.2)";
                }
                else if(data.success[ticket][10]==2){
                    color="none";
                }
                else if(data.success[ticket][10]==3){
                    color = "none";
                }
                $('#'+data.success[ticket][0]).css("background-color",color);
            }    
        },
        error: function (jqXHR) {
            console.log("error");
        }
    });
})