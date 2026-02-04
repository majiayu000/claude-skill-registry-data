---
name: db-metadata
description: 提供v3_metadata数据库的SQL查询模板，包括对象编码（object_code）、对象名称、事件、按钮配置、自定义字段、元数据字段、插件中心等表的查询。查询对象编码、对象名称、自定义对象时使用。使用 exec_sql 工具执行查询。
---

# v3_metadata 数据库查询

## 【通用规范】

参考：[通用规范](./COMMON.md)

## 执行方式

所有查询使用 `exec_sql` 工具执行，参数替换为实际值。

**重要**：在执行 SQL 前，必须先打印出完整的目标 SQL 语句，然后再使用 `exec_sql` 工具执行。

**重要**：执行 SQL 后，必须对查询结果进行结构化展示：
- 明确说明查询到的记录数量
- 提取并展示关键字段的值（如对象编码、对象名称等）
- 多条记录时使用表格或列表形式展示，避免直接输出原始 JSON 数据

## 查询模板

### standard_business_object

**用途**：查询对象编码（object_code）和对象名称。根据对象名称查找对象编码，或根据对象编码查询对象信息。**常用表**。

**字段**：
- `object_code` - 对象编码
- `object_name` - 对象名称
- `org_id` - 租户ID（工厂号）
  - 预置对象：`org_id = -1`
  - 自定义对象：`org_id` 为对应的工厂号
- `object_category` - 对象类别（1=自定义对象，2=预设对象）

### mq_event

**用途**：查询业务事件配置信息。

**字段**：
- `id` - 事件ID

### mq_event_subscribe_target_topic

**用途**：查询事件转发配置信息。

**字段**：
- `event_id` - 事件ID

### mq_event_body_config

**用途**：查询事件体字段配置信息。

**字段**：
- `event_id` - 事件ID
- `biz_field_id` - 业务字段ID（关联 meta_field_config.id）

### meta_field_config

**用途**：查询字段类型配置信息，定义字段的数据类型和属性。

**字段**：
- `id` - 字段配置ID
- `biz_source` - 业务来源（如 'BIZ_EVENT'）

**关联关系**：
- `meta_field_config.id` = `mq_event_body_config.biz_field_id`

### button_config

**用途**：查询按钮配置信息，包括按钮分类、来源等。

**字段**：
- `object_code` - 对象编码
- `category` - 按钮分类（1=通用，2=新自定义，3=预置）
- `source` - 按钮来源（1=web，2=app）

### custom_field

**用途**：查询自定义字段元数据配置信息，可以查询对象下的自定义字段定义。**常用表**。

**字段**：
- `object_code` - 对象编码
- `field_id` - 字段ID（关联 meta_field_config.id）

**关联关系**：
- `custom_field.object_code` = `standard_business_object.object_code`
- `custom_field.field_id` = `meta_field_config.id`

**查询示例**：
```sql
-- 按对象编码查询自定义字段
SELECT * FROM v3_metadata.custom_field WHERE object_code = '{object_code}' AND deleted_at = 0;

-- 按租户ID和对象编码查询自定义字段（关联对象表验证）
SELECT cf.* FROM v3_metadata.custom_field cf
INNER JOIN v3_metadata.standard_business_object sbo ON cf.object_code = sbo.object_code
WHERE sbo.org_id = {org_id} AND cf.object_code = '{object_code}' AND cf.deleted_at = 0 AND sbo.deleted_at = 0;
```

### plugin_center

**用途**：查询插件中心配置信息，包括流程插件等。用于统计插件中心的租户数和流程个数。

**字段**：
- `id` - 插件ID
- `org_id` - 租户ID（工厂id）
- `code` - 按钮编号
- `name` - 按钮名称
- `type` - 插件类型（1=流程插件）
- `status` - 状态（表示是否发布）
- `wf_id` - 流程ID（用于统计流程个数）

**查询示例**：
```sql
-- 按租户查询插件中心配置
SELECT * FROM v3_metadata.plugin_center WHERE org_id = {org_id} AND deleted_at = 0;

-- 统计已发布的流程插件
SELECT 
    COUNT(DISTINCT org_id) as tenant_count,
    COUNT(DISTINCT wf_id) as workflow_count
FROM v3_metadata.plugin_center
WHERE type = 1 AND status = 1 AND deleted_at = 0 AND wf_id IS NOT NULL;
```

## 事件相关查询模板

### 根据 event_id 查询事件配置

**用途**：根据事件ID查询完整的事件配置数据，用于生成插入语句。

#### 1. 事件源转发配置
```sql
SELECT * FROM v3_metadata.mq_event_subscribe_target_topic 
WHERE event_id IN ({event_id}) AND deleted_at = 0;
```

#### 2. 事件配置
```sql
SELECT * FROM v3_metadata.mq_event 
WHERE id IN ({event_id}) AND deleted_at = 0;
```

#### 3. 事件字段配置
```sql
SELECT * FROM v3_metadata.mq_event_body_config 
WHERE event_id IN ({event_id}) AND deleted_at = 0;
```

#### 4. 事件字段类型配置
```sql
SELECT * FROM v3_metadata.meta_field_config t1
LEFT JOIN v3_metadata.mq_event_body_config t2 ON t1.id = t2.biz_field_id
WHERE biz_source = 'BIZ_EVENT' AND event_id IN ({event_id}) AND deleted_at = 0;
```

## 对象名称和 object_code 对应关系

**用途**：根据对象名称查找对应的 object_code。如果对象名称中包含"-"，则视为匹配失败。

```
仓库 : Warehouse
仓库区域 : Zone
仓位 : StorageLocation
单位 : Unit
设备 : Equipment
角色 : Role
部门 : Department
用户 : User
物料 : Material
物料分类 : MaterialCategory
区域 : Location
标识码 : IdentificationCode
班次 : Shift
排班规则 : ShiftRule
批次 : BatchNo
检验方案 : QualityInspectionScheme
检验项分类 : InspectionItemCategory
检验项 : InspectionItem
自定义AQL : CustomizedAQL
检验计划 : QualityInspectionPlan
检验计划行 : QualityInspectionPlanDetail
入库单 : InboundOrder
入库单行 : InboundOrderItem
出库单 : OutboundOrder
出库单行 : OutboundOrderItem
SOP方案 : SOPScheme
不良等级 : DefectLevel
不良原因 : CauseOfDefect
销售订单 : SalesOrder
客户 : Customer
销售订单行 : SalesOrderItem
供应商 : Supplier
SOP步骤 : SubStep
SOP步骤组 : SubStepGroup
SOP任务 : SOPTask
SOP控件 : SOPControl
电子签名 : ElectronicSignature
签名人配置 : ElectronicSignatureSet
调拨单 : TransferOrder
SOP方案副本 : CopySOPScheme
检验项明细 : SpecificInspectionItem
工作日历 : WorkCalendar
班次时段 : TimeInterval
周期班次 : PeriodShift
特殊日 : ExceptionDate
物料清单 : BOM
工序 : Process
工艺路线 : Routing
工艺路线行 : RoutingProcess
工序接续关系 : ProcessConnection
工序在制品 : ProcessProduct
子项物料 : SubItemMaterial
子项物料子行 : SubItemMaterialChild
投料管控行 : MaterialFeedControl
多产出物料 : Coproduct
生产工单 : ProductionOrder
工序计划行 : ProductionOrderProcess
工序计划 : ProductionOrderProcessPlan
工单产出物料 : POProduct
用料清单行 : InputMaterialDetail
用料清单投料管控行 : InputMaterialFeedControlDetail
工作中心 : WorkCenter
资源组 : ResourceGroup
领料申请 : PickOrder
客户物料注册审核单 : CustomerMaterialRegisteredAudit
客户物料注册审核单行 : CustomerMaterialRegisteredAuditItem
客户注册审核单 : CustomerRegisteredAudit
质量手动调整记录 : QualityAdjustmentRecord
质量手动调整记录行 : QualityAdjustmentRecordDetail
接收质量限 : ReceptionQualityLimit
接收质量限行 : ReceptionQualityLimitDetail
样本记录 : SampleInventoryRecord
总体记录 : OverallInventoryRecord
生产任务 : ProduceTask
物料属性值 : MaterialAttributeValue
编号规则 : NumberingRule
编号规则元素 : NumberingRuleElement
物料单位列表 : MaterialConversionUnitList
调拨单行 : TransferOrderItem
采购订单 : PurchaseOrder
采购订单物料行 : PurchaseOrderItem
文件管理 : Document
收货单物料行 : ReceiveNoteItem
协同采购申请单 : PurchaseAuditNote
协同采购申请单明细行 : PurchaseAuditNoteItem
批次属性配置 : BatchAttributeConfig
库存属性配置 : InventoryAttributeConfig
物料属性项 : MaterialAttributeItem
报告模板 : ReportTemplate
报告模板控件 : ReportTemplateControl
工序计划行接续方式 : ProductionOrderProcessConnection
报告 : Report
报工记录 : ProgressReportRecord
库存明细 : InventoryElement
库存变动记录 : InventoryElementChangeLog
入库记录 : InboundRecord
出库记录 : OutboundRecord
调拨记录 : TransferRecord
库存调整记录 : AmountAdjustRecord
属性变更记录 : AttrAdjustRecord
检验项记录 : InspectionItemRecord
样本量行 : SampleSizeInterval
投料回撤记录 : MaterialRetractRecord
检验任务 : QualityInspectionTask
货源清单 : SourceList
货源清单供应商行 : SourceListRegisteredItem
工序计划行在制品 : ProductionOrderProcessProduct
投料记录 : MaterialFeedRecord
数据集 : Dataset
电子单据模版 : eReport
领料申请行 : PickOrderDetail
发货单 : ShipmentsNote
发货单行 : ShipmentsNoteItem
检验方案关联物料 : MaterialOfQualityInspectionScheme
检验方案关联工序 : ProcessOfQualityInspectionScheme
检验方案关联设备 : EquipmentOfQualityInspectionScheme
检验方案关联供应商 : SupplierOfQualityInspectionScheme
检验方案关联客户 : CustomerOfQualityInspectionScheme
销售退货单 : SalesOrderReturn
销售退货单行 : SalesOrderReturnItem
检验方案副本 : CopyOfQualityInspectionScheme
检验方案版本 : QualityInspectionSchemeVersion
工艺路线行快照 : RoutingProcessSnapshot
采购退货单 : PurchaseReturnOrder
采购退货单物料行 : PurchaseReturnOrderItem
退货申请单 : ReturnAuditNote
退货申请单行 : ReturnAuditNoteItem
自动创建任务触发器 : QcTrigger
检验范围 : QualityInspectionTaskRange
检验项标准配置关联客户 : QualityInspectionCheckItemCustomer
物料业务范围 : MaterialBizRange
收货单 : ReceiveNote
元素格式 : FormatConfigAbstract
检验项标准配置资源 : QualityInspectionCheckItemEquipment
检验方案自动触发规则 : TriggerRulesForInspectionPlans
检验范围关联批号 : QualityInspectionTaskRangeBatchNo
对象 : Object
字段 : Field
元素来源 : ElementFieldAbstract
工作中心快照 : WorkCenterSnapShot
资源组快照 : ResourceGroupSnapShot
库存明细辅助单位信息 : InventoryElementAuxAmount
投料仓位 : WorkCenterFeedStorage
产出仓位 : WorkCenterProductStorage
投料仓位快照 : WorkCenterFeedStorageSnapShot
产出仓位快照 : WorkCenterProductStorageSnapShot
检验任务-检验项记录-不良等级 : QualityInspectionTaskInspectionItemDefectRank
检验任务-检验项记录-不良数量 : QualityInspectionTaskInspectionItemDefectCount
检验任务-检验项记录-不良原因 : QualityInspectionTaskInspectionItemDefectReason
库存明细关键业务属性 : MaterialInventoryBizKey
物料生产信息 : MaterialProductionInfo
报工记录详情 : ProgressReportRecordDetail
AQL接受质量限 : AQL
AQL检验水平 : AQLInspectionLevel
AQL样本量字码表 : AQLSampleCode
AQL抽样方案表 : AQLSamplingPlan
检验项明细所有选项 : QcConfigCheckItemOption
检验项目明细合格选项 : QcConfigCheckItemQualityOption
触发器进度 : QcTriggerProgress
检验计划行上检验方案 : QualityInspectionPlanDetailScheme
检验范围关联客户 : QualityInspectionTaskRangeCustomer
检验范围关联质量状态 : QualityInspectionTaskRangeQcStatus
检验范围关联存储位置 : QualityInspectionTaskRangeStorage
检验范围关联供应商 : QualityInspectionTaskRangeSupplier
检验范围关联供应商批次 : QualityInspectionTaskRangeSupplierBatch
基于样本整体填写的报告 : QualityInspectionTaskRecordCount
数据权限 : Data privilege
功能权限表 : Privilege
角色字段权限 : Role field permission
角色许可项 : Role permission
载具基本定义信息 : HandlingEquipmentBaseInfo
供应商注册物料行 : SupplierRegisteredItem
资源分类 : ResourceType
通知模板 : MessageTemplate
触发事件 : TriggerAction
触发条件 : TriggerConditions
触发规则 : TriggerRules
操作详情 : OperationLogDetails
从对象日志 : SubObjectOperationLog
批号 : BatchNum
租户信息 : Tenant
操作日志 : OperationLog
通知接收人 : MessageReceiver
客户注册信息 : CustomerRegister
客户注册物料信息 : CustomerRegisterMaterial
客户已注册物料行 : CustomerRegisteredItem
对象属性值 : ObjectAttributeValue
资源参数定义 : ResourceParameter
被替代物料 : OriginalAlternativeMaterial
替代物料 : AlternativeMaterial
替代方案 : AlternativePlan
能源仪表 : EnergyInstrument
资源标签值 : ResourceLabelValue
设备标签 : EquipmentLabel
设备参数 : EquipmentParameter
能源仪表参数 : EnergyInstrumentParameter
能源仪表标签 : EnergyInstrumentLabel
资源标签 : ResourceLabel
统计设备 : StatisticsOfEquipment
布局控件 : LayoutComponent
资源参数记录 : ResourceParameterRecord
资源参数监控 : ResourceParameterMonitoring
审批任务 : ApprovalTask
计划订单 : PlanOrder
审批流程节点 : ApprovalNode
审批流程方案 : ApprovalScheme
审批节点副本 : CopyApprovalNode
审批流程方案副本 : CopyApprovalScheme
审批单 : ApprovalInstance
SOP任务信息 : QcTaskSopInfo
SOP步骤执行记录 : StepExecRecord
SOP任务记录 : SOPTaskRecord
不良信息 : qcTaskCheckItemDefectInfo
工作日历行 : WorkCalendarInfo
工单替代方案 : WorkOrderAlternativePlan
工单替代物料 : WorkOrderAlternativeMaterial
工单被替代物料 : WorkOrderOriginalAlternativeMaterial
可选资源部门行 : ResourceGroupInfoDepartment
可选资源设备行 : ResourceGroupInfoResource
可选资源用户行 : ResourceGroupInfoUser
工艺参数 : ResourceParams
维保任务 : MaintenanceTask
维保方案 : MaintenanceCase
维保任务暂停记录 : MaintenancePauseRecording
异常参数监控 : WarningParamMonitor
异常参数记录 : WarningParamRecord
电子单据对象匹配规则 : eReportMatch
定制化报表配置 : Cus_eReport
叫料单 : DeliveryScheduleNote
叫料单行 : DeliveryScheduleNoteItem
客户叫料单 : CustomerDeliveryScheduleNote
客户叫料单行 : CustomerDeliveryScheduleNoteItem
币种 : Currency
自定义布局 : Layout
资源故障记录 : ResourceMalfunctionRecord
资源故障记录标签 : MalfunctionLabel
数采规则 : DataAcquisitionRule
工作日历负责人 : WorkerCalendarManager
智能分析平台 : IntelligentAnalysisPlatform
追溯关系 : TrackTrace
业务类型 : BusinessType
生产库存变动记录-报工记录 : ProductionInventoryLogProgess
生产库存变动记录-入库记录 : ProductionInventoryLogInbound
枚举字段映射 : EnumFieldMapping
投料申请 : MaterialFeedApply
工序配置项 : ProcessConfigurationItems
物料投料信息 : MaterialFeedInfo
自定义菜单 : CustomMenu
外协用料清单物料行 : OutsourceMaterialList
维修方案 : RepairCase
维修任务暂停记录 : RepairPauseRecording
维修任务 : RepairTask
维修方案故障标签 : RepairCaseMalfunctionLabel
维修任务故障标签 : RepairTaskMalfunctionLabel
报告单据记录 : ReportDocumentsRecord
电子单据 : eReportCase
物料计划配置 : MaterialPlanConfigura
占用 : PlanReserved
补料申请行 : ReplenishOrderDetail
补料申请 : ReplenishOrder
退料申请 : RetractOrder
退料申请行 : RetractOrderDetail
库存调整单 : AmountAdjustOrder
收发货单采购订单关联表 : ReceiveShipmentPoMapping
模具 : SinoMold
模具标签 : SinoMoldLabel
模具参数 : SinoMoldParameter
销售库存 : SalesInventory
供应商库存 : SupplyInventory
HD设备 : HDdevice
采购订单变更快照 : PurchaseOrderChangeSnapshot
采购订单物料行变更快照 : PurchaseOrderItemChangeSnapshot
采购变更单 : OrderChangeNote
采购变更单行 : OrderChangeNoteItem
外协用料清单快照 : OutsourceMaterialListSnapshot
采购变更申请单 : OrderChangeApplication
刀具 : BladeTools
刀具参数 : BladeToolsParameter
称具 : WeighingTools
称具标签 : WeighingToolsLabel
称具参数 : WeighingToolsParameter
刀具标签 : BladeToolsLabel
异常类型 : ExceptionType
处理标签 : ExceptionHandleLabel
异常主题 : ExceptionSubject
异常订阅 : ExceptionSubscribe
异常事件 : ExceptionEvent
异常事件记录 : ExceptionEventLog
异常事件报告 : ExceptionEventReport
条码解析规则 : BarcodeParseRule
条码解析元素 : BarcodeParseElement
发货预约单 : DeliveryAppointment
发货预约单行 : DeliveryAppointmentItem
标签模板 : LabelTemplate
标签模板配置 : LabelTemplateConfig
标签模板对象匹配规则 : LabelTemplateMatch
维保任务审批记录 : MaintenanceApprovalRecording
维修任务审批记录 : RepairApprovalRecording
维保任务执行记录 : MaintenanceExecRecording
维修任务执行记录 : RepairExecRecording
发货记录 : ShipmentRecord
交货计划 : DeliverySchedule
客户交货计划 : CuDeliverySche
生产任务操作记录 : TaskOperationRecord
报表模板 : eReportform
报表模板对象匹配规则 : eReportformMatch
生产库存 : ProductionInventory
待收清单 : WaitingReceivingList
收货记录 : ReceivingRecord
采购申请单 : PurchaseRequisitions
采购申请单行 : PurchaseRequisitionsItem
采购申请单行关联 : PurchaseRequisitionsItemRel
生产库存变动记录-冲销记录 : ProductionInventoryLogOutbound
外协发料单 : OutsourceSendMaterial
外协发料单行 : OutsourceSendMaterialItem
客户外协发料单 : CusOutsourceSendMaterial
客户外协发料单行 : CusOutsourceSendMaterialItem
嵌套规格 : ContainSpec
嵌套规格明细 : ContainSpecItem
嵌套任务 : ContainTask
嵌套任务明细 : ContainTaskItem
嵌套记录 : ContainRecord
嵌套规格快照 : ContainSpecVersion
嵌套单元 : MaterialContainerLot
标签 : Label
电子单据模板打印日志 : ePrintLog
标签模板打印日志 : lPrintLog
新智能分析平台 : DaasBI
供应链通知模板 : ScmMessageTemplate
供应链通知模板下发日志 : ScmMessageTemplateDistributeLog
供应链通知模板关联表 : ScmMessageTemplateRel
离线调度 : OfflineSchedule
收货记录明细 : ReceivingRecordItem
接口日志 : OpenApiLog
生产任务主产出物料 : ProduceTaskMainOutputMaterial
系统配置 : SystemConfig
自定义页面 : CustomPage
系统菜单设置 : SystemMenu
外协退料单 : OutsourceReturnMaterial
外协退料单行 : OutsourceReturnMaterialItem
供应商退料单 : SupOutsourceReturnMaterial
供应商退料单行 : SupOutsourceReturnMaterialItem
地址 : AddressInfo
生产工作台 : ProductionWorkbench
盘点单 : InventoryCountingOrder
盘点任务 : InventoryCountingTask
盘点记录 : InventoryCountingRecord
盘点结果 : InventoryCountingResult
生产暂停原因 : ProductionPauseReason
采购计划 : PurchasePlan
采购计划行 : PurchasePlanItem
客户计划反馈 : CustomerPlanFeedback
客户计划反馈行 : CustomerPlanFeedbackItem
计划反馈 : PlanFeedback
计划反馈行 : PlanFeedbackItem
自定义按钮 : CustomButton
SOP数字控件 : SOPControlNumeric
可销清单 : PermissibleSalesList
可销清单客户行 : PermissibleSalesListItem
供应链BOM : ScBom
供应链BOM子项物料行 : ScBomMaterial
运算方案 : MrpCalculateScheme
MRP物料配置 : ScmMrpMaterialSetting
MRP运算任务 : MrpCalculateTask
MRP运算物料行 : MrpCalculateItem
MRP物料运算明细 : MrpCalculateDetail
计划工单 : ScmPlanWorkOrder
计划工单产出物料 : ScmPlanWorkOrderOutputMaterial
计划工单用料清单 : ScmPlanWorkOrderInputMaterial
工单销售订单关联 : ProductionOrderSalesOrderRelevance
返工记录 : ReworkRecord
报废记录 : ScrapRecord
生产过程原因 : ProductionProcessReason
生产追溯 : ProductTrace
工作流 : Workflow
数据看板 : Dashboard
MRP生产变动周期配置行 : ScmMrpProduceChangeCycleItem
报工工序 : ScmProgressReportWorkingProcedure
报工工序行 : ScmWorkingProcedureItem
供应链报工记录 : ScProgressReportRecord
MRP运算结果物料行 : MrpCalculateResultItem
嵌套标签 : ContainLabel
外协待收清单 : OutsourceWaitingReceivingList
外协收料记录 : OutsourceReceivingRecord
外协发料记录 : OutsourceShipmentRecord
外协收料记录明细 : OutsourceReceivingRecordItem
看板投屏 : TVDashboard
库存转换记录 : InventoryConversionRecord
库存转换单 : InventoryConversionOrder
转换生成物料信息记录 : ConvertGenerateInventoryRecord
调拨接收记录 : TransferReceiveRecord
企业自建应用 : EnterpriseSelfBuiltApplication
批次库存 : batchInventory
流转卡 : FlowCard
库存冻结解冻记录 : InventoryFreezeThawRecord
称量方案 : WeighingScheme
称量方案行 : WeighingSchemeItem
称量任务 : WeighingTask
称量任务行 : WeighingTaskItem
称量任务行细分 : WeighingTaskItemSplitInstruction
称量记录 : WeighingRecord
资源寿命记录 : ResourceLifeRecord
资源使用记录 : ResourceUsageRecord
模具刀具切换记录 : ResourceSwitchRecord
生产业务报表 : ProductionReport
仓储业务报表 : StorageReport
库存扩展标签信息配置 : ExtendConfig
库存占用关系 : EntityInventoryOccupyRel
库存占用解占记录 : InventoryOccupationDisposaRecord
用料清单齐套明细 : InputMaterialCompleteDetail
生产工单齐套数 : ProductionOrderCompleteSet
齐套分析 : CompleteAnalysisPlan
标准产能-行 : StandardCapacityItem
生产日历关联工位 : ProductionCalendarWorkstation
生产日历 : ProductionCalendar
标准产能 : StandardCapacity
产线约束 : LineConstraints
产线约束-行 : LineConstraintsItem
排产区域 : ScheduleArea
生产任务生产排产单 : ProductionSchedule
工位 : WorkStation
执行步骤方案 : ExecutiveStepScheme
生产执行步骤 : ProductionExecutionStep
生产步骤执行记录 : ProductionStepExecutionRecord
标签样式模板 : LabelAppearanceTemplate
占用库存 : holdingInventory
物料可占用库存质量状态配置 : MaterialAvailableInventoryQualityStatusConfig
标签记录 : LabelRecord
安全配置 : SecurityConfiguration
检验触发日志 : QcTriggerRecord
倒冲投报关联关系 : BackFlushRelation
鉴权设置 : authentication_settings
集成流版本 : IntegratedFlowVersion
执行日志 : IntegratedFlowInstance
执行动作 : execute_action
集成流 : IntegratedFlow
连接器信息 : connector_basic_information
集成流节点 : IntegratedFlowNode
定制化报表配置-自定义模版上传 : Cus_eReport_upload
SOP控件编辑记录 : SopControlValueEditRecord
仪表盘 : JMDashboard
非主产出标签 : SecondaryOutPutLabel
分析告警规则 : AnalysisConfig
分析告警记录 : AnalysisRecord
```

## 注意事项

1. 参数替换：所有模板中的`{参数名}`都需要替换为实际值
2. 删除标记：所有查询都包含`deleted_at = 0`条件
3. 执行方式：必须通过 MCP 工具 `exec_sql` 执行
4. 表结构查询：使用 `DESC table_name` 或 `SHOW COLUMNS FROM table_name` 查询
5. 对象映射：如果对象名称中包含"-"，则视为匹配失败，返回错误信息

