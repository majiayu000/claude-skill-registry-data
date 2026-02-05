---
name: java-best-practices
description: Java 编码最佳实践与设计模式
version: 1.0.0
category: development
triggers:
  - java best practice
  - Java 最佳实践
  - 设计模式
  - Java 编码规范
scriptPath: check-java-env.sh
scriptType: bash
autoExecute: true
scriptTimeout: 5
---

# Java 最佳实践技能包

## 编码规范

### 命名规范
- **类名**：PascalCase（UserService）
- **方法/变量**：camelCase（getUserById）
- **常量**：UPPER_SNAKE_CASE（MAX_SIZE）
- **包名**：小写（com.example.service）

### 常用设计模式

**单例模式（枚举实现）**：
```java
public enum Singleton {
    INSTANCE;
    public void doSomething() {}
}
```

**工厂模式**：
```java
public class UserFactory {
    public static User createUser(String type) {
        return switch (type) {
            case "admin" -> new AdminUser();
            case "guest" -> new GuestUser();
            default -> new RegularUser();
        };
    }
}
```

**Builder 模式**：
```java
User user = User.builder()
    .name("张三")
    .age(25)
    .build();
```

## Stream API

```java
List<String> names = users.stream()
    .filter(u -> u.getAge() > 18)
    .map(User::getName)
    .collect(Collectors.toList());
```

## 异常处理

```java
try {
    // 业务逻辑
} catch (SpecificException e) {
    log.error("Error: {}", e.getMessage(), e);
    throw new BusinessException("操作失败");
} finally {
    // 清理资源
}
```

## 并发编程

```java
ExecutorService executor = Executors.newFixedThreadPool(10);
executor.submit(() -> {
    // 异步任务
});
```

## Optional 使用

```java
Optional<User> user = userRepository.findById(id);
return user.orElseThrow(() -> new NotFoundException());
```
