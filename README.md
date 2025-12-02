# Catálogo (API)

Descripción
----------
API REST para gestionar un catálogo multimedia (películas, series y juegos). Incluye operaciones CRUD, configuración de base de datos (SQLite) y endpoints públicos para consumo. También se provee configuración Docker para ejecución local/producción ligera.

Estructura del proyecto
-----------------------
- app/                 -> código fuente de la aplicación (FastAPI, modelos, rutas, seed, etc.)
- docker-compose.yml   -> orquesta servicios (api, client, seed)
- Dockerfile           -> imagen de la API (si aplica)
- requirements.txt     -> dependencias Python
- .env.example         -> ejemplo de variables de entorno (si existe)
- data/                -> (local) contenedor/volumen para la base de datos SQLite
- README.md            -> este documento

Requisitos
----------
- Python 3.12.3 (recomendado)
- pip
- virtualenv / venv o pyenv (opcional)
- Docker & docker-compose (opcional, para ejecutar con contenedores)

Instalación y ejecución: guía paso a paso (Linux)
------------------------------------------------

A) Preparar Python 3.12.3
- Usando pyenv (recomendado si no tienes 3.12.3):
  - Instalar pyenv: sigue la guía oficial https://github.com/pyenv/pyenv
  - Instalar versión: `pyenv install 3.12.3`
  - Seleccionar localmente: `pyenv local 3.12.3`
- O usar el binario del sistema si ya tienes Python 3.12.3.

B) Crear y activar entorno virtual
- Desde la raíz del repo:
  - `python3.12 -m venv .venv`
  - `source .venv/bin/activate`

C) Instalar dependencias
- `pip install --upgrade pip`
- `pip install -r requirements.txt`

D) Variables de entorno
- Crear archivo `.env` en la raíz (opcional). Ejemplo mínimo:
  - `DATABASE_URL=sqlite:///./data/app.db`
- Para ejecución en contenedor o con la configuración por defecto Docker se usa: `sqlite:////app/data/app.db`

E) Preparar base de datos local
- Crear carpeta de datos:
  - `mkdir -p data`
- Si la aplicación incluye un módulo de seed, ejecutarlo para crear tablas y datos iniciales:
  - `python -m app.seed`
- Si no hay seed, al iniciar la API normalmente se crea el archivo SQLite y las tablas (dependiendo de la implementación).

F) Ejecutar la API en desarrollo (uvicorn)
- Desde la raíz del proyecto:
  - `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- Abrir en el navegador:
  - Documentación interactiva: http://localhost:8000/docs
  - Health: http://localhost:8000/health

G) Ejecutar con Docker (recomendado para entorno aislado)
- Construir y levantar con docker-compose:
  - `docker-compose up --build`
- Ejecutar en background:
  - `docker-compose up --build -d`
- Ver logs:
  - `docker-compose logs -f api`
- El servicio `seed` en docker-compose está pensado para correr una vez y sembrar datos. Si lo incluyes en el `up`, se ejecutará cuando la API esté healthy. También puedes correr:
  - `docker-compose run --rm seed` (si la imagen ya está construida)

Entorno ya Listo
--------------------
Una vez el entorno ya esta listo solo es necesario usar la imagen de docker con el siguiente comando:
- `docker compose up -d`

Endpoints (ejemplos)
--------------------
- GET /health           -> estado del servicio
- GET /movies           -> listar películas
- POST /movies          -> crear película
- GET /movies/{id}      -> obtener película por id
- PUT /movies/{id}      -> actualizar
- DELETE /movies/{id}   -> borrar
- (igual para /series y /games)

Ejemplos curl
-------------
- Health:
  - `curl http://localhost:8000/health`
- Listar películas (muestra los primeros 300 caracteres):
  - `curl -s http://localhost:8000/movies | head -c 300`

Notas sobre configuración
-------------------------
- En entorno local se usa `DATABASE_URL=sqlite:///./data/app.db` (ruta relativa).
- En Docker la ruta monta un volumen y la URL en docker-compose es `sqlite:////app/data/app.db`.
- Si usas otro motor de BD (Postgres/MySQL), exporta la URL correspondiente y ajusta dependencias/configuración.

Resolución de problemas comunes
-------------------------------
- Permisos al crear `data/app.db`: asegurar permisos de escritura en la carpeta `data`.
- Puerto 8000 en uso: cambiar puerto en `uvicorn` o en `docker-compose.yml`.
- Error de versión de Python: verificar `python --version` y usar pyenv o instalar 3.12.3.
- Dependencias no instaladas: activar el virtualenv antes de ejecutar `pip install -r requirements.txt`.

Buenas prácticas
----------------
- Añadir `.env` a `.gitignore` (ya incluido).
- Mantener el volumen Docker para persistencia de datos.
- Versionar requirements y reconstruir imagen cuando cambien dependencias.


Licencia
--------
Añade aquí tu licencia preferida (MIT, Apache, etc.) o elimina esta sección si no aplica.

- Test WebHook