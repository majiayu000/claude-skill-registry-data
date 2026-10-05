---
name: legacy-modernizer
description: Modernize legacy codebases using proven migration strategies like Strangler Fig pattern. Use when upgrading frameworks, migrating to new architectures.
---

# Legacy Modernizer

Specialized expertise in modernizing legacy codebases using proven migration strategies and patterns. Provides guidance on upgrading frameworks, migrating architectures, and incrementally improving old code while maintaining system stability.

## When to Use This Skill

Use this skill for:

- Upgrading to new framework versions
- Migrating from monolith to microservices
- Replacing deprecated APIs
- Modernizing database access patterns
- Updating authentication/authorization
- Moving from on-premises to cloud
- Incrementally improving without rewrites

**Trigger phrases**: "legacy code", "modernize", "migrate", "upgrade framework", "deprecated", "technical debt", "old codebase", "outdated"

## What This Skill Does

Provides modernization guidance including:

- **Assessment**: Evaluating legacy code health and risk
- **Strategy Selection**: Choosing appropriate migration approach
- **Incremental Migration**: Step-by-step modernization
- **Risk Mitigation**: Maintaining stability during changes
- **Compatibility**: Managing old/new code coexistence
- **Validation**: Ensuring feature parity

## Instructions

### Step 1: Assess the Legacy System

**Legacy Assessment Framework**:

```markdown
## Legacy System Assessment: [System Name]

### System Profile
| Attribute | Value | Risk Level |
|-----------|-------|------------|
| Age | [years] | [H/M/L] |
| Lines of Code | [count] | [H/M/L] |
| Technology Stack | [list] | [H/M/L] |
| Test Coverage | [%] | [H/M/L] |
| Documentation | [level] | [H/M/L] |
| Active Maintainers | [count] | [H/M/L] |

### Technical Debt Inventory
| Area | Debt Type | Severity | Effort to Fix |
|------|-----------|----------|---------------|
| [Component] | [Type] | High/Med/Low | [S/M/L/XL] |

### Dependency Analysis
| Dependency | Current Version | Latest | EOL Status |
|------------|-----------------|--------|------------|
| [Library] | [version] | [version] | [date/active] |

### Pain Points
1. [Pain point 1 - description and impact]
2. [Pain point 2 - description and impact]
3. [Pain point 3 - description and impact]

### Modernization Priority Score
**Overall Risk**: [1-10]
**Business Impact**: [1-10]
**Modernization Urgency**: [calculated]
```

### Step 2: Select Migration Strategy

**Strategy Selection Matrix**:

| Strategy | When to Use | Risk | Duration | Team Size |
|----------|-------------|------|----------|-----------|
| **Big Bang Rewrite** | Small system, new team | Very High | Long | Large |
| **Strangler Fig** | Large system, gradual | Low | Long | Any |
| **Branch by Abstraction** | Internal components | Medium | Medium | Small |
| **Parallel Run** | Critical systems | Low | Medium | Medium |
| **Feature Toggle** | User-facing features | Low | Short | Any |

**Recommended: Strangler Fig Pattern**

```
┌─────────────────────────────────────────────────────────────────┐
│                     STRANGLER FIG PATTERN                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: Initial State     Phase 2: Introduce New             │
│  ┌───────────────────┐      ┌───────────────────┐              │
│  │   Legacy System   │      │   Legacy System   │              │
│  │   ┌───────────┐   │      │   ┌───────────┐   │              │
│  │   │Feature A  │   │      │   │Feature A  │   │              │
│  │   │Feature B  │   │      │   │Feature B  │   │              │
│  │   │Feature C  │   │      │   │Feature C  │   │              │
│  │   └───────────┘   │      │   └───────────┘   │              │
│  └───────────────────┘      └─────────┬─────────┘              │
│           │                           │                        │
│           ▼                           ▼                        │
│       [Users]                 ┌───────────────┐                │
│                               │ Proxy/Router  │                │
│                               └───────┬───────┘                │
│                                       │                        │
│                               ┌───────▼───────┐                │
│                               │  New System   │                │
│                               │ ┌───────────┐ │                │
│                               │ │Feature A' │ │                │
│                               │ └───────────┘ │                │
│                               └───────────────┘                │
│                                                                 │
│  Phase 3: Expand             Phase 4: Complete                 │
│  ┌───────────────────┐      ┌───────────────────┐              │
│  │   Legacy System   │      │                   │              │
│  │   ┌───────────┐   │      │   [Deprecated]    │              │
│  │   │Feature C  │   │      │                   │              │
│  │   └───────────┘   │      └───────────────────┘              │
│  └─────────┬─────────┘                                         │
│            │                           │                        │
│            ▼                           ▼                        │
│    ┌───────────────┐           ┌───────────────┐               │
│    │ Proxy/Router  │           │  New System   │               │
│    └───────┬───────┘           │ ┌───────────┐ │               │
│            │                   │ │Feature A' │ │               │
│    ┌───────▼───────┐           │ │Feature B' │ │               │
│    │  New System   │           │ │Feature C' │ │               │
│    │ ┌───────────┐ │           │ └───────────┘ │               │
│    │ │Feature A' │ │           └───────────────┘               │
│    │ │Feature B' │ │                   │                        │
│    │ └───────────┘ │                   ▼                        │
│    └───────────────┘               [Users]                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Step 3: Plan the Migration

**Migration Plan Template**:

```markdown
## Migration Plan: [System/Component]

### Scope
**Migrating from**: [Old system/version]
**Migrating to**: [New system/version]
**Timeline**: [Duration]

### Migration Phases

#### Phase 1: Foundation (Week 1-2)
- [ ] Set up new system infrastructure
- [ ] Create routing/proxy layer
- [ ] Establish monitoring and logging
- [ ] Define rollback procedures

**Success Criteria**: New system deployed, no traffic routed

#### Phase 2: First Feature Migration (Week 3-4)
- [ ] Select lowest-risk feature: [Feature name]
- [ ] Implement in new system
- [ ] Add feature toggle
- [ ] Test with synthetic traffic
- [ ] Route 5% of traffic to new system
- [ ] Monitor and validate
- [ ] Gradually increase to 100%

**Success Criteria**: First feature fully migrated

#### Phase 3: Expand Migration (Week 5-12)
| Feature | Priority | Complexity | Target Week |
|---------|----------|------------|-------------|
| [Feature B] | High | Medium | Week 5-6 |
| [Feature C] | Medium | High | Week 7-9 |
| [Feature D] | Low | Low | Week 10-11 |

#### Phase 4: Cleanup (Week 13-14)
- [ ] Remove routing to legacy
- [ ] Archive legacy code
- [ ] Update documentation
- [ ] Decommission old infrastructure

### Risk Mitigation
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Data inconsistency | Medium | High | Dual-write during transition |
| Performance regression | Low | High | Load testing before cutover |
| Feature gap | Medium | Medium | Comprehensive testing |

### Rollback Plan
1. Feature toggle to route back to legacy
2. Database sync if needed
3. Communication plan
```

### Step 4: Implement Migration Patterns

#### Pattern 1: API Gateway Migration

```python
# routing_layer.py
from flask import Flask, request
import requests

app = Flask(__name__)

# Feature flags for migration
MIGRATED_ENDPOINTS = {
    '/api/users': True,      # Migrated to new system
    '/api/orders': False,    # Still on legacy
    '/api/products': 'canary'  # Canary deployment (10%)
}

LEGACY_URL = "http://legacy-system:8080"
NEW_URL = "http://new-system:8080"

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_request(path):
    full_path = f'/api/{path}'

    # Determine target system
    migration_status = MIGRATED_ENDPOINTS.get(full_path, False)

    if migration_status == True:
        target = NEW_URL
    elif migration_status == 'canary':
        # 10% to new system
        import random
        target = NEW_URL if random.random() < 0.1 else LEGACY_URL
    else:
        target = LEGACY_URL

    # Forward request
    response = requests.request(
        method=request.method,
        url=f"{target}{full_path}",
        headers={k: v for k, v in request.headers if k != 'Host'},
        data=request.get_data(),
        params=request.args
    )

    return response.content, response.status_code, response.headers.items()
```

#### Pattern 2: Database Migration with Dual-Write

```python
# dual_write_repository.py
class DualWriteUserRepository:
    """Writes to both old and new database during migration"""

    def __init__(self, legacy_db, new_db, read_from_new=False):
        self.legacy_db = legacy_db
        self.new_db = new_db
        self.read_from_new = read_from_new

    def create_user(self, user_data):
        # Write to both databases
        legacy_result = self.legacy_db.insert_user(user_data)
        new_result = self.new_db.insert_user(self._transform_to_new_schema(user_data))

        # Verify consistency
        if legacy_result.id != new_result.id:
            self._log_inconsistency('create', legacy_result, new_result)

        return new_result if self.read_from_new else legacy_result

    def get_user(self, user_id):
        if self.read_from_new:
            return self.new_db.get_user(user_id)
        return self.legacy_db.get_user(user_id)

    def _transform_to_new_schema(self, data):
        """Transform data from legacy to new schema"""
        return {
            'id': data['user_id'],  # Renamed field
            'email': data['email'].lower(),  # Normalized
            'full_name': f"{data['first_name']} {data['last_name']}",  # Combined
            'created_at': data.get('created', datetime.now())
        }

    def _log_inconsistency(self, operation, legacy, new):
        logger.warning(f"Dual-write inconsistency in {operation}: "
                      f"legacy={legacy}, new={new}")
```

#### Pattern 3: Feature Toggle Migration

```python
# feature_flags.py
class FeatureFlags:
    """Feature flag system for gradual migration"""

    def __init__(self, config_source):
        self.flags = config_source.load_flags()

    def is_enabled(self, feature_name, user_id=None):
        flag = self.flags.get(feature_name)
        if not flag:
            return False

        # Boolean flag
        if isinstance(flag, bool):
            return flag

        # Percentage rollout
        if 'percentage' in flag:
            return self._check_percentage(flag['percentage'], user_id)

        # User whitelist
        if 'users' in flag:
            return user_id in flag['users']

        return flag.get('default', False)

    def _check_percentage(self, percentage, user_id):
        if user_id is None:
            return False
        # Consistent hashing so same user always gets same result
        hash_value = hash(f"{user_id}") % 100
        return hash_value < percentage

# Usage
flags = FeatureFlags(config)

def get_user_profile(user_id):
    if flags.is_enabled('new_profile_page', user_id):
        return new_profile_service.get_profile(user_id)
    else:
        return legacy_profile_service.get_profile(user_id)
```

### Step 5: Validate Migration

**Validation Checklist**:

```markdown
## Migration Validation: [Feature/Component]

### Functional Validation
- [ ] All existing functionality preserved
- [ ] Edge cases handled correctly
- [ ] Error handling matches or improves
- [ ] API contracts maintained

### Performance Validation
| Metric | Legacy | New | Status |
|--------|--------|-----|--------|
| Response time (p50) | [ms] | [ms] | ✅/❌ |
| Response time (p99) | [ms] | [ms] | ✅/❌ |
| Throughput | [rps] | [rps] | ✅/❌ |
| Error rate | [%] | [%] | ✅/❌ |

### Data Validation
- [ ] Data migrated completely
- [ ] Data transformed correctly
- [ ] No data loss
- [ ] Referential integrity maintained

### Integration Validation
- [ ] Upstream systems work correctly
- [ ] Downstream systems receive correct data
- [ ] External APIs compatible
- [ ] Event/message contracts maintained

### Rollback Validation
- [ ] Rollback procedure tested
- [ ] Data can be synced back if needed
- [ ] Time to rollback acceptable
```

### Step 6: Document and Clean Up

**Post-Migration Documentation**:

```markdown
## Migration Complete: [System/Component]

### Summary
- **Started**: [date]
- **Completed**: [date]
- **Duration**: [weeks]

### What Changed
| Aspect | Before | After |
|--------|--------|-------|
| Framework | [old] | [new] |
| Database | [old] | [new] |
| Architecture | [old] | [new] |

### Migration Statistics
- Lines of code migrated: [count]
- APIs migrated: [count]
- Data records migrated: [count]
- Zero-downtime achieved: Yes/No

### Lessons Learned
1. [Lesson 1]
2. [Lesson 2]
3. [Lesson 3]

### Cleanup Tasks
- [ ] Remove legacy code
- [ ] Update documentation
- [ ] Archive old infrastructure
- [ ] Remove feature flags
- [ ] Update monitoring

### Future Considerations
- [Recommendations for similar migrations]
```

## Best Practices

- **Incremental over big-bang** - Small changes, frequent validation
- **Test coverage first** - Add tests before migrating
- **Parallel run** - Validate before switching
- **Feature flags** - Enable quick rollback
- **Monitor closely** - Watch metrics during migration
- **Document everything** - Future maintainers will thank you
- **Celebrate milestones** - Migration is hard work
- **Don't gold-plate** - Migrate first, optimize later

## Common Patterns

### Pattern: Version Coexistence

```python
# Support multiple API versions during migration
@app.route('/api/v1/users')
def users_v1():
    return legacy_users_handler()

@app.route('/api/v2/users')
def users_v2():
    return new_users_handler()

# Deprecation header for v1
@app.after_request
def add_deprecation_header(response):
    if '/api/v1/' in request.path:
        response.headers['Deprecation'] = 'true'
        response.headers['Sunset'] = 'Sat, 01 Jan 2027 00:00:00 GMT'
    return response
```

## Quality Checklist

- [ ] Legacy system fully assessed
- [ ] Migration strategy selected and documented
- [ ] Phased plan created
- [ ] Rollback procedures defined
- [ ] Feature flags/toggles in place
- [ ] Monitoring configured
- [ ] Validation criteria defined
- [ ] Team aligned on approach

## Related Skills

- `refactoring-expert` - Code-level improvements
- `dependency-manager` - Upgrading dependencies
- `context-manager` - Understanding legacy code
- `cicd-architect` - Deployment strategies

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Based on**: Martin Fowler's patterns, awesome-claude-code-subagents


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
