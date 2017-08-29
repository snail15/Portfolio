$(document).ready(function () {
    $('.grid').masonry({
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        percentPosition: true,
        horizontalOrder: true,
        gutter: '.gutter-sizer'
    })
});