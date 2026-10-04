---
name: inspect-database
description: "Workflow para inspeccionar y auditar Supabase/Postgres sin modificar datos, entendiendo esquema, relaciones, migraciones, logs y riesgos. USE FOR: diagnóstico de estructura, inventario de tablas, análisis de dependencias, revisión de seguridad y troubleshooting de consultas."
---

# Inspect Database

## Objetivo
Obtener una visión confiable del estado de la base de datos (estructura, relaciones, salud y riesgo) sin aplicar cambios destructivos.

## Resultado Esperado
- Mapa de esquema actualizado y entendible.
- Hallazgos priorizados de integridad, seguridad y performance.
- Hipótesis de diagnóstico con evidencia.
- Recomendaciones accionables para el siguiente cambio.

## Entradas Mínimas
- Pregunta de inspección principal (qué se quiere entender).
- Alcance (schema, tablas o dominio funcional).
- Entorno consultado.
- Síntoma asociado, si existe (error, lentitud, inconsistencias).

## Flujo Paso a Paso

### 1. Definir pregunta y alcance
- Traducir la necesidad en preguntas concretas:
  - ¿Qué tablas participan?
  - ¿Qué relaciones/cascadas existen?
  - ¿Qué migración introdujo el cambio?
- Limitar alcance para evitar análisis difuso.

Chequeo de salida:
- Hay objetivo de inspección claro y verificable.

### 2. Inventario estructural
- Listar tablas por schema.
- Para cada tabla crítica, identificar:
  - columnas y tipos,
  - PK/FK,
  - índices,
  - constraints.
- Detectar tablas huérfanas o naming inconsistente.

Chequeo de salida:
- Estructura base documentada con foco en entidades críticas.

### 3. Trazabilidad de cambios
- Revisar historial de migraciones aplicadas.
- Relacionar cambios estructurales con síntomas reportados.
- Señalar discrepancias entre lo esperado y lo realmente aplicado.

Decisiones:
- Si faltan migraciones esperadas, marcar drift de entorno.
- Si hay cambios manuales fuera de migración, elevar riesgo.

Chequeo de salida:
- Se entiende cuándo y cómo evolucionó el esquema.

### 4. Diagnóstico operativo
- Revisar logs de servicios relevantes (postgres/api/auth/realtime según caso).
- Correlacionar errores con endpoints o consultas específicas.
- Identificar patrones:
  - timeouts,
  - locks,
  - violaciones de constraints,
  - picos de errores.

Chequeo de salida:
- Existe evidencia operacional para sostener hipótesis.

### 5. Revisión de seguridad y performance
- Ejecutar advisors de seguridad/performance.
- Validar si hay:
  - RLS ausente o incompleta,
  - políticas demasiado permisivas,
  - índices faltantes en rutas de consulta frecuentes.
- Priorizar hallazgos por severidad e impacto.

Chequeo de salida:
- Hallazgos categorizados con prioridad y recomendación.

### 6. Entrega de hallazgos
- Presentar resumen ejecutivo corto.
- Listar findings priorizados:
  - severidad,
  - evidencia,
  - impacto,
  - acción sugerida.
- Incluir riesgos residuales y supuestos abiertos.

Chequeo de salida:
- El equipo puede decidir próximos pasos sin investigación adicional inmediata.

## Reglas de Calidad
- No ejecutar DDL durante inspección.
- Separar hechos observados de inferencias.
- Citar evidencia mínima por hallazgo.
- Evitar conclusiones sin correlación técnica.

## Checklist Rápido
1. Objetivo y alcance definidos.
2. Esquema inventariado.
3. Migraciones y drift revisados.
4. Logs y síntomas correlacionados.
5. Advisors analizados.
6. Hallazgos priorizados y accionables.

## Prompt de Ejemplo
- "Usa inspect-database para mapear relaciones y constraints del dominio de simulaciones."
- "Ejecuta inspect-database para investigar por qué fallan inserciones intermitentes en una tabla con RLS."
