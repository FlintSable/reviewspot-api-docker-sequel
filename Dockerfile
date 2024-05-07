FROM python:3.11.5
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV GOOGLE_APPLICATION_CREDENTIALS=./secrets/key.json
RUN export $(grep -v '^#' /app/secrets/db.json | xargs)
EXPOSE 8080
CMD ["python", "main.py"]