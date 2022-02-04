import sys
from spn import spn_
import os
import pygame
# Этот класс поможет нам сделать картинку из потока байт

import requests


pygame.init()

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

t, t2 = spn_(json_response)

delta, delta2 = str(abs(t[0] - t2[0])), str(abs(t[1] - t2[1]))
# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta, delta2]),
    "l": "map",
    "pt": ",".join([toponym_longitude, toponym_lattitude]) + ",pm2rdm",
    "size": "650,450"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

clock = pygame.time.Clock()
size = width, height = 650, 450
screen = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove(map_file)
            sys.exit()
    screen.fill((0, 0, 0))
    k = pygame.image.load(f'map.png').convert()
    screen.blit(k, (0, 0))

    font = pygame.font.Font(None, 30)
    text = font.render(map_params["ll"], True, (200, 10, 10))
    screen.blit(text, (340, 220))

    pygame.display.flip()
    clock.tick(60)
