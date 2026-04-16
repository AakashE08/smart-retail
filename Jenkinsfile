pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Code pulled from GitHub'
            }
        }

        stage('Build') {
            steps {
                bat 'echo Building project...'
            }
        }

        stage('Test') {
            steps {
                bat 'echo Running tests...'
            }
        }

        stage('Deploy') {
            steps {
                bat 'echo Deployment successful'
            }
        }
    }
}
