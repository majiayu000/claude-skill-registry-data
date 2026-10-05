---
name: epic-11-notifications
description: 执行 Epic 11 —— 站内消息通知（分红到账、提现状态、合同签约完成，站内 + 可选外部渠道）。依赖 Epic 5/6 已完成。
---

# Epic 11 — 消息通知

## 前置条件
- Epic 5/6 (分红/钱包事件) + Epic 3 (合同签约事件) 已完成
- 已读取 `shareflow-context/SKILL.md`

## 任务清单

### 后端

#### Domain 层

**`Notification` 实体** (`src/Domain/Entities/Notification.cs`)
```csharp
public class Notification : Entity<long>
{
    public Guid UserId { get; private set; }
    public NotificationType Type { get; private set; }
    public string Title { get; private set; } = string.Empty;
    public string Body { get; private set; } = string.Empty;
    public bool IsRead { get; private set; }
    public DateTime? ReadAt { get; private set; }
    public string? ActionUrl { get; private set; }  // 前端跳转路径

    public void MarkRead() { IsRead = true; ReadAt = DateTime.UtcNow; }

    public static Notification Create(Guid userId, NotificationType type,
        string title, string body, string? actionUrl = null) =>
        new() { Id = 0, UserId = userId, Type = type, Title = title,
                Body = body, IsRead = false, ActionUrl = actionUrl };
}

public enum NotificationType
{
    DividendReceived,       // 分红到账
    WithdrawalApproved,     // 提现审批通过
    WithdrawalCompleted,    // 提现完成（打款）
    WithdrawalRejected,     // 提现拒绝
    ContractSigned,         // 合同签约完成
    ContractRenewRequested, // 合同续签申请
    SystemAnnouncement      // 系统公告
}
```

**Repository** `INotificationRepository`
```csharp
Task<PagedResult<Notification>> GetByUserIdAsync(Guid userId, bool unreadOnly, PagedRequest paged);
Task<int> GetUnreadCountAsync(Guid userId);
Task MarkAllReadAsync(Guid userId);
Task AddAsync(Notification notification);
```

#### Application 层

**`INotificationService`**
```csharp
public interface INotificationService
{
    Task SendAsync(Guid userId, NotificationType type, string title, string body, string? actionUrl = null);
    Task<PagedResult<NotificationDto>> GetMyNotificationsAsync(Guid userId, bool unreadOnly, PagedRequest paged);
    Task<int> GetUnreadCountAsync(Guid userId);
    Task MarkAllReadAsync(Guid userId);
    Task MarkReadAsync(long notificationId, Guid userId);
}
```

**Event Handlers**（监听 Domain Events 发送通知）:

| Event | Handler | 通知类型 |
|-------|---------|----------|
| `DividendDistributedEvent` | `DividendNotificationHandler` | DividendReceived |
| `WithdrawalRequest.Approved` | `WithdrawalNotificationHandler` | WithdrawalApproved |
| `WithdrawalRequest.Completed` | 同上 | WithdrawalCompleted |
| `WithdrawalRequest.Rejected` | 同上 | WithdrawalRejected |
| `ContractSignedEvent` | `ContractNotificationHandler` | ContractSigned |

**通知内容模板**（`src/Application/Common/NotificationTemplates.cs`）:
```csharp
public static class NotificationTemplates
{
    public static (string title, string body) DividendReceived(decimal amount, string currency) =>
        ($"分红到账", $"您有 {currency} {amount:F2} 分红已到账，请查看钱包。");
    // ...en-US 版本通过 IRegionContext 判断
}
```

#### API Controller

```
GET  /v1/notifications              站内消息列表（分页 + unreadOnly 过滤）
GET  /v1/notifications/unread-count 未读数
POST /v1/notifications/mark-all-read
PUT  /v1/notifications/{id}/read
```

### 前端

#### Pinia Store `stores/notification.ts`
```typescript
export const useNotificationStore = defineStore('notification', () => {
  const unreadCount = ref(0)
  const notifications = ref<Notification[]>([])

  async function fetchUnreadCount() {
    const res = await notificationApi.getUnreadCount()
    unreadCount.value = res.data
  }

  // 轮询：每 30 秒刷新未读数（或 SSE）
  function startPolling() {
    setInterval(fetchUnreadCount, 30_000)
  }

  return { unreadCount, notifications, fetchUnreadCount, startPolling }
})
```

#### 通知铃铛组件 `components/layout/NotificationBell.vue`
```html
<n-badge :value="notificationStore.unreadCount" :max="99">
  <n-icon :component="BellIcon" @click="openDrawer" />
</n-badge>
<!-- 点击打开 NotificationDrawer -->
```

**`NotificationDrawer.vue`**
- 全部 / 未读 Tab
- 列表 + 点击标记已读 + 跳转 ActionUrl
- "全部标为已读"按钮

## 完成标准
- [ ] 分红到账 → 投资人有站内通知
- [ ] 提现审批/完成/拒绝 → 投资人有通知
- [ ] 铃铛数字实时更新（30s 轮询）
- [ ] 点击通知标记已读 + 可跳转
