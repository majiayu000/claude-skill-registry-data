---
name: infra-sre
description: >
  Monitoreo, alertas y confiabilidad de sistemas — Prometheus, Grafana,
  logging, SLIs/SLOs, incident response y observabilidad.
  Trigger: Cuando necesitás monitorear un servicio, configurar alertas, definir SLOs o responder a un incidente.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Skill: infra-sre

Si no está monitoreado, no existe.

## Trigger

- Un servicio está caído y no te diste cuenta
- Querés dashboards para ver el estado del sistema
- Necesitás alertas que avisen antes de que explote
- Hay que definir SLOs y error budgets
- Estás haciendo postmortem de un incidente

## Workflow LEND

```
1. ANALIZAR
   ├── ¿Qué servicios corren? (API, worker, DB, frontend)
   ├── Stack actual (Prometheus? Datadog? CloudWatch? Nada?)
   ├── ¿Qué métricas importan? (latencia, errores, throughput, saturación)
   └── ¿Hay logs centralizados?

2. OFRECER (Menú del Senior)
   ├── A) Mínimo: healthcheck endpoint + uptime monitoring (UptimeRobot/Heartbeat)
   ├── B) Standard: Prometheus + Grafana dashboards + alertas críticas
   └── C) Full SRE: todo + SLIs/SLOs + error budgets + runbooks + logging (Loki/ELK)

3. ELEGIR → el usuario confirma

4. HACER
   ├── Endpoint /health y /metrics en la app
   ├── Exporters (node_exporter, postgres_exporter, blackbox_exporter)
   ├── Prometheus config + reglas de alerta
   ├── Grafana dashboards (USE method for infra, RED method for services)
   ├── Alertmanager (Slack, email, PagerDuty)
   └── Runbooks para incidentes comunes

5. VERIFICAR
   ├── Las métricas llegan a Prometheus
   ├── Las alertas se disparan correctamente (probar con condiciones reales)
   └── El dashboard muestra datos con sentido
```

## Patrones

- **USE method**: Utilization, Saturation, Errors (para infra)
- **RED method**: Rate, Errors, Duration (para servicios)
- **Four golden signals**: latency, traffic, errors, saturation
- **SLIs**: medir lo que importa al usuario (latencia P99, error rate)
- **SLOs**: objetivos realistas (99.9% okay, 99.99% requiere esfuerzo)
- **Error budget**: 100% - SLO. Cuando se acaba, parar features, arreglar estabilidad
- **Postmortems sin blame**: el sistema falló, no la persona

## Anti-patrones

- Alertas que nadie mira (alerta que no duele = ruido)
- Dashboards sin contexto (métrica sin unidad = números flotando)
- SLOs aspiracionales sin data histórica
- No tener runbooks — en medio de un incidente no se piensa
- Monitorear todo menos lo que ve el usuario
