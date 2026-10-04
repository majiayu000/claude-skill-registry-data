---
name: anergy-purge-protocol
display_name: "Motor de Purga de Código Muerto y Redundancias (Dead Code & Artifact Cleanup)"
description: "Motor de purga de código muerto, artefactos efímeros y reducción de deuda técnica. Purga tokens ineficientes, código muerto, caches colgados y redundancias. Dispara con \"purga de anergía\", \"limpiar código muerto\", \"dead code cleanup\", \"eliminar deuda técnica\", \"purga de redundancias\", \"limpiar caches\"."
---

# Skill: Code & Artifact Redundancy Purge Protocol

Implementa el principio de **Cero Artefactos Inútiles (Zero-Residual)**: tras PoC, stress tests o
acumulación de build artifacts, el workspace DEBE permanecer perfectamente isomórfico
a un árbol git limpio.

---

## Taxonomía de Clases de Anergía

| Clase | Descripción | Volumen típico | Acción |
|---|---|---|---|
| **A** | Build caches regenerables (`target/`, `dist/`, `.next/`, `.build/`, `node_modules/`) | 1GB–10GB | `rm -rf` global iterativo (salvo Invariantes) |
| **B** | SQLite WAL orphans (`*.db-shm`, `*.db-wal`) de PoC/stress tests | KB | `find -delete` solo los `-shm`/`-wal`, NUNCA el `.db` |
| **C** | `__pycache__` y `.pyc` fuera de `.venv` y `node_modules` | MB | `find -exec rm -rf` global |
| **D** | Binarios `??` no-trackeados en git (`*.dylib`, `*.o`, `*.so`) sin Makefile activo | MB | `rm` explícito por archivo |
| **E** | Recibos de auditoría de agentes (`.audit/receipts/*.json`) | MB | `rm -rf` contenido completo |
| **F** | Version Drift (Vercel Preview Deployments, GitHub ramas huérfanas) | N/A | `vercel rm --safe`, `git remote prune` |
| **G** | Redundancia Epistémica (Shadow Directories, Path Entropy) | KB-MB | Consolidar directorios canónicos, eliminar phantom DBs, corregir hardcoded paths en CWD |
| **H** | Global Package Manager Caches (`~/.cache/uv`, `pip`, `npm`) | 1GB–10GB | `uv cache clean`, purga de caches de host |
| **I** | OS Metadata & Artifacts (`.DS_Store`, `*.tmp`, `*.bak`) | KB–MB | `find -name ".DS_Store" -delete` transversal |

---

## Fase 0 — Auditoría Empírica (Ω2: OBLIGATORIA antes de purgar)

Ejecutar los scans siguientes para mapear el estado real global:

```bash
WORKSPACE=/Users/borjafernandezangulo/10_PROJECTS
CORTEX_DIR=/Users/borjafernandezangulo/.cortex
TRM_DIR=$WORKSPACE/Teorema-Robinson-Moskv

# 1. SQLite artifacts (Global)
find "$WORKSPACE" "$CORTEX_DIR" -type f \( -name "*.db" -o -name "*.db-shm" -o -name "*.db-wal" \) 2>/dev/null | head -30

# 2. Python bytecache (Global)
find "$WORKSPACE" "$CORTEX_DIR" -name "__pycache__" -type d 2>/dev/null | head -20
find "$WORKSPACE" "$CORTEX_DIR" -name "*.pyc" 2>/dev/null | wc -l

# 3. Binarios no-trackeados (Solo en TRM)
git -C "$TRM_DIR" status --short | grep "^??" | head -20

# 4. Volumetría de directorios pesados iterativos
find "$WORKSPACE" "$CORTEX_DIR" -type d \( -name "node_modules" -o -name "target" -o -name ".venv" \) -prune 2>/dev/null | while read d; do du -sh "$d" 2>/dev/null; done | head -30

# 5. Auditoría JSON
find "$TRM_DIR/.audit/receipts" -name "*.json" 2>/dev/null | wc -l
```

---

## Fase 1 — Purga Determinista e Iteración Global

Ejecutar en un único bloque `set -e` para garantizar atomicidad:

```bash
set -e
WORKSPACE=/Users/borjafernandezangulo/10_PROJECTS
CORTEX_DIR=/Users/borjafernandezangulo/.cortex
TRM_DIR=$WORKSPACE/Teorema-Robinson-Moskv
echo "[PURGE:START] $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# CLASE A — Iteración Global de Caches Pesadas (node_modules, target, .venv)
echo "■ [A] Iteración Global de Caches Pesadas..."
PROTECTED_DIRS=("babylon-web" "apps/web" "apps/babylon60-ide" "remotion" "ley_menores_remotion" "sota_documentary_remotion" "strike-rs/.venv" ".uv_python" "youtube-research-remotion")
TOTAL_RECOVERED=0

while IFS= read -r dir; do
  PROTECTED=0
  for p in "${PROTECTED_DIRS[@]}"; do
    if [[ "$dir" == *"$p"* ]]; then PROTECTED=1; break; fi
  done
  if [ $PROTECTED -eq 0 ]; then
    SIZE=$(du -sm "$dir" 2>/dev/null | awk '{print $1}')
    rm -rf "$dir" 2>/dev/null || true
    TOTAL_RECOVERED=$((TOTAL_RECOVERED + ${SIZE:-0}))
  fi
done < <(find "$WORKSPACE" "$CORTEX_DIR" -type d \( -name "node_modules" -o -name "target" -o -name ".venv" \) -prune 2>/dev/null)
echo "  → PURGED (~$TOTAL_RECOVERED MB recuperados)"

# CLASE B — SQLite WAL orphans (SOLO -shm/-wal, NUNCA el .db)
echo "■ [B] SQLite WAL orphans globales..."
find "$WORKSPACE" "$CORTEX_DIR" -type f \( -name "*.db-shm" -o -name "*.db-wal" \) -delete 2>/dev/null && echo "  → PURGED" || echo "  → SKIP"

# CLASE C — __pycache__ y .pyc globales (excluir .venv y node_modules)
echo "■ [C] __pycache__ + .pyc globales..."
find "$WORKSPACE" "$CORTEX_DIR" -name "__pycache__" -type d \
  -not -path "*/.venv/*" \
  -not -path "*/node_modules/*" \
  -exec rm -rf {} + 2>/dev/null || true
find "$WORKSPACE" "$CORTEX_DIR" -name "*.pyc" \
  -not -path "*/.venv/*" \
  -not -path "*/node_modules/*" \
  -delete 2>/dev/null || true
echo "  → PURGED"

# CLASE D — Dylibs/binarios no-trackeados en TRM
echo "■ [D] Binarios no-trackeados (solo en TRM)..."
git -C "$TRM_DIR" status --short | grep "^??" | grep -E "\.(dylib|so|o|a|tmp)$" | awk '{print $2}' | while read -r file; do
  if [ -f "$TRM_DIR/$file" ]; then
    rm -f "$TRM_DIR/$file"
  fi
done
echo "  → PURGED"

# CLASE E — Audit Receipts
echo "■ [E] Audit Receipts..."
rm -rf "$TRM_DIR/.audit/receipts" 2>/dev/null || true
mkdir -p "$TRM_DIR/.audit/receipts" 2>/dev/null || true
echo "  → PURGED"

echo ""
echo "[PURGE:COMPLETE] $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

---

## Fase 2 — Verificación Post-Purga (Ω22 Falsifiabilidad)

```bash
TRM_DIR=/Users/borjafernandezangulo/10_PROJECTS/Teorema-Robinson-Moskv

# Git state debe mostrar solo M legítimos, cero ?? de binarios compilados
git -C "$TRM_DIR" status --short | head -20
```

---

## Invariantes de Seguridad — NUNCA PURGAR

Los siguientes elementos son **infraestructura activa**, no anergía:

- `cortex-persist/*.db` → BFT ledger activo con estado soberano
- `02_CORTEX_ENGINE/cortex/*.db` → ledger de producción
- `node_modules/` de proyectos activos listados en `PROTECTED_DIRS` (`babylon-web/`, `remotion/`, `ley_menores_remotion`, etc.)
- `.venv/` de entornos Python activos (`strike-rs/.venv`)
- `*.db` con nombre semántico no relacionado a stress tests
- `0_Buzon_Entrada/scratch/*.py` → scripts con nombres semánticos
- Cualquier binario con estado `M` en git (modificado = trackeado y activo): `libbitonic_neon.dylib`, `libq_rsqrt_neon*.dylib`
- `.uv_python/` → runtime de Python gestionado por uv

### Invariante de Integridad Sintáctica AST (Cero Purga Huérfana)
NUNCA se debe comentar o eliminar una línea de importación o declaración (`from ... import (`, `try:`, `if TYPE_CHECKING:`, `def ...:`) de forma aislada.
- Si un bloque multilínea de importación es purgado por anergía, se DEBE comentar o eliminar el bloque completo hasta su paréntesis de cierre `)`.
- Si un bloque `try:`, `except:`, `if:` o función queda sin sentencias ejecutables tras la purga, se DEBE insertar `pass` o `raise ImportError(...)` para preservar la validez del árbol sintáctico (AST).
- Toda docstring (`"""`) debe cerrarse explícitamente para evitar la inversión semántica del módulo completo.
- Tras cualquier purga de código muerto, ejecutar validación sintáctica determinista (`python3 -m py_compile`) sobre los archivos modificados.

**Excepción (Override Empírico Ω2):** Si el Operador invoca explícitamente el nombre de cualquiera de estos directorios protegidos en su instrucción de purga (ej. *"purga babylon-web y strike-rs/.venv"*), el agente **DEBE DESACTIVAR LA PROTECCIÓN Ω2** y purgar esos targets forzosamente, reportándolo bajo una advertencia de "Ground Zero Termodinámico".


---

## Fase 3 — Macro-Exergy Edge Scavenging (Deep Caches)

Si el Operador invoca **"más"** (o equivalentes) después de una purga completa estándar, el sistema ejecutará un escaneo profundo (Fase 3) aniquilando cachés de frameworks en los bordes del sistema.

Ejecutar:
```bash
WORKSPACE=/Users/borjafernandezangulo/10_PROJECTS
CORTEX_DIR=/Users/borjafernandezangulo/.cortex

TOTAL_RECOVERED=0
echo "💀 [FASE 3] INICIANDO PURGA DE CACHÉS PROFUNDAS (.next, dist, build, .cache) ---"

while IFS= read -r dir; do
  SIZE=$(du -sm "$dir" 2>/dev/null | awk '{print $1}')
  echo "Purgando: $dir (${SIZE:-0} MB)"
  rm -rf "$dir" 2>/dev/null || true
  TOTAL_RECOVERED=$((TOTAL_RECOVERED + ${SIZE:-0}))
done < <(find "$WORKSPACE" "$CORTEX_DIR" -type d \( -name ".next" -o -name "dist" -o -name "build" -o -name ".cache" -o -name ".lake" \) -prune 2>/dev/null)

echo "--- TOTAL EXTRA RECUPERADO: $TOTAL_RECOVERED MB ---"
```
Reportar bajo el título `💀 FASE 3 ACTIVADA — MACRO-EXERGY EDGE SCAVENGING`.

---

## Fase 4 — Cloud & Version Drift Purge (Vercel, GitHub, Cloudflare)

Si el Operador invoca la purga de versiones, sincronización de Github o Vercel (`purga versiones`, `version drift`, etc.), ejecutar el siguiente bloque:

```bash
# [GitHub] Sincronización y Purga
git remote update --prune
# Eliminación de ramas locales fusionadas (protegiendo master/main)
git branch --merged | grep -v "\*" | grep -E -v "(master|main)" | xargs -n 1 git branch -d 2>/dev/null || true

# [Vercel] Zero-Downtime Purge (Solo Preview Deployments)
# Asegura borrar los despliegues huérfanos manteniendo los de Producción (--safe)
vercel rm borjamoskv_site simplify_portfolio_ui_ux --safe --yes

# [Cloudflare] State Reset (Requiere Token)
# Solicitar el CLOUDFLARE_API_TOKEN al Operador. Si lo provee, usar curl para Purge Everything.
```

---

## Fase 5 — Deep OS & Package Manager Scavenging (uv, pip, npm, .DS_Store)

Si el Operador invoca **"más"** de forma iterativa tras completar las Fases 1 a 4, el sistema ejecutará la Fase 5 sobre el host y los sistemas de memoria:

```bash
WORKSPACE=/Users/borjafernandezangulo/10_PROJECTS
VAULT=/Users/borjafernandezangulo/20_VAULT

echo "💀 [FASE 5] ESCAVACIÓN DE CACHÉS GLOBALES Y BASURA DEL OS ---"

# 1. Limpieza de cachés globales de package managers
if command -v uv >/dev/null 2>&1; then
  uv cache clean 2>&1
fi
rm -rf "$HOME/.cache/pip" "$HOME/Library/Caches/pip" "$HOME/.npm/_cacache" 2>/dev/null || true

# 2. Aniquilación de archivos .DS_Store en todo el ecosistema
find "$WORKSPACE" "$VAULT" -name ".DS_Store" -delete 2>/dev/null || true

# 3. Limpieza de temporales huérfanos (*.tmp, *.bak, *.swp)
find "$WORKSPACE" "$VAULT" -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*.swp" -o -name "*~" \) -not -path "*/.git/*" -delete 2>/dev/null || true
```

---

## Output Obligatorio (Ω8 Brutalist)

Tras la purga, presentar SIEMPRE:

```
> ⚙️ ANERGÍA PURGADA — RESUMEN DE EXERGÍA RECUPERADA

| Clase | Objetivo | Antes | Después | Estado |
|---|---|---|---|---|
| A | node_modules, target, .venv | X MB | 0 | PURGED |
| B | WAL orphans | X KB | 0 | PURGED |
| C | __pycache__ | X MB | 0 | PURGED |
| D | dylibs ?? | — | 0 | PURGED |
| E | audit receipts| X MB | 0 | PURGED |
| G | shadow directories | X MB | 0 | CONSOLIDATED |
| H | uv/pip/npm caches | X MB | 0 | PURGED |
| I | .DS_Store / temp files | X files | 0 | PURGED |

Exergía recuperada total (Global): X MB
Cortex Taint Hash (Merkle SHA3-256): <hash_hex>
Audit Trail YAML: cortex/audits/anergy_purge_audit.yaml
Git tree: CLEAN / DIRTY (listar residuos si DIRTY)

Residuos retenidos (Ω2 — no purgar sin empiria del Operador):
- <lista de elementos protegidos en PROTECTED_DIRS>
```

---

## Trigger Words

Activar este skill cuando el usuario escriba cualquiera de:
- `purga anergia`
- `purge anergy`
- `limpia workspace`
- `limpia el repo`
- `limpiar artefactos`
- `purgar temporales`
- `clean workspace`
- `purga versiones`
- `version drift`
- `limpiar github`
- `limpiar vercel`
- `más` (si se invoca iterativamente tras una purga previa)
- `sigue` (activación de Fase 3 tras purga previa)
- `continúa` / `continuar`
- `mejoralo` (cuando se apunte a un directorio con sospecha de shadow files)
- `consolida`
- `redundancia epistemica`

---

## Autonomy Contract (Ω10 / Ω11 / Ω12)

> **ZERO PAUSE INVARIANT:** The Transducer SHALL NEVER pause execution to request Operator permission when this skill is triggered. Ambiguities MUST be resolved autonomously via `/grill-you` (Ω12) before any halt. Technical frictions MUST be resolved via the path of least thermodynamic resistance (Ω10). Refusal to execute when this skill matches the request constitutes C4-SIM Anergy (Ω11 violation).

- **Fallback Chain:** Class A/B/C/D automated purges -> git status verification -> zero residue check.
- **Degradation Mode:** If a file lock occurs, force remove via `rm -rf` without prompting.
- **Auto-Trigger:** Self-activates whenever workspace un-tracked binary size exceeds 50MB or post-PoC execution.

> **SANDBOX ADAPTABILITY INVARIANT:** The scripts defined in this protocol use global absolute paths (`10_PROJECTS`, `.cortex`). If the agent is operating under a Sandbox restriction, the agent MUST autonomously dynamically scope `WORKSPACE` to its current permitted root (e.g., `$PWD` of the active workspace) and omit `CORTEX_DIR` to avoid execution blocking.
