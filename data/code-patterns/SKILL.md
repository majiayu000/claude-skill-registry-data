---
name: ruoyi-vue-plus-code-patterns
description: |
  基于若依-vue-plus框架的全栈代码规范指南。定义后端Java Spring Boot与前端Vue3 + TypeScript的标准化编码模式。
  
  核心内容：
  - 后端分层架构规范：Controller/Service/Mapper三层设计，对象流转模式（Bo/DTO → Entity → Vo）
  - 前端Vue3组合式API规范：<script setup>语法糖、响应式数据管理、组件通信模式
  - 数据库操作规范：MyBatis-Plus的使用规范、批量操作、事务管理
  - 统一响应处理：AjaxResult封装、异常处理、日志记录
  - 安全与权限：@PreAuthorize注解、数据权限、敏感字段处理
  
  触发场景：
  - 编写新的业务模块（CRUD功能）
  - 重构旧代码或优化现有代码
  - 进行代码审查（Code Review）
  - 解决分层架构设计问题
  - 处理Vue3响应式数据丢失问题
  
  触发关键词：代码规范、若依框架、分层架构、DTO/VO转换、对象映射、Vue3 Setup、Composition API、组件封装、响应式、MyBatis-Plus
---

# 若依框架代码规范指南

## 核心规范

### 规范1：分层架构与对象映射规范

**架构层次划分：**
- **Controller层（控制器层）**：负责接收HTTP请求、参数校验、权限控制、响应封装
- **Service层（业务逻辑层）**：负责业务逻辑处理、事务控制、数据组装
- **Mapper层（数据访问层）**：负责数据库CRUD操作，仅处理数据持久化

**对象流转规范：**
1. **Bo (Business Object)** / **DTO (Data Transfer Object)**：前端传入的数据传输对象
   - 用于接收前端表单数据
   - 包含校验注解（@NotNull、@NotBlank等）
   - 命名规则：`实体名称Bo.java`（如 SysOrderBo.java）

2. **Entity (实体对象)**：数据库表映射对象
   - 与数据库表结构一一对应
   - 仅在Service层和Mapper层使用
   - 包含MyBatis-Plus注解（@TableName、@TableId等）
   - 命名规则：`实体名称.java`（如 SysOrder.java）

3. **Vo (View Object)**：返回给前端的视图对象
   - 用于返回给前端展示的数据
   - 可能包含关联对象、计算字段、格式化数据
   - 严禁直接返回Entity，避免暴露敏感字段（密码、盐值等）
   - 命名规则：`实体名称Vo.java`（如 SysOrderVo.java）

**对象转换工具：**
- 优先使用：`BeanUtil.copyProperties(source, targetClass)`（若依封装的Hutool工具）
- 复杂场景使用：MapStruct（编译期生成转换代码，性能更优）
- 严禁手写大量setter/getter进行属性拷贝

**完整数据流转示例：**
```
前端请求 → Bo/DTO（Controller接收） → Entity（Service处理） → Vo（Controller返回） → 前端展示
```

**Controller层完整示例：**

```java
package com.ruoyi.web.controller.system;

import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.common.utils.bean.BeanUtil;
import com.ruoyi.system.domain.SysOrder;
import com.ruoyi.system.domain.bo.SysOrderBo;
import com.ruoyi.system.domain.vo.SysOrderVo;
import com.ruoyi.system.service.ISysOrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 订单管理Controller
 * 
 * @author ruoyi
 */
@RestController
@RequestMapping("/system/order")
public class SysOrderController extends BaseController {

    @Autowired
    private ISysOrderService orderService;

    /**
     * 查询订单列表
     * 返回类型：TableDataInfo（包含分页信息）
     */
    @PreAuthorize("@ss.hasPermi('system:order:list')")
    @GetMapping("/list")
    public TableDataInfo list(SysOrderBo bo) {
        // 开启分页（从BaseController继承）
        startPage();
        // 查询数据（Service返回Vo列表）
        List<SysOrderVo> list = orderService.selectOrderList(bo);
        // 封装分页响应
        return getDataTable(list);
    }

    /**
     * 获取订单详细信息
     * 返回类型：AjaxResult（包含单个Vo对象）
     */
    @PreAuthorize("@ss.hasPermi('system:order:query')")
    @GetMapping(value = "/{orderId}")
    public AjaxResult getInfo(@PathVariable Long orderId) {
        return success(orderService.selectOrderById(orderId));
    }

    /**
     * 新增订单
     * 接收流程：Bo (DTO) → 转换 Entity → Service处理 → 返回操作结果
     */
    @PreAuthorize("@ss.hasPermi('system:order:add')")
    @Log(title = "订单管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@Validated @RequestBody SysOrderBo bo) {
        // 1. Bo (DTO) 转 Entity
        SysOrder order = BeanUtil.copyProperties(bo, SysOrder.class);
        
        // 2. 调用Service（Service负责业务逻辑处理）
        boolean result = orderService.insertOrder(order);
        
        // 3. 返回统一响应（toAjax方法会根据boolean返回成功/失败信息）
        return toAjax(result);
    }

    /**
     * 修改订单
     * 必须先校验数据权限（是否有权限修改该订单）
     */
    @PreAuthorize("@ss.hasPermi('system:order:edit')")
    @Log(title = "订单管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@Validated @RequestBody SysOrderBo bo) {
        SysOrder order = BeanUtil.copyProperties(bo, SysOrder.class);
        return toAjax(orderService.updateOrder(order));
    }

    /**
     * 删除订单（支持批量删除）
     * 参数：订单ID数组
     */
    @PreAuthorize("@ss.hasPermi('system:order:remove')")
    @Log(title = "订单管理", businessType = BusinessType.DELETE)
    @DeleteMapping("/{orderIds}")
    public AjaxResult remove(@PathVariable Long[] orderIds) {
        return toAjax(orderService.deleteOrderByIds(orderIds));
    }

    /**
     * 导出订单数据（Excel）
     */
    @PreAuthorize("@ss.hasPermi('system:order:export')")
    @Log(title = "订单管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, SysOrderBo bo) {
        List<SysOrderVo> list = orderService.selectOrderList(bo);
        ExcelUtil<SysOrderVo> util = new ExcelUtil<>(SysOrderVo.class);
        util.exportExcel(response, list, "订单数据");
    }
}
```

**Service层实现示例：**

```java
package com.ruoyi.system.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.common.utils.bean.BeanUtil;
import com.ruoyi.system.domain.SysOrder;
import com.ruoyi.system.domain.bo.SysOrderBo;
import com.ruoyi.system.domain.vo.SysOrderVo;
import com.ruoyi.system.mapper.SysOrderMapper;
import com.ruoyi.system.service.ISysOrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * 订单服务实现
 */
@Service
public class SysOrderServiceImpl implements ISysOrderService {

    @Autowired
    private SysOrderMapper orderMapper;

    /**
     * 查询订单列表
     * Entity → Vo 转换
     */
    @Override
    public List<SysOrderVo> selectOrderList(SysOrderBo bo) {
        // 1. 构建查询条件（使用MyBatis-Plus的LambdaQueryWrapper）
        LambdaQueryWrapper<SysOrder> wrapper = Wrappers.lambdaQuery();
        wrapper.like(StringUtils.isNotBlank(bo.getOrderNo()), 
                     SysOrder::getOrderNo, bo.getOrderNo())
               .eq(bo.getStatus() != null, 
                   SysOrder::getStatus, bo.getStatus())
               .between(bo.getBeginTime() != null && bo.getEndTime() != null,
                       SysOrder::getCreateTime, bo.getBeginTime(), bo.getEndTime());
        
        // 2. 查询数据库
        List<SysOrder> list = orderMapper.selectList(wrapper);
        
        // 3. Entity → Vo 转换（使用Stream流处理）
        return list.stream()
                   .map(entity -> BeanUtil.copyProperties(entity, SysOrderVo.class))
                   .collect(Collectors.toList());
    }

    /**
     * 新增订单（带事务）
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public boolean insertOrder(SysOrder order) {
        // 业务逻辑处理
        order.setOrderNo(generateOrderNo()); // 生成订单号
        order.setCreateBy(SecurityUtils.getUsername()); // 设置创建人
        
        // 插入数据库（MyBatis-Plus方法）
        return orderMapper.insert(order) > 0;
    }

    /**
     * 批量删除（带事务）
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public boolean deleteOrderByIds(Long[] orderIds) {
        // 使用MyBatis-Plus的批量删除
        return orderMapper.deleteBatchIds(Arrays.asList(orderIds)) > 0;
    }

    /**
     * 生成订单号（业务逻辑）
     */
    private String generateOrderNo() {
        return "ORD" + System.currentTimeMillis();
    }
}
```

### 规范2：Vue3 组合式 API (Composition API) 编码标准

**核心原则：**
- 所有新组件必须使用 `<script setup lang="ts">` 语法糖
- 禁止使用 Options API（`export default {}`）编写新组件
- 优先使用 TypeScript 提供类型安全

**响应式数据定义规范：**

1. **ref() - 用于基本类型和单一对象引用**
   - 适用场景：字符串、数字、布尔值、单个对象引用
   - 访问方式：通过 `.value` 访问/修改
   - 模板中自动解包，无需 `.value`

2. **reactive() - 用于复杂对象和表单数据**
   - 适用场景：表单对象、查询参数、状态管理
   - 特性：深度响应式，自动解包嵌套的ref
   - 注意：解构会丢失响应性，需使用 `toRefs()` 转换

3. **toRefs() - 保持解构后的响应性**
   - 使用场景：需要解构 reactive 对象时
   - 作用：将 reactive 对象的每个属性转为 ref

**组件通信规范：**

1. **父传子：defineProps（类型定义）**
   ```typescript
   // 使用 TypeScript 类型定义（推荐）
   interface Props {
     orderId: number;
     orderData?: SysOrder; // 可选属性
   }
   const props = defineProps<Props>();
   
   // 或使用 withDefaults 定义默认值
   const props = withDefaults(defineProps<Props>(), {
     orderData: () => ({})
   });
   ```

2. **子传父：defineEmits（事件定义）**
   ```typescript
   // 定义事件类型
   interface Emits {
     (e: 'update:modelValue', value: string): void;
     (e: 'submit', data: FormData): void;
   }
   const emit = defineEmits<Emits>();
   
   // 触发事件
   emit('submit', formData);
   ```

3. **跨层级通信：provide/inject（谨慎使用）**
   - 仅用于深层组件树共享状态
   - 优先使用 props/emits 保持数据流清晰

**生命周期钩子：**
- `onMounted()` - 组件挂载后（替代 mounted）
- `onBeforeUnmount()` - 组件卸载前（替代 beforeDestroy）
- `onUpdated()` - 组件更新后
- `watch()` / `watchEffect()` - 侦听响应式数据变化

**完整示例：**

```vue
<template>
  <div class="app-container">
    <!-- 搜索栏 -->
    <el-form :model="queryParams" ref="queryFormRef" :inline="true" v-show="showSearch">
      <el-form-item label="订单编号" prop="orderNo">
        <el-input
          v-model="queryParams.orderNo"
          placeholder="请输入订单编号"
          clearable
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="订单状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择订单状态" clearable>
          <el-option
            v-for="dict in sys_order_status"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 操作按钮 -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['system:order:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:order:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['system:order:remove']"
        >删除</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <!-- 数据表格 -->
    <el-table v-loading="loading" :data="orderList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="订单编号" align="center" prop="orderNo" />
      <el-table-column label="订单金额" align="center" prop="amount" />
      <el-table-column label="订单状态" align="center" prop="status">
        <template #default="scope">
          <dict-tag :options="sys_order_status" :value="scope.row.status" />
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" prop="createTime" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button
            type="text"
            icon="Edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['system:order:edit']"
          >修改</el-button>
          <el-button
            type="text"
            icon="Delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['system:order:remove']"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <pagination
      v-show="total > 0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改订单对话框 -->
    <el-dialog :title="title" v-model="open" width="600px" append-to-body>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="订单编号" prop="orderNo">
          <el-input v-model="form.orderNo" placeholder="请输入订单编号" />
        </el-form-item>
        <el-form-item label="订单金额" prop="amount">
          <el-input-number v-model="form.amount" :precision="2" :min="0" />
        </el-form-item>
        <el-form-item label="订单状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio
              v-for="dict in sys_order_status"
              :key="dict.value"
              :label="dict.value"
            >{{ dict.label }}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" placeholder="请输入内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="OrderList">
import { ref, reactive, toRefs, computed, onMounted, nextTick } from 'vue';
import { listOrder, getOrder, addOrder, updateOrder, delOrder } from '@/api/system/order';
import { SysOrderVo, SysOrderForm, SysOrderQuery } from '@/api/system/order/types';
import type { FormInstance, FormRules } from 'element-plus';

// ==================== 1. 响应式数据定义 ====================

// 基本类型使用 ref
const loading = ref(false);
const showSearch = ref(true);
const open = ref(false);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref('');

// 列表数据使用 ref
const orderList = ref<SysOrderVo[]>([]);
const ids = ref<Array<string | number>>([]);

// 表单对象使用 reactive（配合双向绑定）
const queryParams = reactive<SysOrderQuery>({
  pageNum: 1,
  pageSize: 10,
  orderNo: '',
  status: undefined,
  beginTime: undefined,
  endTime: undefined
});

// 表单数据使用 reactive
const form = reactive<SysOrderForm>({
  orderId: undefined,
  orderNo: '',
  amount: 0,
  status: '0',
  remark: ''
});

// 表单校验规则
const rules = reactive<FormRules>({
  orderNo: [
    { required: true, message: '订单编号不能为空', trigger: 'blur' }
  ],
  amount: [
    { required: true, message: '订单金额不能为空', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '订单状态不能为空', trigger: 'change' }
  ]
});

// ==================== 2. 引用和字典 ====================

// 表单引用
const queryFormRef = ref<FormInstance>();
const formRef = ref<FormInstance>();

// 字典数据（从store获取或本地定义）
const { sys_order_status } = proxy.useDict('sys_order_status');

// ==================== 3. 计算属性 ====================

// 示例：计算已选中的订单数量
const selectedCount = computed(() => ids.value.length);

// ==================== 4. 方法定义 ====================

/** 查询订单列表 */
const getList = async () => {
  loading.value = true;
  try {
    const res = await listOrder(queryParams);
    orderList.value = res.rows;
    total.value = res.total;
  } finally {
    loading.value = false;
  }
};

/** 搜索按钮操作 */
const handleQuery = () => {
  queryParams.pageNum = 1;
  getList();
};

/** 重置按钮操作 */
const resetQuery = () => {
  queryFormRef.value?.resetFields();
  handleQuery();
};

/** 多选框选中数据 */
const handleSelectionChange = (selection: SysOrderVo[]) => {
  ids.value = selection.map(item => item.orderId);
  single.value = selection.length !== 1;
  multiple.value = !selection.length;
};

/** 新增按钮操作 */
const handleAdd = () => {
  reset();
  open.value = true;
  title.value = '添加订单';
};

/** 修改按钮操作 */
const handleUpdate = async (row?: SysOrderVo) => {
  reset();
  const orderId = row?.orderId || ids.value[0];
  try {
    const res = await getOrder(orderId);
    Object.assign(form, res.data);
    open.value = true;
    title.value = '修改订单';
  } catch (error) {
    proxy.$modal.msgError('获取订单详情失败');
  }
};

/** 提交按钮 */
const submitForm = async () => {
  const valid = await formRef.value?.validate();
  if (!valid) return;
  
  try {
    if (form.orderId) {
      await updateOrder(form);
      proxy.$modal.msgSuccess('修改成功');
    } else {
      await addOrder(form);
      proxy.$modal.msgSuccess('新增成功');
    }
    open.value = false;
    await getList();
  } catch (error) {
    proxy.$modal.msgError('操作失败');
  }
};

/** 删除按钮操作 */
const handleDelete = async (row?: SysOrderVo) => {
  const orderIds = row?.orderId ? [row.orderId] : ids.value;
  try {
    await proxy.$modal.confirm(`是否确认删除订单编号为"${orderIds}"的数据项？`);
    await delOrder(orderIds);
    proxy.$modal.msgSuccess('删除成功');
    await getList();
  } catch {}
};

/** 取消按钮 */
const cancel = () => {
  open.value = false;
  reset();
};

/** 表单重置 */
const reset = () => {
  Object.assign(form, {
    orderId: undefined,
    orderNo: '',
    amount: 0,
    status: '0',
    remark: ''
  });
  formRef.value?.resetFields();
};

// ==================== 5. 生命周期钩子 ====================

onMounted(() => {
  getList();
});

// ==================== 6. 暴露给模板的方法（可选）====================
// defineExpose({
//   getList
// });
</script>

<style scoped lang="scss">
// 组件样式
</style>
```

**组件封装示例（子组件）：**

```vue
<template>
  <el-dialog
    :title="title"
    v-model="dialogVisible"
    width="500px"
    @close="handleClose"
  >
    <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
      <el-form-item label="订单编号" prop="orderNo">
        <el-input v-model="formData.orderNo" placeholder="请输入订单编号" />
      </el-form-item>
      <el-form-item label="订单金额" prop="amount">
        <el-input-number v-model="formData.amount" :min="0" :precision="2" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" @click="handleConfirm">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts" name="OrderDialog">
import { ref, reactive, watch } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';

// ==================== Props 定义 ====================
interface Props {
  visible: boolean;
  orderId?: number;
  title?: string;
}

const props = withDefaults(defineProps<Props>(), {
  visible: false,
  title: '订单详情'
});

// ==================== Emits 定义 ====================
interface Emits {
  (e: 'update:visible', value: boolean): void;
  (e: 'confirm', data: any): void;
}

const emit = defineEmits<Emits>();

// ==================== 响应式数据 ====================
const formRef = ref<FormInstance>();
const dialogVisible = ref(props.visible);

const formData = reactive({
  orderNo: '',
  amount: 0
});

const rules = reactive<FormRules>({
  orderNo: [{ required: true, message: '请输入订单编号', trigger: 'blur' }],
  amount: [{ required: true, message: '请输入订单金额', trigger: 'blur' }]
});

// ==================== 侦听器 ====================
// 侦听 props.visible 变化，同步到内部状态
watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal;
});

// 侦听内部状态变化，同步到父组件
watch(dialogVisible, (newVal) => {
  emit('update:visible', newVal);
});

// ==================== 方法 ====================
const handleConfirm = async () => {
  const valid = await formRef.value?.validate();
  if (valid) {
    emit('confirm', { ...formData });
    handleClose();
  }
};

const handleCancel = () => {
  handleClose();
};

const handleClose = () => {
  dialogVisible.value = false;
  formRef.value?.resetFields();
};

// ==================== 暴露方法给父组件 ====================
defineExpose({
  // 父组件可以通过 ref 调用这些方法
  resetForm: () => formRef.value?.resetFields()
});
</script>
```

**使用子组件示例：**

```vue
<template>
  <div>
    <el-button @click="openDialog">打开对话框</el-button>
    
    <!-- 使用 v-model:visible 双向绑定 -->
    <OrderDialog
      ref="orderDialogRef"
      v-model:visible="dialogVisible"
      :order-id="currentOrderId"
      title="编辑订单"
      @confirm="handleDialogConfirm"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import OrderDialog from './components/OrderDialog.vue';

const dialogVisible = ref(false);
const currentOrderId = ref<number>();
const orderDialogRef = ref<InstanceType<typeof OrderDialog>>();

const openDialog = () => {
  currentOrderId.value = 123;
  dialogVisible.value = true;
};

const handleDialogConfirm = (data: any) => {
  console.log('接收到的数据:', data);
  // 处理业务逻辑
};

// 调用子组件暴露的方法
const resetDialog = () => {
  orderDialogRef.value?.resetForm();
};
</script>
```

### 规范3：MyBatis-Plus 使用规范

**核心原则：**
- 优先使用 MyBatis-Plus 提供的 CRUD 方法，减少 XML 配置
- 复杂查询使用 LambdaQueryWrapper，避免字符串拼接
- 批量操作使用批处理方法，提升性能
- 自定义 SQL 放在 Mapper.xml 中，保持代码整洁

**常用查询方法：**

```java
// 1. 基础查询
SysOrder order = orderMapper.selectById(orderId);
List<SysOrder> list = orderMapper.selectList(null);

// 2. 条件查询（LambdaQueryWrapper - 类型安全）
LambdaQueryWrapper<SysOrder> wrapper = Wrappers.lambdaQuery();
wrapper.eq(SysOrder::getOrderNo, "ORD123")              // 等于
       .like(SysOrder::getCustomerName, "张三")         // 模糊查询
       .between(SysOrder::getAmount, 100, 1000)        // 区间查询
       .in(SysOrder::getStatus, Arrays.asList(1, 2))   // IN 查询
       .isNotNull(SysOrder::getCreateTime)             // 非空判断
       .orderByDesc(SysOrder::getCreateTime);          // 排序
List<SysOrder> orders = orderMapper.selectList(wrapper);

// 3. 动态条件查询（根据条件拼接）
wrapper.like(StringUtils.isNotBlank(orderNo), SysOrder::getOrderNo, orderNo)
       .eq(status != null, SysOrder::getStatus, status)
       .ge(beginTime != null, SysOrder::getCreateTime, beginTime)
       .le(endTime != null, SysOrder::getCreateTime, endTime);

// 4. 分页查询
Page<SysOrder> page = new Page<>(pageNum, pageSize);
IPage<SysOrder> result = orderMapper.selectPage(page, wrapper);

// 5. 只查询特定字段（select）
wrapper.select(SysOrder::getOrderId, SysOrder::getOrderNo, SysOrder::getAmount);

// 6. 统计查询
Long count = orderMapper.selectCount(wrapper);
```

**增删改操作：**

```java
// 1. 新增
SysOrder order = new SysOrder();
order.setOrderNo("ORD123");
order.setAmount(new BigDecimal("999.99"));
orderMapper.insert(order); // 返回影响行数，主键会自动回填到 order 对象

// 2. 修改（根据ID）
order.setStatus(2);
orderMapper.updateById(order); // 只更新非null字段

// 3. 条件修改
LambdaUpdateWrapper<SysOrder> updateWrapper = Wrappers.lambdaUpdate();
updateWrapper.set(SysOrder::getStatus, 2)
             .eq(SysOrder::getOrderNo, "ORD123");
orderMapper.update(null, updateWrapper);

// 4. 删除（根据ID）
orderMapper.deleteById(orderId);

// 5. 批量删除
orderMapper.deleteBatchIds(Arrays.asList(1L, 2L, 3L));

// 6. 条件删除
LambdaQueryWrapper<SysOrder> deleteWrapper = Wrappers.lambdaQuery();
deleteWrapper.eq(SysOrder::getStatus, 0);
orderMapper.delete(deleteWrapper);
```

**批量操作（高性能）：**

```java
// 批量插入（推荐使用 Service 的批量方法）
List<SysOrder> orderList = new ArrayList<>();
// ... 填充数据
orderService.saveBatch(orderList); // 默认批次大小 1000

// 批量更新
orderService.updateBatchById(orderList);

// 自定义批次大小
orderService.saveBatch(orderList, 500); // 每批 500 条
```

**自定义 SQL（Mapper.xml）：**

```xml
<!-- SysOrderMapper.xml -->
<mapper namespace="com.ruoyi.system.mapper.SysOrderMapper">
    
    <!-- 结果映射 -->
    <resultMap id="SysOrderResult" type="SysOrder">
        <id     property="orderId"     column="order_id"     />
        <result property="orderNo"     column="order_no"     />
        <result property="amount"      column="amount"       />
        <result property="status"      column="status"       />
        <result property="createTime"  column="create_time"  />
    </resultMap>

    <!-- 复杂查询：订单关联商品信息 -->
    <select id="selectOrderWithProducts" resultType="SysOrderVo">
        SELECT 
            o.order_id,
            o.order_no,
            o.amount,
            GROUP_CONCAT(p.product_name) as product_names
        FROM sys_order o
        LEFT JOIN sys_order_product op ON o.order_id = op.order_id
        LEFT JOIN sys_product p ON op.product_id = p.product_id
        WHERE o.del_flag = '0'
        <if test="orderNo != null and orderNo != ''">
            AND o.order_no LIKE CONCAT('%', #{orderNo}, '%')
        </if>
        GROUP BY o.order_id
        ORDER BY o.create_time DESC
    </select>

    <!-- 批量插入（MySQL） -->
    <insert id="insertBatch">
        INSERT INTO sys_order (order_no, amount, status, create_time)
        VALUES
        <foreach collection="list" item="item" separator=",">
            (#{item.orderNo}, #{item.amount}, #{item.status}, #{item.createTime})
        </foreach>
    </insert>

</mapper>
```

**Mapper 接口定义：**

```java
@Mapper
public interface SysOrderMapper extends BaseMapper<SysOrder> {
    
    /**
     * 查询订单及关联商品信息
     */
    List<SysOrderVo> selectOrderWithProducts(@Param("orderNo") String orderNo);
    
    /**
     * 批量插入订单
     */
    int insertBatch(@Param("list") List<SysOrder> orderList);
}
```

### 规范4：事务管理规范

**事务注解使用：**

```java
@Service
public class SysOrderServiceImpl implements ISysOrderService {
    
    /**
     * 事务方法（标准写法）
     * rollbackFor: 指定哪些异常触发回滚（必须指定 Exception.class）
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public boolean createOrder(SysOrderBo bo) {
        // 1. 插入订单主表
        SysOrder order = BeanUtil.copyProperties(bo, SysOrder.class);
        orderMapper.insert(order);
        
        // 2. 插入订单明细
        List<OrderDetail> details = bo.getDetails();
        for (OrderDetail detail : details) {
            detail.setOrderId(order.getOrderId());
            orderDetailMapper.insert(detail);
        }
        
        // 3. 扣减库存
        for (OrderDetail detail : details) {
            productService.reduceStock(detail.getProductId(), detail.getQuantity());
        }
        
        // 如果任何步骤抛出异常，所有操作都会回滚
        return true;
    }
    
    /**
     * 只读事务（查询优化）
     */
    @Override
    @Transactional(readOnly = true)
    public List<SysOrderVo> selectOrderList(SysOrderBo bo) {
        // 只读事务可以提升查询性能
        return orderMapper.selectOrderList(bo);
    }
}
```

**事务传播行为：**

```java
// REQUIRED（默认）：如果当前存在事务则加入，否则新建事务
@Transactional(propagation = Propagation.REQUIRED)

// REQUIRES_NEW：总是新建事务，挂起当前事务（用于日志记录）
@Transactional(propagation = Propagation.REQUIRES_NEW)

// NESTED：嵌套事务，子事务回滚不影响父事务
@Transactional(propagation = Propagation.NESTED)
```

### 规范5：异常处理与日志规范

**统一异常处理：**

```java
@Service
public class SysOrderServiceImpl implements ISysOrderService {
    
    private static final Logger log = LoggerFactory.getLogger(SysOrderServiceImpl.class);
    
    @Override
    public boolean insertOrder(SysOrder order) {
        try {
            // 业务逻辑
            orderMapper.insert(order);
            return true;
        } catch (DuplicateKeyException e) {
            // 捕获特定异常，抛出业务异常
            log.error("订单号重复: {}", order.getOrderNo(), e);
            throw new ServiceException("订单号已存在");
        } catch (Exception e) {
            // 记录日志
            log.error("创建订单失败", e);
            throw new ServiceException("创建订单失败，请联系管理员");
        }
    }
}
```

**Controller 层异常处理（全局异常处理器已配置）：**

```java
@RestController
public class SysOrderController {
    
    @PostMapping
    public AjaxResult add(@Validated @RequestBody SysOrderBo bo) {
        // 不需要 try-catch，全局异常处理器会统一处理
        // 校验失败会自动返回 400 错误
        // ServiceException 会自动返回友好的错误信息
        return toAjax(orderService.insertOrder(order));
    }
}
```

**日志记录规范：**

```java
// 1. 使用 Slf4j 注解（推荐）
@Slf4j
@Service
public class SysOrderServiceImpl {
    
    public void processOrder(Long orderId) {
        log.debug("开始处理订单: {}", orderId);        // 调试信息
        log.info("订单处理成功: {}", orderId);         // 一般信息
        log.warn("订单库存不足: {}", orderId);         // 警告信息
        log.error("订单处理失败: {}", orderId, ex);   // 错误信息（带异常堆栈）
    }
}

// 2. 使用操作日志注解（记录到数据库）
@Log(title = "订单管理", businessType = BusinessType.INSERT)
@PostMapping
public AjaxResult add(@RequestBody SysOrderBo bo) {
    // 会自动记录操作人、操作时间、操作模块、请求参数等
    return toAjax(orderService.insertOrder(order));
}
```

### 规范6：参数校验规范

**DTO/Bo 对象校验：**

```java
import javax.validation.constraints.*;

public class SysOrderBo {
    
    /** 订单ID（修改时必填） */
    @NotNull(message = "订单ID不能为空", groups = {EditGroup.class})
    private Long orderId;
    
    /** 订单编号（必填，最长50字符） */
    @NotBlank(message = "订单编号不能为空")
    @Size(max = 50, message = "订单编号长度不能超过50个字符")
    private String orderNo;
    
    /** 订单金额（必填，最小0.01，最大99999.99） */
    @NotNull(message = "订单金额不能为空")
    @DecimalMin(value = "0.01", message = "订单金额必须大于0")
    @DecimalMax(value = "99999.99", message = "订单金额不能超过99999.99")
    private BigDecimal amount;
    
    /** 客户手机号（必填，手机号格式） */
    @NotBlank(message = "手机号不能为空")
    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String phone;
    
    /** 邮箱（可选，邮箱格式） */
    @Email(message = "邮箱格式不正确")
    private String email;
    
    /** 订单明细（至少1项） */
    @NotEmpty(message = "订单明细不能为空")
    @Valid // 级联校验
    private List<OrderDetailBo> details;
}
```

**Controller 层校验：**

```java
// 1. 使用 @Validated 触发校验
@PostMapping
public AjaxResult add(@Validated @RequestBody SysOrderBo bo) {
    // 校验失败会自动返回 400 错误和错误信息
    return toAjax(orderService.insertOrder(order));
}

// 2. 分组校验（新增和修改使用不同的校验规则）
@PostMapping
public AjaxResult add(@Validated(AddGroup.class) @RequestBody SysOrderBo bo) {
    return toAjax(orderService.insertOrder(order));
}

@PutMapping
public AjaxResult edit(@Validated(EditGroup.class) @RequestBody SysOrderBo bo) {
    return toAjax(orderService.updateOrder(order));
}

// 3. 路径参数校验
@GetMapping("/{orderId}")
public AjaxResult getInfo(@PathVariable @Min(value = 1, message = "订单ID必须大于0") Long orderId) {
    return success(orderService.selectOrderById(orderId));
}
```

**自定义校验注解：**

```java
// 自定义注解
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = OrderStatusValidator.class)
public @interface ValidOrderStatus {
    String message() default "订单状态值不合法";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

// 校验器实现
public class OrderStatusValidator implements ConstraintValidator<ValidOrderStatus, Integer> {
    
    private static final Set<Integer> VALID_STATUS = Set.of(0, 1, 2, 3, 4);
    
    @Override
    public boolean isValid(Integer value, ConstraintValidatorContext context) {
        if (value == null) {
            return true; // null 值由 @NotNull 校验
        }
        return VALID_STATUS.contains(value);
    }
}

// 使用
public class SysOrderBo {
    @ValidOrderStatus(message = "订单状态只能是0-4之间的值")
    private Integer status;
}
## 禁止事项

### 后端开发禁止事项

1. **❌ 对象流转违规**
   - 禁止在Controller层直接返回数据库实体`Entity`，必须使用`Vo`进行数据裁剪
   - 禁止Controller直接操作Mapper层，必须通过Service层处理业务逻辑
   - 禁止在Entity中添加非数据库字段（应放在Vo中）
   - 禁止手写大量的setter/getter进行对象拷贝，必须使用`BeanUtil.copyProperties`或MapStruct

2. **❌ Service层违规**
   - 禁止在Service层中直接使用`HttpServletRequest`获取参数，必须通过Controller层传递
   - 禁止在Service层返回`AjaxResult`，应返回业务对象或boolean
   - 禁止Service方法抛出不明确的`Exception`，应抛出`ServiceException`并附带友好错误信息
   - 禁止在无事务方法中进行多表操作，必须添加`@Transactional`注解

3. **❌ MyBatis-Plus违规**
   - 禁止使用字符串拼接SQL（容易SQL注入），必须使用LambdaQueryWrapper
   - 禁止在循环中执行单条insert/update（性能低下），应使用批量方法
   - 禁止直接使用`selectList(null)`查询全表（数据量大会OOM），必须添加分页或限制条件
   - 禁止在Entity上使用`@TableField(exist = false)`定义过多非数据库字段

4. **❌ 事务管理违规**
   - 禁止忘记添加`rollbackFor = Exception.class`（默认只回滚RuntimeException）
   - 禁止在事务方法中捕获异常后不抛出（会导致事务不回滚）
   - 禁止在Controller层方法上添加`@Transactional`（应在Service层）
   - 禁止事务方法调用同类中的另一个事务方法（事务会失效，应使用AOP代理）

5. **❌ 异常处理违规**
   - 禁止捕获异常后只打印日志不处理（`e.printStackTrace()`或空catch块）
   - 禁止抛出Exception基类，应抛出具体异常（`ServiceException`、`BusinessException`等）
   - 禁止在finally块中使用return（会覆盖try块的返回值和异常）
   - 禁止使用`System.out.println`打印日志，必须使用Logger

6. **❌ 日志记录违规**
   - 禁止在生产代码中使用`System.out.println`，必须使用Slf4j
   - 禁止使用字符串拼接记录日志（`log.info("用户:" + username)`），应使用占位符（`log.info("用户: {}", username)`）
   - 禁止在高频调用的方法中使用`log.info`（应使用`log.debug`）
   - 禁止记录敏感信息（密码、身份证号、银行卡号等）到日志

7. **❌ 安全违规**
   - 禁止在Vo中返回密码、盐值等敏感字段
   - 禁止在日志中打印完整的用户敏感信息
   - 禁止在前端直接传递SQL语句或表名
   - 禁止使用字符串拼接构造SQL（必须使用参数化查询）

8. **❌ 性能违规**
   - 禁止在循环中调用数据库（N+1查询问题）
   - 禁止查询大量数据不分页（应使用`PageHelper.startPage()`）
   - 禁止在MyBatis的`<select>`中使用`SELECT *`（应明确指定字段）
   - 禁止在高并发接口中使用synchronized同步代码块（应使用分布式锁或Redis）

### 前端开发禁止事项

1. **❌ Vue3语法违规**
   - 禁止在Vue3中继续使用Options API（`export default {}`），必须使用`<script setup>`
   - 禁止直接修改props（props是只读的），应通过emit通知父组件修改
   - 禁止解构reactive对象而不使用`toRefs`（会丢失响应性）
   - 禁止在模板中使用复杂的表达式（应使用computed计算属性）

2. **❌ 响应式数据违规**
   - 禁止使用`var`声明变量，必须使用`const`或`let`
   - 禁止直接给reactive对象赋值（`queryParams = {}`），应使用`Object.assign`或单独修改属性
   - 禁止在ref对象上忘记使用`.value`（模板中会自动解包，但JS代码中需要）
   - 禁止过度使用`any`类型，应明确定义TypeScript接口

3. **❌ API调用违规**
   - 禁止在前端API调用中使用硬编码的URL，必须统一在`@/api/xxx`中定义
   - 禁止不处理API异常（应使用try-catch或全局错误处理）
   - 禁止在组件中直接调用axios，必须封装成API方法
   - 禁止同步调用API（应使用async/await或Promise）

4. **❌ 组件设计违规**
   - 禁止在一个组件中编写超过500行代码（应拆分成多个子组件）
   - 禁止在子组件中直接修改父组件的数据（应使用emit事件）
   - 禁止过度使用`provide/inject`（应优先使用props和emit）
   - 禁止在组件中直接操作DOM（应使用ref和Vue的响应式系统）

5. **❌ 表单处理违规**
   - 禁止不校验表单就提交（应使用`formRef.value?.validate()`）
   - 禁止表单提交后不重置表单（应调用`resetFields()`）
   - 禁止在v-model上绑定非响应式数据
   - 禁止使用字符串作为表单字段名（应使用对象的属性名）

6. **❌ 性能优化违规**
   - 禁止在computed中执行异步操作（应使用watch或watchEffect）
   - 禁止在template中频繁调用方法（应使用computed缓存结果）
   - 禁止不使用key绑定v-for循环（会导致渲染错误）
   - 禁止在高频触发的事件中不使用防抖/节流（如input、scroll）

7. **❌ TypeScript违规**
   - 禁止滥用`as any`强制类型转换（会失去类型检查）
   - 禁止不定义API响应的接口类型（应在`types.ts`中定义）
   - 禁止使用隐式any（应开启`strict`模式）
   - 禁止在接口中使用可选属性而不提供默认值（容易出现undefined错误）

8. **❌ 调试代码违规**
   - 禁止在生产代码中保留`console.log`（应在构建时移除或使用环境变量控制）
   - 禁止在生产代码中保留`debugger`语句
   - 禁止提交注释掉的大段代码（应使用Git版本控制）
   - 禁止在代码中硬编码测试数据

## 参考代码与最佳实践

### 若依框架参考文件

#### 后端参考文件
- **Controller层示例**：`ruoyi-admin/src/main/java/com/ruoyi/web/controller/system/SysUserController.java`
  - 标准的CRUD操作示例
  - 权限注解使用
  - 日志记录注解使用
  - 分页查询处理

- **Service层示例**：`ruoyi-system/src/main/java/com/ruoyi/system/service/impl/SysUserServiceImpl.java`
  - 业务逻辑处理
  - 事务管理
  - 对象转换
  - 异常处理

- **Mapper层示例**：`ruoyi-system/src/main/java/com/ruoyi/system/mapper/SysUserMapper.java`
  - MyBatis-Plus基础用法
  - 自定义SQL方法

- **实体类示例**：
  - Entity: `ruoyi-system/src/main/java/com/ruoyi/system/domain/SysUser.java`
  - Bo: `ruoyi-system/src/main/java/com/ruoyi/system/domain/bo/SysUserBo.java`
  - Vo: `ruoyi-system/src/main/java/com/ruoyi/system/domain/vo/SysUserVo.java`

- **工具类**：
  - BeanUtil: `ruoyi-common/src/main/java/com/ruoyi/common/utils/bean/BeanUtil.java`
  - StringUtils: `ruoyi-common/src/main/java/com/ruoyi/common/utils/StringUtils.java`
  - SecurityUtils: `ruoyi-common/src/main/java/com/ruoyi/common/utils/SecurityUtils.java`

#### 前端参考文件
- **Vue3页面示例**：`ruoyi-ui/src/views/system/user/index.vue`
  - 完整的CRUD页面
  - 表格、表单、对话框组件使用
  - 分页处理
  - 权限按钮控制

- **API封装示例**：`ruoyi-ui/src/api/system/user.js`
  - 统一的API接口定义
  - 请求参数封装
  - 响应数据处理

- **类型定义示例**：`ruoyi-ui/src/api/system/user/types.ts`
  - TypeScript接口定义
  - 请求/响应类型

- **组件封装示例**：
  - 字典标签: `ruoyi-ui/src/components/DictTag/index.vue`
  - 分页组件: `ruoyi-ui/src/components/Pagination/index.vue`
  - 文件上传: `ruoyi-ui/src/components/FileUpload/index.vue`

### 命名规范

#### 后端命名规范

```java
// 1. 包名：全小写，使用点分隔
com.ruoyi.system.controller
com.ruoyi.system.service.impl

// 2. 类名：大驼峰（PascalCase）
public class SysUserController {}
public class SysUserServiceImpl {}

// 3. 方法名：小驼峰（camelCase）
public List<SysUserVo> selectUserList() {}
public boolean insertUser(SysUser user) {}

// 4. 变量名：小驼峰
private String userName;
private List<SysUser> userList;

// 5. 常量名：全大写，下划线分隔
public static final String USER_STATUS_NORMAL = "0";
public static final int MAX_PAGE_SIZE = 1000;

// 6. 实体类字段：小驼峰（数据库字段使用下划线）
private String userName;    // 对应数据库字段 user_name
private Long userId;        // 对应数据库字段 user_id

// 7. Boolean类型：使用 is/has/can 前缀
private Boolean isAdmin;
private Boolean hasPermission;

// 8. 集合类型：使用复数或加上 List/Map 后缀
private List<SysUser> userList;
private Map<String, Object> userMap;
```

#### 前端命名规范

```typescript
// 1. 文件名：kebab-case（短横线命名）
user-list.vue
order-detail.vue
sys-user.ts

// 2. 组件名：PascalCase（大驼峰）
<script setup lang="ts" name="UserList">
export default {
  name: 'OrderDetail'
}

// 3. 变量名和方法名：camelCase（小驼峰）
const userName = ref('');
const handleQuery = () => {};

// 4. 常量名：SCREAMING_SNAKE_CASE（全大写下划线）
const MAX_UPLOAD_SIZE = 10 * 1024 * 1024;
const API_BASE_URL = 'http://api.example.com';

// 5. 接口/类型：PascalCase
interface UserInfo {
  userId: number;
  userName: string;
}

type UserStatus = 0 | 1 | 2;

// 6. 枚举：PascalCase（枚举值全大写）
enum OrderStatus {
  PENDING = 0,
  PAID = 1,
  SHIPPED = 2,
  COMPLETED = 3
}

// 7. CSS类名：kebab-case
.user-list-container {}
.order-detail-header {}

// 8. 事件处理方法：handle开头
const handleClick = () => {};
const handleSubmit = () => {};
const handleDelete = () => {};
```

### 代码注释规范

#### 后端注释规范

```java
/**
 * 订单管理Controller
 * 
 * @author ruoyi
 * @date 2024-01-20
 */
@RestController
@RequestMapping("/system/order")
public class SysOrderController extends BaseController {

    /**
     * 查询订单列表
     * 
     * @param bo 查询条件
     * @return 订单列表（分页）
     */
    @GetMapping("/list")
    public TableDataInfo list(SysOrderBo bo) {
        startPage();
        List<SysOrderVo> list = orderService.selectOrderList(bo);
        return getDataTable(list);
    }

    /**
     * 新增订单
     * 
     * 业务流程：
     * 1. 校验订单号是否重复
     * 2. 创建订单主表记录
     * 3. 创建订单明细记录
     * 4. 扣减商品库存
     * 
     * @param bo 订单业务对象
     * @return 操作结果
     */
    @PostMapping
    public AjaxResult add(@Validated @RequestBody SysOrderBo bo) {
        return toAjax(orderService.insertOrder(bo));
    }
}
```

#### 前端注释规范

```typescript
/**
 * 订单管理页面
 */
<script setup lang="ts" name="OrderList">

/**
 * 查询订单列表
 * @description 根据查询条件获取订单列表，支持分页
 */
const getList = async () => {
  loading.value = true;
  try {
    const res = await listOrder(queryParams);
    orderList.value = res.rows;
    total.value = res.total;
  } finally {
    loading.value = false;
  }
};

/**
 * 处理表格多选变化
 * @param selection 选中的行数据
 */
const handleSelectionChange = (selection: SysOrderVo[]) => {
  ids.value = selection.map(item => item.orderId);
  single.value = selection.length !== 1;
  multiple.value = !selection.length;
};

// TODO: 待实现订单导出功能
// FIXME: 修复订单状态更新后不刷新列表的问题
// NOTE: 此处使用防抖避免频繁调用接口
</script>
```

### 文件结构规范

#### 后端模块结构

```
ruoyi-system/
├── src/main/java/com/ruoyi/system/
│   ├── controller/          # 控制器层
│   │   └── SysOrderController.java
│   ├── service/             # 服务接口层
│   │   ├── ISysOrderService.java
│   │   └── impl/            # 服务实现层
│   │       └── SysOrderServiceImpl.java
│   ├── mapper/              # 数据访问层
│   │   └── SysOrderMapper.java
│   ├── domain/              # 领域模型层
│   │   ├── SysOrder.java    # 实体类
│   │   ├── bo/              # 业务对象
│   │   │   └── SysOrderBo.java
│   │   └── vo/              # 视图对象
│   │       └── SysOrderVo.java
│   └── enums/               # 枚举类
│       └── OrderStatusEnum.java
└── src/main/resources/
    └── mapper/system/       # MyBatis XML
        └── SysOrderMapper.xml
```

#### 前端模块结构

```
ruoyi-ui/
├── src/
│   ├── views/system/order/  # 页面目录
│   │   ├── index.vue        # 主页面
│   │   ├── components/      # 页面专用组件
│   │   │   ├── OrderDialog.vue
│   │   │   └── OrderDetail.vue
│   │   └── types.ts         # 页面类型定义（可选）
│   ├── api/system/          # API接口
│   │   └── order/
│   │       ├── index.ts     # API方法
│   │       └── types.ts     # 接口类型定义
│   ├── components/          # 全局公共组件
│   │   ├── DictTag/
│   │   └── Pagination/
│   ├── utils/               # 工具函数
│   │   ├── request.ts       # axios封装
│   │   └── validate.ts      # 校验函数
│   └── stores/              # Pinia状态管理
│       └── modules/
│           └── order.ts
```

## 代码质量检查清单

### 提交代码前必须检查的项目

#### 后端代码检查清单

- [ ] **分层架构检查**
  - [ ] Controller只负责接收请求和响应，没有业务逻辑
  - [ ] Service层包含所有业务逻辑
  - [ ] Mapper层只负责数据库操作
  - [ ] 对象流转遵循：Bo → Entity → Vo

- [ ] **对象转换检查**
  - [ ] Controller返回的是Vo，不是Entity
  - [ ] 使用了BeanUtil.copyProperties或MapStruct进行对象拷贝
  - [ ] 没有在Entity中添加非数据库字段
  - [ ] Vo中不包含敏感字段（密码、盐值等）

- [ ] **数据库操作检查**
  - [ ] 使用了LambdaQueryWrapper，没有字符串拼接SQL
  - [ ] 批量操作使用了批量方法（saveBatch/updateBatchById）
  - [ ] 查询大量数据时使用了分页
  - [ ] 没有在循环中执行数据库操作

- [ ] **事务管理检查**
  - [ ] Service层的数据修改方法添加了@Transactional注解
  - [ ] 包含了rollbackFor = Exception.class
  - [ ] 没有在Controller层使用@Transactional
  - [ ] 捕获异常后重新抛出，避免事务失效

- [ ] **异常处理检查**
  - [ ] 使用了try-catch捕获异常
  - [ ] 抛出了具体的业务异常（ServiceException）
  - [ ] 异常信息对用户友好
  - [ ] 记录了必要的错误日志

- [ ] **日志记录检查**
  - [ ] 使用了Slf4j，没有System.out.println
  - [ ] 日志使用占位符{}，没有字符串拼接
  - [ ] 没有记录敏感信息
  - [ ] 日志级别使用正确（debug/info/warn/error）

- [ ] **参数校验检查**
  - [ ] Bo对象添加了校验注解（@NotNull、@NotBlank等）
  - [ ] Controller方法使用了@Validated触发校验
  - [ ] 重要参数进行了非空判断
  - [ ] 数值范围进行了校验

- [ ] **安全检查**
  - [ ] Controller方法添加了权限注解（@PreAuthorize）
  - [ ] SQL使用参数化查询，没有拼接
  - [ ] 敏感操作添加了操作日志（@Log）
  - [ ] 返回的Vo不包含敏感信息

- [ ] **代码规范检查**
  - [ ] 类、方法、变量命名符合规范
  - [ ] 添加了必要的注释（类注释、方法注释）
  - [ ] 没有大段注释掉的代码
  - [ ] 导入的包没有使用通配符（import xxx.*）

- [ ] **性能检查**
  - [ ] 没有N+1查询问题
  - [ ] 查询只返回需要的字段，没有SELECT *
  - [ ] 高频调用的方法考虑了缓存
  - [ ] 大数据量处理使用了分批处理

#### 前端代码检查清单

- [ ] **Vue3语法检查**
  - [ ] 使用了<script setup lang="ts">语法
  - [ ] ref用于基本类型，reactive用于对象
  - [ ] 解构reactive对象时使用了toRefs
  - [ ] ref访问时正确使用了.value

- [ ] **TypeScript检查**
  - [ ] 定义了接口类型（Props、Emits、API响应等）
  - [ ] 没有滥用any类型
  - [ ] 组件props和emits有明确的类型定义
  - [ ] 变量声明使用了const或let，没有var

- [ ] **组件设计检查**
  - [ ] 组件代码不超过500行（考虑拆分）
  - [ ] props是只读的，没有直接修改
  - [ ] 使用emit向父组件传递事件
  - [ ] 组件有清晰的name属性

- [ ] **API调用检查**
  - [ ] API方法定义在@/api目录中
  - [ ] 使用了async/await处理异步
  - [ ] 添加了try-catch或错误处理
  - [ ] loading状态在finally中正确关闭

- [ ] **表单处理检查**
  - [ ] 表单提交前进行了校验（formRef.value?.validate()）
  - [ ] 表单定义了校验规则（rules）
  - [ ] 提交成功后重置了表单（resetFields()）
  - [ ] 对话框关闭时清理了数据

- [ ] **性能优化检查**
  - [ ] 计算属性使用了computed
  - [ ] v-for绑定了唯一的key
  - [ ] 高频事件使用了防抖或节流
  - [ ] 大列表考虑了虚拟滚动

- [ ] **代码规范检查**
  - [ ] 文件名使用kebab-case
  - [ ] 组件名使用PascalCase
  - [ ] CSS类名使用kebab-case
  - [ ] 添加了必要的注释

- [ ] **调试代码检查**
  - [ ] 移除了所有console.log
  - [ ] 移除了debugger语句
  - [ ] 移除了注释掉的代码
  - [ ] 移除了测试用的硬编码数据

### 代码审查（Code Review）清单

在进行代码审查时，重点关注以下方面：

#### 功能性审查
- [ ] 代码实现是否符合需求
- [ ] 边界条件是否处理正确
- [ ] 异常情况是否有合理的处理
- [ ] 是否有潜在的空指针异常

#### 安全性审查
- [ ] 是否存在SQL注入风险
- [ ] 是否暴露了敏感信息
- [ ] 权限控制是否完善
- [ ] 是否验证了用户输入

#### 性能审查
- [ ] 是否存在N+1查询
- [ ] 大数据量处理是否优化
- [ ] 是否有不必要的循环或递归
- [ ] 缓存是否合理使用

#### 可维护性审查
- [ ] 代码是否易读易懂
- [ ] 是否有重复代码（考虑抽取公共方法）
- [ ] 命名是否清晰准确
- [ ] 注释是否充分合理

#### 规范性审查
- [ ] 是否遵循了项目的代码规范
- [ ] 文件结构是否合理
- [ ] 是否符合分层架构要求
- [ ] 是否使用了项目统一的工具类和组件

## 常见问题与解决方案

### 后端常见问题

**问题1：Entity直接返回给前端**
```java
// ❌ 错误写法
@GetMapping("/{id}")
public AjaxResult getInfo(@PathVariable Long id) {
    SysOrder order = orderService.getById(id);
    return success(order); // 直接返回Entity
}

// ✅ 正确写法
@GetMapping("/{id}")
public AjaxResult getInfo(@PathVariable Long id) {
    SysOrderVo vo = orderService.selectOrderById(id);
    return success(vo); // 返回Vo
}
```

**问题2：忘记添加事务注解**
```java
// ❌ 错误写法（多表操作没有事务）
public boolean createOrder(SysOrder order) {
    orderMapper.insert(order);
    orderDetailMapper.insert(detail); // 如果这里失败，订单已插入
}

// ✅ 正确写法
@Transactional(rollbackFor = Exception.class)
public boolean createOrder(SysOrder order) {
    orderMapper.insert(order);
    orderDetailMapper.insert(detail); // 失败会回滚
}
```

**问题3：循环中执行数据库操作**
```java
// ❌ 错误写法（性能差）
for (Long id : ids) {
    orderMapper.deleteById(id);
}

// ✅ 正确写法（批量操作）
orderMapper.deleteBatchIds(Arrays.asList(ids));
```

**问题4：查询全表数据**
```java
// ❌ 错误写法（数据量大会OOM）
List<SysOrder> list = orderMapper.selectList(null);

// ✅ 正确写法（分页查询）
startPage(); // 使用PageHelper分页
List<SysOrderVo> list = orderService.selectOrderList(bo);
```

### 前端常见问题

**问题1：解构reactive对象丢失响应性**
```typescript
// ❌ 错误写法
const state = reactive({ count: 0 });
const { count } = state; // 丢失响应性
count++; // 不会触发更新

// ✅ 正确写法
const state = reactive({ count: 0 });
const { count } = toRefs(state); // 保持响应性
count.value++; // 正确触发更新
```

**问题2：直接修改props**
```typescript
// ❌ 错误写法
const props = defineProps<{ visible: boolean }>();
props.visible = false; // 错误！props是只读的

// ✅ 正确写法
const props = defineProps<{ visible: boolean }>();
const emit = defineEmits<{ (e: 'update:visible', value: boolean): void }>();
emit('update:visible', false); // 通知父组件修改
```

**问题3：ref忘记使用.value**
```typescript
// ❌ 错误写法
const count = ref(0);
count++; // 错误！应该使用count.value

// ✅ 正确写法
const count = ref(0);
count.value++; // 正确
```

**问题4：表单提交不校验**
```typescript
// ❌ 错误写法
const submitForm = () => {
  addOrder(form); // 直接提交，没有校验
};

// ✅ 正确写法
const submitForm = async () => {
  const valid = await formRef.value?.validate();
  if (!valid) return;
  addOrder(form);
};
```

## 总结

遵循本规范可以：
1. ✅ 提高代码质量和可维护性
2. ✅ 减少常见错误和安全隐患
3. ✅ 提升开发效率和团队协作
4. ✅ 保持代码风格统一
5. ✅ 降低系统维护成本

**记住：规范不是限制，而是让我们写出更好代码的指引！**