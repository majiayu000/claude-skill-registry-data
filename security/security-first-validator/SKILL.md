---
name: security-first-validator
description: This skill should be used when the user asks to "create an API endpoint", "add a view", "write a viewset", "create a serializer", or when writing Django REST Framework code. Enforces security requirements (permissions, authentication, rate limiting).
---

# Security-First Validator

Enforces security requirements for all Django REST Framework API endpoints.

## Activation Triggers

This skill activates when:
- Creating API views or viewsets
- Creating serializers
- Mentioning "endpoint", "API", "view", "route"
- Writing DRF classes (APIView, ViewSet, Serializer)
- Creating URL patterns for APIs
- Discussing authentication or permissions

## Security Requirements (MANDATORY)

Every API endpoint MUST have:

### 1. Permission Classes (REQUIRED)

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # ✅ REQUIRED
    # ...
```

### 2. Serializer Validation (REQUIRED)

```python
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name']
        # NO sensitive fields exposed ✅

    def validate_email(self, value):
        # Custom validation ✅
        if not value.endswith('@company.com'):
            raise serializers.ValidationError("Must use company email")
        return value
```

### 3. No Raw SQL (REQUIRED)

```python
# ❌ DANGEROUS
User.objects.raw(f"SELECT * FROM users WHERE id = {user_id}")

# ✅ SAFE
User.objects.filter(id=user_id)
```

### 4. Rate Limiting (REQUIRED for sensitive endpoints)

```python
from rest_framework.throttling import UserRateThrottle

class LoginView(APIView):
    throttle_classes = [UserRateThrottle]  # ✅ REQUIRED for auth
    # ...
```

## Validation Process

### Step 1: Detect New API Endpoint

When API code is being written:

```python
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Missing security! ❌
```

### Step 2: Run Security Checklist

Verify:
1. ✅ Permission classes defined
2. ✅ Serializer has proper validation
3. ✅ No raw SQL queries
4. ✅ Rate limiting on sensitive endpoints
5. ✅ No password/token fields in serializer
6. ✅ Proper CORS configuration

### Step 3: Auto-Add Security Requirements

**Before (Insecure):**
```python
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

**After (Secure):**
```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    """User management endpoints."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # ✅ Added

    def get_queryset(self):
        """Filter queryset to exclude soft-deleted records."""
        return super().get_queryset().filter(is_deleted=False)
```

### Step 4: Validate Serializer Security

**Check for exposed sensitive fields:**

```python
# ❌ DANGEROUS - Exposes password!
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Never use __all__!
```

**Auto-fix to:**

```python
# ✅ SAFE - Explicit field list
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'created_at', 'updated_at']
        # Password excluded ✅
```

### Step 5: Report Security Issues

Report to developer:

> **Security Issues Detected and Fixed**
>
> **Fixed:**
> 1. ✅ Added `permission_classes = [IsAuthenticated]` to UserViewSet
> 2. ✅ Changed serializer from `fields = '__all__'` to explicit field list
> 3. ✅ Excluded sensitive fields (password, tokens)
> 4. ✅ Added `read_only_fields` for audit fields
>
> **Why:**
> - Permission classes prevent unauthorized access
> - Explicit fields prevent accidental data exposure
> - Read-only fields prevent tampering with audit trail

## Complete Secure Endpoint Example

```python
import users.models as _users_models
import users.serializers as _users_serializers

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle


class UserViewSet(viewsets.ModelViewSet):
    """
    User management API.

    Security:
    - Requires authentication
    - Users can only access their own data (see get_queryset)
    - Rate limited for sensitive actions
    - Input validation via serializer
    """

    queryset = _users_models.User.objects.all()
    serializer_class = _users_serializers.UserSerializer
    permission_classes = [IsAuthenticated]  # ✅ Authentication required

    def get_queryset(self):
        """Users can only see active, non-deleted records."""
        qs = super().get_queryset().filter(is_deleted=False)

        # Users see only their own data unless admin
        if not self.request.user.is_staff:
            qs = qs.filter(id=self.request.user.id)

        return qs

    def perform_create(self, serializer):
        """Auto-set created_by on creation."""
        serializer.save(created_by=self.request.user)

    @action(
        detail=False,
        methods=['post'],
        throttle_classes=[UserRateThrottle],  # ✅ Rate limiting
        permission_classes=[IsAuthenticated]
    )
    def change_password(self, request):
        """Change user password (rate limited)."""
        serializer = _serializers.ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # ✅ Validation

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'status': 'password changed'})
```

## Security Checklist by Endpoint Type

### Read-Only Endpoints (GET)

```python
class PublicArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """Public articles (read-only)."""

    queryset = Article.objects.filter(is_published=True, is_deleted=False)
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]  # ✅ Explicit - public endpoint

    # Still apply rate limiting to prevent scraping
    throttle_classes = [AnonRateThrottle]
```

### Create Endpoints (POST)

```python
class UserCreateView(generics.CreateAPIView):
    """User registration (public)."""

    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]  # ✅ Public registration
    throttle_classes = [AnonRateThrottle]  # ✅ Prevent abuse

    def perform_create(self, serializer):
        """
        Create user and send verification email.

        Security: Rate limited, email validation in serializer.
        """
        user = serializer.save()
        send_verification_email(user)
```

### Update Endpoints (PUT/PATCH)

```python
class UserUpdateView(generics.UpdateAPIView):
    """Update user profile."""

    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwner]  # ✅ Auth + ownership

    def get_object(self):
        """Users can only update their own profile."""
        return self.request.user
```

### Delete Endpoints (DELETE)

```python
class UserDestroyView(generics.DestroyAPIView):
    """Soft delete user account."""

    permission_classes = [IsAuthenticated, IsOwner]  # ✅ Auth + ownership

    def perform_destroy(self, instance):
        """Soft delete instead of hard delete."""
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted', 'updated_at'])
```

## Common Security Violations

### Violation 1: No Permission Classes

```python
# ❌ DANGEROUS - Anyone can access!
class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
```

**Auto-fix:**
```python
# ✅ SECURE
class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]  # Added!
```

### Violation 2: Serializer Exposes Sensitive Data

```python
# ❌ DANGEROUS - Exposes password!
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
```

**I auto-fix:**
```python
# ✅ SECURE
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        # password, tokens excluded!
```

### Violation 3: Raw SQL Injection Risk

```python
# ❌ DANGEROUS - SQL injection!
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return User.objects.raw(query)
```

**I auto-fix:**
```python
# ✅ SECURE
def get_user(user_id):
    return User.objects.filter(id=user_id).first()
```

### Violation 4: No Rate Limiting on Auth

```python
# ❌ DANGEROUS - Brute force attacks possible!
class LoginView(APIView):
    def post(self, request):
        # Login logic
        pass
```

**I auto-fix:**
```python
# ✅ SECURE
from rest_framework.throttling import AnonRateThrottle

class LoginView(APIView):
    throttle_classes = [AnonRateThrottle]  # Added!

    def post(self, request):
        # Login logic
        pass
```

## OWASP Top 10 Coverage

Automatically check for:

1. **Broken Access Control** → Permission classes required
2. **Cryptographic Failures** → No sensitive fields in serializers
3. **Injection** → No raw SQL, use ORM
4. **Insecure Design** → Enforce secure-by-default patterns
5. **Security Misconfiguration** → CORS, HTTPS, rate limiting
6. **Vulnerable Components** → (Check in CI/CD)
7. **Authentication Failures** → Throttling on auth endpoints
8. **Data Integrity Failures** → Serializer validation required
9. **Logging Failures** → (Suggest logging for sensitive ops)
10. **SSRF** → Validate URLs in serializers

## Custom Permission Classes

Recognize and allow custom permissions:

```python
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """User can only access their own objects."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# Usage ✅ VALID
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
```

## Integration with Other Skills

Works together with:
- **model-entity-validator**: Ensures models don't expose sensitive fields
- **test-coverage-advisor**: Suggests security tests
- **django-reviewer**: Full security audit during review

## Success Criteria

✅ ALL endpoints have permission classes
✅ ALL serializers use explicit field lists
✅ NO raw SQL queries
✅ Rate limiting on sensitive endpoints
✅ NO sensitive fields exposed
✅ Input validation on all write operations
✅ Developer understands OWASP risks

## Behavior

**Proactive enforcement:**
- Check security without being asked
- Add permission classes automatically
- Fix serializer field exposure immediately
- Explain WHY each security measure is critical
- Reference OWASP categories

**Never:**
- Require explicit "check security" request
- Wait for pen test results
- Just warn without fixing
- Allow endpoints without security

**Block completion if:**
- No permission classes defined
- Serializer uses `fields = '__all__'`
- Raw SQL detected
- Sensitive endpoints lack rate limiting
