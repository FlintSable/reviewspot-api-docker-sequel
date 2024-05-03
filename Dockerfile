FROM python:3.12
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV GOOGLE_APPLICATION_CREDENTIALS=./secrets/reviewspot-api-docker-sequel-642ee89c74f0.json
EXPOSE 8080
CMD ["python", "main.py"]
