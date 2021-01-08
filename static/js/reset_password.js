$(document).ready(function(){
    $('form').on('submit',function(event){
        
        $.ajax({
            data : {
                email : $('#email_hidden').val(),
                token : $('#token_hidden').val(),
                password : $('#password1').val(),
                password2 : $('#password2').val()
            },
            type : 'POST',
            url : '/reset_password_confirm_api'
        })


        .done(function(){
            if(data.error){
                $('#errorAlert').setAttribute("type", "text");
                $('#successAlert').setAttribute("type", "hidden");
            }
            if(data.done){
                $('#successAlert').setAttribute("type", "text");
                $('#errorAlert').setAttribute("type", "hidden");
            }
        });

        event.preventDefault();

    });
});
    