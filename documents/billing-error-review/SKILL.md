---
name: billing-error-review
description: Detecta posibles errores de facturacion cometidos por administracion desde exports CSV/XLS/XLSX (duplicados, matematica fiscal, estados de pago, fechas y datos faltantes). Use when the user asks to review billing errors, invoice inconsistencies, admin mistakes, month close controls, or pre-audit billing checks.
---

# Billing Error Review

**Before working:** Read `docs/team/knowledge/Billing.md` if it exists.

## Purpose

Actuar como auditor operativo de facturacion para identificar errores
administrativos antes de cierre mensual, liquidacion o defensa documental.

## Inputs Expected

Priorizar datos tabulares (CSV/XLS/XLSX):

- Export de facturas y notas de credito.
- Export de estado de cobro/pago (si viene separado, unir por documento).
- Periodo de control (`YYYY-MM`) cuando aplique.
- Contexto operativo: reglas internas de negocio y tolerancia de redondeo.

Si faltan datos, continuar con lo disponible y explicitar limitaciones.

## Propagation

Si el cambio afecta a otros (Mapping, Fiscal, Audit): actualizar `docs/team/PROJECT-STATE.md` y consultar tabla de propagación en `docs/team/PROJECT-TEAM-FULL-COVERAGE.md` §4.

## Mandatory Execution Rules

1. No modificar datos originales de facturacion.
2. No borrar documentos ni ejecutar cambios contables automaticos.
3. Separar hechos verificados de hipotesis.
4. Reportar evidencia por fila (doc_key, fila fuente, regla violada).
5. Mantener salida accionable para administracion.

## Workflow

Copiar y actualizar este progreso:

```text
Billing Review Progress:
- [ ] 1. Validar archivo y columnas minimas
- [ ] 2. Normalizar estructura y llaves de documento
- [ ] 3. Ejecutar reglas de control
- [ ] 4. Clasificar hallazgos por severidad
- [ ] 5. Emitir reporte y acciones recomendadas
```

### 1) Validacion inicial

- Confirmar formato soportado: `.csv`, `.xls`, `.xlsx`.
- Confirmar columnas minimas: tipo, numero, fecha, neto, impuesto, total.
- Detectar columnas alternativas por alias.

### 2) Normalizacion

Normalizar campos:

- `tipo`, `serie`, `numero`, `fecha`, `rut_cliente`.
- `neto`, `impuesto`, `total`.
- `estado_pago`, `fecha_pago`, `referencia_pago` (si existen).

Construir `doc_key = tipo|serie|numero`.

### 3) Reglas de control (v1)

- Duplicados por `doc_key`.
- Inconsistencia matematica: `neto + impuesto != total`
  (tolerancia configurable).
- Nota de credito con signo/uso invalido (ej. total positivo).
- Campos obligatorios faltantes o con formato invalido.
- Desfase de periodo respecto al mes auditado.
- Contradiccion de estado de pago:
  marcado pago sin fecha/referencia.

### 4) Severidad sugerida

- `critical`: duplicados y matematica fiscal material.
- `high`: documento invalido o fecha fuera de periodo.
- `medium`: estado de pago inconsistente o NC dudosa.
- `low`: datos incompletos no bloqueantes.

### 5) Salida obligatoria

Entregar:

1. `diagnostico_rapido` con conteos por severidad/tipo.
2. `hallazgos` por fila con causa y sugerencia de correccion.
3. `acciones_recomendadas` priorizadas:
   hoy / esta semana / cierre de mes.

## Output Contract

Responder en este formato:

1. Hallazgos criticos (primero).
2. Errores recurrentes por tipo.
3. Lista de documentos a corregir.
4. Acciones de control preventivo.
5. Limites del analisis (si faltan datos).

## Additional Resources

- Reglas y mapeos: [reference.md](reference.md)
- Casos de uso: [examples.md](examples.md)
- Script opcional: [scripts/check_billing_errors.py](scripts/check_billing_errors.py)
