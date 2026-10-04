---
name: audit-quick
description: Audit rapide securite et qualite du projet courant. Utiliser avant un deploiement ou en revue.
context: fork
agent: Explore
model: haiku
---

# Audit rapide du projet

Effectuer un audit en 5 minutes max. Reponses concises, pas de blabla.

## 1. Secrets exposes

Chercher dans le code : API keys, passwords, tokens, secrets en dur.
```
grep -rn "password\|secret\|api_key\|token" --include="*.ts" --include="*.env*" --exclude-dir=node_modules
```

## 2. Vulnerabilites evidentes

- SQL injection (interpolation de strings dans les requetes)
- XSS (innerHTML, dangerouslySetInnerHTML sans sanitize)
- SSRF (URLs construites depuis input utilisateur)
- Path traversal (chemins fichiers depuis input)

## 3. Couverture de tests

```bash
pnpm test -- --coverage 2>&1 | tail -20
```

Reporter : % couverture, fichiers non couverts critiques.

## 4. Dependances

```bash
pnpm audit 2>&1 | tail -20
```

## 5. Resume

Format strict :
```
SECURITE: [OK|WARN|CRITICAL] — [details]
TESTS: [X%] couverture — [fichiers critiques non couverts]
DEPS: [X vulns] — [critiques listees]
VERDICT: [DEPLOY OK|BLOQUER]
```
