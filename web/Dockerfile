FROM python:3.11.4

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=web.settings

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]