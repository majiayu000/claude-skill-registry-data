---
name: backup-engineer
description: >
  Estrategias de backup, disaster recovery, RPO/RTO, restauración y
  continuidad de negocio. Que los datos no se pierdan nunca.
  Trigger: Cuando necesitás diseñar backup strategy, configurar backups automáticos, o planificar disaster recovery.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Skill: backup-engineer

Backups que funcionan cuando los necesitás. No cuando los probás.

## Trigger

- Diseñar estrategia de backup para un servicio
- Configurar backups automáticos de DB o archivos
- Probar restauración (drill)
- Definir RPO/RTO para un proyecto
- Planificar disaster recovery

## Workflow LEND

1. ANALIZAR
   ├── Datos: DB (PostgreSQL, MySQL), archivos, configuraciones, estado
   ├── Volumen: tamaño, tasa de cambio, retención necesaria
   ├── RPO: ¿cuántos datos podemos perder? (5 min, 1 hora, 1 día)
   └── RTO: ¿cuánto tiempo para recuperar? (minutos, horas, días)

2. OFRECER (Menú del Senior)
   ├── A) Backup simple — pg_dump + rsync a otro disco/S3, útil para proyectos chicos
   ├── B) Estrategia 3-2-1 — 3 copias, 2 medios, 1 offsite. Restic/Borg + S3
   └── C) DRP completo — replicación en caliente, failover automático, drills periódicos

3. ELEGIR → confirmación

4. HACER
   ├── DB: pg_dump / WAL archiving / replicación. Probar restore periódicamente
   ├── Archivos: rsync, restic, borg. Con cifrado, compresión, deduplicación
   ├── 3-2-1: 3 copias (prod + backup local + backup remoto), 2 medios, 1 offsite
   ├── Automatización: cron + script con logging y notificación
   ├── Retention: diario 7 días, semanal 4 semanas, mensual 12 meses
   └── DRP: documento con procedimientos, contactos, RPO/RTO, playbook de recuperación

5. VERIFICAR
   ├── El backup se completa sin errores
   ├── El restore funciona (probado en ambiente aislado)
   └── Las notificaciones llegan si el backup falla
