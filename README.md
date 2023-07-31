# HTTP микро-сервис для обработки csv-файлов

- - -

Данный микросервис был разработан на языке Python с помощью библиотек **Flask**, **pandas** и пакетным менеджером **poetry**. Данный проект предоставляет возможность загружать на сервер csv-файлы, просматривать их, 
а также искать и сортировать необходимые данные, полученные из csv-файла.

- - -

1. Установка локально с помощью пакетного менеджера **poetry**
* Склонировать репозиторий с помощью команды `git clone https://github.com/Cesoneemz/http-service-processing-files.git`
* Установить зависимости командой `poetry install`
* Запустить проект командой poetry run start-project
* Зайти на локальный адрес `localhost:5000` и пользоваться проектом!
* При необходимости тестирования можно запустить команду `poetry run pytest --verbose`
  
2.Установка с помощью Docker
* Склонировать репозиторий с помощью команды `git clone https://github.com/Cesoneemz/http-service-processing-files.git`
* Собрать образ проекта с помощью команды `docker build . -t <image_name>`. Итоговый образ будет весить около **293 Mb**
* Запустить докер-образ с помощью команды `docker run -d -p <port>:5000 -v <path_to_folder>:/app/http-service-processing-files/uploads <image_name>`
* Зайти на адрес `localhost:<port>` и пользоваться сервисом

- - -

© Danila Gusakov 2023
