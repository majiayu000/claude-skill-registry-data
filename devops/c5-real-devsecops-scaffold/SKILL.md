---
name: c5-real-devsecops-scaffold
display_name: "Scaffold DevSecOps & Endurecimiento Zero-Trust CI/CD"
description: "Scaffold DevSecOps soberano, verificación de firmas GPG/SSH, endurecimiento CI/CD y políticas Zero-Trust. Dispara con \"devsecops\", \"inicializar repo\", \"seguridad ci/cd\", \"hardening repo\", \"gpg ci/cd\", \"devsecops scaffold\"."
---

# Protocolo de Scaffolding C5-REAL (DevSecOps)

Activa esta skill cuando el usuario pida inicializar un repositorio nuevo o aplicar el "andamiaje C5-REAL" (o DevSecOps) a un repositorio existente.

El agente DEBE generar la siguiente estructura de archivos, asegurándose de que los contenidos respeten las reglas del framework C5-REAL:

## 1. Gobernanza Criptográfica y Git Flow
1. **`.github/CODEOWNERS`**: Exigir revisión de `@borjamoskv`.
2. **`.git-blame-ignore-revs`**: Archivo para ignorar hashes de formateo masivo.
3. **`.github/PULL_REQUEST_TEMPLATE.md`**: Plantilla con checklist obligatorio sobre Fricción Latente, Phantom Target e Idempotencia.
4. **`.github/ISSUE_TEMPLATE/bug_falsification.yml`**: Plantilla para exigir scripts deterministas Popperianos.

## 2. Automatización y Seguridad (Swarms)
1. **`.github/dependabot.yml`**: Vigilar la cadena de suministro semanalmente.
2. **`.github/workflows/ci.yml`**: Pipeline de Matrix Builds sobre ubuntu, macos y windows.
3. **`.github/workflows/codeql.yml`**: Escaneo semántico (AST) semanal y por PR.
4. **`.github/workflows/oidc-deploy.yml`**: Plantilla de despliegue Zero-Trust usando `id-token: write` para evitar secretos en texto plano.

## 3. Fricción Latente Local (Shift-Left)
1. **`lefthook.yml`**: Configurar pre-commits ultrarrápidos para `detect-secrets` y linters (evitando que la Entropía escape a la red).
2. **`scripts/enforce_c5_rules.sh`**: Script bash que usa `gh api` para proteger la rama `main` (branch protection, requerir firmas, PRs obligatorias).

> [!NOTE]
> **Heurística de Falsos Positivos:** Al auditar repositorios en busca de credenciales planas, excluir siempre los scripts de infraestructura (ej. `preflight.sh`, `lefthook.yml`, `pre-commit`) ya que contienen expresiones regulares de detección (`ghp_`, `sk-ant-`) que el escáner confundirá con entropía real.

## 4. Topología Front-End (Si se requiere Node/Web)
1. **`babylon-web/vite.config.ts`**: Configuración con función `manualChunks` determinista para separar el vendor de React.

## 5. Motor Interno BFT (Si se requiere backend Python/Rust)
Si el usuario solicita generar los motores de backend (Fase 3/4), generar:
1. **`src/bft_sqlite.py`**: Wrapper SQLite con *Exponential Backoff* y *Jitter* (mitigación de `SQLITE_BUSY`).
2. **`src/c5_telemetry.py`**: Cola asíncrona no bloqueante (Válvula Termodinámica).
3. **`src/cognitive_guardrail.py`**: Cortacircuitos contra el *Intent Decay* y el *Ontological Drift*.
4. **`src/bft_falsification.py`**: Script de 20 hilos concurrentes para probar que el BFT colapsa limpiamente (Fail-Fast).
5. **`src/strike_rs_template/Cargo.toml` & `lib.rs`**: Plantilla nativa PyO3 (`maturin`) para delegar el cómputo termodinámico al silicio.
6. **`src/devsecops_attest.py`**: Atestación determinista L5 con anclaje Bitcoin asíncrono, protección de candado `.lock` y caché LRU de `git ls-tree`.

Al finalizar, el agente debe proporcionar un `walkthrough.md` listando la exergía y arquitectura inyectada en el nodo.
