(function ($) {
    window.savanoriai = {};

    var savanoriai = window.savanoriai;

    savanoriai.toggle_choice(button, url, volunteer_id) {
        $.post(url, {'volunteer_id': volunteer_id}, function(data) {
            if (data.state == 'free') {
                label = 'info';
            } else if (data.state == 'accepted') {
                label = 'success';
            } else if (data.state == 'invited') {
                label = 'warning';
            } else {
                label = 'danger';
            }
            $(button).parent().html('<span class="label label-' + label + '">' + data.label + '</span>');
        });
    };
}(jQuery));


(function ($) {
    // Set up Django csrftoken handling

    var csrftoken = getCookie('csrftoken');

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}(jQuery));
