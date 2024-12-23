from django.shortcuts import render
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
from lxml import html


def home(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        data = scrape_data(city)
        return JsonResponse({'data': data})
    return render(request, 'sites/main.html')


def scrape_data(city):
    url = f"https://meteobox.pl/{city.lower()}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            tree = html.fromstring(response.content)

            # XPath dla odpowiednich elementów
            sunrise_element = tree.xpath('//*[@id="basicastro"]/text()')
            sunset_element = tree.xpath('//*[@id="basicastro"]/text()[2]')
            temperature_element = tree.xpath('//*[@id="svgforecast"]/svg/text[3]')
            precipitation_element = tree.xpath('//*[@id="svgforecast"]/svg/text[7]')
            wind_element = tree.xpath('//*[@id="svgforecast"]/svg/text[9]')

            print(temperature_element)
            # Pobieranie i przetwarzanie danych
            sunrise = sunrise_element[0].strip()[-5:] if sunrise_element and isinstance(sunrise_element[0],str) else None
            sunset = sunset_element[0].strip()[-5:] if sunset_element and isinstance(sunset_element[0], str) else None
            temperature = temperature_element[0].text.strip() if temperature_element and hasattr(temperature_element[0], 'text') else None
            precipitation = precipitation_element[0].text.strip() if precipitation_element and hasattr(precipitation_element[0], 'text') else None
            wind = wind_element[0].text.strip() if wind_element and hasattr(wind_element[0], 'text') else None

            # Zwracamy wszystkie dane
            return {
                "sunrise": sunrise,
                "sunset": sunset,
                "temperature": temperature,
                "precipitation": precipitation,
                "wind": wind,
                "city": city.capitalize()
            }
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def index(request):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        city = request.GET.get('city')
        if city:
            weather_data = scrape_data(city)
            if weather_data:
                return JsonResponse(weather_data)
            else:
                return JsonResponse({'error': 'Nie udało się pobrać danych pogodowych.'})
        else:
            return JsonResponse({'error': 'Miasto nie zostało podane.'})

    return render(request, 'sites/main.html')

