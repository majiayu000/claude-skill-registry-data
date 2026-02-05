---
name: prisma-relations-mapping
description: >
  CRITICAL: Use this skill when working with Prisma database models, API routes with includes/relations,
  or debugging "500 errors", "relation not found", "undefined from backend" errors.

  AUTO-ACTIVATE when user mentions (FR/EN):
  - prisma, relation, relations, mapping, PascalCase, camelCase
  - API 500, erreur 500, backend error, erreur backend
  - undefined, null, relation introuvable, relation not found
  - créer API, create API, endpoint, route API
  - include, select, findMany, findUnique, create, update
  - OperatingRoom, OperatingSector, Personnel, Assignment, Site

  This skill contains the COMPLETE mapping table for post-PascalCase migration (Oct 26, 2025).
  ALL 121 models with correct relation names and required fields.
---

# Prisma Relations Mapping - Post-Migration PascalCase

**Version**: 1.0
**Migration**: commit 3d353115d (26 Oct 2025)
**Purpose**: Éviter erreurs 500 et mapping incorrects après migration PascalCase

---

## 🎯 Problems Solved

### ❌ Common Errors Without This Guide
```typescript
// ❌ ERROR 500 - Relation doesn't exist after migration
const rooms = await prisma.operatingRoom.findMany({
  include: { operatingSector: true }  // ❌ TypeError: relation not found
});

// ❌ Frontend receives undefined - Incorrect mapping
return NextResponse.json(rooms);
// Frontend: room.operatingSector = undefined (expects camelCase)
```

### ✅ Solutions Here
1. Complete relation conversion table (PascalCase ↔ camelCase)
2. API → Frontend mapping patterns
3. Required fields without `@default` per model
4. ID generation patterns

---

## 📊 Naming Rules (Post-Migration)

```
1. Relations "to parent" (1:1, N:1) → PascalCase
   Example: OperatingSector, Personnel, User

2. Collections (1:N) → snake_case
   Example: operating_rooms, assignments, planned_absences

3. Frontend expectations → camelCase
   Example: operatingSector, site, rooms
```

---

## 🔥 TOP 5 CRITICAL MODELS (Quick Reference)

### 1. OperatingRoom

```typescript
// ✅ Prisma Query
const rooms = await prisma.operatingRoom.findMany({
  include: {
    OperatingSector: true,  // ← PascalCase (to parent)
    sites: true             // ← PascalCase (to parent)
  }
});

// ✅ Frontend Mapping
const mappedRooms = rooms.map(room => ({
  ...room,
  operatingSector: room.OperatingSector,  // → camelCase
  site: room.sites                         // Rename sites → site
}));

return NextResponse.json(mappedRooms);
```

**Reference**: `src/app/api/admin/rooms-order/route.ts:19-38`

---

### 2. OperatingSector

```typescript
// ✅ Prisma Query
const sectors = await prisma.operatingSector.findMany({
  include: {
    sites: true,                     // ← PascalCase (to parent)
    operating_rooms: {               // ← snake_case (collection)
      orderBy: [{ displayOrder: 'asc' }]
    },
    _count: {
      select: { operating_rooms: true }
    }
  }
});

// ✅ Frontend Mapping
const mappedSectors = sectors.map(sector => ({
  ...sector,
  site: sector.sites,                          // Rename sites → site
  _count: {
    rooms: sector._count.operating_rooms       // Rename
  }
}));
```

**Reference**: `src/app/api/admin/sectors-order/route.ts:12-43`

---

### 3. Site

```typescript
// ✅ Prisma Query
const sites = await prisma.site.findMany({
  include: {
    OperatingSector: true,           // ← PascalCase (collection)
    operating_rooms: true,            // ← snake_case (collection)
    _count: {
      select: {
        OperatingSector: true,
        operating_rooms: true
      }
    }
  }
});

// ✅ Frontend Mapping (for _count)
const mapped = sites.map(site => ({
  ...site,
  _count: {
    operatingSectors: site._count.OperatingSector,
    operatingRooms: site._count.operating_rooms
  }
}));
```

**Reference**: `src/app/api/admin/sites-order/route.ts:7-37`

---

### 4. Assignment

```typescript
// ✅ Query with nested relations
const assignments = await prisma.assignment.findMany({
  where: { date: { gte: startDate, lte: endDate } },
  include: {
    User: {                          // ← PascalCase
      select: { id: true, name: true, professionalRole: true }
    },
    TrameModele: true                // ← PascalCase
  }
});

// ✅ Frontend expects camelCase
const mapped = assignments.map(a => ({
  ...a,
  user: a.User,
  trameModele: a.TrameModele
}));
```

---

### 5. Personnel

```typescript
// ✅ Query with relations
const personnel = await prisma.personnel.findMany({
  include: {
    User: true,                      // ← PascalCase
    Site: true,                      // ← PascalCase
    Specialty: true,                 // ← PascalCase
    planned_absences: true           // ← snake_case (collection)
  }
});

// ✅ Map if frontend needs camelCase
const mapped = personnel.map(p => ({
  ...p,
  user: p.User,
  site: p.Site,
  specialty: p.Specialty,
  plannedAbsences: p.planned_absences
}));
```

**⚠️ Important**: No direct FK `personnelId` in Assignment.
Relation: `Personnel → User → Assignment` (via `userId`)

---

## 🔑 Required Fields Without @default

### Site (id: String)
```typescript
// ✅ Pattern tested
const siteId = `site-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;

await prisma.site.create({
  data: {
    id: siteId,              // ⚠️ REQUIRED
    name: 'Clinique Mathilde',
    address: '...',
    updatedAt: new Date(),   // ⚠️ REQUIRED
    displayOrder: 999,
    isActive: true
  }
});
```

**Reference**: `src/app/api/admin/sites-order/route.ts:98-111`

---

### OperatingSector (id: Int @autoincrement)
```typescript
await prisma.operatingSector.create({
  data: {
    name: 'Bloc Central',
    siteId: 'site-123',
    category: 'STANDARD',      // ⚠️ REQUIRED (enum, no @default)
    updatedAt: new Date(),     // ⚠️ REQUIRED
    displayOrder: 999,
    isActive: true
  }
});
```

**Reference**: `src/app/api/admin/sectors-order/route.ts:107-119`

---

### OperatingRoom (id: Int @autoincrement)
```typescript
// ✅ Pattern with fallback auto-generation
const roomNumber = data.number || `SALLE-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;

await prisma.operatingRoom.create({
  data: {
    name: 'Salle 1',
    number: roomNumber,           // ⚠️ User-editable or auto-gen
    operatingSectorId: 1,
    siteId: 'site-123',
    roomType: 'STANDARD',
    updatedAt: new Date(),        // ⚠️ REQUIRED
    displayOrder: 999,
    isActive: true,
    capacity: 1
  }
});
```

**Reference**: `src/app/api/admin/rooms-order/route.ts:106-122`

---

## 🛠️ Reusable Mapping Patterns

### Pattern 1: Simple Rename
```typescript
// Case: Single relation to rename
const items = await prisma.model.findMany({
  include: { UpperCaseRelation: true }
});

const mapped = items.map(item => ({
  ...item,
  lowerCaseRelation: item.UpperCaseRelation
}));
```

---

### Pattern 2: _count Mapping
```typescript
// Case: Count collections with different names
const items = await prisma.model.findMany({
  include: {
    _count: {
      select: {
        UpperCaseCollection: true,
        snake_case_collection: true
      }
    }
  }
});

const mapped = items.map(item => ({
  ...item,
  _count: {
    lowerCaseCollection: item._count.UpperCaseCollection,
    camelCaseCollection: item._count.snake_case_collection
  }
}));
```

---

### Pattern 3: Nested Relations
```typescript
// Case: Multi-level nested relations
const items = await prisma.model.findMany({
  include: {
    ParentRelation: {
      include: {
        GrandParentRelation: true
      }
    },
    child_relations: true
  }
});

const mapped = items.map(item => ({
  ...item,
  parentRelation: {
    ...item.ParentRelation,
    grandParentRelation: item.ParentRelation?.GrandParentRelation
  },
  childRelations: item.child_relations
}));
```

---

## ✅ Checklist for CRUD API Creation

### GET Endpoint
- [ ] Use correct PascalCase/snake_case relation names in `include`
- [ ] Map `_count` to camelCase if needed
- [ ] Rename relations for frontend (UpperCase → camelCase)
- [ ] Test with Postman/curl before frontend integration

### POST Endpoint
- [ ] Check all **required fields without @default** in schema
- [ ] Generate ID if needed (Site, BlocDayPlanning)
- [ ] Add `updatedAt: new Date()` if required
- [ ] Add default values for required enums (e.g., `category: 'STANDARD'`)
- [ ] Parse Int if FK is integer (`parseInt(data.sectorId)`)

### PATCH Endpoint
- [ ] Always include `updatedAt: new Date()` in data
- [ ] Parse Int for integer FKs
- [ ] Validate required fields don't become null

### DELETE Endpoint
- [ ] Check FK constraints (cascade delete configured?)
- [ ] Parse Int if ID is integer

---

## 🚨 Common Errors & Solutions

### Error 1: `PrismaClientKnownRequestError: Invalid relation name`
```typescript
❌ const rooms = await prisma.operatingRoom.findMany({
  include: { operatingSector: true }  // ❌ Doesn't exist after migration
});

✅ const rooms = await prisma.operatingRoom.findMany({
  include: { OperatingSector: true }  // ✅ PascalCase
});
```

---

### Error 2: `TypeError: Cannot read property 'name' of undefined`
```typescript
❌ // API returns { OperatingSector: {...} }
// Frontend reads room.operatingSector.name  // undefined

✅ // Map before returning
const mapped = rooms.map(room => ({
  ...room,
  operatingSector: room.OperatingSector
}));
return NextResponse.json(mapped);
```

---

### Error 3: `PrismaClientValidationError: Missing required field`
```typescript
❌ await prisma.site.create({
  data: { name: 'Test' }  // ❌ Missing id and updatedAt
});

✅ await prisma.site.create({
  data: {
    id: `site-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
    name: 'Test',
    updatedAt: new Date()
  }
});
```

---

## 📍 Progressive Resources

For complete detailed mappings:
- **`resources/relations-table.md`** - All 121 models with relations
- **`resources/required-fields.md`** - Complete list of required fields
- **`resources/mapping-patterns.md`** - Advanced mapping examples

---

## 🔗 References

### APIs with Complete Mapping
- `src/app/api/admin/sites-order/route.ts` (GET:7-37, POST:98-111)
- `src/app/api/admin/sectors-order/route.ts` (GET:12-43, POST:107-119)
- `src/app/api/admin/rooms-order/route.ts` (GET:19-38, POST:106-122)

### Services with Complex Relations
- `src/services/equity/EquityCounterService.ts` (Assignment + User)
- `src/modules/assignments/services/AssignmentService.ts` (Multi-relations)

---

**Last Update**: 27 October 2025
**Next Review**: After next major migration
