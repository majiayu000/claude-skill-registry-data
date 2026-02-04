---
name: error-handler
description: |
  基于若依-vue-plus框架的后端全局异常处理规范。定义业务异常抛出、全局异常捕获、标准错误响应返回的完整规范体系。
  确保系统错误统一处理，避免直接暴露堆栈信息，保障事务一致性和前后端交互的标准化。
  
  触发场景：
  - 编写Service层业务逻辑需要抛出异常时
  - 配置或修改GlobalExceptionHandler全局异常处理器时
  - 处理Controller层错误响应时
  - 实现事务回滚机制时
  - 定义自定义异常类时
  
  触发词：异常处理、全局异常、ServiceException、错误码、捕获异常、事务回滚、统一响应、业务异常
---

# 异常处理规范

## 核心规范

### 规范1：业务异常使用ServiceException抛出
**详细说明：**
在Service层处理业务逻辑时，遇到以下情况必须抛出`ServiceException`：
- 参数校验失败（如格式错误、必填项缺失）
- 业务规则违反（如状态冲突、权限不足）
- 数据唯一性校验失败（如用户名已存在）
- 业务流程中断（如库存不足、账户余额不足）

**关键要点：**
- ✅ 必须抛出`ServiceException`，切勿直接返回封装对象R或仅打印日志
- ✅ 配合`@Transactional`注解可自动触发事务回滚
- ✅ 异常信息应清晰明确，便于前端展示给用户
- ✅ 可指定错误码：`throw new ServiceException("错误信息", 错误码)`

```java
@Service
public class SysUserServiceImpl implements ISysUserService {

    @Autowired
    private SysUserMapper userMapper;

    /**
     * 校验用户名唯一性
     * 示例：数据唯一性校验场景
     */
    @Override
    public void checkUserNameUnique(String userName) {
        int count = userMapper.checkUserNameUnique(userName);
        if (count > 0) {
            // 抛出业务异常，前端接收到统一格式的错误提示
            throw new ServiceException("新增用户'" + userName + "'失败，登录账号已存在");
        }
    }
    
    /**
     * 新增用户
     * 示例：带事务的业务操作，异常自动回滚
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public int insertUser(SysUser user) {
        // 业务校验失败抛出异常，事务自动回滚
        if (StringUtils.isNotEmpty(user.getPhonenumber()) 
            && !UserConstants.isPhone(user.getPhonenumber())) {
            throw new ServiceException("手机号格式不正确");
        }
        
        // 检查用户名唯一性
        checkUserNameUnique(user.getUserName());
        
        // 执行插入操作
        int rows = userMapper.insertUser(user);
        if (rows == 0) {
            throw new ServiceException("新增用户失败");
        }
        return rows;
    }
    
    /**
     * 带错误码的异常抛出
     * 示例：指定特定错误码场景
     */
    @Override
    public void updateUserStatus(Long userId, String status) {
        SysUser user = userMapper.selectUserById(userId);
        if (Objects.isNull(user)) {
            // 指定错误码 404
            throw new ServiceException("用户不存在", HttpStatus.NOT_FOUND);
        }
        if ("1".equals(user.getDelFlag())) {
            throw new ServiceException("用户已删除，无法修改状态", HttpStatus.BAD_REQUEST);
        }
        userMapper.updateUserStatus(userId, status);
    }
}
```

### 规范2：全局异常处理器统一捕获
**详细说明：**
使用`@RestControllerAdvice`注解定义全局异常处理类，集中处理所有异常情况：
- 捕获`ServiceException`业务异常
- 捕获`MethodArgumentNotValidException`参数校验异常
- 捕获`RuntimeException`运行时异常
- 捕获数据库异常、权限异常等系统异常

**关键要点：**
- ✅ 必须记录完整的错误日志（包括请求URI、异常信息、堆栈跟踪）
- ✅ 必须返回标准格式`R`对象，确保前端获得一致的错误响应结构
- ✅ 敏感信息（如SQL错误、系统路径）不得暴露给前端
- ✅ 区分不同异常类型，返回合适的HTTP状态码和业务错误码

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    /**
     * 业务异常
     * 处理Service层主动抛出的业务异常
     */
    @ExceptionHandler(ServiceException.class)
    public R<Void> handleServiceException(ServiceException e, HttpServletRequest request) {
        log.error("业务异常 => 请求地址: {}, 异常信息: {}", request.getRequestURI(), e.getMessage());
        Integer code = e.getCode();
        return StringUtils.isNotNull(code) ? R.fail(code, e.getMessage()) : R.fail(e.getMessage());
    }

    /**
     * 请求参数校验异常
     * 处理@Valid或@Validated注解校验失败的情况
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public R<Void> handleMethodArgumentNotValidException(MethodArgumentNotValidException e) {
        log.error("参数校验异常", e);
        String message = e.getBindingResult().getFieldError().getDefaultMessage();
        return R.fail(message);
    }
    
    /**
     * 请求方式不支持异常
     * 如：前端用POST请求了GET接口
     */
    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    public R<Void> handleHttpRequestMethodNotSupported(HttpRequestMethodNotSupportedException e,
                                                        HttpServletRequest request) {
        log.error("请求方式不支持 => 请求地址: {}, 请求方式: {}", 
                  request.getRequestURI(), e.getMethod());
        return R.fail("不支持'" + e.getMethod() + "'请求方式");
    }
    
    /**
     * 数据库异常
     * 捕获SQL异常，避免暴露数据库信息
     */
    @ExceptionHandler(SQLException.class)
    public R<Void> handleSQLException(SQLException e, HttpServletRequest request) {
        log.error("数据库异常 => 请求地址: {}, SQL状态码: {}, 错误信息: {}", 
                  request.getRequestURI(), e.getSQLState(), e.getMessage(), e);
        return R.fail("数据库操作异常，请联系管理员");
    }
    
    /**
     * 空指针异常
     * 通常是代码bug，需要开发人员修复
     */
    @ExceptionHandler(NullPointerException.class)
    public R<Void> handleNullPointerException(NullPointerException e, HttpServletRequest request) {
        log.error("空指针异常 => 请求地址: {}", request.getRequestURI(), e);
        return R.fail("系统异常，请联系管理员");
    }
    
    /**
     * 运行时异常
     * 兜底处理，捕获所有未被明确处理的RuntimeException
     */
    @ExceptionHandler(RuntimeException.class)
    public R<Void> handleRuntimeException(RuntimeException e, HttpServletRequest request) {
        log.error("运行时异常 => 请求地址: {}", request.getRequestURI(), e);
        return R.fail("系统运行异常，请稍后重试");
    }
    
    /**
     * 系统异常
     * 最终兜底，捕获所有异常
     */
    @ExceptionHandler(Exception.class)
    public R<Void> handleException(Exception e, HttpServletRequest request) {
        log.error("系统异常 => 请求地址: {}", request.getRequestURI(), e);
        return R.fail("系统异常，请联系管理员");
    }
}
```

### 规范3：自定义异常类设计
**详细说明：**
除了框架提供的`ServiceException`，根据业务需要可自定义特定异常类：
- 继承`RuntimeException`以支持事务回滚
- 包含错误码、错误信息、详细描述等属性
- 命名应清晰表达异常类型（如`UserNotFoundException`、`InsufficientBalanceException`）

**示例代码：**

```java
/**
 * 自定义业务异常基类
 */
public class BaseException extends RuntimeException {
    
    private static final long serialVersionUID = 1L;
    
    /** 错误码 */
    private Integer code;
    
    /** 错误详细信息（不展示给前端） */
    private String detailMessage;
    
    public BaseException(String message) {
        super(message);
    }
    
    public BaseException(String message, Integer code) {
        super(message);
        this.code = code;
    }
    
    public BaseException(String message, Integer code, String detailMessage) {
        super(message);
        this.code = code;
        this.detailMessage = detailMessage;
    }
    
    public Integer getCode() {
        return code;
    }
    
    public String getDetailMessage() {
        return detailMessage;
    }
}

/**
 * 具体业务异常示例
 */
public class UserNotFoundException extends BaseException {
    public UserNotFoundException(Long userId) {
        super("用户不存在", HttpStatus.NOT_FOUND, "userId: " + userId);
    }
}
```

### 规范4：Controller层异常处理
**详细说明：**
Controller层应专注于请求参数接收和响应返回，不应处理业务异常：
- ✅ 允许：使用`@Valid`或`@Validated`进行参数校验
- ✅ 允许：直接调用Service方法，让异常向上抛出
- ❌ 禁止：使用try-catch捕获Service层抛出的异常
- ❌ 禁止：在Controller中编写业务逻辑

**正确示例：**

```java
@RestController
@RequestMapping("/system/user")
public class SysUserController {
    
    @Autowired
    private ISysUserService userService;
    
    /**
     * 新增用户
     * 正确：直接调用Service，不捕获异常
     */
    @PostMapping
    public R<Void> add(@Validated @RequestBody SysUser user) {
        // Service层抛出的异常会被全局异常处理器捕获
        userService.insertUser(user);
        return R.ok();
    }
    
    /**
     * 修改用户
     * 正确：参数校验由框架自动处理
     */
    @PutMapping
    public R<Void> edit(@Validated @RequestBody SysUser user) {
        userService.updateUser(user);
        return R.ok();
    }
}
```

**错误示例（禁止）：**

```java
@RestController
@RequestMapping("/system/user")
public class SysUserController {
    
    /**
     * 错误示例：Controller层不应捕获业务异常
     */
    @PostMapping
    public R<Void> add(@RequestBody SysUser user) {
        try {
            userService.insertUser(user);
            return R.ok();
        } catch (ServiceException e) {
            // ❌ 禁止：不应在Controller中捕获异常
            log.error("新增用户失败", e);
            return R.fail(e.getMessage());
        }
    }
}
```

## 禁止事项

### 异常抛出禁止项
- ❌ **禁止在Service层直接返回R对象处理异常**
  - 错误：`return R.fail("用户名已存在");`
  - 正确：`throw new ServiceException("用户名已存在");`

- ❌ **禁止吞没异常**
  - 错误：捕获异常后只打印日志，不重新抛出或处理
  ```java
  try {
      // 业务操作
  } catch (Exception e) {
      log.error("操作失败", e);  // 只记录日志，不处理
      // 异常被吞没，事务无法回滚
  }
  ```

- ❌ **禁止在Controller层使用try-catch捕获业务异常**
  - 错误：在Controller中捕获ServiceException并返回R对象
  - 正确：让异常向上抛出，由全局异常处理器统一处理

- ❌ **禁止捕获Exception或Throwable后不抛出**
  - 错误：`catch (Exception e) { log.error("error", e); }`
  - 正确：`catch (Exception e) { log.error("error", e); throw e; }`

### 异常处理禁止项
- ❌ **禁止将数据库异常信息直接返回给前端**
  - 错误：返回"Duplicate entry 'admin' for key 'user.username'"
  - 正确：返回"用户名已存在"

- ❌ **禁止暴露系统内部信息**
  - 错误：返回堆栈跟踪、文件路径、SQL语句
  - 正确：返回用户友好的提示信息

- ❌ **禁止使用e.printStackTrace()**
  - 错误：`e.printStackTrace();`
  - 正确：`log.error("错误信息", e);`

### 事务处理禁止项
- ❌ **禁止在@Transactional方法中捕获异常不抛出**
  - 捕获异常后不重新抛出会导致事务无法回滚
  ```java
  @Transactional
  public void updateUser(SysUser user) {
      try {
          userMapper.updateUser(user);
          roleMapper.updateUserRole(user.getId());
      } catch (Exception e) {
          log.error("更新失败", e);
          // ❌ 异常被吞没，事务不会回滚
      }
  }
  ```

- ❌ **禁止抛出受检异常（Checked Exception）不配置回滚**
  - 受检异常默认不触发事务回滚
  - 必须使用`@Transactional(rollbackFor = Exception.class)`
  - 推荐直接使用RuntimeException或其子类

### 日志记录禁止项
- ❌ **禁止记录日志时不记录异常堆栈**
  - 错误：`log.error("操作失败: " + e.getMessage());`
  - 正确：`log.error("操作失败", e);`

- ❌ **禁止在循环中记录相同的异常信息**
  - 会导致日志爆炸
  ```java
  for (User user : users) {
      try {
          processUser(user);
      } catch (Exception e) {
          log.error("处理用户失败", e);  // ❌ 循环中重复记录
      }
  }
  ```

### 响应格式禁止项
- ❌ **禁止返回非标准R对象格式**
  - 错误：`return "error message";`
  - 错误：`return Map.of("error", "message");`
  - 正确：`return R.fail("error message");`

- ❌ **禁止在异常处理中返回null**
  - 全局异常处理器必须返回有效的R对象

## 参考代码
### 核心文件路径
- **ServiceException类**：`ruoyi-common/src/main/java/com/ruoyi/common/exception/ServiceException.java`
- **全局异常处理器**：`ruoyi-framework/src/main/java/com/ruoyi/framework/web/exception/GlobalExceptionHandler.java`
- **统一响应对象R**：`ruoyi-common/src/main/java/com/ruoyi/common/core/domain/R.java`
- **HTTP状态码常量**：`ruoyi-common/src/main/java/com/ruoyi/common/constant/HttpStatus.java`

### 相关依赖
```xml
<!-- Spring Web (包含@RestControllerAdvice等注解) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<!-- Spring Validation (参数校验) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

## 检查清单

### 基础配置检查
- [ ] 是否已配置全局异常处理器（@RestControllerAdvice）
- [ ] 是否已定义ServiceException或自定义异常类
- [ ] 是否已配置统一响应对象R
- [ ] 是否已引入必要的依赖（spring-boot-starter-web、validation）

### 异常抛出规范检查
- [ ] Service层是否使用ServiceException抛出业务异常
- [ ] 是否避免在Service层直接返回R对象处理异常
- [ ] 异常信息是否清晰明确，便于用户理解
- [ ] 是否正确使用错误码（可选）
- [ ] 关键业务方法是否添加@Transactional注解

### 异常处理规范检查
- [ ] 全局异常处理器是否捕获了主要异常类型（ServiceException、RuntimeException、Exception等）
- [ ] 是否所有异常返回均为统一的R对象格式
- [ ] 是否在异常处理中记录了完整的Error Log（包含堆栈信息）
- [ ] 是否避免暴露敏感信息（SQL、路径、堆栈）给前端
- [ ] 是否针对不同异常类型返回合适的提示信息

### 事务回滚检查
- [ ] 是否确保异常发生时的事务回滚机制
- [ ] @Transactional方法中是否避免捕获异常不抛出
- [ ] 是否正确配置rollbackFor属性（建议rollbackFor = Exception.class）
- [ ] 是否避免使用受检异常（Checked Exception）

### Controller层检查
- [ ] Controller是否避免使用try-catch捕获业务异常
- [ ] 是否使用@Valid或@Validated进行参数校验
- [ ] 是否直接调用Service方法，让异常向上抛出
- [ ] 是否避免在Controller中编写业务逻辑

### 日志记录检查
- [ ] 是否使用log.error记录异常而非e.printStackTrace()
- [ ] 记录日志时是否包含异常堆栈信息（传入Exception对象）
- [ ] 日志信息是否包含请求URI、关键参数等上下文信息
- [ ] 是否避免在循环中重复记录相同异常

### 代码质量检查
- [ ] 是否避免吞没异常（捕获后不处理也不抛出）
- [ ] 是否避免捕获Exception或Throwable后不抛出
- [ ] 异常处理逻辑是否简洁清晰，易于维护
- [ ] 是否编写了单元测试验证异常处理逻辑

## 常见问题FAQ

### Q1: ServiceException和RuntimeException有什么区别？
**A:** `ServiceException`是若依框架中继承自`RuntimeException`的自定义业务异常类，相比直接使用RuntimeException：
- 支持自定义错误码
- 语义更明确，表示业务逻辑异常
- 便于全局异常处理器识别和处理
- 建议业务层统一使用ServiceException

### Q2: 什么时候需要在Controller层捕获异常？
**A:** 几乎不需要。以下场景可以例外：
- 需要在异常发生后执行特殊清理操作（如释放资源）
- 需要将异常转换为其他类型后重新抛出
- 需要记录额外的业务上下文信息后重新抛出
- **关键**：即使捕获也必须重新抛出，不能吞没异常

### Q3: 如何处理异步方法中的异常？
**A:** 异步方法（@Async）中的异常不会被全局异常处理器捕获，需要：
```java
@Async
public CompletableFuture<Void> asyncTask() {
    return CompletableFuture.runAsync(() -> {
        try {
            // 业务逻辑
        } catch (Exception e) {
            log.error("异步任务执行失败", e);
            // 可以发送消息通知、记录数据库等
        }
    });
}
```

### Q4: 如何区分哪些异常需要回滚事务？
**A:** Spring事务默认行为：
- **会回滚**：RuntimeException及其子类（包括ServiceException）
- **不会回滚**：受检异常（Checked Exception，如IOException）
- **建议配置**：`@Transactional(rollbackFor = Exception.class)` 对所有异常都回滚

### Q5: 全局异常处理器的执行顺序是什么？
**A:** 按照异常的继承关系，从子类到父类：
1. 先匹配具体异常（如ServiceException）
2. 再匹配父类异常（如RuntimeException）
3. 最后匹配Exception
4. **建议**：将Exception的处理方法放在最后作为兜底

### Q6: 如何在异常信息中避免SQL注入风险？
**A:** 构造异常信息时要注意：
```java
// ❌ 错误：直接拼接用户输入
throw new ServiceException("查询失败: " + userInput);

// ✅ 正确：使用占位符或参数化
throw new ServiceException("查询失败，请检查输入参数");
log.error("查询失败，用户输入: {}", userInput);
```

### Q7: 如何处理第三方API调用异常？
**A:** 建议封装为业务异常：
```java
@Service
public class ThirdPartyService {
    
    public String callExternalApi(String param) {
        try {
            return restTemplate.getForObject(url, String.class);
        } catch (HttpClientErrorException e) {
            log.error("调用第三方API失败: {}", e.getMessage(), e);
            throw new ServiceException("外部服务暂时不可用，请稍后重试");
        } catch (Exception e) {
            log.error("调用第三方API异常", e);
            throw new ServiceException("系统异常，请联系管理员");
        }
    }
}
```

## 最佳实践建议

### 1. 异常信息编写原则
- **用户友好**：使用通俗易懂的语言，避免技术术语
- **明确具体**：指出问题所在，而非模糊的"操作失败"
- **可操作**：告诉用户如何解决问题
```java
// ❌ 不好：操作失败
throw new ServiceException("操作失败");

// ✅ 良好：用户名已存在，请使用其他用户名
throw new ServiceException("用户名'" + userName + "'已存在，请使用其他用户名");
```

### 2. 错误码设计规范
建议采用分层错误码体系：
```java
public class ErrorCode {
    // 系统级错误 (1xxx)
    public static final int SYSTEM_ERROR = 1000;
    public static final int DB_ERROR = 1001;
    
    // 业务级错误 (2xxx)
    public static final int USER_NOT_FOUND = 2001;
    public static final int USER_ALREADY_EXISTS = 2002;
    public static final int INSUFFICIENT_BALANCE = 2003;
    
    // 参数错误 (3xxx)
    public static final int PARAM_INVALID = 3000;
    public static final int PARAM_MISSING = 3001;
}
```

### 3. 分层异常处理策略
```
┌─────────────────────────────────────┐
│ Controller层                         │
│ - 只负责接收请求和返回响应            │
│ - 不捕获异常（让异常向上传播）         │
└──────────────┬──────────────────────┘
               │ 异常向上抛出
┌──────────────▼──────────────────────┐
│ Service层                            │
│ - 处理业务逻辑                        │
│ - 抛出ServiceException业务异常        │
│ - 配合@Transactional进行事务管理      │
└──────────────┬──────────────────────┘
               │ 异常继续向上抛出
┌──────────────▼──────────────────────┐
│ GlobalExceptionHandler               │
│ - 统一捕获所有异常                    │
│ - 记录日志                           │
│ - 返回标准R对象                       │
└─────────────────────────────────────┘
```

### 4. 事务边界最佳实践
```java
@Service
public class OrderService {
    
    /**
     * 正确：事务边界清晰，异常自动回滚
     */
    @Transactional(rollbackFor = Exception.class)
    public void createOrder(Order order) {
        // 1. 校验库存
        if (!checkStock(order.getProductId(), order.getQuantity())) {
            throw new ServiceException("库存不足");
        }
        
        // 2. 创建订单
        orderMapper.insert(order);
        
        // 3. 扣减库存
        productMapper.decreaseStock(order.getProductId(), order.getQuantity());
        
        // 4. 扣减余额
        accountMapper.decreaseBalance(order.getUserId(), order.getAmount());
        
        // 任何步骤抛出异常，所有操作都会回滚
    }
}
```

### 5. 日志记录最佳实践
```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);
    
    @ExceptionHandler(ServiceException.class)
    public R<Void> handleServiceException(ServiceException e, HttpServletRequest request) {
        // 记录关键信息：请求URI、请求方法、用户信息、异常信息
        log.error("业务异常 => URI: {}, Method: {}, User: {}, Message: {}", 
                  request.getRequestURI(),
                  request.getMethod(),
                  SecurityUtils.getUsername(),
                  e.getMessage());
        return R.fail(e.getCode(), e.getMessage());
    }
    
    @ExceptionHandler(Exception.class)
    public R<Void> handleException(Exception e, HttpServletRequest request) {
        // 未知异常记录完整堆栈信息
        log.error("系统异常 => URI: {}, Method: {}, User: {}", 
                  request.getRequestURI(),
                  request.getMethod(),
                  SecurityUtils.getUsername(), 
                  e);  // 传入Exception对象，自动记录堆栈
        return R.fail("系统异常，请联系管理员");
    }
}
```

## 总结
遵循本规范可以确保：
1. ✅ **异常处理统一规范**：所有异常都通过全局处理器统一处理
2. ✅ **事务一致性保障**：业务异常自动触发事务回滚
3. ✅ **前端体验友好**：返回标准格式的错误信息，便于前端处理
4. ✅ **系统安全可靠**：避免敏感信息泄露，保障系统安全
5. ✅ **问题快速定位**：完整的日志记录，便于问题追踪和排查