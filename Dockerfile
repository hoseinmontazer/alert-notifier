FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install flask requests

EXPOSE 80

CMD ["python", "alert-notifier.py"]

