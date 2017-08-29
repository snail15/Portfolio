
$(document).ready(function () {
    $(".tooltipster").tooltipster({
        theme: "tooltipster-shadow"
    });
    // $(function(){
    //     $(".type").typed({
    //         strings: ["a Web Developer", "an Attorney"],
    //         loop: true
    //     })
    // })

    //smooth scroll
    $(function () {
        $('a[href*="#"]:not([href="#"])').click(function () {
            if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                if (target.length) {
                    $('html, body').animate({
                        scrollTop: target.offset().top
                    }, 1000);
                    return false;
                }
            }
        });
    });
    
    $("#aboutme").waypoint(function (direction){
        
        if (direction == "down"){
            $(".profile-card1").addClass("animated slideInLeft");
            $(".profile-card2").addClass("animated slideInDown");
            $(".profile-card3").addClass("animated slideInRight");
        } else {
            $(".profile-card1").removeClass("animated slideInLeft");
            $(".profile-card2").removeClass("animated slideInDown");
            $(".profile-card3").removeClass("animated slideInRight");
        }

    }, {
        offset: "30%"
    })

    $('#aboutme').waypoint(function(direction) {
        if (direction == "down") {
            $('.nav').addClass('sticky');
        } else {
            $('.nav').removeClass('sticky');
        }
    }, {
      offset: '85%;'
    });


});

