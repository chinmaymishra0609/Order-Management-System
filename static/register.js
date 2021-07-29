
jQuery('#customerZip').blur(function (e) {
    var url = "{{ url_for('process') }}";
    jQuery.ajax({
        type: "POST",
        url: url,
        dataType: 'json',
        data: {"pincode":jQuery('#customerZip').val()}
    })
    .done(function (data) {
        if(data.result.PostOffice.length > 1){
            jQuery('#customerCity').find('option').not(':first').remove();
            for (i=0; i<data.result.PostOffice.length; i++){
                jQuery('#customerCity').append('<option value="'+ data.result.PostOffice[i].Name.toLowerCase() + '">'+ data.result.PostOffice[i].Name +'</option>');
            }
        }
        else{
            jQuery('#customerCity').append('<option value="'+ data.result.PostOffice[i].Name.toLowerCase() + '">'+ data.result.PostOffice[i].Name +'</option>');
        }
        jQuery('#customerDistrict').val(data.result.PostOffice[0].District);
        jQuery('#customerState').val(data.result.PostOffice[0].State);
        jQuery('#customerCountry').val("India");
    })
    .fail(function (data) {
            console.log("Error in ajax request.");
    });
    e.preventDefault();
});

jQuery.validator.setDefaults({
    submitHandler: function(){
        
        alert("submitted!");
        jQuery(form).ajaxSubmit();
    }
});

jQuery("#customerRegisterationForm").validate({
    onkeyup: false,
    rules:{
        customerName : {
            required : true
        },
        customerEmail : {
            email: true,
            maxlength: 255
        },
        customerContact : {
            required : true,
            minlength: 10,
            maxlength: 11,
            digits: true
        },
        customerZip : {
            required : true,
            digits: true
        },
        customerCity : {
            required : true
        }
    },
    messages:{
        customerName : {
            required: "Please fill customer name."
        },
        customerEmail : {            
            email: "Email must be an valid email address.",
            maxlength: "Username must not greater than 255 characters"
        },
        customerContact : {
            required: "Please fill contact number.",
            minlength: "Contact number must not less than 10 characters",
            maxlength: "Contact number must not greater than 11 characters",
            digits: "Contact number must contain only digits."
        },
        customerZip : {
            required: "Please fill pincode or zip number.",
            digits: "Zip number must contain only digits."
        },
        customerCity : {
            required: "Please select a city.",
        }
    }
    // ,
    // errorElement: "em",
    // errorPlacement: function ( error, element ) {
    // 	// Add the `help-block` class to the error element
    // 	error.addClass( "help-block" );

    // 	// Add `has-feedback` class to the parent div.form-group in order to add icons to inputs
    // 	element.parents( ".form-group" ).addClass( "has-feedback" );

    // 	// Add the span element, if doesn't exists, and apply the icon classes to it.
    // 	if ( !element.next( "span" )[ 0 ] ) {
    // 		jQuery( "<span class='glyphicon glyphicon-remove form-control-feedback'></span>" ).insertAfter( element );
    // 	}
    // },
    // success: function ( label, element ) {
    // 	// Add the span element, if doesn't exists, and apply the icon classes to it.
    // 	if ( !jQuery( element ).next( "span" )[ 0 ] ) {
    // 		jQuery( "<span class='glyphicon glyphicon-ok form-control-feedback'></span>" ).insertAfter( jQuery( element ) );
    // 	}
    // },
    // highlight: function ( element, errorClass, validClass ) {
    // 	jQuery( element ).parents( ".form-group" ).addClass( "has-error" ).removeClass( "has-success" );
    // 	jQuery( element ).next( "span" ).addClass( "glyphicon-remove" ).removeClass( "glyphicon-ok" );
    // },
    // unhighlight: function ( element, errorClass, validClass ) {
    // 	jQuery( element ).parents( ".form-group" ).addClass( "has-success" ).removeClass( "has-error" );
    // 	jQuery( element ).next( "span" ).addClass( "glyphicon-ok" ).removeClass( "glyphicon-remove" );
    // }
});

var response = "";
jQuery.validator.addMethod("validationEmail", function(value, element){
    jQuery.ajax({
        type: "POST",
        url : "{{ url_for('emailValidation') }}",
        dataType: "json",
        data: {"custEmail" : value},
        success: function(data){					
            if (Boolean(data.result) === true){
                response = true;
            }
            if (Boolean(data.result) === false){
                response = false;
            }
        }
    });
    return response;
}, "Username already available.");

jQuery.validator.addMethod("domain", function(value, element) {
    return this.optional(element) || /^http:\/\/www.befinanceguru.com/.test(value);
});
