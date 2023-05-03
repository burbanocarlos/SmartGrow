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
                        sh 'pip install -r requirements.txt'
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
                        sh 'python manage.py migrate'
                    } else {
                        bat 'python manage.py migrate'
                    }
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python manage.py test'
                    } else {
                        bat 'python manage.py test'
                    }
                }
            }
        }
    }
}
