from bs4 import BeautifulSoup
import json,  requests, datetime
# Рандом обойки
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

               

 