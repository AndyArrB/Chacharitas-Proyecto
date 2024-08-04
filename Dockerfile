FROM laudio/pyodbc:latest
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
