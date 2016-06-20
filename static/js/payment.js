$(function() {


    $("#chargeForm input,#chargeForm textarea").jqBootstrapValidation({
        // preventSubmit: true,
        submitError: function($form, event, errors) {
            // additional error messages or events
        },
        submitSuccess: function($form, event) {
            event.preventDefault(); // prevent default submit behaviour
            var $button = $("#pay_btn");
            var name = $("input#name2").val();
            var email = $("input#email2").val();
            var phone = $("input#phone2").val();
            var message = $("textarea#comment").val();
            var opts = $.extend({'email':email}, $button.data(), {
                token: function(result) {
                $form.append($('<input>').attr({ type: 'hidden', name: 'stripeToken', id:'stripeToken_id', value: result.id })).submit();
                }
            });

            params   = $form.serializeArray();
            if (params.length == 0){
                StripeCheckout.open(opts);
            }
            else{

                $.ajax({
                    url: "./charge",
                    type: "POST",
                    data: {
                        first_name: name,
                        last_name: phone,
                        email: email,
                        comment: message,
                        stripeToken:params[0]['value']
                    },
                    cache: false,
                    success: function() {
                        // Success message
                        $('#success2').html("<div class='alert alert-success'>");
                        $('#success2 > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                            .append("</button>");
                        $('#success2 > .alert-success')
                            .append("<strong>Payment Confirmed, a confirmation email will be sent to you shortly. </strong>");
                        $('#success2 > .alert-success')
                            .append('</div>');

                        //clear all fields
                        $('#chargeForm').trigger("reset");
                        $('#stripeToken_id').remove();

                    },
                    error: function() {
                        // Fail message
                        $('#success2').html("<div class='alert alert-danger'>");
                        $('#success2 > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                            .append("</button>");
                        $('#success2 > .alert-danger').append("<strong>Sorry, something went wrong. Please try again later!");
                        $('#success2 > .alert-danger').append('</div>');
                        //clear all fields
                        $('#chargeForm').trigger("reset");
                        $('#stripeToken_id').remove();
                    },
                })
            }
        },
        filter: function() {
            return $(this).is(":visible");
        },
    });


    $("a[data-toggle=\"tab\"]").click(function(e) {
        e.preventDefault();
        $(this).tab("show");
    });


});


/*When clicking on Full hide fail/success boxes */
$('#name2').focus(function() {
    $('#success2').html('');
});
