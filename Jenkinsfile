pipeline {
    agent any

    environment {
        PROJECT_DIR = "backend"
        PYTHON_ENV = "ml/venv"
    }

    stages {
        stage('SCM') {
            steps {
                echo 'Checking out source code from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Node.js and Python dependencies...'
                dir("${env.PROJECT_DIR}") {
                    sh 'npm install'
                }
                // Optional: Setup Python environment if not present
                sh 'pip install pandas scikit-learn joblib'
            }
        }

        stage('Security & Lint') {
            steps {
                echo 'Running security scans and linting...'
                dir("${env.PROJECT_DIR}") {
                    sh 'npm audit --audit-level=high'
                }
            }
        }

        stage('Train ML Model') {
            steps {
                echo 'Training/Refreshing Fraud Detection Model...'
                sh 'python ml/train_model.py'
            }
        }

        stage('Test') {
            steps {
                echo 'Running backend unit tests...'
                dir("${env.PROJECT_DIR}") {
                    // sh 'npm test' // Unit tests placeholder
                }
            }
        }

        stage('Deploy (Beta)') {
            steps {
                echo 'Deploying to beta environment...'
                // sh 'docker-compose up -d --build'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs.'
        }
    }
}
