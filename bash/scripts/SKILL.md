---
name: Scripts patterns
description: Conventions for using sh, bash, bat, python scripts
---

## 1. sdk installation scripts should be updated to use the latest sdk version using sdk-man

In the past, the `sdk{version}.sh` scripts were often used to install and use appropriate SDK versions for the projects.
Without updates, some of these scripts may not work as expected or may not install the latest SDK versions.
These scripts are usually found at the root of the project

To update, please follow these guidelines

1. If multiples are found for different versions of the same sdk, plese keep the latest version and remove the others
2. If they are Java SDK installation scripts please follow guidelines in 1.1

### 1.1 SDK-MAN for Java SDK updates

1. Please create a sdk.sh file to install the latest LTS java version. 
2. Please check if the version needed is CRAC or GraalVM. An update means using the same type.
3. Choose the latest version by choosing in this order
   * OpenSDK
   * AdaptSDK
   * LibreSDK
   * Oracle
4. Once the sdk.sh file is created, please remove all other sdk{version}.sh files
