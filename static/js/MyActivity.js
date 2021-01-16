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
                $("#all_tickets").append("<meta id='meta_data_"+
                data.success[ticket][0]+
                "' TicketID='"+
                data.success[ticket][0]+
                "' UserID='"+
                data.success[ticket][1]+
                "' ContestID='"+
                data.success[ticket][2]+
                "' ObtainedScore='"+
                data.success[ticket][3]+
                "' MaximumScore='"+
                data.success[ticket][4]+
                "' RankAchieved='"+
                data.success[ticket][5]+
                "' AwardReceived='"+
                data.success[ticket][6]+
                "' CreatedDate='"+
                data.success[ticket][7]+
                "' TestSubmitDate='"+
                data.success[ticket][8]+
                "' ModifiedDate='"+
                data.success[ticket][9]+
                "' TicketState='"+
                data.success[ticket][10]+
                "'> <div class='ticket_div' id='"+
                data.success[ticket][0]+"'>" + 
                "<span class='ticket_id'>" + 
                data.success[ticket][2] + 
                "</span>" + "<span class='ticket_date'>" + 
                data.success[ticket][7] + "</span>" + "<div>");
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