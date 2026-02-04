---
name: d365fo-debugging
description: Complete D365 Finance & Operations debugging framework. Routes symptoms to correct playbook (Finance, SCM, WMS, Batch, Security, Integration, Performance, Reporting). Activates for D365, Dynamics, AX, voucher, posting, batch job, SSRS, DMF, work order, wave, security, can't post, missing, wrong amount, slow, stuck.
allowed-tools: [Read, Grep, Bash, Task]
---

# D365 Finance & Operations - Complete Debugging Framework v6

## FORENSICS CORE (The Kernel)

These rules apply to EVERY playbook, EVERY time.

### Anti-Hallucination Rules (NEVER violate)

| Rule | Description |
|------|-------------|
| **SCHEMA FIRST** | NEVER guess columns. Run `SELECT TOP 1 *` or `sys.columns` before any filtered query |
| **NO HARD-CODED FILTERS** | NEVER hard-code DATAAREAID, PARTITION, or database names without validation |
| **PLATINUM RULE** | ALWAYS find a WORKING example and DIFF it. 2 queries beats 15 |
| **DIAMOND RULE** | Check FULL STACK: UI/Form -> Business Logic -> Config -> Batch/Report/Integration |
| **LINE CONTAMINATION** | One bad LINE can override the entire HEADER classification |
| **STOP CONDITIONS** | If not found after 3 queries -> pivot upstream/downstream |

### Universal Inputs

```
REQUIRED (at least one):
- businessKey: The document/record ID (SO number, PO, Invoice, Voucher, WorkId, etc.)
- symptom: What's wrong (missing, wrong amount, can't post, slow, etc.)

OPTIONAL (validate before using):
- legalEntity / company / DATAAREAID
- partition
- environment (DEV/UAT/PROD)
- user (who experienced it)
- timeWindow (when it happened)
- documentType (SalesOrder, PurchaseOrder, TransferOrder, Invoice, etc.)
- journalType (AP/AR/GL/FA)
- reportName / menuItemName
- batchJobId / batchTaskId
- dataEntityName / integrationName
- errorMessage (exact text)
- correlationId (for integrations)
```

### Standard Output Format (Every Run)

```markdown
## D365 Debug: [Symptom] - [BusinessKey]

### 1. Assumptions
- Assuming: [What I'm taking as given]
- NOT assuming: [What I'll verify]
- Routing to: [Playbook name]

### 2. First 3 Safe Checks (Schema-First)
1. [Schema discovery query]
2. [Existence check]
3. [State/status check]

### 3. Platinum Diff Plan
- Good reference: [How to find one]
- Diff query: [Compare bad vs good]

### 4. Diamond Stack Trace
- UI/Form layer: [What to check]
- Business logic: [Classes/methods]
- Configuration: [Setup tables]
- Execution layer: [Batch/report/integration]

### 5. Stop Conditions
- If [X] not found -> Pivot to [Y]
- If data correct but excluded -> Check [Z]

### 6. Resolution
[What fixed it or next steps]
```

---

## SYMPTOM ROUTER

**Start here.** Match symptom to playbook:

| Symptom Pattern | Route To | First Check |
|-----------------|----------|-------------|
| "Missing from report" | `REPORTING` | Data exists? -> DP class filter |
| "Not posted / can't post" | `POSTING` | Validation errors -> Setup -> Workflow |
| "Wrong amount / calculation" | `FINANCE-CALC` | Platinum diff -> Line contamination |
| "User can't see / access" | `SECURITY` | Entry point -> Role -> Privilege |
| "Integration success but no record" | `INTEGRATION` | Staging -> Entity mapping -> Business events |
| "Batch didn't run / stuck" | `BATCH` | History -> Dependencies -> Batch group |
| "Slow / hanging / timeout" | `PERFORMANCE` | Locks -> SQL plan -> AOS load |
| "Invoice missing lines" | `SCM-ORDER` | SO/PO lines -> Packing slip -> Invoice match |
| "Work stuck / not released" | `WMS` | Wave -> Work -> Location directives |
| "Voucher wrong / missing" | `FINANCE-GL` | Journal -> Posting profile -> Dimensions |

---

## CAPABILITY PACK: FINANCE

### GL (General Ledger)

**Key identifiers:** Voucher, JournalNum, AccountingDate, MainAccount

**Canonical lineage:**
```
LedgerJournalTable (header)
  -> LedgerJournalTrans (lines)
    -> GeneralJournalEntry (posted)
      -> GeneralJournalAccountEntry (account splits)
```

**Schema discovery:**
```sql
SELECT TOP 1 * FROM LedgerJournalTable;
SELECT TOP 1 * FROM GeneralJournalEntry;
```

**Common contaminators:**
- Wrong posting profile on line
- Dimension mismatch (MainAccount vs DefaultDimension)
- Currency/exchange rate at line level
- Blocked account or suspended dimension

**Voucher prefix decoder:**
| Prefix | Source | Trace To |
|--------|--------|----------|
| INT | External integration | Staging table |
| INV | AP Invoice | VendInvoiceJour |
| PAY | Payment | VendPaymJournalTrans |
| GJ | GL Journal | LedgerJournalTrans |
| CXI | Customer Invoice | CustInvoiceJour |

### AP (Accounts Payable)

**Key identifiers:** InvoiceId, VendAccount, Voucher, PurchId

**Canonical lineage:**
```
VendInvoiceInfoTable (pending)
  -> VendInvoiceInfoLine
    -> VendInvoiceJour (posted header)
      -> VendInvoiceTrans (posted lines)
        -> VendTrans (subledger)
          -> GeneralJournalEntry (GL)
```

**Common issues:**
```sql
-- Invoice not posting: Check validation
SELECT * FROM VendInvoiceInfoTable
WHERE ParmId = 'INVOICE_ID' AND Posted = 0;

-- Match failures
SELECT PurchId, InvoiceId, MatchStatus, MatchVariance
FROM VendInvoiceInfoTable
WHERE InvoiceAccount = 'VENDOR';
```

### AR (Accounts Receivable)

**Key identifiers:** InvoiceId, CustAccount, SalesId, Voucher

**Canonical lineage:**
```
SalesTable -> SalesLine
  -> CustPackingSlipJour -> CustPackingSlipTrans
    -> CustInvoiceJour -> CustInvoiceTrans
      -> CustTrans -> GeneralJournalEntry
```

---

## CAPABILITY PACK: SUPPLY CHAIN (SCM)

### Order-to-Cash

**Key identifiers:** SalesId, ItemId, InventTransId

**Canonical lineage:**
```
SalesTable (header)
  -> SalesLine (lines)
    -> InventTrans (inventory transactions)
      -> CustPackingSlipJour/Trans (packing slip)
        -> CustInvoiceJour/Trans (invoice)
```

**Missing invoice lines check:**
```sql
-- Compare SO lines to invoice lines
SELECT
    SL.SalesId, SL.ItemId, SL.LineNum,
    SL.SalesQty AS OrderedQty,
    ISNULL(IT.InvoicedQty, 0) AS InvoicedQty
FROM SalesLine SL
LEFT JOIN (
    SELECT InventTransId, SUM(Qty) AS InvoicedQty
    FROM CustInvoiceTrans
    GROUP BY InventTransId
) IT ON SL.InventTransId = IT.InventTransId
WHERE SL.SalesId = 'SO_NUMBER'
  AND SL.SalesQty <> ISNULL(IT.InvoicedQty, 0);
```

### Procure-to-Pay

**Key identifiers:** PurchId, ItemId, InventTransId

**Canonical lineage:**
```
PurchTable -> PurchLine
  -> InventTrans
    -> VendPackingSlipJour/Trans (product receipt)
      -> VendInvoiceJour/Trans (invoice)
```

### Inventory

**Key identifiers:** ItemId, InventDimId, InventTransId

**On-hand investigation:**
```sql
-- Current on-hand
SELECT ItemId, InventDimId, PhysicalInvent, AvailPhysical
FROM InventSum
WHERE ItemId = 'ITEM';

-- Transaction history
SELECT * FROM InventTrans
WHERE ItemId = 'ITEM'
ORDER BY DatePhysical DESC;
```

---

## CAPABILITY PACK: WAREHOUSE (WMS)

**Key identifiers:** WorkId, LoadId, ShipmentId, WaveId, WHSContainerId

**Canonical lineage:**
```
WHSWave
  -> WHSLoadTable -> WHSLoadLine
    -> WHSWorkTable -> WHSWorkLine
      -> WHSContainerTable
        -> WHSWorkInventTrans
```

**Work stuck diagnosis:**
```sql
-- Work status check
SELECT WorkId, WorkStatus, TargetLicensePlateId,
       CreateDateTime, UserId
FROM WHSWorkTable
WHERE LoadId = 'LOAD_ID';

-- Wave status
SELECT WaveId, WaveStatus, WaveProcessed
FROM WHSWave
WHERE WaveId = 'WAVE_ID';
```

**Common issues:**
- Location directive not finding put location
- Work template missing lines
- Reservation not available
- License plate conflicts

**Location directive debug:**
```sql
SELECT * FROM WHSLocDirTable
WHERE WorkType = 1  -- Put
  AND WorkTransType = 1  -- Sales
ORDER BY SeqNum;
```

---

## CAPABILITY PACK: BATCH & OPERATIONS

**Key identifiers:** BatchJobId, Caption, Status, StartDateTime

**Batch job diagnosis:**
```sql
-- Job history
SELECT TOP 20
    RecId, Caption, Status,
    StartDateTime, EndDateTime,
    CreatedBy, AlertsProcessed
FROM BatchJob
WHERE Caption LIKE '%JOB_NAME%'
ORDER BY StartDateTime DESC;

-- Status decoder
-- 0=Hold, 1=Waiting, 2=Executing, 3=Error, 4=Finished, 5=Canceling

-- Stuck tasks
SELECT BJ.Caption, BT.ClassNumber, BT.Status, BT.Info
FROM BatchJob BJ
JOIN BatchTask BT ON BJ.RecId = BT.BatchJobId
WHERE BJ.Status = 2  -- Executing
  AND BJ.StartDateTime < DATEADD(hour, -2, GETDATE());
```

**Why didn't it run?**
1. Check `BatchJob.Status` - is it on Hold (0)?
2. Check `BatchGroup` assignment - is AOS in the group?
3. Check dependencies - `BatchConstraints` table
4. Check recurrence - `BatchJob.RecurrenceData`
5. Check `BatchServerGroup` - is batch server enabled?

---

## CAPABILITY PACK: SECURITY

**Key identifiers:** UserId, SecurityRole, MenuItemName

**"User can't see/do X" diagnosis:**

```sql
-- 1. What roles does user have?
SELECT SR.Name AS RoleName, URS.AssignmentMode
FROM SecurityUserRole URS
JOIN SecurityRole SR ON URS.SecurityRole = SR.RecId
WHERE URS.User = 'USER_ID';

-- 2. What entry point is needed?
SELECT * FROM SecurableObject
WHERE Name = 'MENU_ITEM_NAME';

-- 3. Which roles have that entry point?
SELECT DISTINCT SR.Name AS RoleName
FROM SecurityRole SR
JOIN SecurityRolePermission SRP ON SR.RecId = SRP.SecurityRole
JOIN SecurableObject SO ON SRP.SecurableObject = SO.RecId
WHERE SO.Name = 'MENU_ITEM_NAME';
```

**Stack trace:**
```
Menu Item (entry point)
  -> Security Privilege (atomic permission)
    -> Security Duty (job function)
      -> Security Role (assigned to user)
```

**Common issues:**
- Role assigned but duty excluded
- Data security policy filtering out records
- Privilege exists but grant type is Deny
- Legal entity restriction on role

---

## CAPABILITY PACK: INTEGRATION (DMF/OData)

**Key identifiers:** ExecutionId, EntityName, DefinitionGroupId

**DMF import diagnosis:**
```sql
-- Execution history
SELECT TOP 20
    ExecutionId, DefinitionGroupId, StartTime, EndTime,
    StagingStatus, TargetStatus, ErrorCount
FROM DMFExecutionSummary
WHERE DefinitionGroupId = 'PROJECT_NAME'
ORDER BY StartTime DESC;

-- Staging table errors
SELECT * FROM [STAGING_TABLE]
WHERE DefinitionGroup = 'PROJECT'
  AND TransferStatus = 2;  -- Error

-- Error details
SELECT ExecutionId, Field, ErrorCode, ErrorMessage
FROM DMFExecutionErrors
WHERE ExecutionId = 'EXEC_ID';
```

**"Success but no record" diagnosis:**
1. Check staging table - did data land?
2. Check `TransferStatus` - did it process?
3. Check entity mapping - field mappings correct?
4. Check target table - record exists but different key?
5. Check business validation - rejected by entity logic?

**Integration lineage:**
```
Source File/API
  -> DMF Staging Table (raw data)
    -> DMF Execution (processing)
      -> Target Table (final data)
        -> Business Events (if configured)
```

---

## CAPABILITY PACK: REPORTING (SSRS)

**Key identifiers:** ReportName, DesignName, MenuItemName

**CRITICAL: Logic is in Data Provider (DP), NOT Controller!**

```
Controller Class: Parameters, dialog, print destination
  -> DP Class (*DP): Query building, data population
    -> TMP Table (*Tmp): Holds processed data
      -> SSRS Design: Rendering only
```

**Report not showing records diagnosis:**
```sql
-- 1. Does data exist?
SELECT TOP 10 * FROM [SourceTable]
WHERE [Filter] = 'VALUE';

-- 2. Find the DP class
-- Look for [ReportName]DP in AOT

-- 3. Check DP.processReport() method
-- Look for QueryRun, while select, insertTmp()
```

**Common issues:**
- Query range in DP excludes records
- Print management setup missing
- Report parameters not passed to DP
- TMP table insert logic has additional filters

---

## CAPABILITY PACK: PERFORMANCE

**Key identifiers:** SPID, WaitType, QueryHash

**Blocking/locking diagnosis:**
```sql
-- Current blocks
SELECT
    blocking.session_id AS BlockingSession,
    blocked.session_id AS BlockedSession,
    blocked.wait_type,
    blocked.wait_time,
    OBJECT_NAME(locked.object_id) AS LockedTable
FROM sys.dm_exec_requests blocked
JOIN sys.dm_exec_sessions blocking ON blocked.blocking_session_id = blocking.session_id
JOIN sys.dm_tran_locks locked ON blocked.session_id = locked.request_session_id;

-- Long running queries
SELECT TOP 10
    r.session_id,
    r.start_time,
    r.status,
    SUBSTRING(t.text, 1, 200) AS QueryText
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.status = 'running'
ORDER BY r.total_elapsed_time DESC;
```

**Missing indexes:**
```sql
SELECT TOP 20
    OBJECT_NAME(mid.object_id) AS TableName,
    mid.equality_columns,
    mid.inequality_columns,
    migs.user_seeks,
    migs.avg_user_impact
FROM sys.dm_db_missing_index_details mid
JOIN sys.dm_db_missing_index_groups mig ON mid.index_handle = mig.index_handle
JOIN sys.dm_db_missing_index_group_stats migs ON mig.index_group_handle = migs.group_handle
ORDER BY migs.user_seeks * migs.avg_user_impact DESC;
```

---

## TEST PROMPTS (Validate Coverage)

Use these to verify the skill works:

1. **Finance:** "Voucher INT-123456 exists but amount is wrong"
2. **SCM:** "Sales order SO-001234 invoice missing 3 lines"
3. **WMS:** "Work ID 5678 created but stuck, not releasing"
4. **Batch:** "Vendor invoice posting batch didn't run last night"
5. **Security:** "User JSMITH can't see Post button on vendor invoice"
6. **Integration:** "DMF import shows success but no purchase orders created"

---

## KEY PRINCIPLE

Don't debug blind. **ROUTE -> SCHEMA -> PLATINUM -> DIAMOND -> PIVOT.**

The symptom tells you WHERE to look. The working example tells you WHAT's wrong.
