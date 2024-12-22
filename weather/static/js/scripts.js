// ajax_script.js
$(document).ready(function () {
    $('#get-sunrise').click(function () {
        var city = $('#city').val();

        if (city) {
            // Wysyłamy zapytanie AJAX do serwera
            $.ajax({
                url: "", // Działa na tej samej stronie (GET do widoku 'index')
                method: "GET",
                data: {
                    'city': city,
                },
                success: function (response) {
                    if (response.time) {
                        // Wyświetlamy miasto oraz godzinę wschodu słońca
                        $('#sunrise-time-container').html('Miasto: ' + response.city + '<br>Godzina wschodu słońca: ' + response.time);
                    } else {
                        $('#sunrise-time-container').html(response.error);
                    }
                },
                error: function () {
                    $('#sunrise-time-container').html('Wystąpił błąd podczas próby pobrania godziny.');
                }
            });
        } else {
            $('#sunrise-time-container').html('Proszę wprowadzić nazwę miasta.');
        }
    });
});
