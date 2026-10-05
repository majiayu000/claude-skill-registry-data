---
name: epic-2-project
description: 执行 Epic 2 —— 项目管理（募资项目、固定/灵活槽位机制、投资人管理）。依赖 Epic 1 已完成。
---

# Epic 2 — 项目与槽位管理

## 前置条件
- Epic 1 已完成（用户认证可用）
- 已读取 `shareflow-context/SKILL.md`

## 任务清单

### 后端

#### Domain 层

**`VideoProject` 实体** (`src/Domain/Entities/VideoProject.cs`)
```csharp
public class VideoProject : Entity<Guid>
{
    public string Title { get; private set; } = string.Empty;
    public string PlatformName { get; private set; } = string.Empty;  // TikTok,YouTube,抖音...
    public string PlatformAccountId { get; private set; } = string.Empty;
    public ProjectSlotMode SlotMode { get; private set; }   // Fixed / Flexible
    public int TotalSlots { get; private set; }             // Fixed 模式下总份数
    public decimal TotalAmount { get; private set; }        // 当前已募集总额（Flexible）
    public ProjectStatus Status { get; private set; }       // Draft / Fundraising / Active / Closed
    public Guid SalesOwnerId { get; private set; }
    public DateTime? FundraisingDeadline { get; private set; }
    public IReadOnlyList<ProjectSlot> Slots { get; private set; } = [];

    public void StartFundraising() { /* Status = Fundraising */ }
    public void Activate() { /* Status = Active */ }
    public void Close()    { /* Status = Closed  */ }
    public ProjectSlot AddSlot(decimal amount, int sharePermille) { ... }
}

public enum ProjectSlotMode { Fixed, Flexible }
public enum ProjectStatus   { Draft, Fundraising, Active, Closed }
```

**`ProjectSlot` 实体** (`src/Domain/Entities/ProjectSlot.cs`)
```csharp
public class ProjectSlot : Entity<Guid>
{
    public Guid ProjectId { get; private set; }
    public decimal InvestmentAmount { get; private set; }   // 该槽位投资额
    public int SharePermille { get; private set; }          // 持股千分比 (decimal 8,4 存储)
    public SlotStatus Status { get; private set; }          // Available / Reserved / Occupied / Exited
    public Guid? InvestorUserId { get; private set; }       // 关联投资人

    public void Reserve(Guid investorId) { /* Status = Reserved */ }
    public void Confirm()                { /* Status = Occupied */ }
    public void Exit()                   { /* Status = Exited   */ }
}

public enum SlotStatus { Available, Reserved, Occupied, Exited }
```

#### Infrastructure 配置
- `VideoProjectConfiguration` Fluent API
- `ProjectSlotConfiguration` (owned or separate table，推荐 separate table with FK)
- `IVideoProjectRepository` → `VideoProjectRepository`

#### Application 层

**DTO**
- `CreateProjectRequest` { Title, PlatformName, PlatformAccountId, SlotMode, TotalSlots, FundraisingDeadline? }
- `ProjectDto` { Id, Title, Platform, Status, TotalSlots, FilledSlots, FundingProgress(%), SalesOwnerName }
- `SlotDto` { Id, Amount, SharePermille, Status, InvestorName? }

**Mapster** (`ProjectMappingConfig : IRegister`)
```csharp
config.NewConfig<VideoProject, ProjectDto>()
    .Map(dest => dest.FilledSlots, src => src.Slots.Count(s => s.Status == SlotStatus.Occupied))
    .Map(dest => dest.FundingProgress, src => (decimal)src.Slots.Count(s=>s.Status==SlotStatus.Occupied)
                                                / (src.TotalSlots == 0 ? 1 : src.TotalSlots) * 100);
```

**IProjectService**
```csharp
public interface IProjectService
{
    Task<PagedResult<ProjectDto>> GetListAsync(ProjectQueryRequest query);
    Task<ProjectDto> GetByIdAsync(Guid id);
    Task<Guid> CreateAsync(CreateProjectRequest request, Guid operatorId);
    Task UpdateAsync(Guid id, UpdateProjectRequest request, Guid operatorId);
    Task ChangeStatusAsync(Guid id, ProjectStatus newStatus, Guid operatorId);
    Task<SlotDto> AddSlotAsync(Guid projectId, AddSlotRequest request);
    Task AssignInvestorAsync(Guid slotId, Guid investorUserId);
}
```

#### API Controller

`GET    /v1/admin/projects` `[Permission("project.read")]`
`POST   /v1/admin/projects`  `[Permission("project.write")]`
`PUT    /v1/admin/projects/{id}`
`POST   /v1/admin/projects/{id}/status`
`GET    /v1/admin/projects/{id}/slots`
`POST   /v1/admin/projects/{id}/slots`
`PUT    /v1/admin/slots/{slotId}/investor`

### 前端

#### `types/project.ts`
```typescript
export interface Project {
  id: string
  title: string
  platformName: string
  status: 'Draft' | 'Fundraising' | 'Active' | 'Closed'
  slotMode: 'Fixed' | 'Flexible'
  totalSlots: number
  filledSlots: number
  fundingProgress: number
  salesOwnerName: string
}

export interface ProjectSlot {
  id: string
  amount: number
  sharePermille: number
  status: 'Available' | 'Reserved' | 'Occupied' | 'Exited'
  investorName?: string
}
```

#### `api/project.ts`
```typescript
export const projectApi = {
  list: (params: ProjectQueryRequest) =>
    http.get<PagedResult<Project>>('/v1/admin/projects', { params }),
  create: (data: CreateProjectRequest) =>
    http.post<{ id: string }>('/v1/admin/projects', data),
  changeStatus: (id: string, status: string) =>
    http.post(`/v1/admin/projects/${id}/status`, { status }),
  listSlots: (projectId: string) =>
    http.get<ProjectSlot[]>(`/v1/admin/projects/${projectId}/slots`),
  addSlot: (projectId: string, data: AddSlotRequest) =>
    http.post<ProjectSlot>(`/v1/admin/projects/${projectId}/slots`, data),
  assignInvestor: (slotId: string, investorUserId: string) =>
    http.put(`/v1/admin/slots/${slotId}/investor`, { investorUserId })
}
```

#### `views/admin/projects/` 页面结构
- `ProjectListView.vue` — NDataTable + 分页 + 状态筛选
- `ProjectDetailView.vue` — 基本信息 + 槽位列表
- `SlotProgressBar.vue` — 公共组件：可视化已占/总份数进度条

**`SlotProgressBar.vue` 关键 Props:**
```typescript
defineProps<{
  filled: number
  total: number
  mode: 'Fixed' | 'Flexible'
}>()
```

## 完成标准
- [ ] 项目列表支持按 Status 筛选分页
- [ ] Fixed 模式：添加槽位后进度条正确更新
- [ ] Flexible 模式：总额累加正确
- [ ] 仅 SuperAdmin / `project.write` 权限可创建项目
- [ ] 槽位分配投资人后 Status → Occupied
