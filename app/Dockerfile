FROM python:3.7.5-slim
RUN mkdir -p /var/app/flask_app
WORKDIR /var/app/flask_app
COPY requirement.txt /var/app/flask_app
RUN apt-get update
RUN apt-get install -y default-libmysqlclient-dev gcc
RUN pip install --no-cache-dir -r requirement.txt
COPY . /var/app/flask_app
ENV FLASK_APP ../app.py
CMD exec gunicorn -w 1 -b :8012 app:app --reload