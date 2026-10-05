---
name: epic-1-auth
description: 执行 Epic 1 —— 用户认证与账号体系。实现 JWT 双 Token 认证、自定义角色权限、账号初始化。依赖 Epic 0 已完成。
---

# Epic 1 — 用户认证与账号体系

## 前置条件
- Epic 0 已完成（解决方案可编译）
- 已读取 `shareflow-context/SKILL.md`

## 任务清单

### 后端

#### Domain 层

**`User` 实体** (`src/Domain/Entities/User.cs`)
```csharp
public class User : Entity<Guid>
{
    public string Email { get; private set; } = string.Empty;
    public string PasswordHash { get; private set; } = string.Empty;
    public string DisplayName { get; private set; } = string.Empty;
    public UserRole Role { get; private set; }
    public UserStatus Status { get; private set; }
    public Guid? BackendRoleId { get; private set; }  // 自定义后台角色

    public bool VerifyPassword(string password) => BCrypt.Net.BCrypt.Verify(password, PasswordHash);
    public void SetPassword(string password) { PasswordHash = BCrypt.Net.BCrypt.HashPassword(password); SetUpdatedAt(); }
    public void Activate() { Status = UserStatus.Active; SetUpdatedAt(); }
    public void Disable() { Status = UserStatus.Disabled; SetUpdatedAt(); }

    public static User Create(string email, string password, string displayName, UserRole role) =>
        new() { Id = Guid.NewGuid(), Email = email.ToLower(), DisplayName = displayName, Role = role,
                Status = UserStatus.Active, PasswordHash = BCrypt.Net.BCrypt.HashPassword(password) };
}
```

**枚举** (`src/Domain/Enums/UserRole.cs` / `UserStatus.cs`)
```csharp
public enum UserRole { SuperAdmin, BackendCustom, Sales, Client }
public enum UserStatus { Active, Disabled, PendingSetup }
```

**`BackendRole` 实体** (`src/Domain/Entities/BackendRole.cs`)
```csharp
public class BackendRole : Entity<Guid>
{
    public string Name { get; private set; } = string.Empty;
    public List<string> Permissions { get; private set; } = [];
}
```

**`RefreshToken` 实体** (`src/Domain/Entities/RefreshToken.cs`)
```csharp
public class RefreshToken : Entity<Guid>
{
    public Guid UserId { get; private set; }
    public string Token { get; private set; } = string.Empty;
    public DateTime ExpiresAt { get; private set; }
    public bool IsRevoked { get; private set; }
    public bool IsActive => !IsRevoked && ExpiresAt > DateTime.UtcNow;
    public void Revoke() { IsRevoked = true; SetUpdatedAt(); }
}
```

**Repository 接口** (`src/Domain/Interfaces/IUserRepository.cs`)
```csharp
public interface IUserRepository
{
    Task<User?> GetByIdAsync(Guid id);
    Task<User?> GetByEmailAsync(string email);
    Task<bool> ExistsByEmailAsync(string email);
    Task AddAsync(User user);
    Task<IReadOnlyList<string>> GetPermissionsAsync(Guid userId); // 查 BackendRole.Permissions
}

public interface IRefreshTokenRepository
{
    Task<RefreshToken?> GetByTokenAsync(string token);
    Task AddAsync(RefreshToken token);
    Task RevokeAllByUserIdAsync(Guid userId);
}

public interface IBackendRoleRepository
{
    Task<BackendRole?> GetByIdAsync(Guid id);
    Task<IReadOnlyList<BackendRole>> GetAllAsync();
    Task AddAsync(BackendRole role);
    Task UpdateAsync(BackendRole role);
    Task DeleteAsync(Guid id);
}
```

#### Infrastructure 层

- EF Core Configuration（Fluent API）
- Repository 实现（3个）
- `AppDbContext` 添加 DbSet

#### Application 层

**Mapster 映射** (`src/Application/Auth/MappingConfig.cs`)
```csharp
public class AuthMappingConfig : IRegister
{
    public void Register(TypeAdapterConfig config)
    {
        config.NewConfig<User, UserDto>()
            .Map(dest => dest.RoleName, src => src.Role.ToString());
    }
}
```

**DTO** (`src/Application/Auth/DTOs/`)
- `LoginRequest` { Email, Password }
- `TokenResponse` { AccessToken, RefreshToken, ExpiresAt, User: UserDto }
- `UserDto` { Id, Email, DisplayName, Role, Permissions[] }

**IJwtService** (`src/Application/Auth/Interfaces/IJwtService.cs`)
```csharp
public interface IJwtService
{
    string GenerateAccessToken(User user, IReadOnlyList<string> permissions);
    string GenerateRefreshToken();
    ClaimsPrincipal? ValidateToken(string token);
}
```

**IAuthService**
```csharp
public interface IAuthService
{
    Task<TokenResponse> LoginAsync(LoginRequest request);
    Task<TokenResponse> RefreshTokenAsync(string refreshToken);
    Task LogoutAsync(string refreshToken);
}
```

**`AuthService` 核心逻辑：**
1. 查用户 → 验密码 → 检查状态
2. 查 BackendRole.Permissions（Client/Sales 直接用 Role 判断）
3. 生成 JWT AccessToken（Claims: userId, role, permissions[]）
4. 生成 RefreshToken → 存 DB
5. Logout：Token 加入 Redis 黑名单（key: `token:blacklist:{jti}`，TTL = AccessToken 剩余时效）

**IAccountProvisioningService**
```csharp
public interface IAccountProvisioningService
{
    /// <summary>合同签约完成后自动创建客户账号</summary>
    Task<(string email, string initialPassword)> ProvisionClientAccountAsync(
        string clientName, string clientEmail, Guid contractId);
}
```

**PermissionAttribute + PermissionFilter** (`src/Api/Filters/`)
```csharp
[AttributeUsage(AttributeTargets.Method | AttributeTargets.Class)]
public class PermissionAttribute(string permission) : Attribute
{
    public string Permission { get; } = permission;
}

// ActionFilter: 从 JWT Claims 读取 permissions[]，校验 Permission 常量
```

**权限常量** (`src/Domain/Constants/Permissions.cs`)
```csharp
public static class Permissions
{
    public const string ProjectWrite = "project.write";
    public const string ProjectRead = "project.read";
    public const string RevenueWrite = "revenue.write";
    public const string RevenueVerify = "revenue.verify";
    public const string DividendWrite = "dividend.write";
    public const string DividendRead = "dividend.read";
    public const string ContractRead = "contract.read";
    public const string ContractRenew = "contract.renew";
    public const string WithdrawalApprove = "withdrawal.approve";
    public const string UserManage = "user.manage";
    public const string RoleManage = "role.manage";
    public const string ReportRead = "report.read";
}
```

#### API Controller

`POST /v1/auth/login` → `AuthController.LoginAsync()`
`POST /v1/auth/refresh` → `AuthController.RefreshAsync()`
`POST /v1/auth/logout` → `[Authorize] AuthController.LogoutAsync()`

角色管理（仅 SuperAdmin）：
`GET/POST /v1/admin/roles`
`PUT /v1/admin/roles/{id}/permissions`
`DELETE /v1/admin/roles/{id}`
`POST /v1/admin/users/{id}/role`

### 前端

#### `stores/auth.ts`
```typescript
export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null)
  const user = ref<UserInfo | null>(null)
  const permissions = ref<string[]>([])

  function hasPermission(key: string): boolean {
    if (user.value?.role === 'SuperAdmin') return true
    return permissions.value.includes(key)
  }

  async function login(email: string, password: string) { ... }
  async function refreshToken() { ... }
  function logout() { ... }

  return { accessToken, user, permissions, hasPermission, login, refreshToken, logout }
}, { persist: true })
```

#### 路由守卫 `router/guards.ts`
- 未登录 → `/auth/login`
- 已登录按 Role 跳转：SuperAdmin/BackendCustom → `/admin`，Sales → `/sales`，Client → `/client`

## 完成标准
- [ ] `POST /v1/auth/login` 返回 Token 对
- [ ] `[Permission("report.read")]` 无权限时返回 403
- [ ] SuperAdmin 绕过所有权限校验
- [ ] 前端登录后按角色自动跳转
- [ ] RefreshToken 流程正常（旧 Token 失效后自动续期）
