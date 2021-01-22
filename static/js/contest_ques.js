let question_array = []
let question_response = {}
let question_order = {}
var finished = 0;


window.onbeforeunload = function () {
    return "Do you really want to leave our brilliant application?";
    //if we return nothing here (just calling return;) then there will be no pop-up question at all
    //return;
};


$(window).on('load', function () {
    var startdate = $('#ticketID').attr('timeStart');
    if (startdate != "None") {
        get_question();
    }
    else {  
        document.getElementById("myModal").style.display = "block";
        $('#myModal').addClass('is-blurred');
    }
})


function make_response_array() {
    for (var i = 0; i < question_array.length; i++) {
        question_order[question_array[i][0]] = i;
        question_response[question_array[i][0]] = -1;
    }
}


function get_question() {
    var ticketID = $('#ticketID').attr("ticketID");
    var qurl = "/get_random_questions/" + ticketID;
    $('#myModal').addClass('is-blurred');
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        dataType: "json",
        success: function (data) {
            question_array = data.success;
            make_response_array();
            var startdate = $('#ticketID').attr('timeStart');
            if (startdate == "None") {
                var d = new Date;
                use_ticket(d);
            }
            else {
                question_number(0);
                timer();
            }
        },
        error: function (jqXHR) {
            // noticeify user that we have error in getting question

            console.log("error");
        }
    });
}

var myVar;

var timeLimit = 5 * 60 * 1000;
var time_remain;

function datetostring(d) {
    return d.toISOString().split('T')[0] + " " + d.toTimeString().split(" ")[0];
}

function timer() {
    var startdate = $('#ticketID').attr('timeStart');
    var start = new Date;
    if (startdate != "None") {
        startdate = new Date(startdate);
        start = startdate;
    }
    console.log(start, startdate);
    var interval = setInterval(function () {
        if (new Date - start - timeLimit < 5) {
            time_remain = (timeLimit - (new Date - start)) / 1000;
            $('#Timer').text(Math.floor(time_remain) + " Seconds");
        }
        else{
            clearInterval(interval);
        }
    }, 1000);

    var diff = new Date - startdate;
    setTimeout(timeoutfunc, timeLimit - diff); 

}

function timeoutfunc() {
    finish_contest(question_response);
    alert("Hello!");
}


function use_ticket(d) {
    var ticketID = $('#ticketID').attr("ticketID");
    var qurl = "/use_ticket/" + ticketID;
    start_date = d.toISOString().split('T')[0];
    start_time = d.toTimeString().split(' ')[0];
    start_h = start_time.split(':')[0];
    start_m = start_time.split(':')[1];
    start_s = start_time.split(':')[2];
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        data: { start_date, start_h, start_m, start_s },
        dataType: 'text',
        success: function (data) {
            question_number(0);
            document.getElementById("myModal").style.display = "none";
            $('#myModal').removeClass('is-blurred');
            timer();
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


function question_number(number) {
    var previous = (number - 1) % 10;
    var next = (number + 1) % 10;
    if (number == 0) {
        previous = 9;
        next = 1;
    }

    $('#QuestionNumber').text(Number(number) + Number(1));
    $('#question-id').attr('questionId', question_array[number][0]);
    $("#question_statement").text(question_array[number][1]);
    $("#option1").text(question_array[number][2]);
    $("#option2").text(question_array[number][3]);
    $("#option3").text(question_array[number][4]);
    $("#option4").text(question_array[number][5]);
    $("#navigation_button_previous").attr("previous", previous);
    $("#navigation_button_next").attr("next", next);

    questionId = $('#question-id').attr('questionId');
    clearotherResponse(question_response[questionId]);


    $("#option" + question_response[questionId] + "_clickbox").prop('checked', true);
    $('#option' + question_response[questionId] + '_button').css('border', '3px solid limegreen');
    $('#option' + question_response[questionId] + '_button').css('color', 'limegreen');
}

$(document).on("click", '#navigation_button_previous', function () {
    var previous = $(navigation_button_previous).attr("previous");
    question_number(Number(previous));
})


$(document).on("click", '#navigation_button_next', function () {
    var next = $(navigation_button_next).attr("next");
    question_number(Number(next));
});


$(document).on('click', '#clicker', function () {
    if ($(".panel_slider").prop("checked")) {
        //I am checked
        $(".panel_slider").prop('checked', false);
    } else {
        //I'm not checked
        $(".panel_slider").prop('checked', true);
    }
});




$(document).on('click', '#option1_button', function () {
    questionId = $('#question-id').attr('questionId');
    if ($("#option1_clickbox").prop("checked")) {
        //I am checked
        question_response[questionId] = -1;
        $('#navigation_main_button_' + question_order[questionId]).css('background-color', 'yellow');
        $('#respone_side_panel_' + question_order[questionId]).text('Unattempted');

        $("#option1_clickbox").prop('checked', false);
        $('#option1_button').css('border', 'initial');
        $('#option1_button').css('color', 'black');
    } else {
        //I'm not checked
        question_response[questionId] = 1;
        $('#navigation_main_button_' + question_order[questionId]).css('background-color', 'green');
        $('#respone_side_panel_' + question_order[questionId]).text('A');
        $("#option1_clickbox").prop('checked', true);
        $('#option1_button').css('border', '3px solid limegreen');
        $('#option1_button').css('color', 'limegreen');
        clearotherResponse(Number('1'));
    }
});
$(document).on('click', '#option2_button', function () {
    questionId = $('#question-id').attr('questionId');
    if ($("#option2_clickbox").prop("checked")) {
        //I am checked
        question_response[questionId] = -1;
        $('#navigation_main_button_' + question_order[questionId]).css('background-color', 'yellow');
        $('#respone_side_panel_' + question_order[questionId]).text('Unattempted');
        $("#option2_clickbox").prop('checked', false);
        $('#option2_button').css('border', 'initial');
        $('#option2_button').css('color', 'black');
    } else {
        //I'm not checked
        question_response[questionId] = 2;
        $('#navigation_main_button_' + question_order[questionId]).css('background-color', 'green');
        $('#respone_side_panel_' + question_order[questionId]).text('B');
        $("#option2_clickbox").prop('checked', true);
        $('#option2_button').css('border', '3px solid limegreen');
        $('#option2_button').css('color', 'limegreen');
        clearotherResponse(Number('2'));
    }
});
$(document).on('click', '#option3_button', function () {
    questionId = $('#question-id').attr('questionId');
    if ($("#option3_clickbox").prop("checked")) {
        //I am checked
        question_response[questionId] = -1;
        $('#navigation_main_button_' + question_order[questionId]).css('background-color', 'yellow');
        $('#respone_side_panel_' + question_order[questionId]).text('Unattempted');
        $("#option3_clickbox").prop('checked', false);
        $('#option3_button').css('border', 'initial');
        $('#option3_button').css('color', 'black');
    } else {
        //I'm not checked
        question_response[questionId] = 3;
        $('#navigation_main_button_' + question_order[questionId]).css('background-color', 'green');
        $('#respone_side_panel_' + question_order[questionId]).text('C');
        $("#option3_clickbox").prop('checked', true);
        $('#option3_button').css('border', '3px solid limegreen');
        $('#option3_button').css('color', 'limegreen');
        clearotherResponse(Number('3'));
    }
});
$(document).on('click', '#option4_button', function () {
    questionId = $('#question-id').attr('questionId');
    if ($("#option4_clickbox").prop("checked")) {
        //I am checked
        question_response[questionId] = -1;
        $('#navigation_main_button_' + question_order[questionId]).css('background-color', 'yellow');
        $('#respone_side_panel_' + question_order[questionId]).text('Unattempted');
        $("#option4_clickbox").prop('checked', false);
        $('#option4_button').css('border', 'initial');
        $('#option4_button').css('color', 'black');
    } else {
        //I'm not checked
        question_response[questionId] = 4;
        $('#navigation_main_button_' + question_order[questionId]).css('background-color', 'green');
        $('#respone_side_panel_' + question_order[questionId]).text('D');
        $("#option4_clickbox").prop('checked', true);
        $('#option4_button').css('border', '3px solid limegreen');
        $('#option4_button').css('color', 'limegreen');
        clearotherResponse(Number('4'));
    }
});


function clearotherResponse(num) {
    for (let i = 1; i <= 4; i++) {
        if (i != num) {
            $('#option' + i + '_clickbox').prop('checked', false);
            $('#option' + i + '_button').css('border', 'initial');
            $('#option' + i + '_button').css('color', 'black');
        }
    }
}


$(document).on('click', '#finish_contest', function () {
    if ($("#Finish_checkbox").prop("checked")) {
        finish_contest(question_response);
    }
    else {
        $('#checkbox_msg').text("Check the Checkbox To Finish Contest");
    }
});


function finish_contest(q_response) {
    if (finished == 0) {
        finished = 1;
    }
    else {
        return;
    }
    var ticketID = $('#ticketID').attr("ticketID");
    var qurl = "/finish_ticket/" + ticketID;
    var d = new Date;
    start_date = d.toISOString().split('T')[0];
    start_time = d.toTimeString().split(' ')[0];
    start_h = start_time.split(':')[0];
    start_m = start_time.split(':')[1];
    start_s = start_time.split(':')[2];
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        data: { start_date, start_h, start_m, start_s, q_response },
        success: function (data) {
            document.getElementById("thankYou").style.display = "block";
            // $('#myModal').removeClass('is-blurred');
            console.log(data);
        },
        error: function (jqXHR) {
            // noticity user to try later and your ticket is safe

            console.log("error in finish contest");
        }
    });
}