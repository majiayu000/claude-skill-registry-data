---
name: auth-system-builder
description: Genera sistema completo de autenticación para Django con registro, login, verificación de email, recuperación de contraseña, social auth y protección de vistas. Usa django-allauth y best practices de seguridad.
---

# Auth System Builder - Django

## Propósito

Este skill genera sistemas de autenticación completos para Django que puedes implementar en 15 minutos. Incluye todo el código necesario: registro, login, verificación de email, recuperación de contraseña, social authentication (Google, GitHub) y protección de vistas.

## Stack Tecnológico

**Framework:** Django 4.x / 5.x  
**Paquetes principales:**
- `django-allauth` (auth social + email verification)
- `django-crispy-forms` (formularios bonitos)
- `crispy-bootstrap5` (estilos Bootstrap 5)

**Base de datos:** PostgreSQL / SQLite (desarrollo)

## Cuándo Usar Este Skill

✅ Agregar autenticación completa a proyecto Django nuevo  
✅ Registro con verificación de email obligatoria  
✅ Login con email o username  
✅ Recuperación de contraseña por email  
✅ Social login (Google, GitHub, Facebook)  
✅ Protección de vistas con decoradores  
✅ User profile extendido  

---

## Instalación Rápida (15 minutos)

### 1. Instalar Dependencias

```bash
pip install django-allauth django-crispy-forms crispy-bootstrap5
pip freeze > requirements.txt
```

### 2. Configurar `settings.py`

```python
# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # REQUERIDO por allauth
    
    # Apps de terceros
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # OAuth Google
    'allauth.socialaccount.providers.github',  # OAuth GitHub
    'crispy_forms',
    'crispy_bootstrap5',
    
    # Tus apps
    # 'miapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # AGREGAR ESTO
]

# Site ID requerido por django-allauth
SITE_ID = 1

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configuración de django-allauth
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Login con email
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Obligatorio verificar email
ACCOUNT_USERNAME_REQUIRED = False  # No requerir username
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True  # Confirmar email en registro
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300  # 5 minutos
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_SESSION_REMEMBER = True

# URLs de redirección
LOGIN_REDIRECT_URL = '/dashboard/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'

# Email backend (desarrollo)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Email backend (producción - ejemplo con Gmail)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'tu-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'tu-app-password'
# DEFAULT_FROM_EMAIL = 'tu-email@gmail.com'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Seguridad (producción)
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
```

### 3. Configurar URLs principales

```python
# proyecto/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Todas las URLs de auth
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
]
```

### 4. Migrar Base de Datos

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Crear Site en Admin

```bash
python manage.py shell
```

```python
from django.contrib.sites.models import Site

site = Site.objects.get(id=1)
site.domain = 'localhost:8000'  # o tu dominio
site.name = 'Mi Sitio'
site.save()
```

---

## Templates Base

### Base Template

**Archivo:** `templates/base.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi Sitio{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">Mi Sitio</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'dashboard' %}">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <span class="nav-link">Hola, {{ user.email }}</span>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'account_logout' %}">Cerrar Sesión</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'account_login' %}">Iniciar Sesión</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'account_signup' %}">Registrarse</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <main class="container my-5">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}

        {% block content %}{% endblock %}
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Home Page

**Archivo:** `templates/home.html`

```html
{% extends 'base.html' %}

{% block content %}
<div class="text-center">
    <h1 class="display-4">Bienvenido</h1>
    <p class="lead">Sistema de autenticación completo con Django</p>
    
    {% if not user.is_authenticated %}
        <div class="mt-4">
            <a href="{% url 'account_signup' %}" class="btn btn-primary btn-lg">Crear Cuenta</a>
            <a href="{% url 'account_login' %}" class="btn btn-outline-primary btn-lg">Iniciar Sesión</a>
        </div>
    {% else %}
        <div class="mt-4">
            <a href="{% url 'dashboard' %}" class="btn btn-primary btn-lg">Ir al Dashboard</a>
        </div>
    {% endif %}
</div>
{% endblock %}
```

### Dashboard (Protegido)

**Archivo:** `templates/dashboard.html`

```html
{% extends 'base.html' %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8 mx-auto">
        <h1 class="mb-4">Dashboard</h1>
        
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Información del Usuario</h5>
            </div>
            <div class="card-body">
                <dl class="row">
                    <dt class="col-sm-3">Email:</dt>
                    <dd class="col-sm-9">{{ user.email }}</dd>
                    
                    <dt class="col-sm-3">Usuario:</dt>
                    <dd class="col-sm-9">{{ user.username|default:"No configurado" }}</dd>
                    
                    <dt class="col-sm-3">Email verificado:</dt>
                    <dd class="col-sm-9">
                        {% if user.emailaddress_set.first.verified %}
                            <span class="badge bg-success">Sí</span>
                        {% else %}
                            <span class="badge bg-warning">No</span>
                        {% endif %}
                    </dd>
                    
                    <dt class="col-sm-3">Fecha de registro:</dt>
                    <dd class="col-sm-9">{{ user.date_joined|date:"d/m/Y H:i" }}</dd>
                </dl>
                
                <div class="mt-3">
                    <a href="{% url 'account_email' %}" class="btn btn-primary">Gestionar Emails</a>
                    <a href="{% url 'account_change_password' %}" class="btn btn-secondary">Cambiar Contraseña</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Personalizar Templates de django-allauth

Crea carpeta `templates/account/` y sobrescribe templates:

### Login Personalizado

**Archivo:** `templates/account/login.html`

```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block title %}Iniciar Sesión{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-6 mx-auto">
        <div class="card shadow">
            <div class="card-body p-5">
                <h2 class="card-title text-center mb-4">Iniciar Sesión</h2>
                
                <form method="post" action="{% url 'account_login' %}">
                    {% csrf_token %}
                    {{ form|crispy }}
                    
                    <button type="submit" class="btn btn-primary w-100 mb-3">Iniciar Sesión</button>
                </form>
                
                <div class="text-center mb-3">
                    <a href="{% url 'account_reset_password' %}" class="text-muted small">
                        ¿Olvidaste tu contraseña?
                    </a>
                </div>
                
                <hr>
                
                <p class="text-center mb-3 text-muted">O inicia sesión con:</p>
                
                <div class="d-grid gap-2">
                    <a href="{% url 'google_login' %}" class="btn btn-outline-danger">
                        <i class="fab fa-google"></i> Continuar con Google
                    </a>
                    <a href="{% url 'github_login' %}" class="btn btn-outline-dark">
                        <i class="fab fa-github"></i> Continuar con GitHub
                    </a>
                </div>
                
                <p class="text-center mt-4 mb-0">
                    ¿No tienes cuenta? 
                    <a href="{% url 'account_signup' %}">Regístrate aquí</a>
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Registro Personalizado

**Archivo:** `templates/account/signup.html`

```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block title %}Registro{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-6 mx-auto">
        <div class="card shadow">
            <div class="card-body p-5">
                <h2 class="card-title text-center mb-4">Crear Cuenta</h2>
                
                <form method="post" action="{% url 'account_signup' %}">
                    {% csrf_token %}
                    {{ form|crispy }}
                    
                    <button type="submit" class="btn btn-primary w-100 mb-3">Crear Cuenta</button>
                </form>
                
                <hr>
                
                <p class="text-center mb-3 text-muted">O regístrate con:</p>
                
                <div class="d-grid gap-2">
                    <a href="{% url 'google_login' %}" class="btn btn-outline-danger">
                        <i class="fab fa-google"></i> Continuar con Google
                    </a>
                    <a href="{% url 'github_login' %}" class="btn btn-outline-dark">
                        <i class="fab fa-github"></i> Continuar con GitHub
                    </a>
                </div>
                
                <p class="text-center mt-4 mb-0">
                    ¿Ya tienes cuenta? 
                    <a href="{% url 'account_login' %}">Inicia sesión aquí</a>
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Protección de Vistas

### Con Decorador (Function-Based Views)

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')
```

### Con Mixin (Class-Based Views)

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = '/accounts/login/'
```

---

## Modelo de Usuario Extendido

Si necesitas campos adicionales en el usuario:

```python
# miapp/models.py

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return f'Perfil de {self.user.email}'

# Crear Profile automáticamente al crear User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
```

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Configurar OAuth (Google)

### 1. Crear proyecto en Google Cloud Console

1. Ve a https://console.cloud.google.com
2. Crea nuevo proyecto
3. Habilita "Google+ API"
4. Ve a "Credentials" > "Create Credentials" > "OAuth 2.0 Client ID"
5. Tipo: Web application
6. Authorized redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/`
   - `https://tudominio.com/accounts/google/login/callback/`

### 2. Configurar en Django Admin

1. Inicia sesión en `/admin/`
2. Ve a "Social applications" > "Add social application"
3. Provider: Google
4. Name: Google OAuth
5. Client ID: [tu client id]
6. Secret key: [tu client secret]
7. Sites: Selecciona tu site
8. Save

---

## Email Templates Personalizados

**Archivo:** `templates/account/email/email_confirmation_subject.txt`

```
Confirma tu email en {{ site_name }}
```

**Archivo:** `templates/account/email/email_confirmation_message.txt`

```
Hola {{ user.email }},

Gracias por registrarte en {{ site_name }}.

Para completar tu registro, por favor confirma tu dirección de email haciendo click en el siguiente enlace:

{{ activate_url }}

Este enlace expira en {{ expiration_days }} días.

Saludos,
El equipo de {{ site_name }}
```

---

## Configuración de Email en Producción

### Con Gmail (menos seguro)

```python
# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-app-password'  # Generar en Google Account
DEFAULT_FROM_EMAIL = 'tu-email@gmail.com'
```

### Con SendGrid (recomendado)

```bash
pip install sendgrid
```

```python
# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'tu-api-key-de-sendgrid'
DEFAULT_FROM_EMAIL = 'noreply@tudominio.com'
```

---

## Checklist de Implementación

- [ ] Instalar django-allauth y crispy-forms
- [ ] Configurar INSTALLED_APPS
- [ ] Configurar AUTHENTICATION_BACKENDS
- [ ] Configurar account settings en settings.py
- [ ] Configurar URLs principales
- [ ] Ejecutar migraciones
- [ ] Crear Site en admin
- [ ] Crear templates base
- [ ] Personalizar templates de login/signup
- [ ] Configurar email backend
- [ ] Probar registro + verificación de email
- [ ] Probar login/logout
- [ ] Probar recuperación de contraseña
- [ ] Configurar OAuth providers (opcional)
- [ ] Implementar Profile model (opcional)

---

## Comandos Útiles

```bash
# Verificar configuración de email
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Mensaje', 'from@example.com', ['to@example.com'])

# Limpiar sesiones expiradas
python manage.py clearsessions

# Crear usuario de prueba
python manage.py shell
from django.contrib.auth.models import User
User.objects.create_user('test@example.com', 'test@example.com', 'password123')
```

---

## Troubleshooting

**Error: "Site matching query does not exist"**
```python
python manage.py shell
from django.contrib.sites.models import Site
Site.objects.create(domain='localhost:8000', name='Dev Site')
```

**Email no llega en desarrollo:**
- Verifica `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
- El email se imprime en la consola, no se envía realmente

**OAuth redirect mismatch:**
- Verifica que las URLs en Google Console coincidan exactamente
- Incluye http:// o https://
- No olvides la barra final /

---

## Formato de Output

Cuando uses este skill, especifica:
- Si necesitas OAuth (Google, GitHub, etc.)
- Si necesitas Profile extendido
- Si necesitas email templates personalizados

Ejemplo:
```
"Implementa autenticación completa con django-allauth. 
Necesito registro con verificación de email, OAuth con Google,
y un modelo Profile con teléfono y avatar."
```

El skill generará todo el código necesario listo para implementar.
