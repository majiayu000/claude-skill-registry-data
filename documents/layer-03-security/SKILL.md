---
name: LAYER_03_SECURITY
description: Expert knowledge for Security Layer modeling in Documentation Robotics
triggers:
  [
    "security",
    "authentication",
    "authorization",
    "role",
    "permission",
    "RBAC",
    "ABAC",
    "policy",
    "threat",
    "actor objective",
    "STS-ml",
  ]
version: 0.6.0
---

# Security Layer Skill

**Layer Number:** 03
**Specification:** Metadata Model Spec v0.6.0
**Purpose:** Defines authentication, authorization, access control, data classification, and security policies including STS-ml concepts for goal-oriented security modeling.

---

## Layer Overview

The Security Layer provides **comprehensive security modeling** spanning:

- **Authentication & Authorization** - RBAC, ABAC, field-level access control
- **Goal-Oriented Security** - Actor objectives, social dependencies (STS-ml inspired)
- **Information Flow Rights** - Fine-grained rights: produce, read, modify, distribute
- **Security Patterns** - Separation of duty, binding of duty, need-to-know
- **Threat Modeling** - Threats, countermeasures, accountability

This layer uses a **custom YAML specification** designed to cover authentication, authorization, data classification, threat modeling, and goal-oriented security in a unified model.

**Key Innovation:** Integrates STS-ml 2.0 concepts (goal-oriented security, information flow, delegation, social dependencies) with modern RBAC/ABAC patterns.

---

## Entity Types

### Authentication & Authorization (14 entities)

| Entity Type              | Description                                                                                         |
| ------------------------ | --------------------------------------------------------------------------------------------------- |
| **SecurityModel**        | Root container for complete security model                                                          |
| **AuthenticationConfig** | Authentication providers (OAuth2, OIDC, SAML, JWT, session, API key, certificate)                   |
| **PasswordPolicy**       | Password requirements and policies                                                                  |
| **Role**                 | User role definition with inheritance and hierarchy                                                 |
| **Permission**           | Permission definition with scopes (global, resource, attribute, owner) and format "resource.action" |
| **SecureResource**       | Protected resource (types: api, screen, data, file, service)                                        |
| **ResourceOperation**    | Operation on a resource with role-based access, conditions, rate limits, audit                      |
| **AccessCondition**      | Conditional access rule with operators and data sources                                             |
| **FieldAccessControl**   | Field-level access control with read/write permissions and masking                                  |
| **SecurityPolicy**       | Declarative security policy with rules and actions                                                  |
| **PolicyRule**           | Individual policy rule with conditions and effects (allow, deny, audit, warn)                       |
| **PolicyAction**         | Action to take when policy rule matches                                                             |
| **DataClassification**   | Data classification and protection policies (levels: public, internal, confidential, restricted)    |
| **RateLimit**            | Throttling constraints for API/service access                                                       |

### STS-ml Inspired Security (17 entities)

| Entity Type                   | Description                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------ |
| **Actor**                     | Security actor (types: role, agent, organization, system) with objectives and dependencies |
| **ActorObjective**            | Security-related goal of an actor (links to motivation layer goals)                        |
| **ActorDependency**           | Dependency between actors on resources                                                     |
| **InformationEntity**         | Information asset with fine-grained rights (produce, read, modify, distribute)             |
| **InformationRight**          | Fine-grained information access rights per actor                                           |
| **Delegation**                | Explicit delegation of permissions or goals (types: execution, permission, approval)       |
| **SecurityConstraints**       | Container for security patterns (separation/binding of duty, need-to-know)                 |
| **SeparationOfDuty**          | Pattern requiring different actors to perform related tasks                                |
| **BindingOfDuty**             | Pattern requiring same actor to complete related tasks                                     |
| **NeedToKnow**                | Information access based on objective/purpose requirements                                 |
| **SocialDependency**          | Dependencies and trust between actors with verification levels                             |
| **AccountabilityRequirement** | Accountability and non-repudiation requirements                                            |
| **Evidence**                  | Evidence required for accountability (digital-signature, timestamp, IP, biometric, etc.)   |
| **Threat**                    | Security threat with likelihood, impact, and countermeasures                               |
| **Countermeasure**            | Security countermeasure for a threat                                                       |
| **AuditConfig**               | Security audit logging configuration                                                       |
| **RetentionPolicy**           | Data retention and deletion policies                                                       |

---

## Intra-Layer Relationships

Security layer uses **containment relationships** rather than explicit ArchiMate-style relationships:

### Containment Hierarchy

```
SecurityModel
├── contains → AuthenticationConfig
├── contains → Actors []
│   └── each Actor contains → ActorObjectives [], ActorDependencies []
├── contains → Roles []
├── contains → Permissions []
├── contains → SecureResources []
│   └── each SecureResource contains → ResourceOperations []
│       └── each ResourceOperation contains → AccessConditions [], FieldAccessControls []
├── contains → InformationEntities []
│   └── each InformationEntity contains → InformationRights []
├── contains → Delegations []
├── contains → SecurityConstraints
│   ├── contains → SeparationOfDuty []
│   ├── contains → BindingOfDuty []
│   └── contains → NeedToKnow []
├── contains → SecurityPolicies []
│   └── each SecurityPolicy contains → PolicyRules []
│       └── each PolicyRule contains → PolicyActions []
├── contains → DataClassification
├── contains → SocialDependencies []
├── contains → AccountabilityRequirements []
│   └── each AccountabilityRequirement contains → Evidence []
└── contains → Threats []
    └── each Threat contains → Countermeasures []
```

### Key Relationship Patterns

| Source           | Relationship  | Target              | Example                                                  |
| ---------------- | ------------- | ------------------- | -------------------------------------------------------- |
| Actor            | has-objective | ActorObjective      | "Support Agent" has objective "Resolve Customer Issues"  |
| Actor            | depends-on    | InformationEntity   | Actor depends on information to achieve objectives       |
| Actor            | delegates-to  | Actor               | "Manager" delegates "Approval Permission" to "Team Lead" |
| Role             | inherits-from | Role                | "Admin" inherits from "User"                             |
| Permission       | applies-to    | SecureResource      | "users.read" applies to "UserData" resource              |
| PolicyRule       | evaluates     | AccessCondition     | Rule evaluates ABAC conditions                           |
| Threat           | mitigated-by  | Countermeasure      | "SQL Injection" mitigated by "Input Validation"          |
| ActorObjective   | references    | Goal (Layer 1)      | Security objective links to business goal                |
| SocialDependency | defines       | Actor → Actor trust | "Vendor" depends on "Company" for payment                |

---

## Cross-Layer References

### Outgoing References (Security → Other Layers)

| Target Layer              | Reference Type                                   | Example                                                   |
| ------------------------- | ------------------------------------------------ | --------------------------------------------------------- |
| **Layer 1 (Motivation)**  | Actor references **Stakeholder**                 | Security actor maps to business stakeholder               |
| **Layer 1 (Motivation)**  | ActorObjective references **Goal**               | "Protect Customer Data" objective links to "Privacy Goal" |
| **Layer 1 (Motivation)**  | Threat references **Assessment**                 | Threat is a risk assessment                               |
| **Layer 1 (Motivation)**  | Countermeasure implements **Requirement**        | Security control fulfills security requirement            |
| **Layer 1 (Motivation)**  | SocialDependency references **Constraint**       | Trust commitments are constraints                         |
| **Layer 2 (Business)**    | Actor references **BusinessActor**               | Security actor maps to business role                      |
| **Layer 2 (Business)**    | SecurityConstraints apply to **BusinessProcess** | Separation of duty applies to business tasks              |
| **Layer 4 (Application)** | SecureResource references **ApplicationService** | Protects application components                           |
| **Layer 4 (Application)** | SecureResource references **DataObject**         | Protects application data                                 |
| **Layer 6 (API)**         | SecureResource references **API Operations**     | API endpoint security                                     |
| **Layer 6 (API)**         | SecurityScheme maps to **API SecurityScheme**    | OAuth2 config maps to OpenAPI security                    |
| **Layer 5 (Technology)**  | Artifact **encryption** property                 | Data-at-rest encryption                                   |
| **Layer 5 (Technology)**  | Artifact **classification** property             | Data classification levels                                |
| **Layer 11 (APM)**        | AuditConfig **retention**                        | Audit log retention policies                              |
| **Layer 11 (APM)**        | AuditConfig **monitoring**                       | Security event monitoring                                 |

### Incoming References (Lower Layers → Security)

Lower layers reference Security layer to:

- Apply authentication/authorization to services and APIs
- Enforce data classification on artifacts and data objects
- Implement security policies and access controls

---

## Codebase Detection Patterns

### Pattern 1: Role-Based Access Control (RBAC)

```python
# FastAPI with role-based authorization
from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

def require_role(role: Role):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Check user role
            pass
        return wrapper
    return decorator

@app.get("/admin/users")
@require_role(Role.ADMIN)
async def list_users():
    pass
```

**Maps to:**

- Role: "Admin", "User", "Guest"
- SecureResource: "/admin/users" (type: api)
- ResourceOperation: "list_users" (allowed-roles: [admin])

### Pattern 2: Permission-Based Authorization

```typescript
// Permission definitions
export const Permissions = {
  USERS_READ: 'users.read',
  USERS_WRITE: 'users.write',
  USERS_DELETE: 'users.delete',
  ORDERS_READ: 'orders.read',
  ORDERS_WRITE: 'orders.write'
} as const;

@RequirePermission(Permissions.USERS_WRITE)
async updateUser(userId: string, data: UpdateUserDto) {
  // Implementation
}
```

**Maps to:**

- Permission entities: "users.read", "users.write", "users.delete", "orders.read", "orders.write"
- SecureResource: "users", "orders"
- ResourceOperation: "updateUser" (required-permissions: ["users.write"])

### Pattern 3: Attribute-Based Access Control (ABAC)

```python
# Policy-based access with conditions
class AccessPolicy:
    def can_access(self, user, resource, action):
        if action == "read" and resource.classification == "public":
            return True
        if action == "write" and user.department == resource.owner_department:
            return True
        if user.role == "admin":
            return True
        return False
```

**Maps to:**

- AccessCondition with field comparisons
- PolicyRule with conditions and effects
- SecurityPolicy containing multiple rules

### Pattern 4: Authentication Configuration

```yaml
# OAuth2 configuration
authentication:
  providers:
    - type: oauth2
      name: google
      client_id: ${GOOGLE_CLIENT_ID}
      authorization_url: https://accounts.google.com/o/oauth2/v2/auth
      token_url: https://oauth2.googleapis.com/token
      scopes: [openid, email, profile]
    - type: jwt
      name: internal
      secret: ${JWT_SECRET}
      expiration: 3600
```

**Maps to:**

- AuthenticationConfig with providers array
- Properties: type, authorization-url, token-url, scopes

### Pattern 5: Field-Level Security

```python
# Data masking based on role
class UserSerializer:
    def serialize(self, user: User, requester_role: Role):
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email if requester_role in [Role.ADMIN, Role.MANAGER] else "***@***.com",
            "ssn": user.ssn if requester_role == Role.ADMIN else "***-**-****"
        }
        return data
```

**Maps to:**

- FieldAccessControl on "email" and "ssn" fields
- Masking strategies: "email" (partial), "redact" (full)
- Role-based field access

### Pattern 6: Threat Modeling Comments

```python
# THREAT: SQL Injection via user input
# COUNTERMEASURE: Parameterized queries
def get_user_by_email(email: str):
    # Safe: uses parameterized query
    query = "SELECT * FROM users WHERE email = ?"
    return db.execute(query, [email])
```

**Maps to:**

- Threat: "SQL Injection" (likelihood: high, impact: critical)
- Countermeasure: "Parameterized Queries"
- Threat mitigated-by Countermeasure

---

## Modeling Workflow

### Step 1: Define Authentication Configuration

```bash
# Create security model
dr add security model "application-security" \
  --description "Complete security model for the application"

# Add authentication providers
dr add security authentication-config "oauth2-google" \
  --properties provider=oauth2,name=google,scopes=openid:email:profile \
  --description "Google OAuth2 authentication"

dr add security authentication-config "jwt-internal" \
  --properties provider=jwt,expiration=3600 \
  --description "Internal JWT authentication"
```

### Step 2: Define Roles and Permissions

```bash
# Add roles
dr add security role "admin" \
  --properties hierarchy=1 \
  --description "System administrator with full access"

dr add security role "user" \
  --properties hierarchy=2,inherits-from=guest \
  --description "Regular authenticated user"

dr add security role "guest" \
  --properties hierarchy=3 \
  --description "Unauthenticated visitor"

# Add permissions
dr add security permission "users.read" \
  --properties scope=resource,resource=users,action=read \
  --description "Read access to user data"

dr add security permission "users.write" \
  --properties scope=resource,resource=users,action=write \
  --description "Write access to user data"

dr add security permission "admin.all" \
  --properties scope=global \
  --description "Full administrative access"
```

### Step 3: Define Secure Resources

```bash
# Protected API endpoint
dr add security secure-resource "user-api" \
  --properties type=api,path=/api/users \
  --description "User management API endpoints"

# Add resource operation
dr add security resource-operation "list-users" \
  --properties resource=user-api,method=GET,allowed-roles=admin:manager \
  --description "List all users operation"

dr add security resource-operation "create-user" \
  --properties resource=user-api,method=POST,required-permissions=users.write \
  --description "Create new user operation"
```

### Step 4: Define Security Actors and Objectives (STS-ml)

```bash
# Security actors
dr add security actor "support-agent" \
  --properties type=role \
  --description "Customer support team member"

# Actor objectives (link to motivation goals)
dr add security actor-objective "resolve-customer-issues" \
  --properties actor=support-agent \
  --description "Provide timely customer support"

# Link objective to motivation layer
dr relationship add "security/actor-objective/resolve-customer-issues" \
  supports "motivation/goal/customer-satisfaction"

# Actor dependencies
dr add security actor-dependency "support-needs-customer-data" \
  --properties depender=support-agent,dependee=system,resource=customer-information \
  --description "Support agent requires customer data to resolve issues"
```

### Step 5: Define Information Entities and Rights

```bash
# Information entity (STS-ml)
dr add security information-entity "customer-pii" \
  --properties classification=confidential \
  --description "Customer personally identifiable information"

# Information rights (produce, read, modify, distribute)
dr add security information-right "support-read-pii" \
  --properties entity=customer-pii,actor=support-agent,rights=read \
  --description "Support can read customer PII"

dr add security information-right "admin-full-pii" \
  --properties entity=customer-pii,actor=admin,rights=produce:read:modify:distribute \
  --description "Admin has full rights to customer PII"
```

### Step 6: Define Security Constraints (Patterns)

```bash
# Separation of duty
dr add security separation-of-duty "approve-payment-sod" \
  --properties tasks=create-payment:approve-payment \
  --description "Payment creation and approval must be done by different actors"

# Binding of duty
dr add security binding-of-duty "handle-refund-bod" \
  --properties tasks=initiate-refund:complete-refund \
  --description "Same actor must initiate and complete refund process"

# Need to know
dr add security need-to-know "customer-data-ntk" \
  --properties information=customer-pii,objective=resolve-customer-issues \
  --description "Access to customer PII only when resolving customer issues"
```

### Step 7: Model Threats and Countermeasures

```bash
# Identify threats
dr add security threat "sql-injection" \
  --properties likelihood=high,impact=critical,category=injection \
  --description "SQL injection via user input fields"

# Add countermeasures
dr add security countermeasure "parameterized-queries" \
  --properties threat=sql-injection,status=implemented \
  --description "Use parameterized queries for all database operations"

# Link threat to motivation layer
dr relationship add "security/threat/sql-injection" \
  references "motivation/assessment/security-vulnerability-risk"
```

### Step 8: Define Policies (ABAC)

```bash
# Declarative security policy
dr add security policy "data-access-policy" \
  --properties priority=100,enabled=true \
  --description "Attribute-based data access control"

# Policy rule
dr add security policy-rule "owner-can-write" \
  --properties policy=data-access-policy,effect=allow \
  --description "Resource owner can write to their own resources"

# Access condition (ABAC expression)
dr add security access-condition "is-owner" \
  --properties field=resource.owner_id,operator=equals,value=user.id \
  --description "User is the resource owner"
```

### Step 9: Cross-Layer Integration

```bash
# Link to application layer
dr relationship add "security/secure-resource/user-api" \
  protects "application/service/user-management-api"

# Link to API layer
dr relationship add "security/resource-operation/list-users" \
  protects "api/operation/get-users"

# Link to motivation layer
dr relationship add "security/actor/support-agent" \
  references "motivation/stakeholder/customer-support-team"
```

### Step 10: Validate

```bash
dr validate --layer security
dr validate --validate-relationships
```

---

## Security Modeling Patterns

### Pattern 1: RBAC with Role Hierarchy

```
Role: "Admin" (hierarchy: 1)
├── inherits-from → Role: "Manager" (hierarchy: 2)
│   ├── inherits-from → Role: "User" (hierarchy: 3)
│   │   └── inherits-from → Role: "Guest" (hierarchy: 4)
│   └── has-permission → Permission: "users.write"
├── has-permission → Permission: "admin.all"
└── allowed-on → ResourceOperation: "delete-user"
```

### Pattern 2: Goal-Oriented Security (STS-ml)

```
Actor: "Data Analyst"
├── has-objective → ActorObjective: "Generate Business Reports"
│   └── supports → Goal: "Data-Driven Decisions" (Layer 1)
├── depends-on → InformationEntity: "Sales Data"
│   ├── has-right → InformationRight: "read" (Data Analyst)
│   └── classification: "internal"
└── subject-to → NeedToKnow: "Access sales data only for reporting objectives"
```

### Pattern 3: Delegation Chain

```
Actor: "CEO"
└── delegates-to → Delegation: "Budget Approval"
    ├── delegatee → Actor: "CFO"
    ├── type: "approval"
    ├── retain-oversight: true
    └── delegates-to → Delegation: "Department Budget"
        ├── delegatee → Actor: "Department Head"
        └── retain-oversight: true
```

### Pattern 4: Threat Model with Countermeasures

```
Threat: "Unauthorized API Access"
├── likelihood: "high"
├── impact: "critical"
├── category: "broken-authentication"
└── mitigated-by → Countermeasure: "JWT Authentication"
    ├── status: "implemented"
    └── mitigated-by → Countermeasure: "Rate Limiting"
        ├── status: "implemented"
        └── mitigated-by → Countermeasure: "API Key Rotation"
            └── status: "planned"
```

---

## STS-ml 2.0 Concepts

The Security Layer integrates **STS-ml 2.0** (Socio-Technical Security Modeling Language) concepts:

### 1. Goal-Oriented Security

- **Actor Objectives** link to Motivation Layer goals
- Security is justified by business goals
- Traceability: Why do we need this security control?

### 2. Information Flow Rights

- **Produce** - Create new information
- **Read** - Access information
- **Modify** - Update existing information
- **Distribute** - Share information with others

### 3. Delegation

- Explicit delegation chains (execution, permission, approval)
- Retention of oversight/control
- Delegation constraints (time-bound, scope-limited)

### 4. Security Patterns

- **Separation of Duty** - Prevent fraud by requiring multiple actors
- **Binding of Duty** - Ensure accountability by requiring same actor
- **Need to Know** - Limit access based on objectives

### 5. Social Dependencies

- Trust relationships between actors
- Verification levels (low, medium, high)
- Depender → Dependee relationships

### 6. Accountability

- Non-repudiation requirements
- Evidence collection (digital signatures, timestamps, audit logs)
- Proof of action

---

## Best Practices

1. **Start with Authentication, Then Authorization** - Get identity right before access control
2. **Use RBAC for Coarse-Grained, ABAC for Fine-Grained** - Roles for broad access, attributes for specific conditions
3. **Model Threats Early** - Security by design, not afterthought
4. **Link to Motivation Layer** - Justify security controls with business goals
5. **Use STS-ml for Compliance** - Goal-oriented security helps with SOX, GDPR, HIPAA
6. **Separate Authentication from Authorization** - Different concerns, different models
7. **Document Delegation Chains** - Explicit delegation prevents confusion
8. **Apply Security Patterns** - Use separation/binding of duty where applicable
9. **Classify Data Early** - Data classification drives access control
10. **Audit Everything Sensitive** - Enable AuditConfig for sensitive operations

---

## Validation Tips

| Issue                        | Cause                                          | Fix                                  |
| ---------------------------- | ---------------------------------------------- | ------------------------------------ |
| Orphaned Actor               | Actor has no objectives or dependencies        | Add actor objectives or remove actor |
| Unmapped Threat              | Threat has no countermeasures                  | Add countermeasures or accept risk   |
| Unused Permission            | Permission not assigned to roles or operations | Assign to roles or remove            |
| Missing Field-Level Security | Sensitive data lacks FieldAccessControl        | Add field-level access rules         |
| Unlinked Objective           | ActorObjective doesn't link to motivation goal | Add cross-layer link                 |
| No Evidence                  | AccountabilityRequirement lacks evidence       | Define required evidence types       |
| Incomplete Delegation        | Delegation chain missing delegatee             | Complete delegation or remove        |

---

## Quick Reference

**Add Commands:**

```bash
dr add security model <name>
dr add security authentication-config <name> --properties provider=<type>
dr add security role <name> --properties hierarchy=<number>
dr add security permission <name> --properties scope=<scope>
dr add security secure-resource <name> --properties type=<type>
dr add security actor <name> --properties type=<type>
dr add security actor-objective <name> --properties actor=<actor-id>
dr add security information-entity <name> --properties classification=<level>
dr add security threat <name> --properties likelihood=<value>,impact=<value>
dr add security countermeasure <name> --properties threat=<threat-id>
dr add security delegation <name> --properties delegator=<actor>,delegatee=<actor>
```

**Relationship Commands:**

```bash
dr relationship add <actor> has-objective <objective>
dr relationship add <threat> mitigated-by <countermeasure>
dr relationship add <secure-resource> protects <application-service>
dr relationship add <actor-objective> supports <motivation-goal>
```

**Cross-Layer Commands:**

```bash
dr relationship add security/<actor> references motivation/<stakeholder>
dr relationship add security/<secure-resource> protects application/<service>
dr relationship add security/<resource-operation> protects api/<operation>
```
