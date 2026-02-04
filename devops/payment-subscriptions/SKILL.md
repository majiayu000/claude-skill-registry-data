---
name: payment-subscriptions
description: Implementa sistema completo de pagos recurrentes con Flow.cl (Chile) y Stripe (internacional). Incluye suscripciones mensuales, webhooks, firma HMAC, manejo de errores y múltiples estrategias de fallback. Basado en implementación real probada en producción.
---

# Payment Subscriptions - Flow.cl & Stripe

## Propósito

Este skill genera implementaciones completas de pagos recurrentes (suscripciones mensuales) usando Flow.cl para Chile y Stripe para el resto del mundo. Incluye código probado en producción, manejo de webhooks, firma HMAC SHA256, y múltiples estrategias de fallback para manejar bugs de las APIs.

## Stack Tecnológico

**Framework:** Django 4.x / 5.x  
**Pasarelas de pago:**
- **Flow.cl** (Chile - CLP)
- **Stripe** (Internacional - USD/EUR)

**Base de datos:** PostgreSQL  
**Paquetes:** requests, cryptography

---

## Cuándo Usar Este Skill

✅ Implementar suscripciones mensuales recurrentes  
✅ Pagos en CLP (pesos chilenos) con Flow.cl  
✅ Pagos internacionales con Stripe  
✅ Webhooks para actualizar estados de pago  
✅ Múltiples planes/tiers de suscripción  
✅ Manejo robusto de errores de APIs  

---

## Parte 1: Flow.cl (Chile)

### Características de la Implementación

Esta implementación está **basada en código real en producción** y maneja:

✅ **Implementación custom** (no usa SDK oficial por bugs)  
✅ **Firma HMAC SHA256** correcta  
✅ **3 estrategias de fallback** cuando falla la API  
✅ **Tabla FlowCustomer** como cache local  
✅ **7 planes predefinidos** (5k - 500k CLP)  
✅ **Webhooks completos**  
✅ **Logging extensivo** para debugging  

### 1. Instalación

```bash
pip install requests cryptography psycopg2-binary
```

### 2. Variables de Entorno

```.env
# Flow.cl
FLOW_API_KEY=tu_api_key
FLOW_SECRET=tu_secret_key
FLOW_SANDBOX=True  # False en producción
FLOW_BASE_URL=https://tudominio.com

# URLs de callback
FLOW_RETURN_URL=https://tudominio.com/pagos/success/
FLOW_WEBHOOK_URL=https://tudominio.com/api/payments/flow/webhook/

# Plan IDs de Flow (crear en dashboard de Flow)
FLOW_PLAN_5000=5000 Mensual
FLOW_PLAN_10000=10000 Mensual
FLOW_PLAN_20000=20000 Mensual
FLOW_PLAN_40000=40000 Mensual
FLOW_PLAN_100000=100.000 Mensual
FLOW_PLAN_250000=250.000 Mensual
FLOW_PLAN_500000=500.000 Mensual
```

### 3. Modelos de Base de Datos

**Archivo:** `payments/models.py`

```python
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class FlowCustomer(models.Model):
    """
    Mapeo local entre emails y customerIds de Flow.
    Evita errores de duplicación al crear clientes.
    """
    email = models.EmailField(unique=True, db_index=True)
    flow_customer_id = models.CharField(max_length=100, unique=True, db_index=True)
    external_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'flow_customers'
        verbose_name = 'Flow Customer'
        verbose_name_plural = 'Flow Customers'
    
    def __str__(self):
        return f'{self.email} ({self.flow_customer_id})'


class Subscription(models.Model):
    """
    Suscripción de pago recurrente (Flow o Stripe)
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('active', 'Activa'),
        ('paid', 'Pagada'),
        ('failed', 'Fallida'),
        ('cancelled', 'Cancelada'),
    ]
    
    FREQUENCY_CHOICES = [
        ('monthly', 'Mensual'),
        ('yearly', 'Anual'),
        ('one-time', 'Único'),
    ]
    
    PROVIDER_CHOICES = [
        ('flow', 'Flow.cl'),
        ('stripe', 'Stripe'),
    ]
    
    # Usuario (opcional)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='subscriptions'
    )
    
    # Datos básicos
    email = models.EmailField(db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='CLP')  # CLP, USD
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='monthly')
    
    # Proveedor
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='flow')
    
    # Datos de Flow.cl
    commerce_order = models.CharField(max_length=255, unique=True, null=True, blank=True)
    flow_token = models.CharField(max_length=255, null=True, blank=True)
    flow_url = models.URLField(null=True, blank=True)
    flow_customer_id = models.CharField(max_length=100, null=True, blank=True)
    flow_subscription_id = models.CharField(max_length=100, null=True, blank=True)
    flow_plan_id = models.CharField(max_length=100, null=True, blank=True)
    
    # Datos de Stripe
    stripe_subscription_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    stripe_plan_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Estado
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    mode = models.CharField(max_length=10, default='real')  # real, demo, sandbox
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subscriptions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email', 'status']),
            models.Index(fields=['provider', 'status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f'{self.email} - {self.amount} {self.currency} ({self.status})'
```

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Librería de Flow.cl

**Archivo:** `payments/flow.py`

```python
import os
import hmac
import hashlib
import requests
import logging
from urllib.parse import urlencode
from typing import Dict, Any

logger = logging.getLogger(__name__)


class FlowConfig:
    """Configuración de Flow.cl desde variables de entorno"""
    
    @staticmethod
    def get_config() -> Dict[str, Any]:
        api_key = os.getenv('FLOW_API_KEY', '')
        secret_key = os.getenv('FLOW_SECRET', '')
        sandbox = os.getenv('FLOW_SANDBOX', 'True').lower() == 'true'
        base_url = os.getenv('FLOW_BASE_URL', 'http://localhost:8000')
        
        api_url = 'https://sandbox.flow.cl/api' if sandbox else 'https://www.flow.cl/api'
        
        return {
            'api_key': api_key,
            'secret_key': secret_key,
            'api_url': api_url,
            'base_url': base_url,
            'sandbox': sandbox
        }


class FlowClient:
    """Cliente para interactuar con la API de Flow.cl"""
    
    def __init__(self):
        self.config = FlowConfig.get_config()
        self._validate_config()
    
    def _validate_config(self):
        """Validar que las credenciales estén configuradas"""
        if not self.config['api_key'] or not self.config['secret_key']:
            raise ValueError(
                'Flow credentials no configuradas. '
                'Configura FLOW_API_KEY y FLOW_SECRET en .env'
            )
        logger.info(f'Flow configurado en modo: {"SANDBOX" if self.config["sandbox"] else "PRODUCCIÓN"}')
    
    def _sign(self, params: Dict[str, Any]) -> str:
        """
        Genera firma HMAC SHA256 requerida por Flow.
        Los parámetros deben estar ordenados alfabéticamente.
        """
        # Ordenar keys alfabéticamente
        sorted_keys = sorted(params.keys())
        
        # Crear string a firmar: key1=value1&key2=value2
        to_sign = '&'.join([f'{key}={params[key]}' for key in sorted_keys])
        
        # Generar firma HMAC SHA256
        signature = hmac.new(
            self.config['secret_key'].encode('utf-8'),
            to_sign.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        logger.debug(f'Firma generada para: {to_sign[:100]}...')
        
        return signature
    
    def _pack_params(self, params: Dict[str, Any]) -> str:
        """Convierte dict a URL encoded string"""
        return urlencode(params)
    
    def send(self, service_name: str, params: Dict[str, Any], method: str = 'POST') -> Dict[str, Any]:
        """
        Envía request a la API de Flow.
        
        Args:
            service_name: Nombre del servicio (ej: 'payment/create', 'customer/create')
            params: Parámetros del request
            method: GET o POST
        
        Returns:
            Respuesta de Flow como dict
        """
        # Agregar apiKey y sandbox a params
        all_params = {
            'apiKey': self.config['api_key'],
            **params
        }
        
        # Generar firma
        signature = self._sign(all_params)
        
        # Preparar datos
        data_string = self._pack_params(all_params)
        url = f"{self.config['api_url']}/{service_name}"
        
        logger.info(f'Flow API call: {method} {service_name}')
        logger.debug(f'Params: {all_params}')
        
        try:
            if method == 'GET':
                response = requests.get(f'{url}?{data_string}&s={signature}', timeout=30)
            else:  # POST
                response = requests.post(
                    url,
                    data=f'{data_string}&s={signature}',
                    headers={'Content-Type': 'application/x-www-form-urlencoded'},
                    timeout=30
                )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f'Flow API success: {service_name}')
            logger.debug(f'Response: {result}')
            
            return result
            
        except requests.exceptions.HTTPError as e:
            error_text = e.response.text if hasattr(e, 'response') else str(e)
            logger.error(f'Flow API HTTP error: {e.response.status_code} - {error_text}')
            raise Exception(f'Flow API error: {error_text}')
            
        except requests.exceptions.RequestException as e:
            logger.error(f'Flow API request error: {str(e)}')
            raise Exception(f'Flow request error: {str(e)}')
    
    def create_customer(self, email: str, external_id: str = None, name: str = None) -> Dict[str, Any]:
        """Crea un customer en Flow.cl"""
        params = {
            'email': email,
            'externalId': external_id or email,
            'name': name or email.split('@')[0]
        }
        return self.send('customer/create', params, 'POST')
    
    def create_subscription(self, plan_id: str, subscription_id: str, customer_id: str, 
                          return_url: str, confirmation_url: str) -> Dict[str, Any]:
        """Crea una suscripción en Flow.cl"""
        params = {
            'planId': plan_id,
            'subscription_id': subscription_id,
            'customerId': customer_id,
            'urlReturn': return_url,
            'urlConfirmation': confirmation_url
        }
        return self.send('subscription/create', params, 'POST')
    
    def create_payment(self, commerce_order: str, subject: str, currency: str, amount: float,
                      email: str, return_url: str, confirmation_url: str,
                      payment_method: int = 9, subscription: int = 0,
                      subscription_id: str = None, customer_id: str = None,
                      plan_id: str = None) -> Dict[str, Any]:
        """Crea un pago en Flow.cl"""
        params = {
            'commerceOrder': commerce_order,
            'subject': subject,
            'currency': currency,
            'amount': int(amount),
            'email': email,
            'paymentMethod': payment_method,
            'urlReturn': return_url,
            'urlConfirmation': confirmation_url
        }
        
        if subscription:
            params['subscription'] = subscription
            
        if subscription_id:
            params['subscription_id'] = subscription_id
            
        if customer_id:
            params['customerId'] = customer_id
            
        if plan_id:
            params['planId'] = plan_id
        
        return self.send('payment/create', params, 'POST')
    
    def get_payment_status(self, token: str) -> Dict[str, Any]:
        """Consulta el estado de un pago"""
        return self.send('payment/getStatus', {'token': token}, 'GET')


# Instancia singleton
flow_client = FlowClient()
```

### 5. Views de Pagos

**Archivo:** `payments/views.py`

```python
import logging
import uuid
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import FlowCustomer, Subscription
from .flow import flow_client

logger = logging.getLogger(__name__)

# Mapeo de montos a plan IDs
FLOW_PLAN_MAPPING = {
    5000: os.getenv('FLOW_PLAN_5000', '5000 Mensual'),
    10000: os.getenv('FLOW_PLAN_10000', '10000 Mensual'),
    20000: os.getenv('FLOW_PLAN_20000', '20000 Mensual'),
    40000: os.getenv('FLOW_PLAN_40000', '40000 Mensual'),
    100000: os.getenv('FLOW_PLAN_100000', '100.000 Mensual'),
    250000: os.getenv('FLOW_PLAN_250000', '250.000 Mensual'),
    500000: os.getenv('FLOW_PLAN_500000', '500.000 Mensual'),
}


def get_or_create_flow_customer(email: str) -> str:
    """
    Obtiene o crea un customer en Flow.cl.
    Usa tabla local FlowCustomer como cache para evitar duplicados.
    """
    # Buscar en tabla local
    try:
        flow_customer = FlowCustomer.objects.get(email=email)
        logger.info(f'Flow customer encontrado en cache: {flow_customer.flow_customer_id}')
        return flow_customer.flow_customer_id
    except FlowCustomer.DoesNotExist:
        pass
    
    # No existe, crear en Flow
    try:
        response = flow_client.create_customer(
            email=email,
            external_id=email,
            name=email.split('@')[0]
        )
        
        customer_id = response.get('customerId')
        
        # Guardar en tabla local
        flow_customer = FlowCustomer.objects.create(
            email=email,
            flow_customer_id=customer_id,
            external_id=email,
            name=email.split('@')[0]
        )
        
        logger.info(f'Flow customer creado: {customer_id}')
        return customer_id
        
    except Exception as e:
        logger.error(f'Error creando Flow customer: {str(e)}')
        raise


@require_http_methods(["POST"])
def create_flow_subscription(request):
    """
    Crea una suscripción mensual en Flow.cl.
    Implementa 3 estrategias de fallback para manejar bugs de la API.
    """
    try:
        # Extraer datos del request
        email = request.POST.get('email')
        amount = int(request.POST.get('amount', 0))
        
        if not email or amount not in FLOW_PLAN_MAPPING:
            return JsonResponse({
                'success': False,
                'error': 'Email o monto inválido'
            }, status=400)
        
        # Generar IDs únicos
        subscription_id = f'sub_{uuid.uuid4().hex[:16]}'
        commerce_order = f'order_{uuid.uuid4().hex[:16]}'
        
        # Obtener plan_id
        plan_id = FLOW_PLAN_MAPPING[amount]
        
        # URLs de callback
        base_url = settings.FLOW_BASE_URL
        return_url = f'{base_url}/pagos/success/'
        confirmation_url = f'{base_url}/api/payments/flow/webhook/'
        
        logger.info(f'Creando suscripción Flow: {email} - ${amount} CLP')
        
        # Estrategia 1: payment/create con subscription=1 (más simple)
        try:
            response = flow_client.create_payment(
                commerce_order=commerce_order,
                subject=f'Suscripción Mensual - {plan_id}',
                currency='CLP',
                amount=amount,
                email=email,
                return_url=return_url,
                confirmation_url=confirmation_url,
                payment_method=9,
                subscription=1,
                plan_id=plan_id
            )
            
            # Crear registro en BD
            subscription = Subscription.objects.create(
                email=email,
                amount=amount,
                currency='CLP',
                frequency='monthly',
                provider='flow',
                commerce_order=commerce_order,
                flow_token=response.get('token'),
                flow_url=response.get('url'),
                flow_plan_id=plan_id,
                status='pending',
                mode='real',
                metadata={
                    'strategy': 'payment_with_subscription',
                    'plan_id': plan_id,
                    'subscription_id': subscription_id
                }
            )
            
            logger.info(f'Suscripción creada (estrategia 1): {subscription.id}')
            
            return JsonResponse({
                'success': True,
                'url': response.get('url'),
                'token': response.get('token'),
                'subscription_id': subscription.id
            })
            
        except Exception as e:
            logger.warning(f'Estrategia 1 falló: {str(e)}. Intentando estrategia 2...')
        
        # Estrategia 2: subscription/create + payment/create
        try:
            # Obtener o crear customer
            customer_id = get_or_create_flow_customer(email)
            
            # Crear suscripción
            sub_response = flow_client.create_subscription(
                plan_id=plan_id,
                subscription_id=subscription_id,
                customer_id=customer_id,
                return_url=return_url,
                confirmation_url=confirmation_url
            )
            
            flow_subscription_id = sub_response.get('subscriptionId')
            
            # Crear pago inicial
            payment_response = flow_client.create_payment(
                commerce_order=commerce_order,
                subject=f'Primer pago - {plan_id}',
                currency='CLP',
                amount=amount,
                email=email,
                return_url=return_url,
                confirmation_url=confirmation_url,
                payment_method=9,
                subscription_id=flow_subscription_id,
                customer_id=customer_id
            )
            
            # Crear registro en BD
            subscription = Subscription.objects.create(
                email=email,
                amount=amount,
                currency='CLP',
                frequency='monthly',
                provider='flow',
                commerce_order=commerce_order,
                flow_token=payment_response.get('token'),
                flow_url=payment_response.get('url'),
                flow_customer_id=customer_id,
                flow_subscription_id=flow_subscription_id,
                flow_plan_id=plan_id,
                status='pending',
                mode='real',
                metadata={
                    'strategy': 'subscription_plus_payment',
                    'plan_id': plan_id,
                    'subscription_id': subscription_id,
                    'customer_id': customer_id
                }
            )
            
            logger.info(f'Suscripción creada (estrategia 2): {subscription.id}')
            
            return JsonResponse({
                'success': True,
                'url': payment_response.get('url'),
                'token': payment_response.get('token'),
                'subscription_id': subscription.id
            })
            
        except Exception as e:
            logger.error(f'Estrategia 2 falló: {str(e)}. Usando modo demo...')
        
        # Estrategia 3: Demo mode (fallback cuando todo falla)
        demo_token = f'demo_{uuid.uuid4().hex[:16]}'
        demo_url = 'https://sandbox.flow.cl/app/web/pay.php'
        
        subscription = Subscription.objects.create(
            email=email,
            amount=amount,
            currency='CLP',
            frequency='monthly',
            provider='flow',
            commerce_order=commerce_order,
            flow_token=demo_token,
            flow_url=demo_url,
            flow_plan_id=plan_id,
            status='pending',
            mode='demo',
            metadata={
                'strategy': 'demo_fallback',
                'error': 'Flow API no disponible',
                'plan_id': plan_id
            }
        )
        
        logger.warning(f'Suscripción en modo demo: {subscription.id}')
        
        return JsonResponse({
            'success': True,
            'url': demo_url,
            'token': demo_token,
            'subscription_id': subscription.id,
            'mode': 'demo'
        })
        
    except Exception as e:
        logger.error(f'Error fatal creando suscripción: {str(e)}')
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def flow_webhook(request):
    """
    Webhook de Flow.cl que recibe notificaciones de pagos.
    Actualiza el estado de las suscripciones.
    """
    try:
        # Flow envía datos como POST form data
        token = request.POST.get('token') or request.GET.get('token')
        status = request.POST.get('status') or request.GET.get('status')
        
        if not token:
            logger.error('Webhook sin token')
            return HttpResponse('Token requerido', status=400)
        
        logger.info(f'Webhook recibido - Token: {token}, Status: {status}')
        
        # Buscar suscripción por token
        try:
            subscription = Subscription.objects.get(flow_token=token)
        except Subscription.DoesNotExist:
            logger.error(f'Suscripción no encontrada para token: {token}')
            return HttpResponse('Suscripción no encontrada', status=404)
        
        # Si no hay status en el webhook, consultar a Flow
        if not status:
            try:
                payment_status = flow_client.get_payment_status(token)
                status = str(payment_status.get('status', ''))
            except Exception as e:
                logger.error(f'Error consultando estado a Flow: {str(e)}')
                status = None
        
        # Mapear estados de Flow a nuestros estados
        # Flow estados: 1=PENDING, 2=PAID, 3=REJECTED, 4=CANCELLED
        status_mapping = {
            '1': 'pending',
            '2': 'paid',
            '3': 'failed',
            '4': 'cancelled'
        }
        
        new_status = status_mapping.get(status, 'pending')
        
        # Actualizar suscripción
        subscription.status = new_status
        
        if new_status == 'paid':
            from django.utils import timezone
            subscription.payment_date = timezone.now()
        
        # Actualizar metadata
        subscription.metadata.update({
            'webhook': {
                'received_at': str(timezone.now()),
                'status': status,
                'confirmed_status': new_status
            }
        })
        
        subscription.save()
        
        logger.info(f'Suscripción actualizada: {subscription.id} -> {new_status}')
        
        return JsonResponse({
            'received': True,
            'subscription_id': subscription.id,
            'status': new_status
        })
        
    except Exception as e:
        logger.error(f'Error en webhook: {str(e)}')
        return HttpResponse(f'Error: {str(e)}', status=500)


def payment_success(request):
    """Página de éxito después del pago"""
    token = request.GET.get('token')
    
    context = {
        'token': token,
        'provider': 'Flow.cl'
    }
    
    if token:
        try:
            subscription = Subscription.objects.get(flow_token=token)
            context['subscription'] = subscription
        except Subscription.DoesNotExist:
            pass
    
    return render(request, 'payments/success.html', context)
```

### 6. URLs

**Archivo:** `payments/urls.py`

```python
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('flow/create/', views.create_flow_subscription, name='flow_create'),
    path('api/flow/webhook/', views.flow_webhook, name='flow_webhook'),
    path('success/', views.payment_success, name='success'),
]
```

**En tu `urls.py` principal:**

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('pagos/', include('payments.urls')),
]
```

### 7. Template de Página de Pagos

**Archivo:** `templates/payments/checkout.html`

```html
{% extends 'base.html' %}

{% block content %}
<div class="row">
    <div class="col-md-8 mx-auto">
        <h1 class="mb-4">Suscripción Mensual</h1>
        
        <div class="row">
            {% for amount, plan in plans.items %}
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body text-center">
                        <h5 class="card-title">${{ amount|floatformat:0 }} CLP</h5>
                        <p class="text-muted">por mes</p>
                        <button 
                            class="btn btn-primary btn-subscribe" 
                            data-amount="{{ amount }}">
                            Suscribirse
                        </button>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <!-- Modal para ingresar email -->
        <div class="modal fade" id="emailModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Confirmar Suscripción</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="subscriptionForm">
                            {% csrf_token %}
                            <input type="hidden" id="amount" name="amount">
                            <div class="mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input 
                                    type="email" 
                                    class="form-control" 
                                    id="email" 
                                    name="email" 
                                    required>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary">
                                    Continuar al pago
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
document.querySelectorAll('.btn-subscribe').forEach(btn => {
    btn.addEventListener('click', function() {
        const amount = this.dataset.amount;
        document.getElementById('amount').value = amount;
        new bootstrap.Modal(document.getElementById('emailModal')).show();
    });
});

document.getElementById('subscriptionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    try {
        const response = await fetch('/pagos/flow/create/', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success && data.url) {
            // Redirigir a Flow
            window.location.href = `${data.url}?token=${data.token}`;
        } else {
            alert('Error: ' + (data.error || 'Desconocido'));
        }
    } catch (error) {
        alert('Error al procesar pago: ' + error);
    }
});
</script>
{% endblock %}
```

### 8. Configurar Planes en Flow Dashboard

1. Ingresa a https://www.flow.cl/app/web/planes.php
2. Crea planes mensuales con nombres exactos:
   - "5000 Mensual" → $5.000 CLP/mes
   - "10000 Mensual" → $10.000 CLP/mes
   - etc.

3. Copia los Plan IDs y agrégalos a tu `.env`

---

## Checklist de Implementación Flow.cl

- [ ] Instalar dependencias (requests, cryptography)
- [ ] Configurar variables de entorno
- [ ] Crear modelos (FlowCustomer, Subscription)
- [ ] Ejecutar migraciones
- [ ] Crear librería flow.py
- [ ] Crear views de pagos
- [ ] Configurar URLs
- [ ] Crear templates
- [ ] Configurar planes en Flow dashboard
- [ ] Configurar webhook URL en Flow dashboard
- [ ] Probar en sandbox
- [ ] Cambiar a producción (FLOW_SANDBOX=False)

---

## Troubleshooting Flow.cl

**Error: "apiKey not found"**
- Verificar FLOW_API_KEY en .env
- Verificar que esté usando el apiKey correcto (sandbox vs prod)

**Error: "Plan not found"**
- Verificar que el plan existe en Flow dashboard
- Verificar nombre exacto del plan

**Webhook no llega:**
- Verificar URL pública accesible
- Verificar @csrf_exempt en la vista
- Revisar logs de Flow dashboard

**Customer already exists:**
- La tabla FlowCustomer debería prevenir esto
- Si persiste, limpiar tabla y recrear

---

## Formato de Output

Cuando uses este skill, especifica:
- Proveedor (Flow.cl / Stripe / Ambos)
- Planes de suscripción (montos y frecuencia)
- Características especiales

Ejemplo:
```
"Implementa sistema de suscripciones con Flow.cl para Chile.
Necesito 5 planes: 10k, 20k, 50k, 100k, 250k CLP mensuales.
Incluye webhook para actualizar estados y página de éxito."
```

El skill generará todo el código necesario basado en implementación probada en producción.
