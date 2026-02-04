---
name: simple-deployment-on-vm
description: How to do simple but secure deployments using virtual machines on different cloud providers
license: MIT
tags:
  - aws
  - deploy
  - security
  - dns
  - ec2
  - tls configuration
metadata:
  author: Stakpak <team@stakpak.dev>
  version: "1.0.2"
---

# Deploying  applications with a simple but secure setup

## Core Principles:

* avoid assumptions
* use only CLI tools
* avoid deleting any existing cloud resource, to not disrupt operations



## Guidelines:

* use wait commands whenever possible instead of polling
* make sure to create and store SSH keys to access deployment machines/instances instead of passwords
* do not delete the SSH Keys you create otherwise you'd be locked out
* always try using CLI tools with default env vars before asking for credentials



## Deployment Requirements:

### 1) Infrastructure

* prefer Virtual Machines over PaaS solutions
* ensure VMs are in public subnets with public IPs
* enable SSH access to VMs
* make sure to provision compute instances with the appropriate CPU and Memory requirements, otherwise you might not be able to run the app successfully

### 2) Networking:

* configure domain names (if requested)

  * add any DNS records needed yoruself when possible
* if TLS is required

  * use let's encrypt unless the user prefers other services
  * DNS must be configured properly for let's encrypt to work
  * use both ports 80 (HTTP), and 443 (HTTPS) to be able to pass let's encrypt http challenge
* if using AWS

  * remember to enable DNS hostnames and resolution (these must be enabled in a separate command after creating the VPC)
* if using Cloudflare

  * prefer using cloudflare in proxy mode to protect sites

### 3) Database (optional)

* deploy appropriate database type and version when required
* prefer managed database services in the cloud provider of choice
* configure proper database credentials and connectivity

  * make sure to set the correct application environment variables so the app can connect successfully to the database
  * you must copy over the database password so it's accessible by the deployed application
* credentials

  * you MUST generate a random secure password (e.g. use openssl cli)
  * store passwords in files, never print passwords in plain text
  * the password should be at least 15 characters long
  * some databases have restrictions on the character set allowed, so only use alphaneumeric characters

### 4) Quality Assurance

* monitor resource readiness before proceeding with downstream dependencies
* test application functionality

  * you MUST check application logs to make sure there are no errors
  * you MUST make a web request as a health check and get status code 200
* make sure your deployments are secure and production-ready



## Mandatory User Confirmation

* domain name configuration preferences
* TLS/HTTPS requirements
* database requirements and preferences



## Success Criteria

* \#1 Application is deployed and functional
* \#2 All required services are properly configured
* \#3 Deployment is production-ready
* \#4 All credentials and access points are documented