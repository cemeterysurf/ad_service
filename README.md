Python 3.10, FastAPI 0.110.0, Postgresql 16.2, Sqlalchemy 2.0.28 

Чтобы запустить приложение, нужно скопировать содержимое файла .env.example в файл .env и заполнить недостающие поля.
Затем с помощью команды docker-compose up -d запустить сервис и перейти по адресу http://localhost:7200/docs#/

Если данный метод не сработал, можно запустить приложение вручную: 

    Установить пакеты командой pip install -r requirements.txt,
    И запустить сервис: uvicorn backend.app:app --host 0.0.0.0 --port 7200