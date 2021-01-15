function get_prize_tag(contestid, id) {
    $(id).text("##").show();
    var qurl = "/get_contest_pay/"+contestid;
    $.ajax({
        type: "POST",
        cache: false,
        url: qurl,
        dataType: "json",
        success: function (data) {
            console.log(data.value);
            $(id).text(data.value).show();
        },
        error: function (jqXHR) {
            alert("error: " + jqXHR.status);
            console.log(jqXHR);
        }
    });
}