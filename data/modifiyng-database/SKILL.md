---
name: modifiyng-database
description: "Workflow para hacer cambios seguros en Supabase/Postgres (DDL y datos) con migraciones, validación y rollback. USE FOR: crear/alterar tablas, índices, constraints, RLS, seeds y cambios de esquema sin romper contratos de aplicación."
---

# Modifiyng Database

## Objetivo
Aplicar cambios de base de datos en Supabase de forma segura, trazable y reversible, priorizando migraciones, compatibilidad y verificación posterior.

## Resultado Esperado
- Cambios de esquema aplicados mediante migraciones versionadas.
- Riesgo de regresión minimizado con validaciones previas y posteriores.
- Compatibilidad protegida para frontend/backend y consumidores legacy.
- Evidencia de seguridad/performance revisada tras cambios.

## Entradas Mínimas
- Qué cambio se quiere hacer (tabla, columna, índice, política, seed).
- Motivación del cambio (feature, bugfix, performance, seguridad).
- Impacto esperado en API/queries actuales.
- Entorno de ejecución (local, staging, prod).

## Flujo Paso a Paso

### 1. Definir alcance y riesgo
- Describir cambio exacto (add, alter, drop, rename).
- Clasificar impacto:
  - `Bajo`: agregado backward-compatible.
  - `Medio`: cambio con migración de datos o índice sensible.
  - `Alto`: drop/rename/restricción que puede romper clientes.
- Confirmar ventanas de despliegue para cambios de riesgo medio/alto.

Chequeo de salida:
- Hay plan explícito de cambio y evaluación de impacto.

### 2. Inspeccionar estado actual
- Listar tablas, columnas, claves y relaciones relevantes.
- Verificar extensiones/migraciones ya aplicadas.
- Identificar dependencias de consultas activas y rutas API.

Decisiones:
- Si existe ambigüedad de esquema, no migrar hasta resolverla.
- Si hay drift entre ambientes, alinear primero antes del cambio.

Chequeo de salida:
- Se conoce el estado base real antes de modificar.

### 3. Diseñar migración segura
- Usar migración versionada para DDL (no cambios manuales ad hoc).
- Favorecer patrón expand-and-contract para compatibilidad:
  1. Expandir (agregar campos/objetos nuevos).
  2. Migrar consumo/aplicación.
  3. Contraer (retirar legado en fase posterior).
- Para datos: evitar hardcode de IDs generados dinámicamente.

Decisiones:
- Si el cambio rompe contrato, dividir en 2 o más releases.
- Si requiere backfill costoso, ejecutar por lotes.

Chequeo de salida:
- Migración diseñada con estrategia de compatibilidad y rollback.

### 4. Aplicar y validar técnicamente
- Aplicar migración en entorno objetivo.
- Verificar:
  - esquema resultante,
  - claves e índices,
  - políticas RLS,
  - funciones/triggers afectados.
- Ejecutar queries de humo para rutas críticas.

Chequeo de salida:
- El estado posterior coincide con el diseño esperado.

### 5. Revisar seguridad y performance
- Ejecutar advisors de seguridad y performance en Supabase.
- Corregir hallazgos críticos antes de cerrar.
- Revisar planes de ejecución de queries sensibles si cambian índices.

Chequeo de salida:
- No quedan alertas críticas abiertas relacionadas al cambio.

### 6. Cierre operacional
- Documentar migración aplicada, impacto y riesgos residuales.
- Registrar plan de rollback y condiciones de activación.
- Listar tareas de follow-up (limpieza, deprecaciones, optimizaciones).

Chequeo de salida:
- Cambio cerrado con trazabilidad y plan de contingencia.

## Reglas de Calidad
- DDL siempre por migración, no por SQL manual aislado.
- Cambios destructivos solo con plan de compatibilidad y rollback.
- Nunca exponer secretos ni depender de datos sensibles en scripts.
- Mantener idempotencia cuando aplique para scripts de datos.

## Checklist Rápido
1. Alcance y riesgo definidos.
2. Estado actual inspeccionado.
3. Migración diseñada con compatibilidad.
4. Migración aplicada y validada.
5. Advisors security/performance revisados.
6. Cierre con rollback y documentación.

## Prompt de Ejemplo
- "Aplica la skill modifiyng-database para agregar una tabla de sesiones con RLS y rollback plan."
- "Usa modifiyng-database para renombrar una columna sin romper clientes legacy."
