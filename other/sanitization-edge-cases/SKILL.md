---
name: sanitization-edge-cases
description: 'Deep expertise in database sanitization edge cases and failure scenarios. Use for: identifying data anomalies, handling circular references, null value strategies, multi-tenant complexities, unicode issues, orphaned records, self-referencing hierarchies, trigger conflicts, deadlock prevention, and testing sanitization robustness. Covers recovery strategies and validation patterns.'
argument-hint: 'Describe the edge case or concern (e.g., handle circular FKs, test for orphaned records, deal with null values)'
---

# Database Sanitization Edge Cases Expert

Specialized knowledge for identifying, handling, and testing edge cases that commonly break database sanitization workflows.

## When to Use

- Identifying potential edge cases before sanitization
- Handling complex data relationships (circular references, hierarchies)
- Dealing with data quality issues (nulls, orphans, duplicates)
- Managing multi-tenant or multi-region databases
- Handling special characters and unicode
- Preventing and recovering from sanitization failures
- Testing sanitization robustness
- Debugging sanitization issues

## Critical Edge Cases

### 1. Circular Foreign Key References

**Problem:** Table A references B, B references C, C references A. Simple update order fails.

**Detection:**
```python
def detect_circular_references(connection_string: str) -> List[List[str]]:
    """
    Detect circular foreign key dependencies.
    
    Returns:
        List of circular dependency chains
    """
    import pyodbc
    from collections import defaultdict, deque
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Build dependency graph
    query = """
    SELECT 
        OBJECT_NAME(fk.parent_object_id) AS from_table,
        OBJECT_NAME(fk.referenced_object_id) AS to_table
    FROM sys.foreign_keys AS fk
    WHERE OBJECT_NAME(fk.parent_object_id) != OBJECT_NAME(fk.referenced_object_id)
    """
    
    cursor.execute(query)
    
    graph = defaultdict(list)
    for row in cursor.fetchall():
        graph[row.from_table].append(row.to_table)
    
    # Detect cycles using DFS
    def find_cycles(node, visited, path, cycles):
        if node in path:
            # Found cycle
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:])
            return
        
        if node in visited:
            return
        
        visited.add(node)
        path.append(node)
        
        for neighbor in graph.get(node, []):
            find_cycles(neighbor, visited, path.copy(), cycles)
    
    cycles = []
    for table in graph:
        find_cycles(table, set(), [], cycles)
    
    # Remove duplicates
    unique_cycles = []
    for cycle in cycles:
        normalized = tuple(sorted(cycle))
        if normalized not in [tuple(sorted(c)) for c in unique_cycles]:
            unique_cycles.append(cycle)
    
    conn.close()
    return unique_cycles


def handle_circular_references(
    connection_string: str,
    circular_tables: List[str],
    sanitization_fn: Callable
):
    """
    Handle circular references by temporarily disabling constraints.
    
    Strategy:
    1. Disable foreign key constraints
    2. Sanitize all tables
    3. Re-enable and validate constraints
    """
    import pyodbc
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    try:
        # Store constraint names for re-enabling
        constraints = {}
        
        for table in circular_tables:
            # Get all FK constraints on this table
            cursor.execute(f"""
                SELECT name 
                FROM sys.foreign_keys 
                WHERE parent_object_id = OBJECT_ID('{table}')
            """)
            
            constraints[table] = [row.name for row in cursor.fetchall()]
            
            # Disable constraints
            for fk_name in constraints[table]:
                cursor.execute(f"ALTER TABLE {table} NOCHECK CONSTRAINT {fk_name}")
        
        conn.commit()
        
        # Sanitize tables
        for table in circular_tables:
            sanitization_fn(table)
        
        # Re-enable and validate constraints
        for table in circular_tables:
            for fk_name in constraints[table]:
                try:
                    cursor.execute(f"ALTER TABLE {table} CHECK CONSTRAINT {fk_name}")
                except pyodbc.Error as e:
                    raise ValueError(
                        f"Constraint {fk_name} on {table} violated after sanitization: {e}"
                    )
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        # Re-enable constraints even on failure
        for table in circular_tables:
            for fk_name in constraints.get(table, []):
                try:
                    cursor.execute(f"ALTER TABLE {table} CHECK CONSTRAINT {fk_name}")
                except:
                    pass
        raise
    finally:
        conn.close()
```

### 2. Self-Referencing Tables (Hierarchies)

**Problem:** Employee table with ManagerID referencing EmployeeID. Sanitizing IDs breaks hierarchy.

**Solution:**
```python
def sanitize_self_referencing_table(
    connection_string: str,
    table: str,
    pk_column: str,
    fk_column: str,
    sanitize_fn: Callable[[int], int]
):
    """
    Sanitize self-referencing table maintaining hierarchy.
    
    Args:
        table: Table name (e.g., 'Employees')
        pk_column: Primary key column (e.g., 'EmployeeID')
        fk_column: Self-referencing FK (e.g., 'ManagerID')
        sanitize_fn: Function mapping old ID to new ID
    """
    import pyodbc
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Build ID mapping maintaining hierarchy
    cursor.execute(f"""
        SELECT {pk_column}, {fk_column}
        FROM {table}
        ORDER BY {pk_column}
    """)
    
    id_mapping = {}
    hierarchy = {}
    
    for row in cursor.fetchall():
        old_id = row[0]
        parent_id = row[1]
        
        # Generate new ID
        new_id = sanitize_fn(old_id)
        id_mapping[old_id] = new_id
        hierarchy[old_id] = parent_id
    
    # Update in topological order (parents before children)
    def get_update_order(hierarchy):
        """Sort IDs in topological order."""
        from collections import deque
        
        # Find roots (no parent or parent is null)
        roots = [id for id, parent in hierarchy.items() 
                if parent is None or parent not in hierarchy]
        
        order = []
        queue = deque(roots)
        
        while queue:
            node = queue.popleft()
            order.append(node)
            
            # Find children
            children = [id for id, parent in hierarchy.items() if parent == node]
            queue.extend(children)
        
        return order
    
    update_order = get_update_order(hierarchy)
    
    # Disable constraint temporarily
    cursor.execute(f"""
        SELECT name 
        FROM sys.foreign_keys 
        WHERE parent_object_id = OBJECT_ID('{table}')
        AND parent_object_id = referenced_object_id
    """)
    
    self_fk = cursor.fetchone()
    if self_fk:
        cursor.execute(f"ALTER TABLE {table} NOCHECK CONSTRAINT {self_fk[0]}")
    
    # Update IDs and parent references
    for old_id in update_order:
        new_id = id_mapping[old_id]
        old_parent = hierarchy[old_id]
        new_parent = id_mapping.get(old_parent) if old_parent else None
        
        cursor.execute(f"""
            UPDATE {table}
            SET {pk_column} = ?,
                {fk_column} = ?
            WHERE {pk_column} = ?
        """, (new_id, new_parent, old_id))
    
    # Re-enable constraint
    if self_fk:
        cursor.execute(f"ALTER TABLE {table} CHECK CONSTRAINT {self_fk[0]}")
    
    conn.commit()
    conn.close()
```

### 3. NULL Value Handling

**Problem:** NULL can mean "not set", "unknown", or "intentionally empty". Different handling required.

**Strategy Matrix:**
```python
from enum import Enum
from typing import Optional, Any

class NullStrategy(Enum):
    """Strategies for handling NULL values during sanitization."""
    PRESERVE = "preserve"           # Keep NULL as NULL
    MASK_AS_EXPLICIT = "mask"       # Replace with explicit value like "UNKNOWN"
    RANDOMIZE = "randomize"          # Treat as valid value to sanitize
    DELETE_ROW = "delete"            # Remove rows with NULL in critical fields
    FAIL = "fail"                    # Raise error if NULL encountered

class NullAwareColumnSanitizer:
    """Handle NULL values with configurable strategies."""
    
    def __init__(self):
        self.strategies = {}
    
    def configure(
        self, 
        table: str, 
        column: str, 
        strategy: NullStrategy,
        explicit_value: Optional[Any] = None
    ):
        """Configure how to handle NULLs for a specific column."""
        key = (table, column)
        self.strategies[key] = (strategy, explicit_value)
    
    def sanitize_value(
        self, 
        table: str, 
        column: str, 
        value: Optional[Any],
        sanitize_fn: Callable
    ) -> Optional[Any]:
        """Sanitize value respecting NULL strategy."""
        strategy, explicit_value = self.strategies.get(
            (table, column), 
            (NullStrategy.PRESERVE, None)
        )
        
        if value is None:
            if strategy == NullStrategy.PRESERVE:
                return None
            elif strategy == NullStrategy.MASK_AS_EXPLICIT:
                return explicit_value or "UNKNOWN"
            elif strategy == NullStrategy.RANDOMIZE:
                # Generate random value of appropriate type
                return sanitize_fn(explicit_value or "dummy")
            elif strategy == NullStrategy.DELETE_ROW:
                raise DeleteRowException(f"NULL in {table}.{column}")
            elif strategy == NullStrategy.FAIL:
                raise ValueError(f"Unexpected NULL in {table}.{column}")
        
        return sanitize_fn(value)

# Usage example
sanitizer = NullAwareColumnSanitizer()

# Critical field - fail if NULL
sanitizer.configure('Users', 'email', NullStrategy.FAIL)

# Optional field - preserve NULL
sanitizer.configure('Users', 'middle_name', NullStrategy.PRESERVE)

# Legacy field - convert to explicit
sanitizer.configure('Users', 'phone', NullStrategy.MASK_AS_EXPLICIT, 
                   explicit_value='000-000-0000')
```

### 4. Orphaned Records

**Problem:** Child records exist without parent records (broken FK relationships).

**Detection and Handling:**
```python
def detect_orphaned_records(connection_string: str) -> Dict[str, List[Dict]]:
    """
    Find all orphaned records in database.
    
    Returns:
        Dict mapping table names to list of orphaned record info
    """
    import pyodbc
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    orphans = {}
    
    # Get all foreign keys
    cursor.execute("""
        SELECT 
            OBJECT_NAME(fk.parent_object_id) AS child_table,
            COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS child_column,
            OBJECT_NAME(fk.referenced_object_id) AS parent_table,
            COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS parent_column
        FROM sys.foreign_keys AS fk
        INNER JOIN sys.foreign_key_columns AS fkc 
            ON fk.object_id = fkc.constraint_object_id
    """)
    
    for row in cursor.fetchall():
        child_table, child_col, parent_table, parent_col = row
        
        # Find orphaned records
        orphan_query = f"""
        SELECT COUNT(*) as orphan_count
        FROM {child_table} c
        WHERE c.{child_col} IS NOT NULL
        AND NOT EXISTS (
            SELECT 1 
            FROM {parent_table} p 
            WHERE p.{parent_col} = c.{child_col}
        )
        """
        
        cursor.execute(orphan_query)
        count = cursor.fetchone()[0]
        
        if count > 0:
            if child_table not in orphans:
                orphans[child_table] = []
            
            orphans[child_table].append({
                'child_column': child_col,
                'parent_table': parent_table,
                'parent_column': parent_col,
                'orphan_count': count
            })
    
    conn.close()
    return orphans


def handle_orphaned_records(
    connection_string: str,
    strategy: str = 'delete'  # 'delete', 'null', 'create_parent'
):
    """
    Handle orphaned records based on strategy.
    
    Strategies:
        - delete: Remove orphaned child records
        - null: Set FK to NULL (if nullable)
        - create_parent: Create placeholder parent records
    """
    import pyodbc
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    orphans = detect_orphaned_records(connection_string)
    
    for table, orphan_list in orphans.items():
        for orphan in orphan_list:
            child_col = orphan['child_column']
            parent_table = orphan['parent_table']
            parent_col = orphan['parent_column']
            
            if strategy == 'delete':
                delete_query = f"""
                DELETE FROM {table}
                WHERE {child_col} IS NOT NULL
                AND NOT EXISTS (
                    SELECT 1 FROM {parent_table} p 
                    WHERE p.{parent_col} = {table}.{child_col}
                )
                """
                cursor.execute(delete_query)
                
            elif strategy == 'null':
                null_query = f"""
                UPDATE {table}
                SET {child_col} = NULL
                WHERE {child_col} IS NOT NULL
                AND NOT EXISTS (
                    SELECT 1 FROM {parent_table} p 
                    WHERE p.{parent_col} = {table}.{child_col}
                )
                """
                cursor.execute(null_query)
                
            elif strategy == 'create_parent':
                # Get orphaned IDs
                cursor.execute(f"""
                    SELECT DISTINCT c.{child_col}
                    FROM {table} c
                    WHERE c.{child_col} IS NOT NULL
                    AND NOT EXISTS (
                        SELECT 1 FROM {parent_table} p 
                        WHERE p.{parent_col} = c.{child_col}
                    )
                """)
                
                orphaned_ids = [row[0] for row in cursor.fetchall()]
                
                # Create placeholder parent records
                for orphaned_id in orphaned_ids:
                    try:
                        insert_query = f"""
                        INSERT INTO {parent_table} ({parent_col})
                        VALUES (?)
                        """
                        cursor.execute(insert_query, (orphaned_id,))
                    except pyodbc.IntegrityError:
                        # Parent might have been created by another orphan
                        pass
    
    conn.commit()
    conn.close()
```

### 5. Unicode and Special Characters

**Problem:** Names with accents, emojis, RTL text, or special characters break sanitization.

**Robust Handling:**
```python
import unicodedata
import re
from typing import Optional

class UnicodeAwareSanitizer:
    """Handle unicode edge cases in text sanitization."""
    
    @staticmethod
    def normalize_unicode(text: str, form: str = 'NFC') -> str:
        """
        Normalize unicode to consistent form.
        
        Forms:
            NFC - Canonical composition (é as single char)
            NFD - Canonical decomposition (é as e + accent)
            NFKC - Compatibility composition
            NFKD - Compatibility decomposition
        """
        if not text:
            return text
        return unicodedata.normalize(form, text)
    
    @staticmethod
    def remove_accents(text: str) -> str:
        """Remove accents from characters (José -> Jose)."""
        if not text:
            return text
        
        # Decompose unicode
        nfd = unicodedata.normalize('NFD', text)
        
        # Remove combining characters (accents)
        without_accents = ''.join(
            char for char in nfd 
            if unicodedata.category(char) != 'Mn'
        )
        
        return unicodedata.normalize('NFC', without_accents)
    
    @staticmethod
    def detect_problematic_characters(text: str) -> List[Dict[str, Any]]:
        """
        Identify potentially problematic characters.
        
        Returns list of character info for:
        - Emojis
        - RTL marks
        - Zero-width characters
        - Control characters
        """
        if not text:
            return []
        
        problems = []
        
        for i, char in enumerate(text):
            category = unicodedata.category(char)
            
            problem = None
            
            # Emoji ranges
            if ord(char) >= 0x1F600 and ord(char) <= 0x1F64F:
                problem = 'emoji'
            # Zero-width characters
            elif char in ['\u200B', '\u200C', '\u200D', '\uFEFF']:
                problem = 'zero_width'
            # Control characters
            elif category.startswith('C'):
                problem = 'control'
            # RTL marks
            elif char in ['\u200E', '\u200F', '\u202A', '\u202B', '\u202C', '\u202D', '\u202E']:
                problem = 'rtl_mark'
            
            if problem:
                problems.append({
                    'position': i,
                    'character': char,
                    'unicode': f'U+{ord(char):04X}',
                    'category': category,
                    'type': problem,
                    'name': unicodedata.name(char, 'UNKNOWN')
                })
        
        return problems
    
    @staticmethod
    def sanitize_to_ascii_safe(text: str, replacement: str = '?') -> str:
        """
        Convert to ASCII, replacing non-ASCII characters.
        
        Useful for legacy systems that don't support unicode.
        """
        if not text:
            return text
        
        # Try to transliterate common characters
        # é -> e, ñ -> n, etc.
        normalized = UnicodeAwareSanitizer.remove_accents(text)
        
        # Replace remaining non-ASCII
        ascii_safe = ''
        for char in normalized:
            if ord(char) < 128:
                ascii_safe += char
            else:
                ascii_safe += replacement
        
        return ascii_safe
    
    @staticmethod
    def handle_mixed_script_name(name: str) -> str:
        """
        Handle names with mixed scripts (e.g., Latin + Cyrillic).
        
        Example: "Иван Smith" -> Keep or transliterate based on rules
        """
        if not name:
            return name
        
        # Detect scripts
        scripts = set()
        for char in name:
            if char.isalpha():
                script_name = unicodedata.name(char, '').split()[0]
                scripts.add(script_name)
        
        # If multiple scripts, might need special handling
        if len(scripts) > 1:
            # Log warning or apply transliteration
            pass
        
        return name

# Example usage
sanitizer = UnicodeAwareSanitizer()

# Test problematic names
test_names = [
    "José García",           # Accents
    "Hello👋World",          # Emoji
    "الاسم العربي",          # RTL text
    "Test\u200BName",        # Zero-width space
    "Café",                  # Mixed ASCII and accents
]

for name in test_names:
    print(f"Original: {name}")
    print(f"Normalized: {sanitizer.normalize_unicode(name)}")
    print(f"No accents: {sanitizer.remove_accents(name)}")
    print(f"ASCII safe: {sanitizer.sanitize_to_ascii_safe(name)}")
    print(f"Problems: {sanitizer.detect_problematic_characters(name)}")
    print("---")
```

### 6. Multi-Tenant Data

**Problem:** Database contains data for multiple customers/tenants. Must sanitize correctly.

**Tenant-Aware Sanitization:**
```python
class MultiTenantSanitizer:
    """Handle multi-tenant database sanitization."""
    
    def __init__(self, connection_string: str, tenant_column: str = 'tenant_id'):
        self.connection_string = connection_string
        self.tenant_column = tenant_column
        self.protected_tenants = set()
        self.tenant_specific_rules = {}
    
    def protect_tenant(self, tenant_id: Any):
        """Mark tenant as protected (don't sanitize)."""
        self.protected_tenants.add(tenant_id)
    
    def set_tenant_rule(
        self, 
        tenant_id: Any, 
        table: str, 
        rule: Callable
    ):
        """Set tenant-specific sanitization rule."""
        key = (tenant_id, table)
        self.tenant_specific_rules[key] = rule
    
    def sanitize_table(
        self,
        table: str,
        columns: List[str],
        default_sanitize_fn: Callable
    ):
        """Sanitize table respecting tenant boundaries."""
        import pyodbc
        
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        
        # Check if table has tenant column
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table}'
            AND COLUMN_NAME = '{self.tenant_column}'
        """)
        
        has_tenant_column = cursor.fetchone()[0] > 0
        
        if not has_tenant_column:
            raise ValueError(
                f"Table {table} doesn't have {self.tenant_column} column"
            )
        
        # Get all tenants
        cursor.execute(f"SELECT DISTINCT {self.tenant_column} FROM {table}")
        tenants = [row[0] for row in cursor.fetchall()]
        
        for tenant_id in tenants:
            # Skip protected tenants
            if tenant_id in self.protected_tenants:
                continue
            
            # Get tenant-specific rule or use default
            rule_key = (tenant_id, table)
            sanitize_fn = self.tenant_specific_rules.get(
                rule_key, 
                default_sanitize_fn
            )
            
            # Sanitize this tenant's data
            self._sanitize_tenant_data(
                table, 
                columns, 
                tenant_id, 
                sanitize_fn
            )
        
        conn.commit()
        conn.close()
    
    def _sanitize_tenant_data(
        self,
        table: str,
        columns: List[str],
        tenant_id: Any,
        sanitize_fn: Callable
    ):
        """Sanitize data for specific tenant."""
        import pyodbc
        
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        
        # Process in batches
        batch_size = 1000
        offset = 0
        
        while True:
            # Fetch batch for this tenant
            select_query = f"""
            SELECT id, {', '.join(columns)}
            FROM {table}
            WHERE {self.tenant_column} = ?
            ORDER BY id
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
            """
            
            cursor.execute(select_query, (tenant_id, offset, batch_size))
            rows = cursor.fetchall()
            
            if not rows:
                break
            
            # Sanitize and update
            for row in rows:
                row_id = row[0]
                values = row[1:]
                
                sanitized = sanitize_fn(dict(zip(columns, values)))
                
                update_query = f"""
                UPDATE {table}
                SET {', '.join([f'{col} = ?' for col in columns])}
                WHERE id = ? AND {self.tenant_column} = ?
                """
                
                update_values = [sanitized[col] for col in columns] + [row_id, tenant_id]
                cursor.execute(update_query, update_values)
            
            conn.commit()
            offset += batch_size
        
        conn.close()

# Usage
sanitizer = MultiTenantSanitizer(conn_str, tenant_column='organization_id')

# Protect production tenant
sanitizer.protect_tenant('PROD-TENANT-001')

# Different rules for different tenants
sanitizer.set_tenant_rule(
    'TEST-TENANT-001',
    'Users',
    lambda row: {'email': 'test@example.com'}  # Simple masking for test tenant
)

sanitizer.set_tenant_rule(
    'DEMO-TENANT-001',
    'Users',
    lambda row: generate_realistic_demo_data(row)  # Realistic data for demos
)
```

### 7. Composite Keys

**Problem:** Table has multi-column primary key. Sanitizing one column breaks references.

**Solution:**
```python
def sanitize_composite_key_table(
    connection_string: str,
    table: str,
    key_columns: List[str],
    sanitize_columns: List[str],
    sanitize_fn: Callable
):
    """
    Sanitize table with composite primary key.
    
    Args:
        table: Table name
        key_columns: Columns that form composite key
        sanitize_columns: Subset of key_columns to sanitize
        sanitize_fn: Function to sanitize key values
    """
    import pyodbc
    
    if not set(sanitize_columns).issubset(set(key_columns)):
        raise ValueError("sanitize_columns must be subset of key_columns")
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Build mapping of old -> new composite keys
    select_query = f"SELECT {', '.join(key_columns)} FROM {table}"
    cursor.execute(select_query)
    
    mappings = {}
    for row in cursor.fetchall():
        old_key = tuple(row)
        
        # Sanitize specified columns
        new_key_list = []
        for i, col in enumerate(key_columns):
            if col in sanitize_columns:
                new_key_list.append(sanitize_fn(row[i], col))
            else:
                new_key_list.append(row[i])
        
        new_key = tuple(new_key_list)
        mappings[old_key] = new_key
    
    # Find all tables referencing this composite key
    dependent_tables = find_composite_key_references(
        connection_string, table, key_columns
    )
    
    # Update in reverse dependency order
    for old_key, new_key in mappings.items():
        # Update dependent tables first
        for dep_table, dep_columns in dependent_tables:
            where_clause = ' AND '.join([
                f"{dep_col} = ?" for dep_col in dep_columns
            ])
            set_clause = ', '.join([
                f"{dep_col} = ?" for dep_col in dep_columns
            ])
            
            update_query = f"""
            UPDATE {dep_table}
            SET {set_clause}
            WHERE {where_clause}
            """
            
            cursor.execute(update_query, list(new_key) + list(old_key))
        
        # Update main table
        where_clause = ' AND '.join([f"{col} = ?" for col in key_columns])
        set_clause = ', '.join([f"{col} = ?" for col in key_columns])
        
        update_query = f"""
        UPDATE {table}
        SET {set_clause}
        WHERE {where_clause}
        """
        
        cursor.execute(update_query, list(new_key) + list(old_key))
    
    conn.commit()
    conn.close()
```

### 8. Triggers and Computed Columns

**Problem:** Triggers fire on UPDATE, potentially logging original values or preventing updates.

**Detection and Handling:**
```python
def detect_triggers(connection_string: str, table: str) -> List[Dict]:
    """Detect all triggers on a table."""
    import pyodbc
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    query = """
    SELECT 
        tr.name AS trigger_name,
        tr.is_disabled,
        OBJECT_DEFINITION(tr.object_id) AS trigger_definition
    FROM sys.triggers tr
    WHERE tr.parent_id = OBJECT_ID(?)
    """
    
    cursor.execute(query, (table,))
    
    triggers = []
    for row in cursor.fetchall():
        triggers.append({
            'name': row.trigger_name,
            'disabled': row.is_disabled,
            'definition': row.trigger_definition
        })
    
    conn.close()
    return triggers


def sanitize_with_trigger_management(
    connection_string: str,
    table: str,
    sanitize_fn: Callable,
    disable_triggers: bool = True
):
    """
    Sanitize table managing triggers appropriately.
    
    Args:
        disable_triggers: If True, disable triggers during sanitization
    """
    import pyodbc
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    triggers = detect_triggers(connection_string, table)
    
    try:
        if disable_triggers:
            # Disable all triggers
            for trigger in triggers:
                if not trigger['disabled']:
                    cursor.execute(f"DISABLE TRIGGER {trigger['name']} ON {table}")
            conn.commit()
        
        # Perform sanitization
        sanitize_fn()
        
    finally:
        if disable_triggers:
            # Re-enable triggers
            for trigger in triggers:
                if not trigger['disabled']:
                    cursor.execute(f"ENABLE TRIGGER {trigger['name']} ON {table}")
            conn.commit()
        
        conn.close()


def detect_computed_columns(connection_string: str, table: str) -> List[str]:
    """
    Detect computed columns that might affect sanitization.
    
    Computed columns can't be directly updated.
    """
    import pyodbc
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    query = """
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = ?
    AND COLUMNPROPERTY(OBJECT_ID(TABLE_SCHEMA + '.' + TABLE_NAME), 
                       COLUMN_NAME, 'IsComputed') = 1
    """
    
    cursor.execute(query, (table,))
    
    computed = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return computed
```

### 9. Large Binary/Text Columns

**Problem:** BLOB columns (images, documents) too large for in-memory processing.

**Streaming Approach:**
```python
def sanitize_large_blob_column(
    connection_string: str,
    table: str,
    blob_column: str,
    pk_column: str,
    sanitize_fn: Callable[[bytes], bytes]
):
    """
    Sanitize BLOB column using streaming to avoid memory issues.
    
    Args:
        sanitize_fn: Function that processes blob data in chunks
    """
    import pyodbc
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Get all primary keys
    cursor.execute(f"SELECT {pk_column} FROM {table} WHERE {blob_column} IS NOT NULL")
    pks = [row[0] for row in cursor.fetchall()]
    
    for pk in pks:
        # Read blob in chunks
        cursor.execute(f"""
            SELECT {blob_column}.PathName(), 
                   GET_FILESTREAM_TRANSACTION_CONTEXT()
            FROM {table}
            WHERE {pk_column} = ?
        """, (pk,))
        
        # Alternative for non-FILESTREAM columns
        cursor.execute(f"""
            SELECT {blob_column}
            FROM {table}
            WHERE {pk_column} = ?
        """, (pk,))
        
        blob_data = cursor.fetchone()[0]
        
        if blob_data:
            # Option 1: Replace with placeholder
            placeholder = b'SANITIZED_CONTENT'
            
            # Option 2: Apply sanitization function
            # For very large blobs, process in chunks
            sanitized = sanitize_fn(blob_data)
            
            # Update
            cursor.execute(f"""
                UPDATE {table}
                SET {blob_column} = ?
                WHERE {pk_column} = ?
            """, (sanitized, pk))
    
    conn.commit()
    conn.close()

# Common BLOB sanitization strategies
def sanitize_image_blob(blob_data: bytes) -> bytes:
    """Replace image with generic placeholder."""
    # Return 1x1 pixel image or generic placeholder
    return b'\x89PNG\r\n\x1a\n...'  # Minimal PNG header

def sanitize_document_blob(blob_data: bytes) -> bytes:
    """Replace document with placeholder."""
    return b'Content has been sanitized for privacy'

def null_blob(blob_data: bytes) -> bytes:
    """Remove blob entirely."""
    return None
```

### 10. Transaction Boundary Issues

**Problem:** Large sanitization operation locks tables for too long or fills transaction log.

**Chunked Transaction Strategy:**
```python
class ChunkedTransactionSanitizer:
    """Sanitize in small transactions to avoid log填充."""
    
    def __init__(
        self,
        connection_string: str,
        chunk_size: int = 1000,
        checkpoint_interval: int = 10000
    ):
        self.connection_string = connection_string
        self.chunk_size = chunk_size
        self.checkpoint_interval = checkpoint_interval
    
    def sanitize_with_chunked_transactions(
        self,
        table: str,
        pk_column: str,
        sanitize_fn: Callable
    ):
        """
        Sanitize table in small transaction chunks.
        
        Benefits:
        - Prevents transaction log growth
        - Allows other transactions to proceed
        - Enables incremental progress tracking
        - Supports pause/resume
        """
        import pyodbc
        
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        total = cursor.fetchone()[0]
        
        processed = 0
        offset = 0
        
        while offset < total:
            # Begin new transaction for this chunk
            batch_query = f"""
            SELECT {pk_column}
            FROM {table}
            ORDER BY {pk_column}
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
            """
            
            cursor.execute(batch_query, (offset, self.chunk_size))
            chunk_pks = [row[0] for row in cursor.fetchall()]
            
            if not chunk_pks:
                break
            
            # Sanitize chunk
            for pk in chunk_pks:
                sanitize_fn(pk)
                processed += 1
            
            # Commit this chunk
            conn.commit()
            
            # Checkpoint
            if processed % self.checkpoint_interval == 0:
                self._save_checkpoint(table, processed, total)
                print(f"Progress: {processed}/{total} ({processed/total*100:.1f}%)")
            
            offset += self.chunk_size
            
            # Small delay to allow other transactions
            import time
            time.sleep(0.01)
        
        conn.close()
        
        return processed
    
    def _save_checkpoint(self, table: str, processed: int, total: int):
        """Save progress checkpoint for recovery."""
        checkpoint_file = f".sanitization_checkpoint_{table}.json"
        
        import json
        from datetime import datetime
        
        checkpoint = {
            'table': table,
            'processed': processed,
            'total': total,
            'timestamp': datetime.now().isoformat(),
            'percentage': processed / total * 100
        }
        
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)
```

## Testing Edge Cases

### Comprehensive Test Suite

```python
import unittest
from typing import Callable

class SanitizationEdgeCaseTests(unittest.TestCase):
    """Test suite for sanitization edge cases."""
    
    def setUp(self):
        """Set up test database with edge case data."""
        self.test_db = self._create_test_database()
        self._load_edge_case_data()
    
    def test_circular_references(self):
        """Test handling of circular FK references."""
        # Create A -> B -> C -> A cycle
        pass
    
    def test_self_referencing_tree(self):
        """Test employee hierarchy sanitization."""
        # Create 3-level hierarchy
        # Verify parent-child relationships preserved
        pass
    
    def test_null_value_strategies(self):
        """Test each NULL handling strategy."""
        pass
    
    def test_orphaned_records_detection(self):
        """Test orphaned record detection."""
        # Create orphaned child record
        # Verify detection
        pass
    
    def test_unicode_edge_cases(self):
        """Test various unicode scenarios."""
        test_cases = [
            "José García",           # Accents
            "Hello👋World",          # Emoji
            "Test\u200BHidden",     # Zero-width
            "Иван Smith",            # Mixed scripts
            "عربى",                  # RTL
        ]
        
        for name in test_cases:
            sanitized = self.sanitizer.sanitize_name(name)
            # Verify no data loss or corruption
            self.assertIsNotNone(sanitized)
    
    def test_composite_key_update(self):
        """Test sanitizing tables with composite keys."""
        pass
    
    def test_trigger_interference(self):
        """Test sanitization with active triggers."""
        pass
    
    def test_transaction_rollback(self):
        """Test rollback on sanitization failure."""
        pass
    
    def test_multi_tenant_isolation(self):
        """Verify tenant data doesn't leak."""
        pass

# Edge case data generator
def generate_edge_case_test_data():
    """Generate comprehensive edge case test data."""
    return {
        'normal_users': [...],
        'users_with_nulls': [...],
        'users_with_unicode': [...],
        'orphaned_records': [...],
        'circular_refs': [...],
        'very_long_text': '...' * 10000,
    }
```

## Edge Case Checklist

Before sanitizing any database, verify:

- [ ] **Circular references detected and handled**
- [ ] **Self-referencing tables use special logic**
- [ ] **NULL handling strategy defined for each column**
- [ ] **Orphaned records identified (delete or keep?)**
- [ ] **Unicode/special characters tested**
- [ ] **Multi-tenant data properly isolated**
- [ ] **Composite keys handled correctly**
- [ ] **Triggers disabled or managed**
- [ ] **Computed columns excluded from updates**
- [ ] **Large BLOBs handled with streaming**
- [ ] **Transaction size appropriate**
- [ ] **Protected accounts/data excluded**
- [ ] **Test data already in DB identified**
- [ ] **Soft-deleted records handled**
- [ ] **Historical/archived data strategy defined**

## Recovery Strategies

### Rollback After Partial Failure

```python
def sanitize_with_rollback_points(
    connection_string: str,
    tables: List[str],
    sanitize_fns: Dict[str, Callable]
):
    """
    Sanitize with ability to rollback to last successful table.
    """
    import pyodbc
    
    completed_tables = []
    
    try:
        for table in tables:
            # Create savepoint
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()
            
            savepoint = f"BEFORE_{table}"
            cursor.execute(f"SAVE TRANSACTION {savepoint}")
            
            try:
                # Sanitize this table
                sanitize_fns[table]()
                conn.commit()
                completed_tables.append(table)
                
            except Exception as e:
                # Rollback just this table
                cursor.execute(f"ROLLBACK TRANSACTION {savepoint}")
                raise SanitizationError(
                    f"Failed on table {table}: {e}",
                    completed_tables=completed_tables
                )
            finally:
                conn.close()
                
    except SanitizationError as e:
        print(f"Successfully completed: {e.completed_tables}")
        print(f"Failed on: {tables[len(e.completed_tables)]}")
        raise
```

## Output Guidelines

When handling sanitization edge cases:

1. **Detect early** - Run validation before sanitization
2. **Document assumptions** - Log why certain edge cases are handled specific ways
3. **Provide options** - Allow configuration for different edge case strategies
4. **Test thoroughly** - Create specific tests for each edge case category
5. **Log everything** - Track which edge cases were encountered
6. **Fail safely** - Rollback on unexpected edge cases rather than corrupt data
7. **Validate results** - Check data integrity after handling edge cases
8. **Plan for scale** - Consider edge case frequency in large databases

## Common Mistakes

❌ **Ignoring circular dependencies** - Leads to constraint violations  
❌ **Not testing unicode** - Breaks on real-world international data  
❌ **Assuming no NULLs** - Crashes or produces incorrect results  
❌ **Forgetting orphaned data** - Creates invalid FK references  
❌ **Not checking triggers** - Triggers log original data defeating sanitization  
❌ **One-size-fits-all approach** - Different tenants need different rules  
❌ **Ignoring transaction size** - Fills transaction log or locks tables  
❌ **No rollback strategy** - Can't recover from partial failures
