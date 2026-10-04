---
name: db-sanitization
description: 'Expert in writing database sanitization logic in Python for anonymizing, masking, and cleaning sensitive data. Use for: PII removal, data masking strategies, sanitization workflows, ETL pipelines, data validation, referential integrity preservation, and compliance (GDPR, HIPAA). Covers SQL Server integration, batch processing, and rollback safety.'
argument-hint: 'Describe sanitization task (e.g., mask email addresses, anonymize users, create sanitization script)'
---

# Database Sanitization Expert

Specialized guidance for writing robust database sanitization logic in Python, focusing on anonymizing sensitive data while preserving referential integrity and data utility.

## When to Use

- Writing data anonymization/masking scripts
- Sanitizing databases for non-production environments
- Removing or obfuscating PII (Personally Identifiable Information)
- Creating reproducible sanitization pipelines
- Ensuring GDPR/HIPAA compliance in test data
- Preserving referential integrity during sanitization
- Validating sanitized data quality
- Implementing reversible or deterministic masking

## Core Principles

### 1. Data Classification

Before sanitizing, identify data sensitivity:

**High Sensitivity (Must Sanitize):**
- Personal names, email addresses, phone numbers
- Social security numbers, passport numbers
- Credit card numbers, bank account details
- Medical records, health information
- IP addresses, location data
- Authentication credentials (passwords, tokens)

**Medium Sensitivity (Contextual):**
- Order history, purchase data
- User preferences and settings
- Non-critical timestamps
- Internal IDs that could be correlated

**Low Sensitivity (Preserve):**
- Product catalogs, reference data
- System configuration
- Statistical aggregates
- Public information

### 2. Sanitization Architecture

**Modular Pipeline Structure:**
```python
from dataclasses import dataclass
from typing import List, Callable, Dict, Any
from abc import ABC, abstractmethod

class SanitizationRule(ABC):
    """Base class for sanitization rules."""
    
    @abstractmethod
    def apply(self, value: Any) -> Any:
        """Apply sanitization to a value."""
        pass
    
    @abstractmethod
    def validate(self, original: Any, sanitized: Any) -> bool:
        """Validate sanitized value maintains required properties."""
        pass

class SanitizationPipeline:
    """Orchestrate database sanitization workflow."""
    
    def __init__(self, connection_string: str, dry_run: bool = True):
        self.connection_string = connection_string
        self.dry_run = dry_run
        self.rules: Dict[str, Dict[str, SanitizationRule]] = {}
        self.audit_log = []
    
    def register_rule(
        self, 
        table: str, 
        column: str, 
        rule: SanitizationRule
    ):
        """Register sanitization rule for table.column."""
        if table not in self.rules:
            self.rules[table] = {}
        self.rules[table][column] = rule
    
    def execute(self) -> Dict[str, Any]:
        """Execute sanitization pipeline with safety checks."""
        try:
            self._validate_preconditions()
            self._backup_data()
            
            for table, columns in self.rules.items():
                self._sanitize_table(table, columns)
            
            self._validate_referential_integrity()
            self._generate_report()
            
            if not self.dry_run:
                self._commit_changes()
            else:
                self._rollback_changes()
                
            return self._get_summary()
            
        except Exception as e:
            self._rollback_changes()
            self._log_error(e)
            raise
    
    def _validate_preconditions(self):
        """Ensure database is in valid state for sanitization."""
        pass
    
    def _backup_data(self):
        """Create backup before sanitization."""
        pass
    
    def _sanitize_table(self, table: str, columns: Dict[str, SanitizationRule]):
        """Apply sanitization rules to table."""
        pass
    
    def _validate_referential_integrity(self):
        """Ensure foreign key constraints still valid."""
        pass
```

### 3. Masking Strategies

**Email Masking:**
```python
import hashlib
import random
from typing import Optional

class EmailMasker:
    """Mask email addresses while preserving format and domain diversity."""
    
    def __init__(self, deterministic: bool = True):
        self.deterministic = deterministic
        self.domains = ['example.com', 'test.com', 'sample.org']
        self._cache = {}
    
    def mask(self, email: str) -> str:
        """
        Mask email address.
        
        Examples:
            john.doe@gmail.com -> user_a1b2c3d4@example.com
        """
        if not email or '@' not in email:
            return email
        
        if self.deterministic and email in self._cache:
            return self._cache[email]
        
        local, domain = email.split('@', 1)
        
        # Generate consistent hash for deterministic mode
        if self.deterministic:
            hash_val = hashlib.sha256(email.encode()).hexdigest()[:8]
            masked_local = f"user_{hash_val}"
        else:
            masked_local = f"user_{random.randint(10000, 99999)}"
        
        masked_domain = random.choice(self.domains)
        masked = f"{masked_local}@{masked_domain}"
        
        if self.deterministic:
            self._cache[email] = masked
        
        return masked
    
    def mask_partial(self, email: str) -> str:
        """
        Partially mask email for debugging.
        
        Examples:
            john.doe@gmail.com -> j***@g*****.com
        """
        if not email or '@' not in email:
            return email
        
        local, domain = email.split('@', 1)
        domain_parts = domain.split('.')
        
        masked_local = local[0] + '***' if len(local) > 0 else '***'
        masked_domain_name = domain_parts[0][0] + '*' * (len(domain_parts[0]) - 1)
        masked_domain = f"{masked_domain_name}.{'.'.join(domain_parts[1:])}"
        
        return f"{masked_local}@{masked_domain}"
```

**Name Masking:**
```python
import random
from typing import List, Optional

class NameMasker:
    """Generate realistic fake names while preserving demographic patterns."""
    
    def __init__(self, seed: Optional[int] = None):
        if seed:
            random.seed(seed)
        
        self.first_names = [
            'Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey',
            'Riley', 'Jamie', 'Quinn', 'Avery', 'Cameron'
        ]
        self.last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones',
            'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'
        ]
        self._cache = {}
    
    def mask(self, name: str, deterministic: bool = True) -> str:
        """
        Generate fake name.
        
        Args:
            name: Original name
            deterministic: If True, same input always returns same output
        """
        if not name:
            return name
        
        if deterministic and name in self._cache:
            return self._cache[name]
        
        # Use hash to deterministically select names
        if deterministic:
            hash_val = hash(name)
            first = self.first_names[hash_val % len(self.first_names)]
            last = self.last_names[(hash_val // 100) % len(self.last_names)]
        else:
            first = random.choice(self.first_names)
            last = random.choice(self.last_names)
        
        fake_name = f"{first} {last}"
        
        if deterministic:
            self._cache[name] = fake_name
        
        return fake_name
    
    def preserve_initials(self, name: str) -> str:
        """
        Mask name while preserving initials.
        
        Examples:
            John Doe -> James Davis
        """
        if not name:
            return name
        
        parts = name.split()
        masked_parts = []
        
        for part in parts:
            initial = part[0].upper()
            matching = [n for n in self.first_names + self.last_names 
                       if n[0].upper() == initial]
            
            if matching:
                masked_parts.append(random.choice(matching))
            else:
                masked_parts.append(part)
        
        return ' '.join(masked_parts)
```

**Phone Number Masking:**
```python
import re
from typing import Optional

class PhoneMasker:
    """Mask phone numbers while preserving format and country code."""
    
    def mask(self, phone: str) -> str:
        """
        Mask phone number digits while keeping format.
        
        Examples:
            +1-555-123-4567 -> +1-555-XXX-XXXX
            (555) 123-4567 -> (555) XXX-XXXX
        """
        if not phone:
            return phone
        
        # Extract format/separators
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) == 0:
            return phone
        
        # Keep country code and area code, mask rest
        if len(digits) <= 3:
            masked_digits = 'X' * len(digits)
        elif len(digits) <= 6:
            masked_digits = digits[:3] + 'X' * (len(digits) - 3)
        else:
            # Keep first 6 digits (country + area), mask rest
            kept = min(6, len(digits) - 4)
            masked_digits = digits[:kept] + 'X' * (len(digits) - kept)
        
        # Reconstruct with original format
        result = phone
        digit_idx = 0
        for i, char in enumerate(phone):
            if char.isdigit():
                if digit_idx < len(masked_digits):
                    result = result[:i] + masked_digits[digit_idx] + result[i+1:]
                digit_idx += 1
        
        return result
    
    def generate_fake(self, preserve_area_code: bool = True) -> str:
        """Generate fake phone number with realistic format."""
        import random
        
        area = random.randint(200, 999)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        
        return f"({area}) {exchange}-{number}"
```

**Credit Card Masking:**
```python
class CreditCardMasker:
    """Mask credit card numbers while preserving validation properties."""
    
    def mask(self, card_number: str) -> str:
        """
        Mask credit card showing only last 4 digits.
        
        Examples:
            4532-1234-5678-9010 -> XXXX-XXXX-XXXX-9010
        """
        if not card_number:
            return card_number
        
        # Remove non-digits
        digits_only = re.sub(r'\D', '', card_number)
        
        if len(digits_only) < 4:
            return 'X' * len(card_number)
        
        # Keep last 4 digits
        masked_digits = 'X' * (len(digits_only) - 4) + digits_only[-4:]
        
        # Restore original format
        result = card_number
        digit_idx = 0
        for i, char in enumerate(card_number):
            if char.isdigit():
                if digit_idx < len(masked_digits):
                    result = result[:i] + masked_digits[digit_idx] + result[i+1:]
                digit_idx += 1
        
        return result
    
    def generate_test_card(self) -> str:
        """Generate valid test credit card number (Luhn algorithm)."""
        # Use test card prefixes that won't validate on real systems
        prefix = '4111111111111'  # Test Visa prefix
        
        # Calculate Luhn checksum
        def luhn_checksum(card_number):
            def digits_of(n):
                return [int(d) for d in str(n)]
            
            digits = digits_of(card_number)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            
            for d in even_digits:
                checksum += sum(digits_of(d * 2))
            
            return checksum % 10
        
        check_digit = (10 - luhn_checksum(prefix + '0')) % 10
        return prefix + str(check_digit)
```

### 4. Referential Integrity Preservation

**Foreign Key Aware Sanitization:**
```python
from typing import Dict, List, Set
import pyodbc

class IntegrityPreservingSanitizer:
    """Sanitize data while maintaining referential integrity."""
    
    def __init__(self, connection_string: str):
        self.conn = pyodbc.connect(connection_string)
        self.fk_relationships = self._discover_foreign_keys()
    
    def _discover_foreign_keys(self) -> Dict[str, List[Dict]]:
        """
        Discover all foreign key relationships in database.
        
        Returns:
            Dict mapping table names to their FK constraints
        """
        query = """
        SELECT 
            fk.name AS fk_name,
            tp.name AS parent_table,
            cp.name AS parent_column,
            tr.name AS referenced_table,
            cr.name AS referenced_column
        FROM sys.foreign_keys AS fk
        INNER JOIN sys.foreign_key_columns AS fkc 
            ON fk.object_id = fkc.constraint_object_id
        INNER JOIN sys.tables AS tp 
            ON fkc.parent_object_id = tp.object_id
        INNER JOIN sys.columns AS cp 
            ON fkc.parent_object_id = cp.object_id 
            AND fkc.parent_column_id = cp.column_id
        INNER JOIN sys.tables AS tr 
            ON fkc.referenced_object_id = tr.object_id
        INNER JOIN sys.columns AS cr 
            ON fkc.referenced_object_id = cr.object_id 
            AND fkc.referenced_column_id = cr.column_id
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        
        relationships = {}
        for row in cursor.fetchall():
            table = row.parent_table
            if table not in relationships:
                relationships[table] = []
            
            relationships[table].append({
                'fk_name': row.fk_name,
                'column': row.parent_column,
                'ref_table': row.referenced_table,
                'ref_column': row.referenced_column
            })
        
        return relationships
    
    def sanitize_with_fk_consistency(
        self, 
        table: str, 
        pk_column: str,
        mapping: Dict[Any, Any]
    ):
        """
        Apply ID mapping while updating all FK references.
        
        Args:
            table: Table containing primary keys to remap
            pk_column: Primary key column name
            mapping: Dict of old_id -> new_id mappings
        """
        cursor = self.conn.cursor()
        
        # Update the primary key values
        for old_id, new_id in mapping.items():
            update_query = f"""
            UPDATE {table}
            SET {pk_column} = ?
            WHERE {pk_column} = ?
            """
            cursor.execute(update_query, (new_id, old_id))
        
        # Update all foreign key references
        for child_table, fks in self.fk_relationships.items():
            for fk in fks:
                if fk['ref_table'] == table and fk['ref_column'] == pk_column:
                    for old_id, new_id in mapping.items():
                        fk_update = f"""
                        UPDATE {child_table}
                        SET {fk['column']} = ?
                        WHERE {fk['column']} = ?
                        """
                        cursor.execute(fk_update, (new_id, old_id))
        
        self.conn.commit()
```

### 5. Batch Processing for Large Datasets

**Memory-Efficient Processing:**
```python
from typing import Iterator, Callable
import pyodbc

class BatchSanitizer:
    """Process large tables in batches to avoid memory issues."""
    
    def __init__(self, connection_string: str, batch_size: int = 1000):
        self.connection_string = connection_string
        self.batch_size = batch_size
    
    def process_table_in_batches(
        self,
        table: str,
        columns: List[str],
        sanitize_fn: Callable[[Dict], Dict],
        pk_column: str = 'id'
    ) -> int:
        """
        Process table in batches applying sanitization function.
        
        Args:
            table: Table name
            columns: Columns to sanitize
            sanitize_fn: Function that takes row dict and returns sanitized dict
            pk_column: Primary key column for batch tracking
        
        Returns:
            Total number of rows processed
        """
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        total_rows = cursor.fetchone()[0]
        
        processed = 0
        offset = 0
        
        while offset < total_rows:
            # Fetch batch
            select_query = f"""
            SELECT {pk_column}, {', '.join(columns)}
            FROM {table}
            ORDER BY {pk_column}
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
            """
            
            cursor.execute(select_query, (offset, self.batch_size))
            rows = cursor.fetchall()
            
            if not rows:
                break
            
            # Sanitize batch
            updates = []
            for row in rows:
                row_dict = dict(zip([pk_column] + columns, row))
                pk_value = row_dict[pk_column]
                
                sanitized = sanitize_fn(row_dict)
                updates.append((pk_value, sanitized))
            
            # Apply updates
            for pk_value, sanitized in updates:
                set_clause = ', '.join([f"{col} = ?" for col in columns])
                update_query = f"""
                UPDATE {table}
                SET {set_clause}
                WHERE {pk_column} = ?
                """
                
                values = [sanitized[col] for col in columns] + [pk_value]
                cursor.execute(update_query, values)
            
            conn.commit()
            processed += len(rows)
            offset += self.batch_size
            
            # Progress logging
            print(f"Processed {processed}/{total_rows} rows ({processed/total_rows*100:.1f}%)")
        
        conn.close()
        return processed
```

### 6. Validation and Quality Checks

**Post-Sanitization Validation:**
```python
class SanitizationValidator:
    """Validate sanitized data meets quality requirements."""
    
    def __init__(self, connection_string: str):
        self.conn = pyodbc.connect(connection_string)
        self.violations = []
    
    def validate_no_pii_leakage(self, table: str, columns: List[str], 
                                 pii_patterns: List[str]) -> bool:
        """
        Check that no PII patterns remain in sanitized columns.
        
        Args:
            table: Table to validate
            columns: Columns that should be sanitized
            pii_patterns: Regex patterns to detect PII
        
        Returns:
            True if no PII found, False otherwise
        """
        import re
        
        cursor = self.conn.cursor()
        
        for column in columns:
            query = f"SELECT {column} FROM {table} WHERE {column} IS NOT NULL"
            cursor.execute(query)
            
            for row in cursor.fetchall():
                value = str(row[0])
                
                for pattern in pii_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        self.violations.append({
                            'table': table,
                            'column': column,
                            'pattern': pattern,
                            'value': value[:50]  # Truncate for logging
                        })
        
        return len(self.violations) == 0
    
    def validate_referential_integrity(self) -> bool:
        """Verify all foreign key constraints are still valid."""
        cursor = self.conn.cursor()
        
        # Check for FK violations
        query = """
        SELECT 
            fk.name AS fk_name,
            OBJECT_NAME(fk.parent_object_id) AS parent_table
        FROM sys.foreign_keys AS fk
        """
        
        cursor.execute(query)
        
        for row in cursor.fetchall():
            fk_name = row.fk_name
            parent_table = row.parent_table
            
            # Try to enable the constraint (will fail if violations exist)
            try:
                cursor.execute(f"ALTER TABLE {parent_table} CHECK CONSTRAINT {fk_name}")
            except pyodbc.Error as e:
                self.violations.append({
                    'type': 'fk_violation',
                    'constraint': fk_name,
                    'table': parent_table,
                    'error': str(e)
                })
                return False
        
        return True
    
    def validate_data_distribution(
        self, 
        table: str, 
        column: str,
        expected_unique_ratio: float = 0.8
    ) -> bool:
        """
        Verify sanitized data maintains reasonable distribution.
        
        Ensures we haven't collapsed too many values to the same sanitized value.
        """
        cursor = self.conn.cursor()
        
        # Get total and unique counts
        cursor.execute(f"SELECT COUNT(*), COUNT(DISTINCT {column}) FROM {table}")
        total, unique = cursor.fetchone()
        
        if total == 0:
            return True
        
        unique_ratio = unique / total
        
        if unique_ratio < expected_unique_ratio:
            self.violations.append({
                'type': 'distribution_anomaly',
                'table': table,
                'column': column,
                'unique_ratio': unique_ratio,
                'expected': expected_unique_ratio
            })
            return False
        
        return True
```

### 7. Complete Sanitization Script Template

**Production-Ready Script:**
```python
#!/usr/bin/env python3
"""
Database Sanitization Script

Sanitizes sensitive data in database for non-production environments.
"""

import argparse
import logging
import pyodbc
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'sanitization_{datetime.now():%Y%m%d_%H%M%S}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DatabaseSanitizer:
    """Main sanitization orchestrator."""
    
    def __init__(self, connection_string: str, dry_run: bool = True):
        self.connection_string = connection_string
        self.dry_run = dry_run
        self.stats = {
            'tables_processed': 0,
            'rows_updated': 0,
            'start_time': datetime.now()
        }
        
        # Initialize maskers
        self.email_masker = EmailMasker(deterministic=True)
        self.name_masker = NameMasker(seed=42)
        self.phone_masker = PhoneMasker()
        
        logger.info(f"Initialized sanitizer (dry_run={dry_run})")
    
    def sanitize_users_table(self):
        """Sanitize Users table."""
        logger.info("Sanitizing Users table...")
        
        def sanitize_user_row(row: Dict) -> Dict:
            """Sanitize individual user row."""
            return {
                'email': self.email_masker.mask(row['email']),
                'first_name': self.name_masker.mask(row['first_name']),
                'last_name': self.name_masker.mask(row['last_name']),
                'phone': self.phone_masker.mask(row['phone'])
            }
        
        batch_processor = BatchSanitizer(
            self.connection_string,
            batch_size=1000
        )
        
        rows = batch_processor.process_table_in_batches(
            table='Users',
            columns=['email', 'first_name', 'last_name', 'phone'],
            sanitize_fn=sanitize_user_row,
            pk_column='user_id'
        )
        
        self.stats['rows_updated'] += rows
        self.stats['tables_processed'] += 1
        logger.info(f"Sanitized {rows} user records")
    
    def sanitize_orders_table(self):
        """Sanitize Orders table (preserve structure, anonymize details)."""
        logger.info("Sanitizing Orders table...")
        
        # Keep order structure but remove sensitive notes/comments
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE Orders
            SET 
                shipping_address = 'REDACTED',
                billing_address = 'REDACTED',
                customer_notes = NULL
            WHERE shipping_address IS NOT NULL
        """)
        
        rows_affected = cursor.rowcount
        
        if not self.dry_run:
            conn.commit()
        else:
            conn.rollback()
        
        conn.close()
        
        self.stats['rows_updated'] += rows_affected
        logger.info(f"Sanitized {rows_affected} order records")
    
    def run(self) -> Dict[str, Any]:
        """Execute complete sanitization workflow."""
        logger.info("=" * 60)
        logger.info("Starting database sanitization")
        logger.info("=" * 60)
        
        try:
            # Pre-flight checks
            self._verify_not_production()
            self._create_backup()
            
            # Execute sanitization
            self.sanitize_users_table()
            self.sanitize_orders_table()
            # Add more tables as needed
            
            # Validation
            self._validate_results()
            
            # Generate report
            return self._generate_report()
            
        except Exception as e:
            logger.error(f"Sanitization failed: {e}", exc_info=True)
            raise
        finally:
            self.stats['end_time'] = datetime.now()
            self.stats['duration'] = (
                self.stats['end_time'] - self.stats['start_time']
            ).total_seconds()
    
    def _verify_not_production(self):
        """Safety check to prevent running on production database."""
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        
        # Check for production indicator
        cursor.execute("SELECT @@SERVERNAME")
        server_name = cursor.fetchone()[0]
        
        if 'prod' in server_name.lower() or 'production' in server_name.lower():
            raise RuntimeError(
                f"SAFETY CHECK FAILED: Refusing to sanitize production database: {server_name}"
            )
        
        conn.close()
        logger.info("✓ Production check passed")
    
    def _create_backup(self):
        """Create database backup before sanitization."""
        if self.dry_run:
            logger.info("Dry run mode: Skipping backup")
            return
        
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        
        backup_name = f"presanitization_{datetime.now():%Y%m%d_%H%M%S}"
        
        logger.info(f"Creating backup: {backup_name}")
        
        # Implementation depends on your backup strategy
        # This is a simplified example
        cursor.execute(f"""
            BACKUP DATABASE [YourDB] 
            TO DISK = N'/backups/{backup_name}.bak'
            WITH NOFORMAT, INIT, NAME = N'{backup_name}', SKIP
        """)
        
        conn.close()
        logger.info("✓ Backup completed")
    
    def _validate_results(self):
        """Validate sanitization results."""
        logger.info("Validating sanitization results...")
        
        validator = SanitizationValidator(self.connection_string)
        
        # Check for PII patterns
        pii_patterns = [
            r'\b[A-Za-z0-9._%+-]+@(?!example\.com|test\.com|sample\.org)[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'  # Credit card
        ]
        
        if not validator.validate_no_pii_leakage('Users', ['email', 'phone'], pii_patterns):
            logger.warning(f"PII leakage detected: {len(validator.violations)} violations")
        else:
            logger.info("✓ No PII leakage detected")
        
        # Check referential integrity
        if not validator.validate_referential_integrity():
            logger.error("❌ Referential integrity violations found!")
            raise RuntimeError("Data integrity compromised")
        else:
            logger.info("✓ Referential integrity validated")
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate sanitization report."""
        report = {
            'success': True,
            'dry_run': self.dry_run,
            'stats': self.stats,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info("=" * 60)
        logger.info("Sanitization Complete")
        logger.info(f"Tables processed: {self.stats['tables_processed']}")
        logger.info(f"Rows updated: {self.stats['rows_updated']}")
        logger.info(f"Duration: {self.stats['duration']:.2f}s")
        logger.info("=" * 60)
        
        return report


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Sanitize database for non-production use'
    )
    parser.add_argument(
        '--connection-string',
        required=True,
        help='Database connection string'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=True,
        help='Preview changes without committing'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually execute sanitization (disables dry-run)'
    )
    
    args = parser.parse_args()
    
    # Safety: require explicit --execute flag
    dry_run = not args.execute
    
    if not dry_run:
        confirm = input("Are you sure you want to sanitize this database? (yes/no): ")
        if confirm.lower() != 'yes':
            logger.info("Sanitization cancelled")
            return
    
    sanitizer = DatabaseSanitizer(
        connection_string=args.connection_string,
        dry_run=dry_run
    )
    
    report = sanitizer.run()
    
    # Save report
    import json
    report_file = f"sanitization_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    logger.info(f"Report saved to: {report_file}")


if __name__ == '__main__':
    main()
```

## Best Practices

### Safety First
1. **Always test in dry-run mode first**
2. **Create backups before sanitization**
3. **Verify not production environment**
4. **Implement rollback capability**
5. **Log all operations for audit trail**

### Data Quality
1. **Preserve data types and formats**
2. **Maintain referential integrity**
3. **Keep statistical properties similar**
4. **Ensure deterministic masking for reproducibility**
5. **Validate post-sanitization**

### Performance
1. **Use batch processing for large tables**
2. **Process in transaction-friendly chunks**
3. **Consider parallel processing for independent tables**
4. **Monitor memory usage**
5. **Add progress logging**

### Compliance
1. **Document what data is sanitized**
2. **Verify GDPR/HIPAA requirements met**
3. **Maintain audit trail**
4. **Test sanitization effectiveness**
5. **Regular review of sanitization rules**

## Common Scenarios

### Scenario 1: Sanitize for Testing Environment

```python
# Quick script to sanitize specific tables
sanitizer = DatabaseSanitizer(connection_string, dry_run=False)
sanitizer.sanitize_users_table()
sanitizer.sanitize_orders_table()
report = sanitizer.run()
```

### Scenario 2: Preserve Specific Test Accounts

```python
# Skip sanitization for specific test accounts
PRESERVED_EMAILS = ['testuser@example.com', 'admin@test.com']

def sanitize_user_row(row: Dict) -> Dict:
    if row['email'] in PRESERVED_EMAILS:
        return row  # Don't sanitize
    
    return {
        'email': email_masker.mask(row['email']),
        'name': name_masker.mask(row['name'])
    }
```

### Scenario 3: Anonymize While Maintaining Relationships

```python
# Use deterministic masking to preserve user relationships
email_masker = EmailMasker(deterministic=True)

# Same email always maps to same fake email
# User relationships in other tables remain consistent
```

## Output Guidelines

When writing sanitization scripts:

1. **Modular design** - Separate concerns (masking, validation, orchestration)
2. **Safety checks** - Production detection, backups, dry-run mode
3. **Comprehensive logging** - Track all operations and errors
4. **Validation** - Verify data quality and integrity post-sanitization
5. **Performance optimization** - Batch processing, memory efficiency
6. **Documentation** - Clear comments explaining masking strategies
7. **Error handling** - Rollback on failures, detailed error messages
8. **Testing** - Unit tests for masking functions, integration tests for pipeline

## Compliance Checklist

- [ ] All PII fields identified and classified
- [ ] Appropriate masking strategy selected for each field
- [ ] Referential integrity preserved
- [ ] Backup created before sanitization
- [ ] Production environment checks in place
- [ ] Validation tests confirm no PII leakage
- [ ] Audit log of all sanitization operations
- [ ] Data distribution remains statistically similar
- [ ] Test accounts/edge cases handled
- [ ] Documentation updated with sanitization rules
