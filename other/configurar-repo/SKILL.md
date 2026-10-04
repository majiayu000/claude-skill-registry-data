---
name: configurar-repo
description: Configura el repositorio de GitHub de punta a punta con gh — descripción, topics, labels, rama develop, protección de ramas, merge settings y metadatos — a partir de la definición del producto. Úsalo al crear el repo de un proyecto nuevo o cuando haya que poner en orden uno existente (p. ej. "configura el repo", "prepara el repositorio en GitHub", "pon los labels y la protección de ramas").
---

Deja el repositorio de GitHub operativo y coherente con la plantilla. Requiere `gh`
autenticado; verifica con `gh auth status` antes de empezar.

## Paso 1 — Contexto

Lee `README.md` y `docs/product/business-model.md` para derivar descripción y
topics. Detecta el repo actual (`gh repo view`). Si no existe remoto, pregunta si
crearlo (`gh repo create` — público/privado lo decide la persona).

## Paso 2 — Metadatos

- **Descripción**: una frase desde la visión del producto (`gh repo edit
--description`). **Homepage**: la URL del producto si existe.
- **Topics**: 3–6 derivados del stack y el dominio (`gh repo edit --add-topic`).

## Paso 3 — Labels

Ejecuta `.github/scripts/setup-labels.sh` (usa `.github/LABELS.md` como catálogo).

## Paso 4 — Ramas y flujo

- Crea `develop` desde `main` si no existe, publícala y **establécela como rama por
  defecto del repo** (`gh api -X PATCH repos/{owner}/{repo} -f default_branch=develop`)
  — no es opcional: la rama por defecto es a donde apuntan los PRs nuevos y los de
  Dependabot; si queda `main`, el Git Flow se rompe (`CONTRIBUTING.md`).
- Verifica que `.github/dependabot.yml` tenga `target-branch: "develop"` en cada
  ecosistema.
- Protección de `main` (y `develop` si la persona quiere): PR obligatorio, sin
  force-push, conversaciones resueltas y **checks requeridos por su nombre de check
  run, no por el del workflow**: `Calidad` (de `quality.yml`) y `Gitleaks` (de
  `secret-scan.yml`). Si pones el nombre del workflow, el PR se queda esperando un
  check que nunca reporta. Verifícalos con
  `gh api repos/{owner}/{repo}/commits/{sha}/check-runs --jq '.check_runs[].name'`
  sobre un commit que ya haya corrido CI.
  Aplica vía `gh api repos/{owner}/{repo}/branches/{branch}/protection` y muestra el
  JSON antes de aplicar.
- **Comprueba que los hooks locales corran**:
  `bash .github/scripts/check-hooks-enabled.sh` (con `--arreglar` los activa).
  `core.hooksPath` no viaja en el repositorio, así que el estado por defecto de
  cualquier clon nuevo es «sin ninguna verificación local».

### Si GitHub responde 403 a la protección

```
gh: Upgrade to GitHub Pro or make this repository public to enable this feature. (HTTP 403)
```

En un repositorio **privado de plan gratuito la protección de ramas no existe**. No es
un error suelto que se reporta al final: es un resultado previsto que **cambia lo que
el proyecto puede prometer**. `CONTRIBUTING.md` y `AGENTS.md` declaran PR obligatorio,
nada de push directo a `main`/`develop` y checks requeridos para fusionar — y todo eso
lo hace cumplir el servidor. Sin él queda esto:

| Control              | Qué cubre                     | Cómo se salta                                 |
| -------------------- | ----------------------------- | --------------------------------------------- |
| `git-guardrails.sh`  | Push desde una rama protegida | Es un hook del agente: no aplica a la persona |
| `.githooks/pre-push` | Los checks antes de publicar  | `git push --no-verify`                        |
| `core.hooksPath`     | Activa lo anterior            | **Se olvida**: es manual, una vez por clon    |

Haz tres cosas, en el momento en que aparece el 403:

1. **Dilo con todas las letras**, sin suavizarlo: «este repositorio no tiene protección
   de ramas; los hooks locales son el único control y se saltan con `--no-verify`».
2. **Plantea la salida real**: hacer público el repositorio activa la protección gratis.
   Es una decisión de producto, no técnica — pregúntala aquí, no después.
3. **Déjalo por escrito** en el `README.md` o en el ADR de instanciación, para que quien
   llegue después no dé por buenas unas reglas que nadie aplica.

## Paso 5 — Ajustes de merge e higiene

- Squash merge habilitado, borrar ramas al mergear, issues habilitados; template de
  PR/issues ya vienen del repo.
- Verifica que Actions esté habilitado y que los workflows activos (`quality.yml`,
  `secret-scan.yml`) corran.

## Paso 6 — Cierre

Resume qué quedó configurado (con los comandos ejecutados) y regístralo en el CHANGELOG
bajo Unreleased. **Y di qué NO quedó protegido**, con su consecuencia — no basta con
listar qué falló por permisos: si no hay protección de ramas, el resumen tiene que decir
que las reglas de `CONTRIBUTING.md` no las hace cumplir nadie (Paso 4).

Reglas: muestra cada comando destructivo o de configuración antes de ejecutarlo la
primera vez; NO borres labels/ramas existentes sin confirmar; NO toques repos que no
sean el del proyecto actual.
