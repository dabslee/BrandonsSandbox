FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
# collectstatic into the bind-mounted staticfiles/ (host nginx serves it),
# then gunicorn on host-loopback (network_mode: host in compose).
CMD python manage.py collectstatic --noinput && \
    exec gunicorn PersonalSite.wsgi:application --bind 127.0.0.1:8000 --workers 3 \
      --access-logfile - --error-logfile -
