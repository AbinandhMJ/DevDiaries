(function ($) {
    'use strict';

    var $window = $(window);

    // :: Preloader Active Code
    $window.on('load', function () {
        $('#preloader').fadeOut('slow', function () {
            $(this).remove();
        });
    });

    // :: Nav Active Code
    if ($.fn.classyNav) {
        $('#originalNav').classyNav();
        $('#footerNav').classyNav();
    }

    // :: Newsticker Active Code
    if ($.fn.simpleTicker) {
        $.simpleTicker($("#breakingNewsTicker"), {
            speed: 1000,
            delay: 3500,
            easing: 'swing',
            effectType: 'roll'
        });
    }

    // :: Tooltip Active Code
    $('[data-toggle="tooltip"]').tooltip();

    // :: Owl Carousel Active Code
    // ... (Your existing Owl Carousel code)

    // :: Countdown Active Code
    if ($.fn.countdown) {
        $('#clock').countdown('2020/10/10', function (event) {
            $(this).html(event.strftime('<div>%D <span>Days</span></div> <div>%H <span>Hours</span></div> <div>%M <span>Minutes</span></div> <div>%S <span>Seconds</span></div>'));
        });
    }

    // :: CounterUp Active Code
    if ($.fn.counterUp) {
        $('.counter').counterUp({
            delay: 10,
            time: 2000
        });
    }

    // :: ScrollUp Active Code
    if ($.fn.scrollUp) {
        $.scrollUp({
            scrollSpeed: 1000,
            easingType: 'easeInOutQuart',
            scrollText: 'Top'
        });
    }

    // :: PreventDefault a Click
    $("a[href='#']").on('click', function ($) {
        $.preventDefault();
    });

    // :: WOW Active Code
    if ($window.width() > 767) {
        new WOW().init();
    }

    // :: Sticky Header Code
    $window.on('scroll', function () {
        var scroll = $window.scrollTop();
        var header = $("#stickyNav");

        if (scroll >= 100) {
            header.addClass('sticky');
        } else {
            header.removeClass('sticky');
        }
    });

})(jQuery);
