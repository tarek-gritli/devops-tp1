pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "lgritli/mon-app-devops"

        DOCKER_CREDENTIALS_ID = "docker-hub-credentials"

        IMAGE_TAG = "${BUILD_NUMBER}"

        LATEST_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "========================================="
                    echo "STAGE 1 : Récupération du code source"
                    echo "========================================="
                    echo "Repository : ${env.GIT_URL ?: 'Local repository'}"
                    echo "Branch : ${env.GIT_BRANCH ?: 'main/master'}"
                }

                checkout scm

                sh 'ls -la'
                sh 'echo "Code source récupéré avec succès"'
            }
        }

        stage('Unit Tests') {
            steps {
                script {
                    echo "========================================="
                    echo "STAGE 2 : Exécution des tests unitaires"
                    echo "========================================="
                }

                sh '''
                    echo "Installation des dépendances de test..."
                    pip3 install --break-system-packages -r requirements.txt

                    echo "Lancement des tests unitaires..."
                    python3 -m pytest test_app.py -v --cov=app --cov-report=term-missing

                    echo "Tests terminés avec succès ✓"
                '''
            }

            post {
                success {
                    echo "✓ Tous les tests sont passés avec succès"
                }
                failure {
                    echo "✗ ERREUR : Les tests ont échoué"
                    echo "Le pipeline s'arrête ici. Corrigez les erreurs avant de continuer."
                }
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    echo "========================================="
                    echo "STAGE 3 : Construction de l'image Docker"
                    echo "========================================="
                    echo "Image : ${DOCKER_IMAGE}"
                    echo "Tags : ${IMAGE_TAG}, ${LATEST_TAG}"
                }

                sh """
                    docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} \
                                 -t ${DOCKER_IMAGE}:${LATEST_TAG} \
                                 .
                """

                sh """
                    echo "Vérification de l'image créée..."
                    docker images | grep ${DOCKER_IMAGE}
                    echo "Image Docker construite avec succès ✓"
                """
            }

            post {
                success {
                    echo "✓ Image Docker créée : ${DOCKER_IMAGE}:${IMAGE_TAG}"
                }
                failure {
                    echo "✗ ERREUR : La construction de l'image Docker a échoué"
                }
            }
        }

        stage('Docker Push') {
            steps {
                script {
                    echo "========================================="
                    echo "STAGE 4 : Publication sur Docker Hub"
                    echo "========================================="
                    echo "Connexion à Docker Hub..."
                }

                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS_ID}",
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh """
                        # Connexion à Docker Hub
                        # Le mot de passe ne sera JAMAIS affiché dans les logs
                        echo "Connexion à Docker Hub en tant que \${DOCKER_USERNAME}..."
                        echo \${DOCKER_PASSWORD} | docker login -u \${DOCKER_USERNAME} --password-stdin

                        # Push de l'image avec le tag du numéro de build
                        echo "Publication de l'image ${DOCKER_IMAGE}:${IMAGE_TAG}..."
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}

                        # Push de l'image avec le tag latest
                        echo "Publication de l'image ${DOCKER_IMAGE}:${LATEST_TAG}..."
                        docker push ${DOCKER_IMAGE}:${LATEST_TAG}

                        echo "Images publiées avec succès sur Docker Hub ✓"
                    """
                }

                sh 'docker logout'
            }

            post {
                success {
                    echo "✓ Images publiées sur Docker Hub :"
                    echo "  - ${DOCKER_IMAGE}:${IMAGE_TAG}"
                    echo "  - ${DOCKER_IMAGE}:${LATEST_TAG}"
                }
                failure {
                    echo "✗ ERREUR : La publication sur Docker Hub a échoué"
                }
            }
        }
    }

    post {
        success {
            echo """
            ╔════════════════════════════════════════════════╗
            ║     PIPELINE TERMINÉ AVEC SUCCÈS ✓             ║
            ╚════════════════════════════════════════════════╝

            Build #${BUILD_NUMBER}
            Image : ${DOCKER_IMAGE}:${IMAGE_TAG}

            Vérifiez votre Docker Hub : https://hub.docker.com
            """
        }

        failure {
            echo """
            ╔════════════════════════════════════════════════╗
            ║       PIPELINE ÉCHOUÉ ✗                        ║
            ╚════════════════════════════════════════════════╝

            Build #${BUILD_NUMBER} a échoué
            Vérifiez les logs ci-dessus pour plus de détails
            """
        }

        always {
            echo "Nettoyage de l'espace de travail..."
            sh """
                docker images -q ${DOCKER_IMAGE} | xargs -r docker rmi -f || true
                echo "Nettoyage terminé"
            """
        }
    }
}
