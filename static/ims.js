jQuery(".center").css({
    'left' : jQuery(window).width()/2 - jQuery(".center").width()/2,
    'top' : jQuery(window).height()/2 - jQuery(".center").height()/2,
    'position' : 'absolute'
});

jQuery(window).resize(function(){jQuery("#customerRegistrationPanel").css({
        'left' : jQuery(window).width()/2 - jQuery("#customerRegistrationPanel").width()/2,
        'right' : jQuery(window).height()/2 - jQuery("#customerRegistrationPanel").height()/2,
        'position' : 'absolute'
    });
});