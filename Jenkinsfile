pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Clonando repositorio desde GitHub...'
                checkout scm
            }
        }

        stage('Setup & Test') {
            steps {
                echo 'Creando entorno virtual, instalando dependencias y ejecutando tests...'
                sh '''
                    # Crear entorno virtual
                    python3 -m venv .venv

                    # Actualizar pip dentro del venv
                    .venv/bin/pip install --upgrade pip

                    # Instalar dependencias del proyecto
                    .venv/bin/pip install -r requirements.txt

                    # Ejecutar pruebas unitarias con pytest
                    .venv/bin/pytest -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Construyendo imagen Docker catalogo-api:jenkins...'
                sh '''
                    docker build -t catalogo-api:jenkins .
                '''
            }
        }

        stage('Verify Docker Image') {
            steps {
                echo 'Verificando que la imagen Docker haya sido creada...'
                sh '''
                    docker images | grep catalogo-api || (echo "La imagen catalogo-api no existe" && exit 1)
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completado correctamente: tests OK e imagen Docker creada.'
        }
        failure {
            echo 'Falló el pipeline — revisar logs.'
        }
    }
}
