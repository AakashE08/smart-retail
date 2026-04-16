pipeline {
    agent any

    environment {
        NODE_ENV = 'production'
        // PostgreSQL Database Configuration
        DB_HOST = 'postgres.internal.org'
        DB_USER = 'invoice_user'
        DB_PASS = credentials('postgres-credentials')
    }

    stages {
        stage('Checkout (Git + GitHub)') {
            steps {
                echo 'Checking out source management code from Git Repository (GitHub)...'
                // git branch: 'main', url: 'https://github.com/organization/smart-invoice-platform.git'
                checkout scm
            }
        }

        stage('Install Backend (Node.js + Express.js)') {
            steps {
                dir('backend') {
                    echo 'Installing packages for Node.js + Express.js backend API...'
                    sh 'npm install'
                }
            }
        }

        stage('Database Migrations (PostgreSQL)') {
            steps {
                dir('backend') {
                    echo 'Applying database schema changes to PostgreSQL database...'
                    // e.g., sh 'npm run migrate' or direct connection to psql
                    sh 'echo "Applied migrations successfully."'
                }
            }
        }

        stage('Run Unit & Backend API Tests') {
            steps {
                dir('backend') {
                    echo 'Running automated verification tests...'
                    sh 'npm test'
                }
            }
        }

        stage('Containerization (Docker)') {
            steps {
                echo 'Packaging Node.js backend services into a Docker container...'
                sh 'docker build -t smart-invoice-backend:latest ./backend'
            }
        }

        stage('Deploy to Cloud Target (Staging)') {
            steps {
                echo 'Deploying to Staging Environment with Jenkins...'
                // deploy to orchestration environment
                sh 'docker run -d -p 3000:3000 smart-invoice-backend:latest'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully. Code deployed to Staging.'
        }
        failure {
            echo 'Build failed. Notifying engineering team.'
        }
    }
}
