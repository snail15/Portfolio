function activateMasonary(){

    // var $grid = $('.grid').imagesLoaded( function() {
    //     $grid.masonry({
    //         itemSelector: '.grid-item',
    //         columnWidth: '.grid-sizer',
    //         percentPosition: true,
    //         horizontalOrder: true,
    //         gutter: '.gutter-sizer',
    //     });
    // });

    // init Masonry
    var $grid = $('.grid').masonry({
    // options...
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        percentPosition: true,
        horizontalOrder: true,
        gutter: '.gutter-sizer',
    });
    // layout Masonry after each image loads
    $grid.imagesLoaded().progress( function() {
        $grid.masonry('layout');
    });

}
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

function activateSearch(selector) {
     $(selector).keyup(function(){
         $.ajax({
            url: 'search',
            method: 'POST',
            data: $(selector).parent().serialize(),
            success: function(serverResponse) {
                $('.pin-row').html(serverResponse)
                if (selector === '#search-bar'){
                    activateMasonary();
                    activateHover('.card-wrapper');
                    activateHover('.board-wrapper')
                }
            }
        })
    })
}

function activateDeleteComment(selector){
      $(selector).click(function(){
        $.ajax({
            url: $(this).attr('path'),
            method: 'GET',
            success: function(serverResponse) {
                $('.comment-row').html(serverResponse);
            },
            complete: function() {
                activateDeleteComment('.shame');
            }
        })
    })
}

function activateHover(selector){

    $(selector).hover(function(){
        $(this).css('background-color', 'wheat');
        $(this).find('a').css('visibility', 'visible');
    }, function(){
        $(this).css('background-color', '');
        $(this).find('a').css('visibility', 'hidden');
    })
}

function activateUnpin(selector){
    $(selector).click(function(){
         $.ajax({
            url: $(this).attr('path'),
            method: 'GET',
            success: function(serverResponse) {
                $('#content-row').html(serverResponse);
            },
            complete: function() {
                activateMasonary();
                activateHover('.card-wrapper');
            }

        })
    })
}

$(document).ready(function () {
   
    activateMasonary();

    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    activateSearch('#search-bar');
    activateSearch('#search-user');
    activateHover('.card-wrapper');
    activateHover('.board-wrapper')
   

    $('.btn-comment').click(function(){
        $.ajax({
            url: 'comment/create',
            method: 'POST',
            data: $('#comment-form').serialize(),
            success: function(serverResponse) {
                $('.comment-row').append(serverResponse);
                $('#comment').val('');
            },
            complete: function(){
                activateDeleteComment('.shame');
            }
        })
    })

    $('.shame').click(function(){
        $.ajax({
            url: $(this).attr('path'),
            method: 'GET',
            success: function(serverResponse) {
                $('.comment-row').html(serverResponse);
                
            },
            complete: function() {
                activateDeleteComment('.shame');
            }
        })
    })

    $('#showBoard').click(function (){
        if ($('#showPin').hasClass('underline')){
            $('#showPin').removeClass('underline');
        }
        if (!$(this).hasClass('underline')){
            $(this).addClass('underline');
        }
        $.ajax({
            url: $(this).attr('path'),
            method: 'GET',
            success: function(serverResponse) {
                $('#content-row').html(serverResponse);
            },
            complete: function() {
                activateHover('.board-wrapper');
            }

        })
    })

    $('#showPin').click(function (){
        if (!$(this).hasClass('underline')){
            $(this).addClass('underline');
        }
        if ($('#showBoard').hasClass('underline')){
            $('#showBoard').removeClass('underline');
        }
        $.ajax({
            url: $(this).attr('path'),
            method: 'GET',
            success: function(serverResponse) {
                $('#content-row').html(serverResponse);
            },
            complete: function() {
                activateMasonary();
                activateHover('.card-wrapper');
                activateUnpin('.unpin');
            }

        })
    })

    $('.unpin').click(function(){
         $.ajax({
            url: $(this).attr('path'),
            method: 'GET',
            success: function(serverResponse) {
                $('#content-row').html(serverResponse);
            },
            complete: function() {
                activateMasonary();
                activateHover('.card-wrapper');
                activateUnpin('.unpin');
            }

        })
    })

    $(".thumbnail").imgCheckbox();


});