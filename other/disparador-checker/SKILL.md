---
name: disparador-checker
description: Conocimiento de fondo sobre los aplazamientos conscientes del MVP y sus disparadores de reapertura (ADR-0015). Cuando la conversación toca algo que se decidió aplazar — multi-rol, soporte interno, native-image, Multi-AZ, ElastiCache, Secrets Manager, CloudFront, NgRx, login con Google, MFA, app móvil, etc. — recuerda el disparador concreto y el ADR origen antes de reabrir nada.
disable-model-invocation: false
---

# Disparador Checker — Runcriticon

Conocimiento de fondo para Claude. **No es invocable por el usuario**: es contexto que Claude debe tener presente cuando la conversación roza un tema aplazado, para no reabrir decisiones cerradas sin que se haya cumplido su disparador.

## Principio

[`docs/adr/0015-temas-aplazados-fuera-del-mvp.md`](../../../docs/adr/0015-temas-aplazados-fuera-del-mvp.md) es el **índice maestro consolidado** de todo lo que queda fuera del MVP, cada cosa con un disparador concreto de reapertura. Antes de proponer construir algo que se decidió aplazar, Claude debe:

1. Reconocer que el tema está aplazado.
2. Citar el **disparador concreto** y el ADR origen.
3. Comprobar (o preguntar) si el disparador se ha cumplido.
4. Solo entonces proponer reabrir el ADR correspondiente (con la skill `/adr-review`).

## Tabla de disparadores (memoria operativa)

> **Esta tabla es caché de ADR-0015.** Antes de citar un disparador, verifícalo en [`docs/adr/0015-temas-aplazados-fuera-del-mvp.md`](../../../docs/adr/0015-temas-aplazados-fuera-del-mvp.md) — si difieren, el ADR manda y esta tabla debe actualizarse (el agente `adr-coherence-scanner` detecta las divergencias).

### Identidad y autorización

| Tema aplazado | Disparador | Origen |
|---|---|---|
| Multi-rol por usuario | Primer caso real que rompe el modelo de dos cuentas | ADR-0003 D2, ADR-0009 |
| Login con Google (OAuth2) | Demanda real o cliente que lo exige | ADR-0003 D5 |
| MFA | Cliente con datos más sensibles o exigencia regulatoria | ADR-0003 D5 |
| Solicitud de acceso + aprobación | Crecimiento donde la delegación a entrenadores no escala | ADR-0003 D3 |
| Logout de todos los dispositivos | Demanda real o equipo con tiempo | ADR-0003 D11 |
| Matriz de autorización configurable | Primer club que pide rol propio **o** segundo club con organización distinta | ADR-0009 D6 |
| Rol de soporte interno | Segundo club piloto **o** incidencia donde soporte necesita ver datos sin admin | ADR-0009 D19 |

### RGPD

| Tema aplazado | Disparador | Origen |
|---|---|---|
| Tratamiento de menores | Entra club con menores **o** primera solicitud de alta de menor | ADR-0014 D17 |
| DPO formal | > 1000 usuarios totales **o** observación sistemática a gran escala | ADR-0014 D21 |
| Self-service export RGPD | Segundo club **o** > 5 solicitudes/mes durante 2 meses | ADR-0014 D12 |

### Infraestructura

| Tema aplazado | Disparador | Origen |
|---|---|---|
| Spring Session en Redis | Al aumentar `min` de App Runner a ≥ 2 | ADR-0003 D10 + ADR-0006 D4 |
| ElastiCache (caché de app) | p95 endpoint > 800 ms 1 semana **o** autoescalado a max=3 | ADR-0006 D4, ADR-0015 A2 |
| Multi-AZ RDS | Segundo club **o** ~500 usuarios activos sostenidos un mes | ADR-0006 D10 |
| ECS Fargate (vs App Runner) | Control de red avanzado **o** coste sostenido > 200 €/mes **o** límites de App Runner | ADR-0006 D5 |
| CloudFront | Latencia p95 Madrid > 500 ms 2 semanas **o** DDoS **o** coste salida > 30 €/mes | ADR-0006 D17 |
| Backups cross-region | Cliente con SLA contractual > 99,5 % | ADR-0006 D9/D29 |

### Email, secretos, observabilidad

| Tema aplazado | Disparador | Origen |
|---|---|---|
| Migración a SES | > 50 000 emails/mes sostenidos 2 meses **o** coste Postmark > 100 €/mes | ADR-0005 D15 |
| Secrets Manager (rotación auto) | Equipo > 4 personas **o** incidente con secretos | ADR-0013 D16 |
| KMS Customer Managed Key | Auditoría externa **o** cliente con regulación específica | ADR-0013 D17 |
| Vault / Doppler | Multi-cloud real **o** > 50 secretos | ADR-0013 D18 |
| Loki / Tempo dedicados | CloudWatch Logs > 30 €/mes 2 meses **o** > 50 GB/mes | ADR-0011 D22 |
| Error tracking (Sentry) | > 10 excepciones únicas/semana durante 4 semanas | ADR-0011 D23 |
| SaaS observabilidad (Datadog) | Cliente con SLA contractual > 99,5 % **o** equipo > 8 | ADR-0011 D24 |
| Slack / PagerDuty alertas | Equipo > 4 **o** > 5 alarmas/semana | ADR-0011 D17 |

### Frontend, CI/CD, runtime

| Tema aplazado | Disparador | Origen |
|---|---|---|
| NgRx por feature | Feature con estado complejo donde Signals + servicios es ilegible | ADR-0012 D16 |
| @ngx-translate dinámico | Idiomas distintos por club en multi-tenant | ADR-0012 D9 |
| WCAG 2.2 | Adopción generalizada del estándar 2.2 | ADR-0012 nota |
| Angular Material (u otra 2ª librería de componentes) | **RECHAZADO** (D5 revisada 2026-07 — un solo paradigma: spartan + Tailwind v4). Reabrir = nueva revisión de ADR | ADR-0012 D5 |
| App móvil nativa | Demanda real validada en discovery | ADR-0001, vision.md |
| Mutation testing en cada PR | Capacidad de runners para no penalizar cadencia | ADR-0010 D9 |
| CODEOWNERS | Equipo > 4 con responsabilidades diferenciadas | ADR-0010 D20 |
| GraalVM native-image (vs JIT) | Factura > 200 €/mes 2 meses por memoria **o** scale-to-zero con cold start penalizando **o** Spring Native maduro | ADR-0016 D11 |

## Cómo actuar

Cuando la conversación toca uno de estos temas:

- **Si el disparador NO se ha cumplido**: recordar que está aplazado conscientemente, citar el disparador, y NO construirlo. Ejemplo: *"Eso es multi-rol, aplazado en ADR-0003 D2. El disparador es 'primer caso real que rompe el modelo de dos cuentas'. ¿Ha aparecido ese caso, o lo resolvemos con dos cuentas como prevé el MVP?"*
- **Si el disparador SÍ se ha cumplido**: confirmarlo, y proponer reabrir el ADR con la skill `/adr-review`.
- **Si es algo RECHAZADO** (reintroducir Material, recuperación sin admin, etc.): señalar que reabrir requiere un ADR nuevo (o revisión formal) que sustituya la decisión, no un cambio sobre la marcha. Precedente: Tailwind estaba RECHAZADO por la D5 original y entró por revisión formal del ADR-0012 (2026-07-10), no por impulso.

## Regla

La existencia de un disparador documentado es lo que distingue un **aplazamiento consciente** de un **olvido**. Esta skill protege contra reabrir decisiones cerradas por impulso. Si el usuario insiste en construir algo aplazado sin disparador cumplido, Claude lo construye igual (es decisión del usuario) pero **deja constancia** de que se está adelantando a un disparador no cumplido.
