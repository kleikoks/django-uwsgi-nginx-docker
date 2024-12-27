FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update
RUN apt-get install -y nginx
RUN apt-get install -y supervisor

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./compose/start-celery-worker /tmp/start-celery-worker
RUN sed -i 's/\r$//g' /tmp/start-celery-worker
RUN chmod +x /tmp/start-celery-worker

COPY ./compose/start-celery-beat /tmp/start-celery-beat
RUN sed -i 's/\r$//g' /tmp/start-celery-beat
RUN chmod +x /tmp/start-celery-beat

COPY ./compose/start-celery-flower /tmp/start-celery-flower
RUN sed -i 's/\r$//g' /tmp/start-celery-flower
RUN chmod +x /tmp/start-celery-flower

COPY ./compose/start-django /tmp/start-django
RUN sed -i 's/\r$//g' /tmp/start-django
RUN chmod +x /tmp/start-django

COPY . .

RUN mkdir -p /tmp/logs

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /app/compose/conf/site.conf /etc/nginx/sites-enabled/site.conf
RUN ln -s /app/compose/conf/supervisor.conf /etc/supervisor/conf.d/
