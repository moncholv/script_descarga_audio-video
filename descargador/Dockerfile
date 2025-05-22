FROM python:3.11-slim

# Evita preguntas interactivas al instalar
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# Crea un directorio de trabajo
WORKDIR /app

# Copia archivos
COPY requirements.txt .
COPY script_descarga.py .
COPY README.md .

# Instala dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Establece el punto de entrada
ENTRYPOINT ["python", "script_descarga.py"]
