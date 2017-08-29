function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }
function disableregistration() {
    $('.btn-registration').click(function (e){
        $.ajax({
        url: 'registration',
        method: 'POST',
        data: $('.registration-form').serialize(),
        success: function(serverResponse){
            console.log("disabled");
            }
        })
    })
}
function attachConfirmClick() {
    console.log("Data:", $('.registration-form').serialize());
    $('#confirm').click(function(){
        $.ajax({
        url: 'registration',
        method: 'POST',
        data: $('.registration-form').serialize(),
        success: function(serverResponse){
                console.log('I am in success!!');
            }
        })
    })
}

function attachValidatorAjax(selector) {
    var selector = selector;
    var error_message;
    var display_message;
    var helper;
    if (selector === '#email'){
        error_message = 'email error';
        display_message = "Your Email must be in valid form";
        helper = "#emailHelp";
    } else if (selector === '#password'){
        error_message = 'password error';
        display_message = 'Your Password must be more than 5 characters';
        helper = '#passwordHelp'
    } else if (selector === '#fullname') {
        error_message = 'name error';
        display_message = 'Full name must be more than 3 characters';
        helper = '#nameHelp'
    } else {
        error_message = 'age error';
        display_message = 'Needs to be born first';
        helper = '#ageHelp'
    }
     $(selector).keyup(function (){
        $.ajax({
            url: 'validate',
            method: 'POST',
            data: $(this).serialize(),
            success: function(serverResponse) {
                if (serverResponse === error_message) {
                    if (!$('.btn-registration').hasClass('disabled')){
                        $('.btn-registration').addClass('disabled');
                    }       
                    $(helper).text(display_message);
                }
                else {
                    $(helper).text('');
                }
                if (serverResponse === 'no error'){
                    $('.btn-registration').removeClass('disabled');
                }

            }
        })
    })

}

$(document).ready(function () {

    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
    
    // $('.btn-registration').click(function (e){
    //     if ($(this).hasClass('disabled')){
    //         return false;
    //     }
    //     console.log("clicked");
    //     $.ajax({
    //     url: 'registration',
    //     method: 'POST',
    //     data: $('.registration-form').serialize(),
    //     success: function(serverResponse){
               
    //         }
    //     })
    // })
    attachConfirmClick();
    attachValidatorAjax('#email');
    attachValidatorAjax('#password');
    attachValidatorAjax('#fullname');
    attachValidatorAjax('#age');
    

});