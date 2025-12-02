pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup & Test') {
      steps {
        sh """
          python3 -m venv .venv
          source .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          pytest -q
        """
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          docker.build("catalogo-api:jenkins")
        }
      }
    }

    stage('Verify Docker Image') {
      steps {
        sh 'docker images | grep catalogo-api'
      }
    }
  }

  post {
    success {
      echo 'Build completo: tests pasaron y la imagen Docker fue generada.'
    }
    failure {
      echo 'Falló el pipeline — revisar logs.'
    }
    always {
      cleanWs()
    }
  }
}
