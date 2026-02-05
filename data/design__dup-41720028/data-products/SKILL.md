---
name: data-products
description: Data product design patterns with contracts, SLAs, and governance for building self-serve data platforms using Data Mesh principles.
triggers:
  - data products
  - data mesh
  - data contracts
  - sla definition
  - data governance
category: architecture
---

# Data Products Skill

## Overview

Data products are self-contained, discoverable data assets with clear ownership, SLAs, and contracts. This skill provides patterns for designing, implementing, and governing data products using Data Mesh principles.

**Key Benefits:**
- Clear ownership and accountability
- Explicit contracts and SLAs
- Discoverable and self-serve
- Version-controlled interfaces
- Quality guarantees
- Consumer-oriented design

## When to Use This Skill

Use data product patterns when you need to:
- Build self-serve data platforms
- Implement Data Mesh architecture
- Define clear data contracts between teams
- Establish data ownership and accountability
- Provide discoverable data assets
- Guarantee data quality and freshness
- Enable cross-domain data sharing

## Core Concepts

### 1. Data Product Definition

**Product Specification:**
```yaml
product:
  name: customer-360
  version: 2.1.0
  description: Complete customer view with demographics, behavior, and preferences
  owner:
    team: customer-data-platform
    email: cdp-team@company.com
  domain: customer
  subdomain: customer-intelligence

interfaces:
  - name: customer_profile
    type: delta_table
    location: catalog.customer.profile_v2
    format: delta
    access_pattern: batch_query

  - name: customer_events_stream
    type: kafka_topic
    location: customer.events.v2
    format: avro
    access_pattern: streaming

contracts:
  schema:
    version: 2.1.0
    evolution_policy: backward_compatible

  sla:
    freshness:
      profile: 1_hour
      events: real_time
    availability: 99.9%
    completeness: 99.5%
    accuracy: 99%

  quality_rules:
    - name: primary_key_uniqueness
      rule: customer_id IS NOT NULL AND UNIQUE
      severity: critical
    - name: email_format
      rule: email matches RFC5322 pattern
      severity: high

governance:
  classification: PII
  retention_days: 2555  # 7 years
  access_controls:
    - role: data_analyst
      permissions: [SELECT]
    - role: data_engineer
      permissions: [SELECT, INSERT]
```

### 2. Data Contracts

**Contract Schema Definition:**
```python
"""
Data contract implementation.
"""
from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum


class DataType(Enum):
    """Supported data types."""
    STRING = "string"
    INTEGER = "integer"
    DOUBLE = "double"
    TIMESTAMP = "timestamp"
    BOOLEAN = "boolean"


@dataclass
class FieldContract:
    """Contract for a single field."""
    name: str
    type: DataType
    required: bool
    description: str
    constraints: Dict[str, Any] = None
    pii: bool = False


@dataclass
class DataContract:
    """Complete data contract specification."""
    product_name: str
    version: str
    fields: List[FieldContract]
    primary_keys: List[str]
    partitioning: List[str]
    quality_rules: List[Dict[str, Any]]
    sla: Dict[str, Any]

    def validate_schema(self, df) -> bool:
        """Validate DataFrame against contract."""
        # Check all required fields present
        contract_fields = {f.name for f in self.fields}
        df_fields = set(df.columns)

        if not contract_fields.issubset(df_fields):
            missing = contract_fields - df_fields
            raise ValueError(f"Missing required fields: {missing}")

        # Check field types
        for field in self.fields:
            if field.required and df.filter(df[field.name].isNull()).count() > 0:
                raise ValueError(f"Required field {field.name} has null values")

        return True


# Example usage
customer_contract = DataContract(
    product_name="customer-360",
    version="2.1.0",
    fields=[
        FieldContract(
            name="customer_id",
            type=DataType.STRING,
            required=True,
            description="Unique customer identifier",
            pii=False
        ),
        FieldContract(
            name="email",
            type=DataType.STRING,
            required=True,
            description="Customer email address",
            constraints={"format": "email"},
            pii=True
        )
    ],
    primary_keys=["customer_id"],
    partitioning=["registration_date"],
    quality_rules=[
        {"name": "uniqueness", "column": "customer_id", "rule": "unique"},
        {"name": "email_format", "column": "email", "rule": "matches_regex", "pattern": r"^[A-Za-z0-9._%+-]+@"}
    ],
    sla={
        "freshness_hours": 1,
        "availability_percent": 99.9,
        "completeness_percent": 99.5
    }
)
```

### 3. SLA Management

**SLA Monitoring:**
```python
"""
SLA monitoring and enforcement.
"""
from datetime import datetime, timedelta
from typing import Dict, Any


class SLAMonitor:
    """Monitor and enforce data product SLAs."""

    def __init__(self, spark):
        self.spark = spark

    def check_freshness(
        self,
        table_name: str,
        timestamp_column: str,
        max_age_hours: int
    ) -> Dict[str, Any]:
        """Check if data meets freshness SLA."""
        df = self.spark.table(table_name)

        latest_timestamp = df.agg(
            {timestamp_column: "max"}
        ).collect()[0][0]

        age_hours = (
            datetime.now() - latest_timestamp
        ).total_seconds() / 3600

        return {
            "met": age_hours <= max_age_hours,
            "latest_timestamp": latest_timestamp,
            "age_hours": age_hours,
            "sla_hours": max_age_hours
        }

    def check_completeness(
        self,
        table_name: str,
        required_columns: List[str],
        threshold_percent: float = 99.0
    ) -> Dict[str, Any]:
        """Check if data meets completeness SLA."""
        df = self.spark.table(table_name)
        total_records = df.count()

        results = {}
        for column in required_columns:
            non_null_count = df.filter(df[column].isNotNull()).count()
            completeness = (non_null_count / total_records) * 100

            results[column] = {
                "completeness_percent": completeness,
                "met": completeness >= threshold_percent,
                "missing_count": total_records - non_null_count
            }

        overall_met = all(r["met"] for r in results.values())

        return {
            "met": overall_met,
            "by_column": results
        }

    def check_availability(
        self,
        table_name: str,
        lookback_days: int = 7
    ) -> Dict[str, Any]:
        """Check if data product meets availability SLA."""
        # Query system tables for availability metrics
        query = f"""
        SELECT
            COUNT(*) as total_checks,
            SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_checks
        FROM system.monitoring.table_health_checks
        WHERE table_name = '{table_name}'
          AND check_time >= current_date() - INTERVAL {lookback_days} DAYS
        """

        result = self.spark.sql(query).first()

        availability_percent = (
            result["successful_checks"] / result["total_checks"] * 100
            if result["total_checks"] > 0 else 0
        )

        return {
            "availability_percent": availability_percent,
            "total_checks": result["total_checks"],
            "successful_checks": result["successful_checks"],
            "lookback_days": lookback_days
        }
```

### 4. Product Metadata

**Metadata Management:**
```python
"""
Data product metadata and discovery.
"""
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from datetime import datetime
import json


@dataclass
class ProductMetadata:
    """Metadata for data product discovery."""
    name: str
    version: str
    description: str
    owner_team: str
    owner_email: str
    domain: str
    tags: List[str]
    interfaces: List[Dict[str, Any]]
    documentation_url: str
    created_at: datetime
    updated_at: datetime

    def to_delta(self, spark, catalog_table: str):
        """Persist metadata to Unity Catalog."""
        metadata_dict = asdict(self)
        metadata_dict["created_at"] = self.created_at.isoformat()
        metadata_dict["updated_at"] = self.updated_at.isoformat()
        metadata_dict["interfaces"] = json.dumps(self.interfaces)
        metadata_dict["tags"] = json.dumps(self.tags)

        df = spark.createDataFrame([metadata_dict])
        df.write.format("delta").mode("append").saveAsTable(catalog_table)


class ProductCatalog:
    """Centralized product catalog for discovery."""

    def __init__(self, spark, catalog_table: str):
        self.spark = spark
        self.catalog_table = catalog_table

    def register_product(self, metadata: ProductMetadata):
        """Register new data product."""
        metadata.to_delta(self.spark, self.catalog_table)

    def search_products(
        self,
        domain: str = None,
        tags: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for data products."""
        query = f"SELECT * FROM {self.catalog_table} WHERE 1=1"

        if domain:
            query += f" AND domain = '{domain}'"

        if tags:
            for tag in tags:
                query += f" AND array_contains(tags, '{tag}')"

        return self.spark.sql(query).collect()

    def get_product(self, name: str, version: str = None) -> Dict[str, Any]:
        """Get specific product metadata."""
        query = f"SELECT * FROM {self.catalog_table} WHERE name = '{name}'"

        if version:
            query += f" AND version = '{version}'"
        else:
            query += " ORDER BY updated_at DESC LIMIT 1"

        result = self.spark.sql(query).first()
        return result.asDict() if result else None
```

## Implementation Patterns

### Pattern 1: Building a Data Product

**Complete Product Implementation:**
```python
"""
Customer 360 Data Product Implementation
"""
import dlt
from pyspark.sql.functions import *


# Product metadata
PRODUCT_NAME = "customer-360"
PRODUCT_VERSION = "2.1.0"
PRODUCT_OWNER = "customer-data-platform"


@dlt.table(
    name="customer_360_profile",
    comment="Customer 360 profile data product",
    table_properties={
        "product.name": PRODUCT_NAME,
        "product.version": PRODUCT_VERSION,
        "product.owner": PRODUCT_OWNER,
        "product.interface": "customer_profile",
        "quality.tier": "gold",
        "pii.contains": "true"
    }
)
@dlt.expect_or_fail("pk_not_null", "customer_id IS NOT NULL")
@dlt.expect_or_fail("pk_unique", "customer_id IS UNIQUE")
@dlt.expect_or_drop("valid_email", "email RLIKE '^[A-Za-z0-9._%+-]+@'")
@dlt.expect("complete_profile", "phone IS NOT NULL AND address IS NOT NULL")
def customer_360_profile():
    """
    Build customer 360 profile data product.

    SLA:
    - Freshness: 1 hour
    - Availability: 99.9%
    - Completeness: 99.5%
    """
    # Source data
    demographics = dlt.read("silver_customer_demographics")
    behavior = dlt.read("silver_customer_behavior")
    preferences = dlt.read("silver_customer_preferences")

    # Join sources
    profile = (
        demographics
        .join(behavior, "customer_id", "left")
        .join(preferences, "customer_id", "left")
        .select(
            "customer_id",
            "email",
            "phone",
            "address",
            "registration_date",
            "segment",
            "lifetime_value",
            "last_purchase_date",
            "total_orders",
            "preferred_category",
            "communication_preference"
        )
        .withColumn("product_version", lit(PRODUCT_VERSION))
        .withColumn("updated_at", current_timestamp())
    )

    return profile


# Product quality monitoring
@dlt.table(
    name="customer_360_quality_metrics",
    comment="Quality metrics for customer 360 product"
)
def quality_metrics():
    """Monitor product quality against SLAs."""
    profile = dlt.read("customer_360_profile")

    return spark.sql(f"""
        SELECT
            current_timestamp() as metric_timestamp,
            '{PRODUCT_NAME}' as product_name,
            '{PRODUCT_VERSION}' as product_version,
            COUNT(*) as total_records,
            COUNT_IF(customer_id IS NOT NULL) * 100.0 / COUNT(*) as id_completeness,
            COUNT_IF(email IS NOT NULL) * 100.0 / COUNT(*) as email_completeness,
            COUNT_IF(phone IS NOT NULL) * 100.0 / COUNT(*) as phone_completeness,
            MAX(updated_at) as last_update_time,
            (unix_timestamp(current_timestamp()) - unix_timestamp(MAX(updated_at))) / 3600 as data_age_hours
        FROM LIVE.customer_360_profile
    """)
```

### Pattern 2: Contract Enforcement

**Automated Contract Validation:**
```python
"""
Contract validation in data pipelines.
"""
from typing import Dict, Any
from pyspark.sql import DataFrame


class ContractValidator:
    """Validate data against contracts."""

    def __init__(self, contract: DataContract):
        self.contract = contract

    def validate(self, df: DataFrame) -> Dict[str, Any]:
        """
        Validate DataFrame against contract.

        Returns validation results with pass/fail status.
        """
        results = {
            "product": self.contract.product_name,
            "version": self.contract.version,
            "timestamp": datetime.now().isoformat(),
            "validations": []
        }

        # Schema validation
        try:
            self.contract.validate_schema(df)
            results["validations"].append({
                "check": "schema",
                "status": "PASS"
            })
        except ValueError as e:
            results["validations"].append({
                "check": "schema",
                "status": "FAIL",
                "error": str(e)
            })

        # Primary key validation
        pk_violations = (
            df.groupBy(self.contract.primary_keys)
            .count()
            .filter(col("count") > 1)
            .count()
        )

        results["validations"].append({
            "check": "primary_key_uniqueness",
            "status": "PASS" if pk_violations == 0 else "FAIL",
            "violations": pk_violations
        })

        # Quality rules validation
        for rule in self.contract.quality_rules:
            violations = self._check_quality_rule(df, rule)
            results["validations"].append({
                "check": rule["name"],
                "status": "PASS" if violations == 0 else "FAIL",
                "violations": violations
            })

        results["overall_status"] = (
            "PASS" if all(v["status"] == "PASS" for v in results["validations"])
            else "FAIL"
        )

        return results

    def _check_quality_rule(self, df: DataFrame, rule: Dict[str, Any]) -> int:
        """Check individual quality rule."""
        if rule["rule"] == "unique":
            total = df.count()
            unique = df.select(rule["column"]).distinct().count()
            return total - unique

        elif rule["rule"] == "matches_regex":
            return df.filter(
                ~col(rule["column"]).rlike(rule["pattern"])
            ).count()

        return 0
```

### Pattern 3: Product Versioning

**Semantic Versioning for Data:**
```python
"""
Data product versioning strategy.
"""


class ProductVersion:
    """Manage data product versions."""

    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def bump_major(self):
        """
        Increment major version (breaking changes).

        Examples:
        - Removing columns
        - Changing column types
        - Changing primary keys
        """
        return ProductVersion(self.major + 1, 0, 0)

    def bump_minor(self):
        """
        Increment minor version (backward compatible changes).

        Examples:
        - Adding new columns
        - Adding new quality rules
        - Improving data quality
        """
        return ProductVersion(self.major, self.minor + 1, 0)

    def bump_patch(self):
        """
        Increment patch version (bug fixes).

        Examples:
        - Fixing data quality issues
        - Correcting transformations
        - Performance improvements
        """
        return ProductVersion(self.major, self.minor, self.patch + 1)

    def is_compatible(self, other: 'ProductVersion') -> bool:
        """
        Check if versions are compatible.

        Compatibility: same major version.
        """
        return self.major == other.major
```

### Pattern 4: Self-Service Discovery

**Product Discovery Interface:**
```python
"""
Self-service data product discovery.
"""


class ProductDiscovery:
    """Enable self-service product discovery."""

    def __init__(self, spark, catalog_table: str):
        self.spark = spark
        self.catalog_table = catalog_table

    def list_products_by_domain(self, domain: str) -> DataFrame:
        """List all products in a domain."""
        return self.spark.sql(f"""
            SELECT
                name,
                version,
                description,
                owner_team,
                tags,
                documentation_url
            FROM {self.catalog_table}
            WHERE domain = '{domain}'
            ORDER BY name, version DESC
        """)

    def get_product_lineage(self, product_name: str) -> Dict[str, Any]:
        """Get upstream and downstream dependencies."""
        lineage_query = f"""
        SELECT
            upstream_table,
            downstream_table,
            transformation_logic
        FROM system.access.table_lineage
        WHERE downstream_table LIKE '%{product_name}%'
           OR upstream_table LIKE '%{product_name}%'
        """

        lineage = self.spark.sql(lineage_query).collect()

        return {
            "product": product_name,
            "upstream": [row.upstream_table for row in lineage],
            "downstream": [row.downstream_table for row in lineage]
        }

    def get_product_usage(
        self,
        product_name: str,
        days: int = 30
    ) -> DataFrame:
        """Get product usage statistics."""
        return self.spark.sql(f"""
        SELECT
            date_trunc('day', request_time) as date,
            user_name,
            COUNT(*) as query_count
        FROM system.access.audit
        WHERE table_name LIKE '%{product_name}%'
          AND request_time >= current_date() - INTERVAL {days} DAYS
        GROUP BY 1, 2
        ORDER BY 1 DESC, 3 DESC
        """)
```

## Best Practices

### 1. Product Organization

```
products/
├── customer-360/
│   ├── product.yaml
│   ├── contract.json
│   ├── pipelines/
│   │   └── build_product.py
│   ├── tests/
│   │   └── test_product.py
│   └── docs/
│       └── README.md
```

### 2. Contract Evolution

- **Major version**: Breaking changes
- **Minor version**: Backward compatible additions
- **Patch version**: Bug fixes and improvements
- Always maintain backward compatibility within major version
- Deprecate fields before removing
- Provide migration guides for major versions

### 3. SLA Definition

Define realistic, measurable SLAs:
- **Freshness**: Maximum data age
- **Availability**: Uptime percentage
- **Completeness**: Minimum non-null percentage
- **Accuracy**: Data correctness threshold

### 4. Ownership Model

- Clear team ownership
- On-call rotation for incidents
- Documented escalation paths
- Regular SLA reviews

## Common Pitfalls to Avoid

Don't:
- Create products without clear consumers
- Skip contract definition
- Ignore versioning strategy
- Overcomplicate products
- Neglect monitoring

Do:
- Start with consumer needs
- Define explicit contracts
- Version semantically
- Keep products focused
- Monitor SLAs continuously

## Complete Examples

See `/examples/` directory for:
- `customer360_product.py`: Complete data product
- `sales_analytics_product.py`: Analytics product example

## Related Skills

- `data-quality`: Quality guarantees
- `delta-live-tables`: Product pipelines
- `delta-sharing`: Product distribution
- `cicd-workflows`: Product deployment

## References

- [Data Mesh Principles](https://www.datamesh-architecture.com/)
- [Data Contracts](https://datacontract.com/)
- [Data Product Design](https://martinfowler.com/articles/data-mesh-principles.html)
