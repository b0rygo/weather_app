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

            # XPath, aby znaleźć godzinę wschodu słońca
            sun_element = tree.xpath('//*[@id="basicastro"]/text()')
            sun_element1 = tree.xpath('//*[@id="basicastro"]/text()[2]')

            if sun_element:
                data = sun_element[0].strip()
                data1 = sun_element1[0].strip()
                # Wyciągamy godzinę
                time = data[-5:]
                time1 = data1[-5:]
                return time + time1
            return None
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None


def index(request):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        city = request.GET.get('city')
        if city:
            sunrise_time = scrape_data(city)
            if sunrise_time:
                return JsonResponse({'time': sunrise_time, 'city': city})
            else:
                return JsonResponse({'error': 'Nie udało się pobrać godziny wschodu słońca.'})
        else:
            return JsonResponse({'error': 'Miasto nie zostało podane.'})

    return render(request, 'sites/main.html')

