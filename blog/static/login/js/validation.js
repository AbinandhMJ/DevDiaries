$(document).ready(function () {
    // Reset form fields on page refresh
    $('#registrationForm')[0].reset();

    // Initialize jQuery validation for the form
    $('#registrationForm').validate({
        rules: {
            {% for field in form %}
                {% if field.name != 'csrfmiddlewaretoken' %}
                    "{{ field.name }}": {
                        required: true
                    },
                {% endif %}
            {% endfor %}
        },
        messages: {
            {% for field in form %}
                {% if field.name != 'csrfmiddlewaretoken' %}
                    "{{ field.name }}": {
                        required: "{{ field.label }} is required."
                    },
                {% endif %}
            {% endfor %}
        },
        errorPlacement: function(error, element) {
            error.appendTo(element.closest('.form-group').find('.helptext')); // Append error message to the helptext span
        },
        highlight: function(element, errorClass, validClass) {
            $(element).closest('.form-group').addClass('has-error');
            $(element).closest('.form-group').removeClass('has-success');
            $(element).closest('.form-group').addClass('animated shake'); // Add shake animation class
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).closest('.form-group').removeClass('has-error');
            $(element).closest('.form-group').addClass('has-success');
            $(element).closest('.form-group').removeClass('animated shake'); // Remove shake animation class
        }
    });
});
