---
name: portal-finops
description: Audit and control cloud costs for the Portal Centralizado de Datos Financieros — budget under $45 USD/month with billing alert at 50%. Use for cost audits, scale-to-zero verification, Gemini token budget checks, lifecycle policies, and reading llm.usage.* attributes from OTel traces (section 23 of the plan, R09).
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal FinOps Skill

## Rules — NON-NEGOTIABLE

- Presupuesto total: **< $45 USD/mes**, alerta de billing al **50%** ($22.50). Superarlo es riesgo R09 — escalar al equipo.
- Cloud Run SIEMPRE `min_instances = 0`. La excepción (`min_instances = 1`) aplica SOLO el día de demo/pruebas de usabilidad, se decide en el cierre de producción y queda documentada — y se revierte al terminar.
- Gemini SOLO Flash-Lite con `thinking_level: medium` por defecto; presupuesto de tools máx 5 calls por consulta; caché de respuestas frecuentes activa.
- Exports en GCS con lifecycle de 7 días; Artifact Registry sin imágenes huérfanas.
- La fuente de verdad del gasto LLM son los atributos OTel `llm.usage.*` del span `llm.call` (skill `portal-observability`) — no estimaciones a mano.

## Presupuesto (§23 del plan)

| Concepto | Estimación mensual | Palanca de control |
|----------|--------------------|--------------------|
| Gemini 3.5 Flash-Lite (dev + demo) | $5–15 USD | Presupuesto de tools (máx 5 calls), caché de respuestas, `thinking_level` medium |
| Cloud Run (front + back) | $0–10 USD | Scale-to-zero; fuera de horario no cuesta; cold start monitoreado en el smoke de producción |
| GCS + Artifact Registry | $1–5 USD | Lifecycle 7 días en exports; limpiar tags viejos de imágenes |
| PostgreSQL (Cloud SQL micro o contenedor) | $0–15 USD | pgvector en contenedor local para dev; cloud solo para demo |
| **Total** | **< $45 USD/mes** | Alerta de billing al 50% |

## Alerta de billing (Terraform)

```hcl
# infra/billing.tf
resource "google_billing_budget" "monthly" {
  billing_account = var.billing_account
  display_name    = "Portal monthly 45 USD"
  amount {
    specified_amount {
      currency_code = "USD"
      units         = "45"
    }
  }
  threshold_rules { threshold_percent = 0.5 }   # alerta comprometida en el plan
  threshold_rules { threshold_percent = 0.9 }
  threshold_rules { threshold_percent = 1.0 }
}
```

## Auditoría rápida

```bash
# scripts/cost_audit.sh
echo "=== Cloud Run scale-to-zero check ==="
for svc in portal-backend portal-frontend; do
  gcloud run services describe "$svc" --region "$REGION" \
    --format="value(spec.template.metadata.annotations['autoscaling.knative.dev/minScale'])"
done   # debe ser vacio o 0 salvo dia de demo documentado

echo "=== GCS lifecycle ==="
gsutil lifecycle get "gs://${PROJECT_ID}-exports"   # debe borrar a los 7 dias

echo "=== Budgets activos ==="
gcloud billing budgets list --billing-account="$BILLING_ACCOUNT_ID"
```

## Dónde leer el consumo LLM

Los tokens reales viven en las trazas OTel — cada span `llm.call` lleva:

| Atributo | Uso FinOps |
|----------|------------|
| `llm.usage.prompt_tokens` / `completion_tokens` / `total_tokens` | Tokens/día y costo/día (tokens × tarifa Flash-Lite) |
| `llm.model` | Verificar que SOLO se usa Flash-Lite (sin upgrades accidentales) |
| `llm.tool_calls.count` | Detectar consultas que agotan el presupuesto de 5 tools |

Tablero de consumo: tokens/día, costo estimado/día, p50/p95 de `llm.call`. Si el costo diario proyectado excede $0.50 (≈$15/mes solo LLM), revisar caché y prompts antes de seguir.

## Palancas de ahorro en código

- Caché en memoria TTL en extractores y caché de respuestas frecuentes del agente (R05).
- Datasets pequeños en demo; agregación server-side antes de graficar (no pagar egress de millones de filas).
- Cancelación real del stream SSE: Stop corta la llamada LLM en ms = tokens no facturados.
- Presupuesto de tools en el system prompt del agente: evita ciclos infinitos de tool calls.

## Checklist de auditoría (semanal + antes de cada demo)

- [ ] Billing budget de $45 con alerta al 50% activo
- [ ] `min_instances = 0` en ambos Cloud Run (o excepción de demo documentada con fecha de reversión)
- [ ] Lifecycle 7 días vigente en bucket de exports
- [ ] Artifact Registry sin imágenes sin tag de más de 30 días
- [ ] `llm.model` en trazas = Flash-Lite únicamente
- [ ] Consultas con `llm.tool_calls.count` = 5 investigadas (presupuesto agotado)
- [ ] Tablero tokens/día revisado; proyección mensual dentro de presupuesto
- [ ] PostgreSQL cloud apagado/mínimo fuera de ventanas de demo
