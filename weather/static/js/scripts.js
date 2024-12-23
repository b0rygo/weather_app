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
                    if (response.sunrise) {
                        // Wyświetlamy miasto oraz dane pogodowe
                        $('#sunrise-time-container').html(
                            'Miasto: ' + response.city + '<br>' +
                            'Godzina wschodu słońca: ' + response.sunrise + '<br>' +
                            'Godzina zachodu słońca: ' + (response.sunset || 'Brak danych') + '<br>' +
                            'Temperatura: ' + (response.temperature + '°C' || 'Brak danych') + '<br>' +
                            'Opady deszczu: ' + (response.precipitation + '°C'|| 'Brak danych') + '<br>' +
                            'Wiatr: ' + (response.wind || 'Brak danych')
                        );
                    } else {
                        $('#sunrise-time-container').html(response.error);
                    }
                },
                error: function () {
                    $('#sunrise-time-container').html('Wystąpił błąd podczas próby pobrania danych pogodowych.');
                }
            });
        } else {
            $('#sunrise-time-container').html('Proszę wprowadzić nazwę miasta.');
        }
    });
});