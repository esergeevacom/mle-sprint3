# возьмем образ, который мы скачали ранее и в котором уже установлен Python
FROM python:3.11-slim


# копируем файлы в Docker
COPY . ./cow_dir


# изменяем рабочую директорию Docker
WORKDIR cow_dir


# в Docker изначально нет библиотеки python-cowsay
# вам нужно инструкцию RUN, которая установит библиотеку с помощью pip
RUN ["pip3", "install", "python-cowsay"]


# команда, которая должна исполняться при старте контейнера
CMD ["python3", "./main.py"]
