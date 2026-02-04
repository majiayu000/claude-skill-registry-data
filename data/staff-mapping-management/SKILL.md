---
name: staff-mapping-management
description: Manage staff-institution mapping table for vehicle insurance platform. Use when updating mapping files, resolving name conflicts, converting Excel to JSON, or checking mapping coverage. Mentions "update mapping", "staff conflicts", "mapping table", or "institution assignment".
allowed-tools: Read, Edit, Grep, Glob
---

# Staff Mapping Management

Manage business staff-to-institution mapping table, handle conflicts, and track versions.

## When to Activate

Use this skill when the user:
- Says "update the mapping table" or "refresh mapping"
- Mentions "staff conflicts", "name conflicts", or "duplicate names"
- Asks "convert mapping Excel to JSON"
- Wants to "check mapping coverage" or "find unmapped staff"
- Needs to "resolve institution assignment conflicts"

## Quick Start Workflow

```
Step 1: Convert Excel → JSON
  ↓
Step 2: Validate & Detect Conflicts
  ↓
Step 3: Update System Mapping
  ↓
Step 4: Verify Coverage
```

---

## Step 1: Convert Mapping Excel to JSON

### 1.1 Expected Excel Structure

**File**: `业务员机构团队对照表YYYYMMDD.xlsx`

| Column | Field | Example |
|--------|-------|---------|
| A | 序号 | 1, 2, 3... |
| B | 三级机构 | 达州, 德阳 |
| C | 四级机构 | 达州, 德阳 |
| D | 团队简称 | 达州业务三部 |
| E | 业务员 | 200049147向轩颉 |

### 1.2 Conversion Script

```python
import pandas as pd
import json

def convert_mapping_excel_to_json(excel_path, json_path):
    """Convert staff mapping Excel → JSON"""

    # Load Excel
    df = pd.read_excel(excel_path)

    # Validate columns
    required = ['业务员', '三级机构', '四级机构', '团队简称']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Build mapping dict
    mapping = {}
    for _, row in df.iterrows():
        staff_key = str(row['业务员'])
        mapping[staff_key] = {
            '三级机构': str(row['三级机构']),
            '四级机构': str(row['四级机构']),
            '团队简称': str(row['团队简称']) if pd.notna(row['团队简称']) else None
        }

    # Save JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"✅ Converted {len(mapping)} records")
    return mapping
```

---

## Step 2: Validate & Detect Conflicts

### 2.1 Conflict Types

| Conflict Type | Description | Example |
|--------------|-------------|---------|
| Name Conflict | Same name, different institutions | 张三 → 达州 vs 张三 → 德阳 |
| Missing Info | Staff without institution | 李四 → null |
| Duplicate Key | Same staff ID appears twice | 200012345 appears 2x |

### 2.2 Conflict Detection

```python
def detect_conflicts(mapping):
    """Find name conflicts and data issues"""
    import re

    # Extract names from "工号+姓名" format
    name_to_records = {}
    for staff_key, info in mapping.items():
        match = re.search(r'[\u4e00-\u9fa5]+', staff_key)
        if not match:
            continue

        name = match.group()
        if name not in name_to_records:
            name_to_records[name] = []
        name_to_records[name].append({
            'key': staff_key,
            'institution': info['三级机构'],
            'team': info['团队简称']
        })

    # Find conflicts (same name, different institution)
    conflicts = []
    for name, records in name_to_records.items():
        if len(records) > 1:
            institutions = set(r['institution'] for r in records)
            if len(institutions) > 1:
                conflicts.append({
                    'name': name,
                    'records': records,
                    'type': 'name_conflict'
                })

    return conflicts
```

### 2.3 Missing Data Detection

```python
def detect_missing_data(mapping):
    """Find records with missing institution"""
    missing = []

    for staff_key, info in mapping.items():
        if not info.get('三级机构') or info['三级机构'] == 'nan':
            missing.append({
                'key': staff_key,
                'issue': 'missing_institution'
            })

    return missing
```

---

## Step 3: Update System Mapping

### 3.1 Backup Current Version

```python
from datetime import datetime
import shutil

def backup_mapping(current_path):
    """Backup current mapping before update"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'业务员机构团队归属_backup_{timestamp}.json'

    shutil.copy(current_path, backup_path)
    print(f"✅ Backed up to {backup_path}")
    return backup_path
```

### 3.2 Apply Update

```python
def update_mapping(new_mapping_path):
    """Update system mapping file"""

    # 1. Backup current
    current_path = '业务员机构团队归属.json'
    backup_mapping(current_path)

    # 2. Load new mapping
    with open(new_mapping_path, 'r', encoding='utf-8') as f:
        new_mapping = json.load(f)

    # 3. Validate
    conflicts = detect_conflicts(new_mapping)
    missing = detect_missing_data(new_mapping)

    # 4. Report issues
    if conflicts:
        print(f"⚠️  Found {len(conflicts)} name conflicts:")
        for c in conflicts[:5]:
            print(f"  - {c['name']}: {len(c['records'])} records")

    if missing:
        print(f"⚠️  Found {len(missing)} records with missing institution")

    # 5. Copy to system location
    shutil.copy(new_mapping_path, current_path)
    print(f"✅ Updated system mapping: {len(new_mapping)} records")

    return {'conflicts': conflicts, 'missing': missing}
```

---

## Step 4: Verify Mapping Coverage

### 4.1 Check Against Data

```python
def verify_mapping_coverage(data_df, mapping):
    """Check how many staff in data are covered by mapping"""
    import re

    # Build name lookup
    name_to_info = {}
    for staff_key, info in mapping.items():
        match = re.search(r'[\u4e00-\u9fa5]+', staff_key)
        if match:
            name_to_info[match.group()] = info

    # Get staff from data
    data_staff = data_df['业务员'].unique()

    # Check coverage
    unmapped = [s for s in data_staff if s not in name_to_info]
    coverage_rate = 1.0 - (len(unmapped) / len(data_staff))

    report = {
        'total_staff_in_data': len(data_staff),
        'mapped_staff': len(data_staff) - len(unmapped),
        'unmapped_staff': unmapped[:10],  # First 10
        'unmapped_count': len(unmapped),
        'coverage_rate': coverage_rate
    }

    return report
```

### 4.2 Coverage Report

```python
def print_coverage_report(report):
    """Print human-readable coverage report"""

    coverage_pct = report['coverage_rate'] * 100

    print(f"\n📊 Mapping Coverage Report")
    print(f"=" * 50)
    print(f"Total staff in data: {report['total_staff_in_data']}")
    print(f"Mapped staff: {report['mapped_staff']}")
    print(f"Unmapped staff: {report['unmapped_count']}")
    print(f"Coverage rate: {coverage_pct:.1f}%")

    if report['unmapped_count'] > 0:
        print(f"\n⚠️  Unmapped staff (first 10):")
        for staff in report['unmapped_staff']:
            print(f"  - {staff}")
        print(f"\n💡 Action: Update mapping table to include these staff")
    else:
        print(f"\n✅ All staff are mapped!")
```

---

## Version Management

### Compare Two Mapping Versions

```python
def compare_mapping_versions(old_json, new_json):
    """Compare two mapping file versions"""

    with open(old_json, 'r', encoding='utf-8') as f:
        old_mapping = json.load(f)

    with open(new_json, 'r', encoding='utf-8') as f:
        new_mapping = json.load(f)

    old_keys = set(old_mapping.keys())
    new_keys = set(new_mapping.keys())

    # Find changes
    added = list(new_keys - old_keys)
    removed = list(old_keys - new_keys)
    changed = []

    for key in old_keys & new_keys:
        if old_mapping[key] != new_mapping[key]:
            changed.append({
                'key': key,
                'old': old_mapping[key],
                'new': new_mapping[key]
            })

    return {
        'added': added,
        'removed': removed,
        'changed': changed,
        'unchanged': len(old_keys & new_keys) - len(changed)
    }
```

---

## Common Use Cases

### Case 1: "Update mapping from new Excel file"

```python
# Full update workflow
excel_file = '业务员机构团队对照表20251109.xlsx'
json_file = '业务员机构团队归属_new.json'

# Step 1: Convert
mapping = convert_mapping_excel_to_json(excel_file, json_file)

# Step 2: Detect conflicts
conflicts = detect_conflicts(mapping)
missing = detect_missing_data(mapping)

# Step 3: Update (if acceptable)
if len(conflicts) < 5:  # Acceptable threshold
    result = update_mapping(json_file)
else:
    print(f"❌ Too many conflicts ({len(conflicts)}), manual review needed")
```

### Case 2: "Check mapping coverage"

```python
import pandas as pd
import json

# Load data and mapping
df = pd.read_csv('data.csv', encoding='utf-8-sig')
mapping = json.load(open('业务员机构团队归属.json'))

# Check coverage
report = verify_mapping_coverage(df, mapping)
print_coverage_report(report)
```

### Case 3: "Resolve name conflicts"

```python
# Find conflicts
conflicts = detect_conflicts(mapping)

# Manual resolution approach
for conflict in conflicts:
    print(f"\nConflict: {conflict['name']}")
    for i, record in enumerate(conflict['records']):
        print(f"  {i+1}. {record['key']} → {record['institution']}")

    # User selects correct record or marks both as valid
    # System updates mapping accordingly
```

---

## Troubleshooting

### "Many unmapped staff after update"

**Cause**: New mapping table is incomplete

**Solution**:
1. Check if Excel file has all staff
2. Verify Excel column names match expected
3. Compare with previous version:
   ```python
   diff = compare_mapping_versions('old.json', 'new.json')
   print(f"Removed: {len(diff['removed'])} staff")
   ```

### "Name conflicts detected"

**Options**:
1. **Accept conflicts**: Use `keep='last'` strategy (keep last record)
2. **Add ID to display**: Show "工号+姓名" instead of just name
3. **Manual resolution**: Update Excel to disambiguate

### "Conversion fails"

**Check**:
- File encoding (should be UTF-8 or GB2312)
- Column names (must match exactly)
- File format (.xlsx vs .xls)

---

## Related Files

**Current mapping**: `业务员机构团队归属.json` (229 records as of 2025-11-04)

**Data processor**: [backend/data_processor.py](../../backend/data_processor.py)
- Uses `_build_name_to_info()` method (lines 23-58)
- See `get_policy_mapping()` (lines 59-101)

**Related Skills**:
- `field-validation` - Check mapping coverage rate
- `data-cleaning-standards` - Use mapping to fill missing institutions

---

**Skill Version**: v1.0
**Created**: 2025-11-09
**File Size**: ~290 lines
**Focuses On**: Mapping management only
