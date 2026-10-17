---
name: agent-mesh-mcp
description: >
  Homelab Agent Mesh Architecture, Cost-Aware Model Routing (Prometheus PromQL integration),
  and Decoupled Component Deployments for K3s-homelab cluster.
license: MIT
compatibility:
  - opencode
metadata:
  author: workstation-agent
  tags: [agent-mesh, mcp, cost-aware, litellm, prometheus, ansible, decoupling]
---

# Agent Mesh & Cost-Aware Routing Skill

Este Skill documenta la arquitectura de comunicación de agentes (Agent-to-Agent Mesh) en la homelab, el sistema de auto-regulación de costes mediante Prometheus, y el flujo para realizar despliegues desacoplados y granulares en el clúster.

---

## 1. Arquitectura de Malla de Agentes (Agent-to-Agent Mesh)

En la homelab, la interacción entre agentes sigue un patrón de **delegación unidireccional y especializada**, evitando acoplamientos innecesarios.

```
                  ┌──────────────────────┐
                  │   Usuario (Telegram) │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │       OpenClaw       │
                  │   (Cliente Principal)│
                  └──────────┬───────────┘
                             │
                             ├───────────────┬────────────────┐
                             │ MCP (8000)    │ MCP (8080)     │ MCP (8084)
                             ▼               ▼                ▼
                  ┌──────────────────────┐┌─────────────┐┌─────────────┐
                  │     Hermes Agent     ││ Kubernetes  ││   Kagent    │
                  │ (Especialista Código)││ MCP (Local) ││(Operaciones)│
                  └──────────────────────┘└─────────────┘└─────────────┘
```

### Reglas Clave de la Malla:
* **OpenClaw como Front-End conversacional**: Recibe las peticiones del usuario por Telegram. Actúa exclusivamente como **Cliente MCP**.
* **Hermes como Especialista de Código**: Expone un **Servidor MCP** en el puerto `8000` (`http://hermes-agent-mcp.ai.svc.cluster.local:8000/mcp`). OpenClaw le delega las tareas multi-paso complejas.
* **El Falso Amigo de la Bidireccionalidad**: El puerto `8080` expuesto en el pod de OpenClaw **no es un servidor MCP del agente**, sino un contenedor sidecar genérico `kubernetes-mcp-server` de solo lectura. Intentar conectar a Hermes hacia `openclaw:8080/mcp` es redundante y erróneo.
* **Elevación Dinámica de Privilegios Aprobada (Hermes)**: Para superar la "Ilusión de Permiso" de forma segura, el clúster cuenta ahora con un mecanismo de **RBAC condicional y declarativo** para Hermes controlado por la variable `hermes_rbac_level` (`readonly`, `operator`, `admin`):
  - **`readonly`** (por defecto): Permisos de solo lectura ultra-seguros.
  - **`operator`** (Nivel Namespace): Otorga permisos de escritura y edición (`edit`) **únicamente dentro del namespace `ai`** para poder restaurar y modificar los bots de inferencia.
  - **`admin`** (Nivel Clúster): Otorga permisos globales de `cluster-admin` para poder modificar RBACs y recursos en todo el clúster.
  - **Comando de Aprobación Manual**: La elevación requiere confirmación del usuario mediante el comando:
    ```bash
    make hermes-rbac LEVEL=admin|operator|readonly
    ```

### 1.1 Puente Conversacional A2A (Cerebro-a-Cerebro)

Para posibilitar una verdadera colaboración conversacional de agente a agente, inyectamos dinámicamente una herramienta MCP llamada `ask_hermes_agent(question: str) -> str` en el arranque del pod de Hermes.
* **Mecanismo Autónomo**: El tool utiliza la biblioteca interna de Hermes en Python (`AIAgent`) para ejecutar un bucle de razonamiento autónomo (`run_conversation()`) de forma sincrónica y segura dentro del propio pod, sin llamadas externas circulares redundantes.
* **Heredabilidad de Seguridad**: Todas las consultas ejecutadas a través de `ask_hermes_agent` heredan estrictamente el contexto de seguridad configurado para la ServiceAccount de Hermes (`hermes-agent-mcp`).

### 1.2 Debates Técnicos Interactivos Multi-Agente (Tito ⚔️ Hermes)

Hemos diseñado e integrado una herramienta de debate estructurado para que Tito (OpenClaw) y Hermes contrasten enfoques técnicos opuestos antes de ejecutar cambios complejos en el clúster.
* **El Script de Debate (`scripts/agent-debate.py`)**: Coordina un debate automatizado de 4 turnos consultando los modelos correspondientes de cada agente a través del proxy de LiteLLM:
  1. **Apertura de Tito (OpenClaw)**: Propuesta pragmática, enfocada en la simplicidad, estabilidad y bajo riesgo (utiliza `openai/gpt-4o`).
  2. **Contrapropuesta de Hermes**: Enfoque de vanguardia, altamente automatizado, escalable y optimizado (utiliza `hermes-qwen`).
  3. **Réplica de Tito**: Defensa del pragmatismo frente a la complejidad.
  4. **Defensa Final de Hermes**: Conclusión y argumentos finales.
* **Aprobación del Usuario**: El debate concluye presentando un resumen estructurado de las dos opciones para que el usuario ingrese la opción que aprueba (`A` o `B`).
* **Uso**:
  ```bash
  python3 scripts/agent-debate.py "¿Debemos migrar a almacenamiento NFS para los PVCs?"
  ```

---

## 2. Monitoreo Financiero y Auto-Regulación (Cost-Awareness)

Para evitar que los agentes autónomos agoten el presupuesto en proveedores de pago (como OpenRouter), se expone un flujo de monitoreo de costes local de **solo lectura** sin revelar API keys sensibles.

### Flujo de Métricas
1. **LiteLLM Proxy** registra cada token consumido y calcula el gasto en USD mediante su base de datos de precios.
2. **Prometheus** recopila estos datos cada 30 segundos utilizando el ServiceMonitor `litellm-proxy-metrics`.
3. **Los Agentes** (Hermes/OpenClaw) pueden consultar Prometheus localmente usando sus herramientas PromQL (`prometheus_query_tool`).

### PromQL de Autodiagnóstico de Gasto:
Los agentes pueden consultar el gasto total acumulado en USD usando:
```promql
sum by (requested_model) (litellm_spend_metric_total)
```

O la tasa de peticiones y errores:
```promql
sum by (status_code) (rate(litellm_requests_metric_total[5m]))
```

### Enrutamiento Dinámico de Modelos (Prompt Pattern)
Para habilitar que un agente elija qué modelo usar autónomamente según la complejidad y el coste, se añade la siguiente instrucción en su directiva de sistema:
```markdown
## SELECCIÓN DINÁMICA DE MODELOS (COST-AWARE ROUTING)
Tienes disponibles tres niveles de modelos de IA en LiteLLM:
1. `local-reason` (Gratis/Local): DeepSeek-R1 8B en GPU. Úsalo para inspeccionar Kubernetes, leer logs, o tareas rutinarias.
2. `hermes-qwen` (Barato/OpenRouter): Qwen-Coder-32B. Úsalo para generación de código estándar y tareas intermedias.
3. `claude-sonnet` (Premium/OpenRouter): Claude 3.5 Sonnet. Úsalo únicamente para refactorizaciones complejas de red o debugging arquitectónico de alto nivel si hay presupuesto suficiente en Prometheus.
```

### Inercia de Memoria Conversacional (Nota de Depuración para Agentes)
Al interactuar en una homelab multi-agente, ten en cuenta que otros agentes conversacionales (como OpenClaw/Tito) pueden experimentar **inercia en su memoria conversacional** tras un despliegue en caliente y seguir informando que el recurso está pendiente debido a su contexto histórico del chat.
* **Acción sugerida**: Solicita explícitamente al agente que vuelva a evaluar e invoque de nuevo la consulta en Prometheus. Las queries directas de PromQL como `sum(litellm_spend_metric_total)` devolverán los datos en caliente inmediatamente tras su aprovisionamiento (ej. devolviendo un spend real de `$1.32 USD`), demostrando que el scraping del ServiceMonitor ya está activo a pesar del reporte histórico.

---

## 3. Despliegues Desacoplados y Granulares (Ansible / Makefile)

Para facilitar la actualización de componentes individuales del Stack de IA y de los servicios comunes sin provocar reinicios colaterales (por ejemplo, actualizar LiteLLM sin reiniciar a Hermes), la infraestructura está completamente desacoplada mediante tags en `playbooks/bootstrap.yml` y comandos granulares en el `Makefile`.

### Comandos de Despliegue Individual:

* **LiteLLM Proxy (Exclusivo)**:
  ```bash
  make ai-litellm-proxy-deploy
  ```
  *Actualiza el Service, el ConfigMap de enrutamiento y el ServiceMonitor de LiteLLM sin tocar el pod de Hermes.*

* **Hermes Agent (Exclusivo)**:
  ```bash
  make ai-hermes-agent-deploy
  ```
  *Actualiza la plantilla del deployment de Hermes, inyecta su system prompt y reinicia el pod sin tocar LiteLLM.*

* **Servicios Comunes**:
  ```bash
  ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini --tags pihole
  ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini --tags argocd
  ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini --tags helm-dashboard
  ```
