---
name: kotlin-schema-first-entities
description: Use when creating Room entities for Kotlin/Android apps that mirror Django/PostgreSQL backend schemas. Enforces exact field alignment, prevents schema drift, validates type mappings. Critical for maintaining zero impedance mismatch between backend and mobile.
---

# Kotlin Schema-First Room Entity Implementation

## When to Use This Skill

**MANDATORY when**:
- Creating ANY `@Entity` class for Room database
- Android app mirrors a Django/PostgreSQL backend
- Backend has Pydantic type-safe contracts
- Documentation exists for PostgreSQL → SQLite schema mapping

**Triggers**:
- About to write `@Entity` annotation
- Creating data models for offline-first mobile app
- Implementing sync between backend database and SQLite

## Core Principle

**Android SQLite is a REPLICA of PostgreSQL, not an independent schema.**

Schema Authority Hierarchy:
```
1. PostgreSQL (Django Models) ← SOURCE OF TRUTH
2. Pydantic Validation ← Contract enforcement
3. OpenAPI Schema ← API contract
4. Kotlin DTOs ← Generated from OpenAPI
5. Room Entities ← Hand-coded to match DTOs ± denormalization
```

---

## MANDATORY VERIFICATION PROTOCOL

### Before Creating ANY Room Entity

**STOP and complete this checklist**:

- [ ] **Step 1**: Locate schema mapping documentation
  - Find: `docs/api-contracts/POSTGRESQL_TO_SQLITE_SCHEMA_MAPPING.md` (or equivalent)
  - If missing: **FAIL** - Cannot proceed without schema reference

- [ ] **Step 2**: Find the corresponding section
  - Example: Section 1.2 for People domain, Section 1.1 for Attendance, etc.
  - Read the COMPLETE field list for that Django model

- [ ] **Step 3**: Copy EXACT field list
  - Do NOT add fields not in Django model
  - Do NOT remove fields from Django model
  - Do NOT assume field types
  - Use the field list EXACTLY as documented

- [ ] **Step 4**: Verify type mappings
  - Check Section 1 of schema mapping doc for type conversion rules
  - DateTimeField → Long (epoch ms), NOT String
  - DecimalField → String (for precision), NOT Double/Float
  - BooleanField → Boolean (stored as INTEGER 0/1)
  - JSONField with known structure → Typed data class, NOT Map<String, Any>
  - ForeignKey → Int/Long (store ID only)
  - PointField (PostGIS) → Separate lat/lng Double columns OR WKT String

- [ ] **Step 5**: Document denormalization
  - If flattening multiple Django tables → Document in KDoc
  - Justify with performance rationale
  - List which Django tables are merged

- [ ] **Step 6**: Add KDoc with schema authority
  ```kotlin
  /**
   * ⚠️ SCHEMA AUTHORITY: Django model apps/domain/models/model_name.py
   *
   * FIELD MAPPING: [list Django fields → Kotlin properties]
   *
   * DENORMALIZATION: [if applicable, explain what's merged and why]
   *
   * Last Verified Against Django: YYYY-MM-DD
   */
  ```

---

## CRITICAL PATTERNS

### Pattern 1: Hybrid Naming Convention (REQUIRED)

```kotlin
@Entity(tableName = "table_name")  // ← PostgreSQL table name
data class EntityName(
    @ColumnInfo(name = "django_field")  // ← MUST be PostgreSQL column name
    val kotlinProperty: Type             // ← CAN be idiomatic Kotlin name
)
```

**Example**:
```kotlin
@Entity(tableName = "peopleeventlog")
data class AttendanceEntity(
    @ColumnInfo(name = "punchintime")  // ← Django field (PostgreSQL column)
    val checkInTime: Long,              // ← Kotlin property (camelCase, descriptive)

    @ColumnInfo(name = "people")       // ← Django FK field
    val personId: Int,                  // ← Kotlin property (explicit it's ID)

    @ColumnInfo(name = "peoplename")   // ← Django field
    val fullName: String                // ← Kotlin property (more descriptive)
)
```

**Rule**:
- `@ColumnInfo(name)` = Django field name (becomes SQLite column)
- Kotlin property = Idiomatic camelCase name

---

### Pattern 2: Indexes MUST Match PostgreSQL (REQUIRED)

```kotlin
@Entity(
    tableName = "peopleeventlog",
    indices = [
        Index(value = ["tenant", "cdtz"]),           // ← From Django Meta.indexes
        Index(value = ["tenant", "people"]),         // ← Column names are Django fields
        Index(value = ["tenant", "datefor"]),
        Index(value = ["tenant", "people", "shift", "datefor"],
              name = "pel_validation_lookup_idx")    // ← Composite index
    ]
)
```

**Rule**: Copy PostgreSQL indexes exactly (use Django field names in `value` arrays).

---

### Pattern 3: Foreign Keys with Cascade Behavior (REQUIRED)

```kotlin
@Entity(
    foreignKeys = [
        ForeignKey(
            entity = PersonEntity::class,
            parentColumns = ["id"],
            childColumns = ["people"],          // ← Django field name
            onDelete = ForeignKey.RESTRICT      // ← Matches Django on_delete
        )
    ]
)
data class AttendanceEntity(
    @ColumnInfo(name = "people") val personId: Int  // ← Store FK ID
)
```

**Django `on_delete` mapping**:
- `models.CASCADE` → `ForeignKey.CASCADE`
- `models.RESTRICT` → `ForeignKey.RESTRICT`
- `models.SET_NULL` → `ForeignKey.SET_NULL`

**CRITICAL**: Enable FK constraints in database:
```kotlin
override fun init(configuration: DatabaseConfiguration) {
    super.init(configuration)
    openHelper.writableDatabase.execSQL("PRAGMA foreign_keys=ON;")
}
```

---

### Pattern 4: TypeConverters for Complex Types (REQUIRED)

**For DateTime** (MANDATORY):
```kotlin
@TypeConverter
fun fromTimestamp(value: Long?): Instant? =
    value?.let { Instant.fromEpochMilliseconds(it) }

@TypeConverter
fun toTimestamp(instant: Instant?): Long? =
    instant?.toEpochMilliseconds()
```

**For Typed JSON** (REQUIRED for known structures):
```kotlin
// ❌ WRONG: Untyped Map
@ColumnInfo(name = "capabilities") val capabilities: Map<String, Any>

// ✅ CORRECT: Typed data class
@Serializable
data class UserCapabilities(
    @SerialName("can_use_ai_query") val canUseAiQuery: Boolean = false,
    // ... match Django JSONField structure EXACTLY
)

@TypeConverter
fun fromCapabilities(value: UserCapabilities): String =
    Json.encodeToString(value)

@TypeConverter
fun toCapabilities(value: String): UserCapabilities =
    Json.decodeFromString(value)
```

---

## FORBIDDEN ANTI-PATTERNS

### ❌ Anti-Pattern 1: Inventing Fields

```kotlin
// ❌ WRONG: Field not in Django model
@Entity
data class UserEntity(
    val firstName: String,   // ← Django doesn't have this!
    val lastName: String,    // ← Django has "peoplename" only!
    val isFavorite: Boolean  // ← Not in Django model!
)
```

**Consequence**: Sync failures, data loss, schema drift.

**How to detect**: Missing field in schema mapping doc = FORBIDDEN

---

### ❌ Anti-Pattern 2: Wrong Type Mappings

```kotlin
// ❌ WRONG: Type mismatch
@ColumnInfo(name = "department") val department: String  // ← Django has FK (Int)
@ColumnInfo(name = "punchintime") val checkInTime: String  // ← Django DateTimeField → Long
@ColumnInfo(name = "hours_worked") val hoursWorked: Double  // ← Django DecimalField → String
```

**Consequence**: Type errors, precision loss, sync failures.

**How to fix**: Check Section 1 type mapping table.

---

### ❌ Anti-Pattern 3: Client-Side Timestamps

```kotlin
// ❌ WRONG: Generating server-authoritative timestamps
@Entity
data class AttendanceEntity(
    val createdAt: Long = Instant.now().toEpochMilliseconds()  // ← Django auto_now_add
)
```

**Consequence**: Timestamp mismatch between client and server, audit trail corruption.

**How to fix**: Server-authoritative timestamps come from API response.

---

### ❌ Anti-Pattern 4: Untyped JSON

```kotlin
// ❌ WRONG: Known structure as untyped map
@ColumnInfo(name = "capabilities") val capabilities: Map<String, Boolean>
```

**Consequence**: Runtime errors, no compile-time safety, typos in keys.

**How to fix**: Create typed data class matching Django JSONField default.

---

## REQUIRED VALIDATION STEPS

### Step 1: Field Count Verification

```kotlin
/**
 * Django People model has 20+ fields.
 * This entity must include ALL exposed via API.
 *
 * Verified field count: 30 (People: 15, Profile: 8, Organizational: 7)
 */
@Entity
data class UserEntity(
    // List all 30 fields here...
)
```

**Test**: Count fields in Django model = Count fields in Room entity (± documented exclusions).

---

### Step 2: Enum Value Verification

```kotlin
// Django TextChoices
class AssignmentStatus(models.TextChoices):
    SCHEDULED = 'SCHEDULED', 'Scheduled'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'

// Kotlin enum MUST match EXACTLY (case-sensitive)
enum class AssignmentStatus {
    @SerialName("SCHEDULED") SCHEDULED,
    @SerialName("CONFIRMED") CONFIRMED,
    @SerialName("IN_PROGRESS") IN_PROGRESS
}

// ❌ WRONG: Different values
enum class AssignmentStatus {
    SCHEDULED,  // Missing @SerialName - won't deserialize correctly
    Confirmed,  // Wrong case - won't match Django
    InProgress  // Wrong format - won't match Django
}
```

**Write test**:
```kotlin
@Test
fun `enum values match Django choices`() {
    val expected = setOf("SCHEDULED", "CONFIRMED", "IN_PROGRESS")
    val actual = AssignmentStatus.values().map { it.name }.toSet()
    assertEquals(expected, actual)
}
```

---

### Step 3: Type Conversion Round-Trip Test

```kotlin
@Test
fun `DateTime conversion is lossless`() {
    val original = Instant.parse("2025-11-08T14:30:00Z")
    val epoch = original.toEpochMilliseconds()
    val restored = Instant.fromEpochMilliseconds(epoch)
    assertEquals(original, restored)
}

@Test
fun `Decimal conversion preserves precision`() {
    val original = BigDecimal("8.123456")
    val text = original.toPlainString()
    val restored = text.toBigDecimal()
    assertEquals(original, restored)
}
```

---

## ENFORCEMENT CHECKLIST

**Before marking Room entity complete**:

- [ ] Schema mapping doc read for this domain
- [ ] ALL Django fields accounted for (or exclusion documented)
- [ ] @ColumnInfo names match Django field names exactly
- [ ] Type mappings verified against mapping table
- [ ] Indexes copied from Django Meta.indexes
- [ ] Foreign keys have correct cascade behavior
- [ ] TypeConverters defined for complex types
- [ ] KDoc includes Django model file path
- [ ] Denormalization documented (if applicable)
- [ ] Verification date added to KDoc

**If ANY checkbox is unchecked → Entity is NOT complete.**

---

## SUCCESS CRITERIA

✅ Room entity compiles without errors
✅ KSP generates DAO implementation successfully
✅ Type conversion tests pass (round-trip lossless)
✅ Enum validation tests pass (match Django choices)
✅ SQLite column names match PostgreSQL exactly
✅ No fields invented (all from Django model)
✅ No type mismatches (all per mapping table)
✅ All complex types have TypeConverters

---

## REFERENCE DOCUMENTS

**Primary**: `docs/api-contracts/POSTGRESQL_TO_SQLITE_SCHEMA_MAPPING.md`
- Section 1: Type mapping table (18 Django types)
- Section 1.1: Attendance domain models
- Section 1.2: People domain models
- Section 1.3: Operations domain models
- Section 1.4: Journal domain models
- Section 1.5: Helpdesk domain models

**Secondary**: `docs/api-contracts/SCHEMA_FIRST_DATA_CONTRACT_VALIDATION.md`
- Forbidden patterns
- Required patterns
- 8-point validation pipeline

**Skill Guides**: `docs/api-contracts/skills/ROOM_IMPLEMENTATION_GUIDE.md`
- Schema modification workflow
- TypeConverter patterns
- Migration strategies

---

## INTEGRATION WITH OTHER SKILLS

**Use with**:
- `room-database-implementation` - For Room-specific errors (missing TypeConverters, FK issues)
- `kotlin-coroutines-safety` - For DAO suspend functions and Flow
- `offline-first-architecture` - For sync status fields and pending operations

**This skill adds**: Schema alignment verification on TOP of Room implementation best practices.

---

## EXAMPLE: Correct Implementation

```kotlin
/**
 * Room Entity for Attendance records (Check-in/Check-out).
 *
 * ⚠️ SCHEMA AUTHORITY: Django model
 *   - File: apps/attendance/models/people_eventlog.py
 *   - Model: PeopleEventlog
 *
 * DENORMALIZATION: None (exact replica of Django model)
 *
 * FIELD MAPPING (per POSTGRESQL_TO_SQLITE_SCHEMA_MAPPING.md Section 1.1):
 *   - Django punchintime (DateTimeField) → Kotlin Long (epoch ms)
 *   - Django people (ForeignKey) → Kotlin Int (person ID)
 *   - Django startlocation (PointField) → Kotlin Double lat/lng (denormalized)
 *   - Django peventlogextras (EncryptedJSONField) → Kotlin String (encrypted JSON)
 *
 * Last Verified: 2025-11-08
 */
@Entity(
    tableName = "peopleeventlog",  // ← PostgreSQL table name
    foreignKeys = [
        ForeignKey(
            entity = PersonEntity::class,
            parentColumns = ["id"],
            childColumns = ["people"],
            onDelete = ForeignKey.RESTRICT  // ← Matches Django on_delete
        )
    ],
    indices = [
        Index(value = ["tenant", "cdtz"]),  // ← From Django Meta.indexes
        Index(value = ["tenant", "people"]),
        Index(value = ["tenant", "datefor"])
    ]
)
data class AttendanceEntity(
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "id") val id: Int? = null,

    @ColumnInfo(name = "uuid")
    val uuid: String = UUID.randomUUID().toString(),

    @ColumnInfo(name = "people")  // ← Django FK field name
    val personId: Int?,            // ← Kotlin property (explicit)

    @ColumnInfo(name = "client")
    val clientId: Int?,

    @ColumnInfo(name = "bu")
    val buId: Int?,

    @ColumnInfo(name = "punchintime")  // ← Django DateTimeField
    val checkInTime: Long?,             // ← Long epoch (per mapping table)

    @ColumnInfo(name = "punchouttime")
    val checkOutTime: Long?,

    @ColumnInfo(name = "datefor")      // ← Django DateField
    val attendanceDate: String?,        // ← ISO8601 date string

    @ColumnInfo(name = "start_latitude")  // ← Denormalized from PointField
    val startLatitude: Double?,

    @ColumnInfo(name = "start_longitude")
    val startLongitude: Double?,

    @ColumnInfo(name = "peventlogextras")  // ← EncryptedJSONField
    val eventExtras: String = "{}",         // ← Store encrypted JSON

    @ColumnInfo(name = "version")      // ← VersionField
    val version: Int = 1,               // ← Optimistic locking

    @ColumnInfo(name = "tenant")       // ← Multi-tenant FK
    val tenantId: Int?,

    @ColumnInfo(name = "cdtz")         // ← auto_now_add
    val createdAt: Long,                // ← Server-authoritative

    @ColumnInfo(name = "mdtz")         // ← auto_now
    val updatedAt: Long,                // ← Server-authoritative

    // Sync metadata (client-managed)
    @ColumnInfo(name = "mobile_id")
    val mobileId: String = UUID.randomUUID().toString(),

    @ColumnInfo(name = "sync_status")
    val syncStatus: String = "pending"
)
```

---

## VERIFICATION TESTS (MANDATORY)

### Test 1: Schema Alignment

```kotlin
@Test
fun `UserEntity has all fields from schema mapping doc`() {
    // Reference field list from schema doc
    val expectedFields = setOf(
        "id", "peoplecode", "peoplename", "loginid", "email",
        "isadmin", "is_staff", "enable", "gender", "dateofbirth",
        "dateofjoin", "department", "designation", "client", "bu",
        "capabilities", "tenant", "cdtz", "mdtz"
        // ... all 30 fields
    )

    val actualFields = UserEntity::class.memberProperties
        .mapNotNull { it.findAnnotation<ColumnInfo>()?.name }
        .toSet()

    val missing = expectedFields - actualFields
    val extra = actualFields - expectedFields

    assertTrue(missing.isEmpty(), "Missing Django fields: $missing")
    assertTrue(extra.isEmpty(), "Extra fields not in Django: $extra")
}
```

### Test 2: Capabilities Match Django

```kotlin
@Test
fun `UserCapabilities has exact fields from Django default_capabilities`() {
    val expectedKeys = setOf(
        "can_use_ai_query",
        "can_use_nlp_search",
        "can_use_voice_commands",
        "can_use_advanced_analytics",
        "can_use_predictive_insights",
        "can_use_automated_scheduling",
        "can_use_smart_recommendations"
    )

    val json = Json.encodeToString(UserCapabilities())
    val jsonObject = Json.parseToJsonElement(json).jsonObject

    assertEquals(expectedKeys, jsonObject.keys)
}
```

---

## COMMON ERRORS & FIXES

### Error 1: "Field not in schema mapping doc"

**Symptom**: You want to add field `notes: String` to entity.

**Check**: Is `notes` in the Django model section of schema mapping doc?
- ✅ Yes → Safe to add
- ❌ No → **FORBIDDEN** - Do not add

**Fix**: If field is needed, add to Django model FIRST, then update mobile.

---

### Error 2: "Capabilities structure doesn't match"

**Symptom**: Capabilities test fails - JSON keys don't match.

**Check**: Schema mapping doc has exact capabilities structure.

**Fix**:
```kotlin
// Read schema doc Section 1.2
// Copy EXACT field list for capabilities
// Do NOT invent permission fields
```

---

### Error 3: "Type mismatch in DTO → Entity mapping"

**Symptom**:
```kotlin
// DTO has: departmentName: String (from API)
// Entity has: @ColumnInfo(name = "department") val departmentId: Int
```

**This is CORRECT** if:
- API enriches response with department name
- PostgreSQL stores department ID (FK)
- Entity stores ID (matches PostgreSQL)

**Mapper handles enrichment**:
```kotlin
fun UserDto.toEntity() = UserEntity(
    departmentId = this.departmentId  // Use ID from DTO, ignore name
)
```

---

## SUCCESS INDICATORS

**Green flags** (entity is correct):
- ✅ KDoc references Django model file path
- ✅ All @ColumnInfo names are Django field names
- ✅ Field count matches schema doc (± documented denormalization)
- ✅ Type mappings match Section 1 table
- ✅ Indexes copied from Django Meta
- ✅ TypeConverters for all complex types
- ✅ Tests validate schema alignment

**Red flags** (entity is WRONG):
- 🚩 No KDoc referencing Django model
- 🚩 @ColumnInfo names are camelCase or different from Django
- 🚩 Field count doesn't match schema doc
- 🚩 Type mappings don't match (String instead of Int, Double instead of String)
- 🚩 No indexes defined (Django has indexes)
- 🚩 Map<String, Any> for known JSON structure
- 🚩 Invented fields (firstName, isFavorite, etc.)

---

## SUMMARY

**This skill enforces**:
1. Schema mapping doc is authoritative source
2. Django field names in @ColumnInfo
3. Exact type mappings per documentation
4. No invented/assumed fields
5. Typed JSON for known structures
6. Server-authoritative timestamp handling
7. FK IDs (not resolved objects)

**Use this skill BEFORE room-database-implementation skill** - it ensures schema alignment, then room-database-implementation ensures Room-specific correctness.

**Prevents**: Schema drift, sync failures, type mismatches, data loss.

**Ensures**: Perfect PostgreSQL → SQLite replica with zero impedance mismatch.
