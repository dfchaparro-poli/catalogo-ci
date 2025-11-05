FROM python:3.12-slim

# Crea un usuario sin privilegios para ejecutar la app
RUN useradd -m appuser

# Define el directorio de trabajo
WORKDIR /app

# Instala herramientas necesarias (curl y sqlite)
RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 curl && \
    rm -rf /var/lib/apt/lists/*

# Copia los requisitos e instala dependencias
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia la aplicación
COPY app /app/app

# Crea carpeta para la base de datos
RUN mkdir -p /app/data && chown -R appuser:appuser /app
ENV DATABASE_URL=sqlite:////app/data/app.db

EXPOSE 8000

USER appuser

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
