---
name: local-deployment
description: skill that dictates the deployment strategy for local development
---

# When To Use
1. When tasked to deploy and test an application locally
2. Use this skill AFTER you have written your code and executed your tests successfully

# Deployment Strategy

## Step 1- Local Execution
1. Run the app locally via terminal. If there are multiple services like frontend and backend, launch them both via separate terminals. 
2. Validate the deployment by following the **Deployment Validation** instructions

## Step 2- Docker Execution
1. Build the docker images for each service
2. Generate a docker-compose yaml script to spin up all the services together
3. Execute docker-compose
4. Validate the deployment by following the **Deployment Validation** instructions 

## Step 3- Local Kubernetes cluster (using minikube)
1. Confirm with the user if they require this deployment
2. Push the docker images to docker hub. Confirm the docker hub username with the user 
3. minikube should pull these docker images, deploy and run 2 pods. 
4. Validate the deployment by following the **Deployment Validation** instructions 

## Step 4
1. Generate a docs/local-deployment-guide.md and write all the steps required for user to execute the app through steps 1, 2 and 3
2. Include a deployment diagram
3. Include steps to validate the app is running and a test request

# Deployment Validation
Test that the services have launched successfully, i.e. you are able to ping them, and that the services are able to communicate among each other as expected by the application 