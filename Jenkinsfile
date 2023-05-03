def config = new ConfigSlurper().parseText(
  new ConfigFileProvider().getFileContentsByName('local_settings.py')
)

environment {
  SECRET_KEY = config.SECRET_KEY
  TPLINK_USERNAME = config.TPLINK_USERNAME
  TPLINK_PASSWORD = config.TPLINK_PASSWORD
}

pipeline {
    agent any

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    if (isUnix()) {
                        sh '/Users/carlosburbano/.pyenv/shims/python3.9 -m venv venv'
                        sh 'source venv/bin/activate'
                    } else {
                        bat 'python -m venv venv'
                        bat 'call venv\\Scripts\\activate.bat'
                    }
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'venv/bin/pip install -r requirements.txt'
                    } else {
                        bat 'pip install -r requirements.txt'
                    }
                }
            }
        }
        stage('Run Migrations') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'venv/bin/python smartGrowIoT/manage.py migrate'
                    } else {
                        bat 'venv\\Scripts\\python smartGrowIoT\\manage.py migrate'
                    }
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'venv/bin/python smartGrowIoT/manage.py test'
                    } else {
                        bat 'venv\\Scripts\\python smartGrowIoT\\manage.py test'
                    }
                }
            }
        }
    }
}
