---
name: yukyu-compliance
description: Asistente especializado en normativa japonesa de vacaciones pagadas (有給休暇) y cumplimiento laboral
---

# Yukyu Compliance Skill (有給休暇コンプライアンススキル)

Este skill proporciona expertise especializada en la normativa japonesa de vacaciones pagadas y cumplimiento laboral según el Labor Standards Act de Japón.

## Normativa Japonesa Fundamental

### 1. Ley Básica de Vacaciones Pagadas (Labor Standards Act Article 39)

**Adquisición de Días de Vacaciones**:
- **6 meses continuos**: 10 días de vacaciones pagadas
- **1.5 años**: 11 días
- **2.5 años**: 12 días
- **3.5 años**: 14 días
- **4.5 años**: 16 días
- **5.5 años**: 18 días
- **6.5 años+**: 20 días (máximo)

**Requisitos**:
- Empleado debe haber trabajado al menos 6 meses continuos
- Tasa de asistencia del 80% o superior

### 2. Uso Obligatorio de 5 Días (平成31年4月施行)

**Reforma Laboral 2019**:
- Empleadores **DEBEN** asegurar que empleados con 10+ días tomen **mínimo 5 días** al año
- Aplicable a empleados a tiempo completo y tiempo parcial con días suficientes
- **Penalización**: Multa hasta ¥300,000 por empleado no conforme

**Métodos de Cumplimiento**:
1. **Solicitud voluntaria del empleado**: Empleado solicita días
2. **Designación por empleador**: Empleador asigna días específicos
3. **Plan de vacaciones programadas**: Sistema de calendario de vacaciones (計画的付与)

### 3. Período de Validez y Vencimiento

**Reglas de Caducidad**:
- Días de vacaciones vencen **2 años** después de otorgamiento
- Sistema de "carry-over" (繰越): Días no usados pasan al siguiente año
- Después de 2 años, días expiran automáticamente

**Ejemplo**:
```
2022年4月: 10日付与
2023年4月: 11日付与 (+ 10日繰越 = 21日総数)
2024年4月: 2022年分10日 → 失効
```

### 4. Cálculo de Tasa de Uso (使用率計算)

**Fórmula Estándar**:
```
使用率 = (使用日数 ÷ 付与日数) × 100
Usage Rate = (Days Used ÷ Days Granted) × 100
```

**Objetivo Nacional (政府目標)**:
- Meta del gobierno japonés: **70% de tasa de uso para 2025**
- Promedio actual nacional: ~58-60%

### 5. Tipos de Vacaciones

**Clasificación**:
1. **年次有給休暇 (Nenji Yukyu Kyuka)**: Vacaciones anuales pagadas estándar
2. **半日休暇 (Hannichi Kyuka)**: Medio día de vacaciones
3. **時間単位休暇 (Jikan Tani Kyuka)**: Vacaciones por horas (hasta 5 días/año convertibles)
4. **計画的付与 (Keikaku-teki Fuyo)**: Vacaciones planificadas por empresa

## Funcionalidades de Compliance para YuKyuDATA

### Verificaciones Automáticas

#### 1. Alerta de 5 Días Obligatorios
```python
def check_5day_compliance(employee_data, year):
    """
    Verifica si empleados con 10+ días han tomado mínimo 5 días
    """
    alerts = []
    for emp in employee_data:
        if emp['granted'] >= 10 and emp['used'] < 5:
            days_needed = 5 - emp['used']
            alerts.append({
                'employee': emp['name'],
                'status': 'NON_COMPLIANT',
                'days_needed': days_needed,
                'deadline': calculate_fiscal_year_end(year)
            })
    return alerts
```

#### 2. Detección de Días Próximos a Expirar
```python
def check_expiring_days(employee, current_date):
    """
    Detecta días que expirarán en los próximos 3 meses
    """
    expiring_days = []
    for grant in employee['grants']:
        expiry_date = grant['grant_date'] + timedelta(days=730)  # 2 años
        days_until_expiry = (expiry_date - current_date).days

        if 0 < days_until_expiry <= 90:  # 3 meses
            expiring_days.append({
                'days': grant['remaining_days'],
                'expiry_date': expiry_date,
                'urgency': 'HIGH' if days_until_expiry <= 30 else 'MEDIUM'
            })
    return expiring_days
```

#### 3. Validación de Tasa de Uso
```python
def validate_usage_rate(department_data):
    """
    Compara tasa de uso departamental con objetivo nacional
    """
    target_rate = 70.0  # Meta gobierno 2025

    for dept in department_data:
        usage_rate = (dept['total_used'] / dept['total_granted']) * 100

        if usage_rate < 50:
            status = 'CRITICAL'
        elif usage_rate < target_rate:
            status = 'NEEDS_IMPROVEMENT'
        else:
            status = 'GOOD'

        dept['compliance_status'] = status
```

### Generación de Reportes Legales

#### Libro Anual de Vacaciones (年次有給休暇管理簿)
**Requisito Legal**: Artículo 7-2 del Labor Standards Act

**Información Obligatoria**:
- Fecha de otorgamiento (基準日)
- Días otorgados (付与日数)
- Fechas de uso (取得日)
- Días restantes (残日数)
- Debe conservarse por **3 años**

```python
def generate_annual_ledger(employee_id, year):
    """
    Genera libro anual conforme a normativa
    """
    ledger = {
        'employee_id': employee_id,
        'fiscal_year': year,
        'grant_records': [],
        'usage_records': [],
        'balance_records': []
    }

    # Registros detallados por mes
    for month in range(1, 13):
        monthly_record = {
            'month': month,
            'granted': get_granted_days(employee_id, year, month),
            'used': get_used_days(employee_id, year, month),
            'balance': get_balance(employee_id, year, month),
            'expired': get_expired_days(employee_id, year, month)
        }
        ledger['usage_records'].append(monthly_record)

    return ledger
```

## Alertas Inteligentes

### Sistema de Notificaciones Proactivas

**Nivel 1: Informativo (情報)**
- "Tiene días próximos a expirar en 3 meses"
- "Ha usado el 30% de sus vacaciones anuales"

**Nivel 2: Advertencia (警告)**
- "Faltan 2 meses para fin de año fiscal, necesita usar 3 días más"
- "Tasa de uso departamental bajo objetivo (45% vs 70%)"

**Nivel 3: Crítico (緊急)**
- "Empleado no ha tomado 5 días obligatorios - quedan 30 días"
- "10 días expirarán en 15 días"
- "Posible incumplimiento legal - acción inmediata requerida"

### Calendario de Cumplimiento

```python
compliance_calendar = {
    'quarterly': [
        {
            'period': 'Q1 (Apr-Jun)',
            'checks': [
                'Verificar nuevos otorgamientos (6 meses)',
                'Revisar carry-over del año anterior',
                'Identificar empleados en riesgo de no cumplir 5 días'
            ]
        },
        {
            'period': 'Q2 (Jul-Sep)',
            'checks': [
                'Checkpoint 50% del año fiscal',
                'Alertar empleados con <2.5 días usados',
                'Review de tasas departamentales'
            ]
        },
        {
            'period': 'Q3 (Oct-Dec)',
            'checks': [
                'Checkpoint 75% del año fiscal',
                'Inicio de campaña uso de vacaciones',
                'Planning de vacaciones obligatorias si necesario'
            ]
        },
        {
            'period': 'Q4 (Jan-Mar)',
            'checks': [
                'Verificación final 5 días obligatorios',
                'Asignar vacaciones forzosas si <5 días',
                'Calcular días que expirarán 31/Marzo',
                'Preparar libro anual para auditoría'
            ]
        }
    ]
}
```

## Best Practices de Implementación

### 1. Enfoque Preventivo vs Reactivo
- ✅ **Preventivo**: Alertas tempranas, planificación proactiva
- ❌ **Reactivo**: Esperar hasta último mes del año fiscal

### 2. Comunicación con Empleados
- Notificaciones mensuales de balance
- Dashboard personal de vacaciones
- Recordatorios automáticos antes de expiración

### 3. Soporte a Managers
- Dashboard departamental de compliance
- Lista de empleados en riesgo
- Herramientas de planificación de equipo

### 4. Documentación Legal
- Backup automático de registros
- Audit trail de todas las transacciones
- Export a formato legal (Excel/PDF)

## Cálculos Especiales

### Para Empleados a Tiempo Parcial
```python
def calculate_prorated_days(weekly_hours, weekly_days, years_of_service):
    """
    Cálculo prorrateado según horas/días trabajados
    """
    if weekly_hours >= 30:
        return get_fulltime_days(years_of_service)

    # Tabla prorrateada según horas y días semanales
    prorated_table = {
        # (weekly_days, years): days_granted
        (4, 0.5): 7,
        (4, 1.5): 8,
        (4, 2.5): 9,
        # ... tabla completa según normativa
    }

    return prorated_table.get((weekly_days, years_of_service), 0)
```

### Año Fiscal Japonés (会計年度)
```python
def get_japanese_fiscal_year(date):
    """
    Año fiscal japonés: 1 Abril - 31 Marzo
    """
    if date.month >= 4:
        return date.year
    else:
        return date.year - 1

def fiscal_year_end(fiscal_year):
    """
    Retorna fecha fin de año fiscal
    """
    return datetime(fiscal_year + 1, 3, 31)
```

## Referencias Legales

**Leyes Principales**:
- 労働基準法 第39条 (Labor Standards Act Article 39)
- 労働基準法施行規則 第24条の7 (Enforcement Regulations Article 24-7)
- 平成30年改正労働基準法 (2019 Labor Law Reform)

**Recursos Oficiales**:
- Ministry of Health, Labour and Welfare (厚生労働省)
- Japan Labour Standards Inspection Office (労働基準監督署)

## Para Desarrolladores

Al implementar funcionalidades de compliance:

1. **Siempre usar año fiscal japonés** (Abril-Marzo) no calendario
2. **Validar requisito 80% asistencia** antes de otorgar días
3. **Calcular carry-over correctamente** considerando expiración 2 años
4. **Implementar logging de auditoría** para todas las operaciones
5. **Generar alertas con suficiente antelación** (mínimo 3 meses)
6. **Soportar múltiples formatos de fecha** japoneses (和暦/西暦)

---

**Principio Guía**: "Compliance no es solo evitar multas, es cuidar el bienestar de los empleados y promover work-life balance conforme a los valores japoneses."

使用者の健康と幸福を第一に考えましょう。
