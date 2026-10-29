
pipeline {
    agent any

    parameters {
        choice(
            name: 'VERSION',
            choices: ['v1', 'v2', 'v3'],
            description: 'Select project version'
        )
    }

    environment {
        DOCKERHUB_USERNAME = 'mohanraj741'
        IMAGE_NAME = 'recommendation-show-list'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${params.VERSION}",
                    url: 'YOUR_GITHUB_REPOSITORY_URL'
            }
        }

        stage('Install Dependencies and Test') {
            steps {
                sh '''
                    python3 -m pip install -r requirements.txt
                    python3 -m pip install pytest
                    python3 -m pytest -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      --build-arg APP_VERSION=${VERSION} \
                      -t ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${VERSION} .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login \
                          -u "$DOCKER_USER" --password-stdin

                        docker push \
                          ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${VERSION}

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/${VERSION}.yaml
                    kubectl rollout status deployment/recommendation-${VERSION}
                '''
            }
        }
    }
}
