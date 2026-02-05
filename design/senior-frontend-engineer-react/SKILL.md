---
name: senior-frontend-engineer-react
description: |
  Enterprise React development skill for building CRUD applications with React 16.14, DVA 2.x, and @lianjia/antd-life component library.

  Core capabilities: (1) Auto-generate list pages with pagination/filtering/sorting, (2) Form dialog management with validation, (3) Detail page rendering in read-only/edit modes, (4) DVA model integration for state management, (5) API service layer with async/await patterns.

  Tech stack: React 16.14, DVA 2.x, TypeScript, @lianjia/antd-life, Ant Design 3.x. Best suited for internal management systems, dashboards, and data-driven applications.

  Important: NOT compatible with React 18 or Ant Design 5. Use appropriate versions for your project.
version: 2.1.0
author: USK Team
tags:
  - react
  - dva
  - typescript
  - crud
  - enterprise
  - frontend
platform: claude
---

# Senior Frontend Engineer - React Skill

专业的企业级React开发技能，适用于快速构建CRUD应用。

## 🎯 核心功能

### 1. 列表页生成

自动生成带有完整功能的列表页：

```typescript
import { createListPage } from '@/utils/page-generator';

const UserListPage = createListPage({
  entity: 'user',
  columns: [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: '姓名', dataIndex: 'name', key: 'name' },
    { title: '邮箱', dataIndex: 'email', key: 'email' },
    { title: '角色', dataIndex: 'role', key: 'role' }
  ],
  actions: ['create', 'edit', 'delete'],
  filters: ['name', 'role']
});

export default UserListPage;
```

**特性**：
- ✅ 自动分页
- ✅ 多条件筛选
- ✅ 排序功能
- ✅ 批量操作
- ✅ 导出数据

### 2. 表单弹窗管理

```typescript
import { FormDialog } from '@/components/FormDialog';

<FormDialog
  visible={visible}
  title="新建用户"
  fields={[
    { name: 'name', label: '姓名', type: 'input', required: true },
    { name: 'email', label: '邮箱', type: 'email', required: true },
    { name: 'role', label: '角色', type: 'select', options: roleOptions }
  ]}
  onSubmit={handleSubmit}
  onCancel={() => setVisible(false)}
/>
```

**特性**：
- ✅ 自动表单验证
- ✅ 异步提交处理
- ✅ 错误提示
- ✅ Loading状态

### 3. DVA Model集成

```typescript
// models/user.ts
export default {
  namespace: 'user',

  state: {
    list: [],
    pagination: { current: 1, pageSize: 10, total: 0 }
  },

  effects: {
    *fetchList({ payload }, { call, put }) {
      const response = yield call(services.getUserList, payload);
      yield put({ type: 'saveList', payload: response });
    }
  },

  reducers: {
    saveList(state, { payload }) {
      return {
        ...state,
        list: payload.data,
        pagination: payload.pagination
      };
    }
  }
};
```

### 4. API服务层

```typescript
// services/user.ts
import request from '@/utils/request';

export async function getUserList(params) {
  return request('/api/users', {
    method: 'GET',
    params
  });
}

export async function createUser(data) {
  return request('/api/users', {
    method: 'POST',
    data
  });
}

export async function updateUser(id, data) {
  return request(`/api/users/${id}`, {
    method: 'PUT',
    data
  });
}

export async function deleteUser(id) {
  return request(`/api/users/${id}`, {
    method: 'DELETE'
  });
}
```

## 📦 项目结构

```
src/
├── pages/              # 页面组件
│   ├── User/
│   │   ├── List.tsx
│   │   ├── Detail.tsx
│   │   └── model.ts
│   └── Dashboard/
├── components/         # 通用组件
│   ├── FormDialog/
│   ├── TableList/
│   └── DetailView/
├── services/           # API服务
│   ├── user.ts
│   └── common.ts
├── models/             # DVA模型
│   ├── global.ts
│   └── user.ts
└── utils/              # 工具函数
    ├── request.ts
    └── page-generator.ts
```

## 🚀 快速开始

### 1. 安装依赖

```bash
npm install react@16.14 dva@2.x @lianjia/antd-life
```

### 2. 配置路由

```typescript
// router.config.ts
export default [
  {
    path: '/user',
    component: './User/List'
  },
  {
    path: '/user/:id',
    component: './User/Detail'
  }
];
```

### 3. 创建页面

使用提供的模板快速创建新页面：

```bash
npm run generate:page User
```

## 🎨 最佳实践

### 1. 组件设计

```typescript
// ✅ 好的实践
interface UserListProps {
  dispatch: Dispatch;
  loading: boolean;
  userList: UserItem[];
}

const UserList: React.FC<UserListProps> = ({
  dispatch,
  loading,
  userList
}) => {
  // 组件逻辑
};

export default connect(({ user, loading }) => ({
  userList: user.list,
  loading: loading.effects['user/fetchList']
}))(UserList);
```

### 2. 状态管理

```typescript
// ✅ 使用DVA管理复杂状态
dispatch({ type: 'user/fetchList', payload: { page: 1 } });

// ❌ 避免直接在组件中请求
const fetchData = async () => {
  const res = await api.getUsers();
  setUsers(res.data);
};
```

### 3. 错误处理

```typescript
// ✅ 统一错误处理
effects: {
  *fetchList({ payload }, { call, put }) {
    try {
      const response = yield call(services.getUserList, payload);
      yield put({ type: 'saveList', payload: response });
    } catch (error) {
      message.error('获取用户列表失败');
      console.error(error);
    }
  }
}
```

## 📚 参考资料

- [React 16.14 Documentation](https://legacy.reactjs.org/docs/getting-started.html)
- [DVA Documentation](https://dvajs.com/)
- [@lianjia/antd-life Components](https://antd-life.ke.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## ⚠️ 注意事项

1. **版本兼容性**
   - React 16.14（不支持React 18）
   - Ant Design 3.x（不支持Ant Design 5）
   - DVA 2.x

2. **性能优化**
   - 使用React.memo避免不必要的重渲染
   - 合理使用useCallback和useMemo
   - 虚拟滚动处理大列表

3. **类型安全**
   - 所有组件使用TypeScript
   - API响应需要类型定义
   - 避免使用any类型

## 🔧 故障排除

### 问题1: DVA model未加载

```bash
# 检查model是否正确注册
console.log(app._models);
```

### 问题2: 组件未更新

```bash
# 检查connect是否正确
export default connect(({ user }) => ({ user }))(Component);
```

## 📝 更新日志

### v2.1.0 (2024-12-05)
- ✨ 新增批量操作功能
- ✨ 支持自定义筛选器
- 🐛 修复分页重置问题
- 📝 完善文档和示例

### v2.0.0 (2024-11-01)
- ✨ 完全重写，支持TypeScript
- ✨ 新增表单弹窗组件
- ✨ 优化API服务层

---

Made with ❤️ by USK Team
