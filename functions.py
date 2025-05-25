import random, json, time, requests, datetime, os, asyncio
from bs4 import BeautifulSoup
from aiogram.types import message
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from random import choice
from os import getcwd, remove

def randomWallpaper():
    with open("wallpapersInfo.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    randomWallpaperInfo = choice(data) 
    return randomWallpaperInfo.get("Ссылка")

async def DownloadWallpaper(randomWallpaper=randomWallpaper()):




    # Должен быть включенныый впн если на локалке. Сервак должен находиться в странах с разрешенным MoEwalls
    edge_driver_path = "./edgedriver_win64/msedgedriver.exe"
    edge_options = Options()
    edge_options.add_argument("--headless")
    # Аргументы для базовой настройки
    edge_options.add_argument("--disable-blink-features=AutomationControlled")  # Маскировка автоматизации
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0")

    # Опционально: отключить всплывающие окна и ошибки
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option("useAutomationExtension", False)
    edge_options.add_experimental_option('prefs', {
        'download.default_directory': os.path.join(getcwd(), "Wallpapers"),
        'download.prompt_for_download':False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })



    service = EdgeService(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.get(randomWallpaper)
    time.sleep(5)
    eulaSupport = driver.find_element(By.CLASS_NAME, "fc-button-label")
    eulaSupport.click()
    download_button = driver.find_element(By.ID, "moe-download")
    download_button.click()
    time.sleep(20)

    while True:
        if len(os.listdir("./Wallpapers")) == 1:
            print(os.listdir[0])
        else:
            print("Нема")
            



def intPages():
    url = "https://moewalls.com/page/1"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        numbersList = soup.find_all('a', class_="page-numbers")
    return numbersList[-2].get_text(strip=True)

def intWallpapers(i):

    url = "https://moewalls.com/page/{i}"
    response = requests.get(url)

    wallpapers = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('a', class_='g1-frame')
        for card in cards:
            classCard = card.get('class', [])
            if 'g1-injected-unit' not in classCard:
                wallpapers.append(card)
    numberWallpapers = len(wallpapers)
    return numberWallpapers


def parser():
    intpages = int(intPages())
    data = []

    for i in range(1, intpages):
        
        print(f"Создание файла с информацией о обоях {i}/{intpages}")
        url = f"https://moewalls.com/page/{i}/"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('a', class_='g1-frame')
            
            card_i = intWallpapers(i)
            for index, card in enumerate(cards, start=1):
                classCard = card.get('class', [])
                if  'g1-injected-unit' not in classCard:                
                    title = card.get('title', 'Названия нету')
                    href = card.get('href', "Ссылки нету")
                    data.append({"Название":title,"Ссылка":href})
        else:
            print(f"Ошибка при запросе: {response.status_code}") 
    print(f"Данные обновлены {datetime.datetime.now().strftime('%Y-%m-%d')}")

    with open("wallpapersInfo.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)