---
name: docker-setup
description: Docker 容器化配置指南
version: 1.0.0
category: devops
triggers:
  - docker
  - 容器化
  - dockerfile
  - docker compose
scriptPath: docker-check.sh
scriptType: bash
autoExecute: true
scriptTimeout: 10
---

# Docker 容器化技能包

## Dockerfile 最佳实践

### Java Spring Boot 应用

```dockerfile
# 多阶段构建
FROM maven:3.8-openjdk-17 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

FROM openjdk:17-jdk-slim
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
    depends_on:
      - mysql
  
  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=password
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## 常用命令

```bash
# 构建镜像
docker build -t myapp:latest .

# 运行容器
docker run -d -p 8080:8080 myapp:latest

# 查看日志
docker logs -f container_id

# 进入容器
docker exec -it container_id /bin/bash
```
