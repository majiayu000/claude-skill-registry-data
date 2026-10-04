---
name: sf-fflib-selector-layer
description: Deep coverage of the fflib selector layer - extending fflib_SObjectSelector, getSObjectType/getSObjectFieldList/getOrderBy, the constructor flag and DataAccess.USER_MODE matrix, selectSObjectsById and queryLocatorById, the full fflib_QueryFactory fluent API (selectField, setCondition, addOrdering, setLimit, setOffset, subselectQuery, toSOQL, deepClone), parent field traversal and child subselects via configureQueryFactoryFields and addQueryFactorySubselect, FLS and CRUD enforcement old versus WITH USER_MODE, dynamic filters without SOQL injection using Database.queryWithBinds, QueryLocator selectors for Batch Apex, and selector anti-patterns. Use it when writing or reviewing any class extending fflib_SObjectSelector, when a selector query must add a filter, a child subselect, a field set, or a parent field, when fflib_QueryFactory.InvalidFieldException or NonReferenceFieldException or InvalidSubqueryRelationshipException appears, or when deciding how a selector enforces field-level security.
---

# fflib Selector Layer

Every signature below was read this session from `apex-enterprise-patterns/fflib-apex-common`
@ `master` commit `dab5977`: `sfdx-source/apex-common/main/classes/fflib_SObjectSelector.cls`,
`fflib_QueryFactory.cls`, `fflib_ISObjectSelector.cls`, `fflib_SecurityUtils.cls`,
`fflib_SObjectDescribe.cls`. Selector examples follow `fflib-apex-common-samplecode` @ `master`
commit `4657d63`. Items marked `[unverified]` were not read from source.

## When to use

| Task | Where |
| --- | --- |
| New selector class for an SObject | pattern 1 + `references/selector-recipes.md` |
| Add a filtered query method | pattern 4 |
| Add a child subselect or parent fields | pattern 5 + recipes 4-6 |
| Field sets in a query | pattern 3 |
| FLS/CRUD posture decision | pattern 6 + `references/selector-security.md` |
| Dynamic/optional filters from user input | pattern 7 |
| Batch Apex start() method | pattern 8 |
| Aggregate or COUNT() query | pattern 9 |
| Reviewing a selector | `references/selector-antipatterns.md` |
| `fflib_QueryFactory` method lookup | `references/query-factory-api.md` |
| Registering the selector, factory wiring | skill `sf-fflib-foundations` |
| Mocking a selector in a test | skill `sf-fflib-testing` |

## Quick reference: constructor matrix

Read from the five `fflib_SObjectSelector` constructors and the field initialisers.

| Constructor | includeFieldSetFields | enforceCRUD | enforceFLS | sortSelectFields | DataAccess |
| --- | --- | --- | --- | --- | --- |
| `fflib_SObjectSelector()` | `false` | `true` | `false` | `true` | `LEGACY` |
| `(Boolean includeFieldSetFields)` | arg | `true` | `false` | `true` | `LEGACY` |
| `(Boolean, DataAccess)` | arg | `false` | `false` | **`false`** | arg |
| `(Boolean, Boolean enforceCRUD, Boolean enforceFLS)` *(deprecated)* | arg | arg | arg | `true` | `LEGACY` |
| `(Boolean, Boolean, Boolean, Boolean sortSelectFields)` *(deprecated)* | arg | arg | arg | arg | `LEGACY` |

The `(Boolean, DataAccess)` constructor is the modern one and it also turns select-field sorting
**off** - your generated SOQL will list fields in `Set<String>` iteration order, not alphabetically.
Tests that assert on a SOQL string must account for that.

`setDataAccess(DataAccess access)` mutates a live selector and, for any value other than `LEGACY`,
forces `ignoreCRUD()` and `m_enforceFLS = false`: legacy checks and native modes are mutually
exclusive by construction.

| Fluent mutator | Effect |
| --- | --- |
| `includeFieldSetFields()` | `m_includeFieldSetFields = true` |
| `ignoreCRUD()` | `m_enforceCRUD = false` |
| `enforceFLS()` *(deprecated)* | `m_enforceFLS = true` |
| `unsortedSelectFields()` | `m_sortSelectFields = false` |
| `setDataAccess(DataAccess)` | sets mode, disables legacy CRUD/FLS when not `LEGACY` |

All five return `fflib_SObjectSelector`, so they chain but do not return your subclass type - assign
before casting.

## Core patterns

### 1. Selector anatomy

```apex
public inherited sharing class AccountsSelector extends fflib_SObjectSelector
    implements IAccountsSelector
{
    public static IAccountsSelector newInstance() {
        return (IAccountsSelector) Application.Selector.newInstance(Account.SObjectType);
    }

    public AccountsSelector() {
        super(false, fflib_SObjectSelector.DataAccess.USER_MODE);
    }

    public Schema.SObjectType getSObjectType() {
        return Account.SObjectType;
    }

    public List<Schema.SObjectField> getSObjectFieldList() {
        return new List<Schema.SObjectField> {
            Account.Id,
            Account.Name,
            Account.AccountNumber,
            Account.LastInvoiceDate__c
        };
    }

    public List<Account> selectById(Set<Id> idSet) {
        return (List<Account>) selectSObjectsById(idSet);
    }
}
```

```apex
public interface IAccountsSelector extends fflib_ISObjectSelector {
    List<Account> selectById(Set<Id> idSet);
}
```

Required members: `getSObjectType()` and `getSObjectFieldList()` are `abstract` on the base class.
Optional overrides: `getSObjectFieldSetList()` (returns `null` by default) and `getOrderBy()`.

`getOrderBy()` default, computed once and cached in `m_orderBy`: the object's Name field if it exists
and is not encrypted, else `CreatedDate`, else `Id`. Override it to return a comma-delimited clause;
`configureQueryFactory` splits on `,`, then on space, recognises `ASC`/`DESC` and detects
`NULLS LAST` case-insensitively:

```apex
public override String getOrderBy() {
    return 'LastInvoiceDate__c DESC NULLS LAST, Name ASC';
}
```

### 2. The two base query methods

```apex
// SELECT <fields> FROM Account WHERE id in :idSet ORDER BY <getOrderBy()> [WITH USER_MODE]
public virtual List<SObject> selectSObjectsById(Set<Id> idSet)   // Database.query
public virtual Database.QueryLocator queryLocatorById(Set<Id> idSet) // Database.getQueryLocator
```

Both call `protected String buildQuerySObjectById()`, which is literally
`newQueryFactory().setCondition('id in :idSet').toSOQL()`. The bind `:idSet` resolves against the
local scope of the method that calls `Database.query`, which is why the parameter is named `idSet`.
**If you re-use `buildQuerySObjectById()` from your own method, the local variable must also be named
`idSet`** or the query throws an unbound-variable `QueryException`.

`getSObjectName()` returns the API name via the cached `fflib_SObjectDescribe`. `sObjectType()` and
`getSObjectType2()` are public aliases of the abstract `getSObjectType()` and exist so mock
registration can read the type (see skill `sf-fflib-foundations`).

### 3. Field sets

```apex
public ProductsSelector(Boolean includeFieldSetFields) {
    super(includeFieldSetFields, fflib_SObjectSelector.DataAccess.USER_MODE);
}

public override List<Schema.FieldSet> getSObjectFieldSetList() {
    return new List<Schema.FieldSet> { SObjectType.Product2.FieldSets.OpportunityDiscount };
}
```

Field set fields are added only when both `m_includeFieldSetFields` is true and
`getSObjectFieldSetList()` is non-null (`configureQueryFactory`). `selectFieldSet` throws
`fflib_QueryFactory.InvalidFieldSetException` if the field set belongs to another SObject, and with
`allowCrossObject = false` it rejects any member whose `getFieldPath()` contains a dot.

Multi-currency: `configureQueryFactory` appends `CurrencyIsoCode` automatically when
`UserInfo.isMultiCurrencyOrganization()` and the SObject has the field. You do not list it.

### 4. Custom query methods

```apex
public List<Account> selectByNameAndRating(Set<String> names, String rating) {
    return (List<Account>) Database.query(
        newQueryFactory()
            .setCondition('Name IN :names AND Rating = :rating')
            .setLimit(200)
            .toSOQL());
}
```

Rules that keep custom methods honest:

| Rule | Reason |
| --- | --- |
| Return a concrete `List<Account>`, never `List<SObject>` | callers should not cast |
| Start from `newQueryFactory()`, never a raw `new fflib_QueryFactory(...)` | you lose the field list, order by and security posture |
| Name locals exactly as the bind tokens in `setCondition` | `Database.query` binds from local scope |
| Guard empty input: `if (idSet.isEmpty()) { return new List<Account>(); }` | saves a SOQL statement against the 100 limit |
| One SOQL per method, never inside a loop | skill `sf-governor-limits` |
| Selective filters on indexed fields | skill `sf-soql-sosl-optimization` |

`newQueryFactory(false)` omits the selector's own field list, which is how you build a narrow
projection query (the samplecode's `selectOpportunityInfo` does exactly this).

### 5. Parent fields and child subselects

```apex
public List<Opportunity> selectByIdWithProducts(Set<Id> idSet) {
    fflib_QueryFactory oppFactory = newQueryFactory();

    // Child subselect: (SELECT ... FROM OpportunityLineItems)
    fflib_QueryFactory lineFactory =
        new OpportunityLineItemsSelector()
            .addQueryFactorySubselect(oppFactory, 'OpportunityLineItems');

    // Parent fields on the child, contributed by other selectors' field lists
    new PricebookEntriesSelector().configureQueryFactoryFields(lineFactory, 'PricebookEntry');
    new ProductsSelector().configureQueryFactoryFields(lineFactory, 'PricebookEntry.Product2');

    return (List<Opportunity>) Database.query(
        oppFactory.setCondition('id in :idSet').toSOQL());
}
```

| Method | Effect |
| --- | --- |
| `addQueryFactorySubselect(parent)` | uses the deprecated `subselectQuery(SObjectType)` overload; logs a `WARN` debug |
| `addQueryFactorySubselect(parent, 'RelationshipName')` | **preferred**; resolves the `ChildRelationship` by name |
| `addQueryFactorySubselect(parent, name, Boolean includeSelectorFields)` | subselect with a hand-picked field list |
| `configureQueryFactoryFields(qf, 'PricebookEntry')` | adds this selector's field list prefixed with the relationship path, plus `CurrencyIsoCode` in MC orgs |

Ad-hoc parent traversal without another selector is just `selectField('Account.Owner.Name')`:
`fflib_QueryFactory.getFieldPath` walks each segment through `fflib_SObjectDescribe`, substitutes
`getRelationshipName()`, and throws `NonReferenceFieldException` when a mid-path segment is not a
lookup or master-detail field. For polymorphic lookups (`Lead.Owner` -> `Group|User`) pass the
intended type: `selectField('Owner.Name', User.SObjectType)`.

Subselects go one level deep; the source comment states this explicitly and the child factory is
created through a private constructor that carries the `ChildRelationship`. `subselectQuery(String)`
throws `InvalidSubqueryRelationshipException` for an unknown relationship name. A subselect never
emits `WITH USER_MODE` - `toSOQL()` only appends the mode clause when `relationship == null`.

### 6. Security posture

| Posture | Constructor | What is enforced | Generated SOQL |
| --- | --- | --- | --- |
| Modern (default choice) | `super(false, DataAccess.USER_MODE)` | object + field read permission by the platform | `... WITH USER_MODE` |
| Explicit elevation | `super(false, DataAccess.SYSTEM_MODE)` | nothing; documents intent | `... WITH SYSTEM_MODE` |
| Legacy assertions | `super(false, true, true)` | `fflib_SecurityUtils` describe checks per field, throws `FlsException`/`CrudException` | no mode clause |
| None | `super()` | CRUD read only (`enforceCRUD` defaults true) | no mode clause |

API version boundary, from the Apex Developer Guide "Apex Security and Sharing Model" versioned
behavior changes: at **67.0 and later** Apex runs in user context by default (object permissions and
FLS enforced unless you opt into system mode), `WITH SECURITY_ENFORCED` is **not allowed** in an
Apex SOQL `SELECT`, and a class with no sharing declaration behaves as `with sharing`. That does not
make the selector setting redundant: `fflib_QueryFactory.toSOQL()` emits a mode clause only for
`USER_MODE`/`SYSTEM_MODE`, so a `LEGACY` selector on a pre-67.0-versioned class still runs in system
context. Pin the posture explicitly with `DataAccess`, and never write `WITH SECURITY_ENFORCED`
except in a comment describing legacy code.

Never mixed: `setDataAccess` disables the legacy flags. Record-level sharing is **not** a selector
setting - `fflib_SObjectSelector` is declared `with sharing`, so `selectSObjectsById` and
`queryLocatorById` enforce sharing, while a query you issue from your own subclass method runs under
your subclass's sharing declaration. Declare `inherited sharing` on selectors unless you have a
reason not to. Full matrix, before/after code and proving tests: `references/selector-security.md`
and skill `sf-security-model`.

### 7. Dynamic filters without SOQL injection

```apex
public List<Account> search(String nameFragment, Set<String> ratings, Integer maxRows) {
    fflib_QueryFactory qf = newQueryFactory();

    List<String> clauses = new List<String>();
    Map<String, Object> binds = new Map<String, Object>();
    if (String.isNotBlank(nameFragment)) {
        clauses.add('Name LIKE :nameLike');
        binds.put('nameLike', '%' + String.escapeSingleQuotes(nameFragment) + '%');
    }
    if (ratings != null && !ratings.isEmpty()) {
        clauses.add('Rating IN :ratings');
        binds.put('ratings', ratings);
    }
    if (!clauses.isEmpty()) {
        qf.setCondition(String.join(clauses, ' AND '));
    }
    qf.setLimit(maxRows == null ? 200 : Math.min(maxRows, 2000));

    return (List<Account>) Database.queryWithBinds(
        qf.toSOQL(), binds, AccessLevel.USER_MODE);
}
```

`Database.queryWithBinds(String, Map<String, Object>, System.AccessLevel)` takes bind values from the
map instead of local scope, so the selector never concatenates a value into the query. Bind keys are
evaluated case-insensitively and must be valid identifiers. Only field *values* may come from the
caller - a caller-supplied field or object name must be validated against
`fflib_SObjectDescribe.getDescribe(getSObjectType()).getFieldsMap()` before it reaches
`selectField`.

### 8. QueryLocator selectors for Batch Apex

```apex
public Database.QueryLocator queryLocatorReadyToInvoice() {
    return Database.getQueryLocator(
        newQueryFactory()
            .setCondition(Opportunity.InvoicedStatus__c + ' = \'Ready\'')
            .toSOQL());
}
```

`queryLocatorById(Set<Id>)` exists on the base class for the id-filtered case. Batch jobs must call
the selector from `start()` and re-query per chunk in `execute()` only through another selector
method - never with inline SOQL. `Database.getQueryLocator` ignores `LIMIT`-based paging
expectations; use `setLimit` only for non-batch queries. Batch integration: skills
`sf-async-apex-patterns` and `sf-fflib-operations`.

### 9. Aggregates live outside the selector contract

`fflib_ISObjectSelector.selectSObjectsById` returns `List<SObject>`, and `fflib_QueryFactory` has no
`COUNT()`/`GROUP BY` support - `toSOQL()` always emits `SELECT <fields>`. Aggregates therefore need a
hand-written query inside the selector, returning a typed wrapper:

```apex
public class OpenPipelineByStage {
    public String stageName;
    public Decimal totalAmount;
    public Integer recordCount;
}

public List<OpenPipelineByStage> selectOpenPipelineByStage(Set<Id> ownerIds) {
    List<OpenPipelineByStage> results = new List<OpenPipelineByStage>();
    for (AggregateResult ar : [
            SELECT StageName stage, SUM(Amount) total, COUNT(Id) cnt
              FROM Opportunity
             WHERE OwnerId IN :ownerIds AND IsClosed = false
             GROUP BY StageName
              WITH USER_MODE]) {
        OpenPipelineByStage row = new OpenPipelineByStage();
        row.stageName = (String) ar.get('stage');
        row.totalAmount = (Decimal) ar.get('total');
        row.recordCount = (Integer) ar.get('cnt');
        results.add(row);
    }
    return results;
}
```

Keep it in the selector class so all SOQL stays in one layer, return the wrapper (never
`AggregateResult`, which is unmockable in a meaningful way), and add `WITH USER_MODE` by hand because
the query factory is not involved.

### 10. Caching

`fflib_SObjectDescribe.getDescribe(...)` caches describes for the transaction; call `flushCache()`
only in tests that mutate metadata expectations. For record caching, do it in the **service** layer
(a `Map<Id, SObject>` for the transaction) or in Platform Cache - never a `static` record map inside
a selector, because it survives across `Test.startTest()` boundaries and hides stale data from the
next caller in the same transaction.

## Anti-patterns

**Selector calling a service or domain.** Creates a cycle and makes the selector impossible to mock.

```apex
// Wrong
public List<Account> selectActive() {
    AccountsService.recalculate(...);   // NO
    return (List<Account>) Database.query(newQueryFactory().toSOQL());
}
```

**Raw `new fflib_QueryFactory(Account.SObjectType)` in a selector method.** Silently drops the field
list, the order by, and the security mode. Always `newQueryFactory()`.

**`getSObjectFieldList()` returning every field.** A 400-field object at 200 rows is a heap problem
and pushes long text fields into memory for no reason. List the fields the layer above actually uses;
add a second selector method with `newQueryFactory(false)` for wide one-off reads.

**One selector class per query.** `AccountByNameSelector`, `AccountByRatingSelector`... The registry
is keyed by SObjectType, so only one can be registered. One selector per SObjectType, many methods.

**Returning `List<SObject>` from a custom method.** Forces every caller to cast and defeats compile-time
checking.

**Unbounded query with no `LIMIT` and a non-selective filter.** See skill
`sf-soql-sosl-optimization`; a selector is exactly where a `QUERY_TIMEOUT` or
`Non-selective query against large object type` surfaces.

**Interpolating caller input into `setCondition`.** `setCondition('Name = \'' + name + '\'')` is
injection. Use bind tokens plus `Database.queryWithBinds`.

**Using the deprecated `enforceCRUD`/`enforceFLS` constructor in new code.** The legacy path resolves
every field through `DescribeFieldResult` on each `selectField` call, which the source itself calls
"computationally expensive". Use `DataAccess.USER_MODE`.

Full list with failing/fixed pairs: `references/selector-antipatterns.md`.

## Verification

```bash
# 1. Selector compiles and the field list is valid against the org's schema.
sf project deploy start --source-dir force-app/main/default/classes/selectors \
  --target-org vf-dev --wait 20

# 2. Inspect the SOQL a selector actually generates, including the mode clause.
sf apex run --target-org vf-dev --file scripts/apex/dump-selector-soql.apex

# 3. Run only the selector tests (they need DML, so they are org tests).
sf apex run test --target-org vf-dev --synchronous \
  --tests AccountsSelectorTest --tests OpportunitiesSelectorTest \
  --code-coverage --result-format human

# 4. Confirm the query plan is selective before shipping a new filter.
sf data query --target-org vf-dev --query \
  "SELECT Id FROM Account WHERE LastInvoiceDate__c = LAST_N_DAYS:7" --result-format csv

# 5. Gates: analyzer (ApexCRUDViolation/ApexSOQLInjection) and coverage.
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" analyzer
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex --target-org vf-dev
```

`scripts/apex/dump-selector-soql.apex`:

```apex
AccountsSelector sel = new AccountsSelector();
System.debug(sel.newQueryFactory().setCondition('id in :idSet').toSOQL());
System.debug('DataAccess=' + sel.getDataAccess()
    + ' CRUD=' + sel.isEnforcingCRUD()
    + ' FLS=' + sel.isEnforcingFLS()
    + ' fieldSets=' + sel.isIncludeFieldSetFields());
```

Expected output for a `DataAccess.USER_MODE` selector ends in `... WITH USER_MODE ORDER BY Name ASC
NULLS FIRST` - if `WITH USER_MODE` is missing, the constructor is wrong. Use `vf-check apex` output
in `<project>/.vibeforce/reports/` as the coverage evidence.

## References

- [references/query-factory-api.md](references/query-factory-api.md) - complete `fflib_QueryFactory` method table with generated SOQL
- [references/selector-recipes.md](references/selector-recipes.md) - twelve complete selector classes
- [references/selector-security.md](references/selector-security.md) - enforcement matrix, before/after, proving tests
- [references/selector-antipatterns.md](references/selector-antipatterns.md) - failing code and the fix
- Skill `sf-fflib-foundations` - registering the selector in `Application.cls`
- Skill `sf-fflib-domain-service-uow` - who is allowed to call a selector
- Skill `sf-fflib-testing` - `Application.Selector.setMock`
- Skill `sf-fflib-operations` - selectors in triggers, batch and packaging
- Skill `sf-soql-sosl-optimization`, `sf-governor-limits`, `sf-security-model`, `sf-data-management`
- SOQL `WITH USER_MODE`: https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_enforce_usermode.htm
- Dynamic SOQL and `Database.queryWithBinds`: https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_dynamic_soql.htm
- `System.AccessLevel`: https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_class_System_AccessLevel.htm
