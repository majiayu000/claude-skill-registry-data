---
name: implmentation
description: when implementing a subproject or a project use this skill
---

# How to implement
 - all projects should be in Java 21 and Springboot 3.5.9
 - always use a standard file structure, to keep things clear and organized
 - always use maven
 - if there is a standard spring approach to solve a problem, use that
 - be spring idiomatic
 - where possible use spring annotations, e.g. @Cacheable
 - where relevant use JPA
 - prefer text blocks over escaping in strings
 - ALWAYS use clean code. Prefer SOLID and DRY and YAGNI
 - use Unit Tests to ensure all logic is OK
 - use integration tests to show that all works
 - in the README.md file, ensure that there are instructions of how to test the system using curl commands
 - if there is a need to pass some value from a previous step, ensure that the user can do copy & paste to get the result they need
 - where relevant make a docker compose file to start all needed (assume docker is working on the computer)
 - have run.sh and test.sh files to run and test the code in each subproject as needed


 # examples
 folder structure (partial)
 roject-root
├─ pom.xml (or build.gradle)
├─ README.md
├─ src
│ ├─ main
│ │ ├─ java
│ │ │ └─ com
│ │ │ └─ example
│ │ │ └─ app
│ │ │ ├─ Application.java
│ │ │ ├─ config
│ │ │ │ ├─ WebConfig.java
│ │ │ │ └─ SecurityConfig.java
│ │ │ ├─ controller <-- HTTP endpoints / MVC / REST
│ │ │ │ ├─ PublicController.java
│ │ │ │ └─ AdminController.java
│ roject-root
├─ pom.xml 
├─ README.md
├─ src
│ ├─ main
│ │ ├─ java
│ │ │ └─ com
│ │ │ └─ example
│ │ │ └─ app
│ │ │ ├─ Application.java
│ │ │ ├─ config
│ │ │ │ ├─ WebConfig.java
│ │ │ │ └─ SecurityConfig.java
│ │ │ ├─ controller <-- HTTP endpoints / MVC / REST
│ │ │ │ ├─ PublicController.java
│ │ │ │ └─ AdminController.java
│ 