function activateMasonary(){
     $('.grid').masonry({
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        percentPosition: true,
        horizontalOrder: true,
        gutter: '.gutter-sizer'
    })
}

$(document).ready(function () {
    activateMasonary();
});