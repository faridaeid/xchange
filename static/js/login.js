$(function() {
   $("#login_tab").click(function (e) {
       $("#login_form_id").delay(100).fadeIn(100);
       $("#signup_form_id").fadeOut(100);
       $("#signup_tab").removeClass('active');
       $(this).addClass('active');
   });

    $("#signup_tab").click(function (e) {
       $("#signup_form_id").delay(100).fadeIn(100);
       $("#login_form_id").fadeOut(100);
       $("#login_tab").removeClass('active');
       $(this).addClass('active');
   })
});

