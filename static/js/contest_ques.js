let question_array = []

$(window).on('load',function(){
    document.getElementById("myModal").style.display = "block";
    $('#myModal').addClass('is-blurred');
})


function get_question(){
    var ticketID = $('#ticketID').attr("ticketID");
    var qurl = "/get_random_questions/"+ticketID;
    $('#myModal').addClass('is-blurred');
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        dataType: "json",
        success: function (data) {
            question_array=data.success;
            var d = new Date
            use_ticket(d);
        },
        error: function (jqXHR) {
            // noticeify user that we have error in getting question

            console.log("error");
        }
    });
}

var myVar;

var timeLimit = 5*60*1000;
var time_remain;

function timer() {
    var start = new Date;
    setInterval(function(){
        if(new Date - start - timeLimit < 5){
            time_remain = (timeLimit-(new Date - start))/1000;
            time_remain.toPrecision(1);
            $('#Timer').text(time_remain + " Seconds");
        }
    }, 1000);
    
    myVar = setTimeout(timeoutfunc, timeLimit);
}

function timeoutfunc() {
    alert("Hello!");
}


function use_ticket(d){
    var ticketID = $('#ticketID').attr("ticketID");
    var qurl = "/use_ticket/"+ticketID;
    start_date = d.toISOString().split('T')[0];
    start_time = d.toTimeString().split(' ')[0];
    start_h = start_time.split(':')[0];
    start_m = start_time.split(':')[1];
    start_s = start_time.split(':')[2];
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        data: {start_date, start_h, start_m, start_s},
        dataType: 'text',
        success: function (data) {
            question_number(0);
            document.getElementById("myModal").style.display = "none";
            $('#myModal').removeClass('is-blurred');
            timer();
            console.log(data);
        },
        error: function (jqXHR) {
            // noticity user to try later and your ticket is safe

            console.log("error in startdate");
        }
    });
}

$(document).on('click', '#start_contest', function () {
    get_question();
});


function question_number(number){
    var previous = (number - 1)%10;
    var next = (number + 1)%10;
    if(number==0){
        previous = 9;
        next = 1; 
    }
    $("#question_statement").text(question_array[number][1]);
    $("#option1").text(question_array[number][2]);
    $("#option2").text(question_array[number][3]);
    $("#option3").text(question_array[number][4]);
    $("#option4").text(question_array[number][5]);
    $("#navigation_button_previous").attr("previous",previous);
    $("#navigation_button_next").attr("next",next);
}

$(document).on("click",'#navigation_button_previous',function(){
    var previous =  $(navigation_button_previous).attr("previous");
    question_number(Number(previous));
})


$(document).on("click",'#navigation_button_next',function(){
    var next =  $(navigation_button_next).attr("next");
    question_number(Number(next));
});


$(document).on('click', '#clicker', function () {
    if($(".panel_slider").prop("checked")) {
        //I am checked
        $(".panel_slider").prop('checked', false);
    }else{
        //I'm not checked
        $(".panel_slider").prop('checked', true);
    }
});