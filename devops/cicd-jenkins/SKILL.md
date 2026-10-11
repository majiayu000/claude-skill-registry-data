---
name: cicd-jenkins
description: Jenkins — declarative Jenkinsfile for build, test, and deploy.
---

# Jenkins Pipelines

## Declarative Jenkinsfile (preferred)

```groovy
// Jenkinsfile
pipeline {
    agent {
        docker {
            image 'node:20-alpine'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        REGISTRY = credentials('docker-registry-url')
        DEPLOY_KEY = credentials('deploy-ssh-key')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Install') {
            steps {
                sh 'npm ci'
            }
        }

        stage('Lint') {
            steps {
                sh 'npm run lint'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test'
            }
            post {
                always {
                    junit 'test-results/*.xml'
                }
            }
        }

        stage('Build Image') {
            when {
                branch 'main'
            }
            steps {
                sh "docker build -t ${REGISTRY}/myapp:${GIT_COMMIT} ."
                sh "docker push ${REGISTRY}/myapp:${GIT_COMMIT}"
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            input {
                message 'Deploy to production?'
                ok 'Deploy'
            }
            steps {
                sshagent(['deploy-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no deploy@${DEPLOY_HOST} '
                            cd /opt/myapp &&
                            IMAGE_TAG=${GIT_COMMIT} docker compose pull app &&
                            IMAGE_TAG=${GIT_COMMIT} docker compose up -d &&
                            docker image prune -f
                        '
                    """
                }
            }
        }
    }

    post {
        failure {
            mail to: 'team@example.com',
                 subject: "Pipeline failed: ${env.JOB_NAME}",
                 body: "Build ${env.BUILD_URL} failed."
        }
    }
}
```

## Credentials Management

- Store all secrets in **Jenkins Credentials** (not Jenkinsfile)
- Use `credentials()` binding or `withCredentials` block
- Types: Username/Password, SSH Key, Secret Text, Secret File
- Never echo credentials — use `set +x` if you must debug

```groovy
withCredentials([usernamePassword(
    credentialsId: 'docker-registry',
    usernameVariable: 'DOCKER_USER',
    passwordVariable: 'DOCKER_PASS'
)]) {
    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
}
```

## Shared Libraries

For reusable pipeline logic across repositories:

```groovy
// Jenkinsfile
@Library('my-shared-library') _

deployApp(environment: 'production', image: 'myapp')
```

## Best Practices

- Use **declarative** syntax over scripted — more readable and constrained
- Use `agent { docker {} }` to run in containers — no environment pollution
- `disableConcurrentBuilds()` prevents race conditions on shared resources
- `buildDiscarder` prevents disk exhaustion from keeping old builds
- Use `input` for manual approval gates before production deploys
- Add `timeout` to prevent stuck builds from blocking the executor
- Use `post { always {} }` for test report publishing — runs even on failure
- Configure Blue Ocean plugin for better UI visualization
