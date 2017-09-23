
// Smooth Scroll on clicking nav items
$('nav a').click(function () {
  var $href = $(this).attr('href');
  $('body').stop().animate({
    scrollTop: $($href).offset().top - 30
  }, 1000);
  return false;
});

// Smooth scroll on logo click
$('footer a').click(function () {
  var $href = $(this).attr('href');
  $('body').stop().animate({
    scrollTop: $($href).offset().top - 30
  }, 1000);
  return false;
});

// Smooth scroll to top of clicked experience section
$('.collapse').on('shown.bs.collapse', function(e) {
  var $card = $(this).closest('.card');
  $('html,body').animate({
    scrollTop: $card.offset().top - 10
  }, 500);
});
