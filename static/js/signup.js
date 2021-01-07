$(document).ready(function(){
    $('form').on('submit',function(event){
        
        if($('#password1').val() != $('#password2').val()){
            $('#errorAlert').show();
        }

        

        event.preventDefault();

    });
});