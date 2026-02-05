---
name: zhongyi-best-practices
description: Follow zhongyi TCM system best practices and coding conventions. Use when writing new code, reviewing existing code, or ensuring consistency with project patterns. Helps maintain Django/DRF patterns, i18n, Bootstrap5 styling, and TCM-specific conventions.
---

# Zhongyi Project Best Practices

Use this guide when writing or modifying code for the zhongyi Traditional Chinese Medicine (TCM) system to ensure consistency with established patterns.

## Project Structure

The project follows a standard Django structure at `/home/user/zhongyi-system/zhongyi_project/`:

```
zhongyi_project/
├── zhongyi_project/    # Project settings
│   ├── settings.py
│   └── urls.py
├── accounts/           # User authentication
├── patients/           # Patient management
├── diagnosis/          # TCM diagnosis system
├── prescriptions/      # Herbal prescriptions
├── api/                # REST API layer
├── templates/          # All HTML templates
├── static/             # CSS, JS, images
└── locale/             # i18n translations
```

## Model Conventions

### Standard Fields
Every model must include:
```python
from django.db import models
from django.utils.translation import gettext_lazy as _

class YourModel(models.Model):
    # Always include timestamps
    created_at = models.DateTimeField(_('Created At (创建时间)'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At (更新时间)'), auto_now=True)

    # Always include soft delete
    is_active = models.BooleanField(_('Active (活跃)'), default=True)

    class Meta:
        verbose_name = _('Model Name (模型名称)')
        verbose_name_plural = _('Model Names (模型名称)')
        ordering = ['-updated_at']

    def __str__(self):
        return self.name  # Always define __str__
```

### Bilingual Field Names
Always use bilingual format for verbose names:
```python
name = models.CharField(_('Name (名称)'), max_length=200)
```

### Choices
Use TextChoices or IntegerChoices:
```python
class Category(models.TextChoices):
    GENERAL = 'general', _('General (全身)')
    HEAD = 'head', _('Head & Face (头面)')
```

### Relationships
Reference User model correctly:
```python
from django.conf import settings

assigned_practitioner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    related_name='model_assignments'
)
```

## View Conventions

### Required Mixins
Always use these mixins for protected views:
```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PractitionerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Require user to be practitioner or admin."""
    def test_func(self):
        return self.request.user.is_practitioner or self.request.user.is_admin
```

### ListView Pattern
```python
class YourModelListView(PractitionerRequiredMixin, ListView):
    model = YourModel
    template_name = 'yourapp/yourmodel_list.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        queryset = YourModel.objects.filter(is_active=True)
        # Filter by practitioner for non-admin users
        if self.request.user.is_practitioner and not self.request.user.is_admin:
            queryset = queryset.filter(assigned_practitioner=self.request.user)

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )
        return queryset.order_by('-updated_at')
```

### CreateView Pattern
```python
class YourModelCreateView(PractitionerRequiredMixin, CreateView):
    model = YourModel
    form_class = YourModelForm
    template_name = 'yourapp/yourmodel_form.html'
    success_url = reverse_lazy('yourapp:list')

    def form_valid(self, form):
        form.instance.assigned_practitioner = self.request.user
        messages.success(self.request, _('Created successfully'))
        return super().form_valid(form)
```

### Soft Delete Pattern
Never hard delete - use soft delete:
```python
class YourModelDeleteView(PractitionerRequiredMixin, DeleteView):
    model = YourModel
    success_url = reverse_lazy('yourapp:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        messages.success(request, _('Deleted successfully'))
        return redirect(self.success_url)
```

## Form Conventions

### Bootstrap5 Styling
All forms must use Bootstrap5 classes:
```python
from django import forms

class YourModelForm(forms.ModelForm):
    class Meta:
        model = YourModel
        fields = ('name', 'category', 'description', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
```

## URL Conventions

### Namespaced URLs
```python
from django.urls import path
from . import views

app_name = 'yourapp'

urlpatterns = [
    path('', views.YourModelListView.as_view(), name='list'),
    path('create/', views.YourModelCreateView.as_view(), name='create'),
    path('<int:pk>/', views.YourModelDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.YourModelUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.YourModelDeleteView.as_view(), name='delete'),
]
```

## Serializer Conventions

### List vs Detail Serializers
Create separate serializers for list and detail views:
```python
from rest_framework import serializers

class YourModelListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    class Meta:
        model = YourModel
        fields = ['id', 'name', 'category', 'created_at']

class YourModelDetailSerializer(serializers.ModelSerializer):
    """Full serializer with nested relationships."""
    assigned_practitioner = UserSerializer(read_only=True)
    assigned_practitioner_id = serializers.PrimaryKeyRelatedField(
        source='assigned_practitioner',
        queryset=User.objects.filter(role='practitioner'),
        write_only=True
    )

    class Meta:
        model = YourModel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
```

## ViewSet Conventions

### Standard ViewSet Pattern
```python
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

class YourModelViewSet(viewsets.ModelViewSet):
    queryset = YourModel.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, IsPractitionerOrAdmin]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['created_at', 'name']

    def get_serializer_class(self):
        if self.action == 'list':
            return YourModelListSerializer
        return YourModelDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_admin:
            queryset = queryset.filter(assigned_practitioner=self.request.user)
        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Custom search endpoint."""
        query = request.query_params.get('q', '')
        results = self.get_queryset().filter(name__icontains=query)[:10]
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
```

## Admin Conventions

### Standard Admin Configuration
```python
from django.contrib import admin

@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)

    fieldsets = (
        (_('Basic Information (基本信息)'), {
            'fields': ('name', 'category', 'description')
        }),
        (_('System (系统)'), {
            'fields': ('is_active', 'assigned_practitioner')
        }),
        (_('Timestamps (时间戳)'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

## Template Conventions

### Extend Base Template
```html
{% extends 'base.html' %}
{% load i18n crispy_forms_tags %}

{% block title %}Page Title{% endblock %}

{% block content %}
<div class="container my-4">
    <!-- Content here -->
</div>
{% endblock %}
```

### Use Bootstrap5 Components
- Cards: `<div class="card">`
- Tables: `<table class="table table-hover">`
- Buttons: `<button class="btn btn-primary">`
- Forms: Use crispy forms with `{% crispy form %}`

### Icons
Use Bootstrap Icons: `<i class="bi bi-icon-name"></i>`

## Internationalization (i18n)

### Mark All Strings
```python
from django.utils.translation import gettext_lazy as _

verbose_name = _('English (中文)')
```

### In Templates
```html
{% load i18n %}
{% trans "Text" %}
{% blocktrans %}Dynamic {{ variable }}{% endblocktrans %}
```

## Permissions

### Custom Permission Class
```python
from rest_framework import permissions

class IsPractitionerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_practitioner or request.user.is_admin
        )
```

### User Roles
The system has three roles:
- `admin` - Full access
- `practitioner` - Access to assigned patients/records
- `patient` - Limited access to own records

## Code Quality Checklist

Before committing code, verify:

- [ ] All models have `created_at`, `updated_at`, `is_active` fields
- [ ] All strings are marked for translation with bilingual format
- [ ] All views use appropriate mixins (`PractitionerRequiredMixin`)
- [ ] All forms use Bootstrap5 CSS classes
- [ ] Soft delete is used instead of hard delete
- [ ] URLs are namespaced with `app_name`
- [ ] Admin configuration includes fieldsets and list_display
- [ ] Serializers have separate List and Detail versions
- [ ] ViewSets filter by user role/assignment
- [ ] Templates extend base.html and use Bootstrap5

## Example Files to Reference

- **Model example**: `patients/models.py`
- **Views example**: `patients/views.py`
- **Forms example**: `patients/forms.py`
- **Admin example**: `patients/admin.py`
- **Serializers example**: `api/serializers.py`
- **ViewSets example**: `api/views.py`
- **URLs example**: `patients/urls.py`
- **Templates**: `templates/patients/`
