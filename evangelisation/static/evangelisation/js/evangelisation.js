$(function() {
    $(document).on('keyup', 'input[id^="id_form-"]', function() {
        input_val = $(this).val();
        console.log(input_val);
        if (input_val != '') {
            $(".form-name").html("formulaire de "+input_val);
        } else {
            $(".form-name").html("formulaire");
        }
    });

    /*$('input#id_form-0-nom_et_prenom').on('keyup', function(){
        input_val = $('input#id_form-0-nom_et_prenom').val();
        if (input_val != '') {
            $(".form-name").html("formulaire de "+input_val);
        } else {
            $(".form-name").html("formulaire");
        }
    })*/
});