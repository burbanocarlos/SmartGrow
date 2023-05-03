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
        stage('Copy local_settings.py') {
            steps {
                configFileProvider([configFile(fileId: '4ba70017-bf34-4252-bcaf-a5474b5b1d39', targetLocation: './smartGrowIoT/smartGrowIoT/local_settings.py')]) {
                    // This step will copy the local_settings.py file to the smartGrowIoT directory
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
