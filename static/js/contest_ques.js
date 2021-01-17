let question_array = []

$(window).on('load',function(){
    var ticketID = $('#ticketID').attr("ticketID");
    var qurl = "/get_random_questions/"+ticketID;
    $('#myModal').addClass('is-blurred');
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        dataType: "json",
        success: function (data) {
            document.getElementById("myModal").style.display = "block";
            question_array=data.success;
        },
        error: function (jqXHR) {
            console.log("error");
        }
    });
})

var myVar;

var timeLimit = 10000;
var time_remain;

function timer() {
    var start = new Date;
    setInterval(function(){
        if(new Date - start - timeLimit < 5){
            time_remain = (timeLimit-(new Date - start))/1000;
            time_remain.toPrecision(1);
            $('.Timer').text(time_remain + " Seconds");
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
    $('#myModal').addClass('is-blurred');
    start_date = d.toISOString().split('T')[0];
    start_time = d.toTimeString().split(' ')[0];
    start_h = start_time.split(':')[0];
    start_m = start_time.split(':')[1];
    start_s = start_time.split(':')[2];
    console.log(d,start_time);
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        data: {start_date, start_h, start_m, start_s},
        dataType: 'text',
        success: function (data) {
            console.log(data);
        },
        error: function (jqXHR) {
            console.log("error in startdate");
        }
    });
}

$(document).on('click', '#start_contest', function () {
    document.getElementById("myModal").style.display = "none";
    $('#myModal').removeClass('is-blurred');
    timer();
    var d = new Date
    use_ticket(d);



    console.log(question_array,d);
});
