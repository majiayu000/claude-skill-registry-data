---
name: security-auditor
description: >
  Auditoría de seguridad automatizada — SAST, DAST, escaneo de
  dependencias, secretos, hardening de contenedores y compliance.
  Trigger: Antes de cada deploy, al integrar dependencias nuevas, o al detectar prácticas inseguras en el código.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Skill: security-auditor

Seguridad no es un feature, es parte del diseño. Si no lo escaneamos, asumimos el riesgo.

## Trigger

- Vas a mergear un PR a main
- Agregaste una dependencia nueva (pip install, npm install)
- Encontraste una key hardcodeada en el código
- Querés hardening de Docker o del servidor
- Necesitás compliance (OWASP Top 10, CIS benchmarks)

## Workflow LEND

```
1. ANALIZAR
   ├── Stack: Python, Node, Go, Docker
   ├── Dependencias: revisar requirements.txt, package-lock.json, go.sum
   ├── ¿Hay secrets en el código? (gitleaks, trufflehog)
   ├── ¿El Dockerfile corre como root?
   └── ¿Hay endpoints sensibles sin autenticación?

2. OFRECER (Menú del Senior)
   ├── A) Quick Scan: dependencias + secrets. 2 minutos, tapa lo urgente.
   ├── B) Standard: dependencias + secrets + SAST (bandit/semgrep) + Docker scan
   └── C) Full Audit: todo + DAST + CIS benchmarks + reporte compliance

3. ELEGIR → el usuario confirma

4. HACER
   ├── pip-audit / npm audit / trivy para dependencias
   ├── trufflehog o gitleaks para secrets
   ├── bandit o semgrep para SAST (Python)
   ├── trivy image scan para imágenes Docker
   ├── Reporte con findings: severidad, ubicación, sugerencia de fix
   └── Si aplica: hardening del Dockerfile (non-root, no secrets en capas)

5. VERIFICAR
   ├── Todos los findings críticos tienen fix
   ├── No hay secrets en el historial de git
   └── El reporte se guarda en engram para auditoría
```

## Patrones

- **SAST first**: escanear código fuente antes de compilar
- **Secret scanning**: en cada commit (pre-commit hook) y en cada PR
- **Dependency scanning**: semanal como mínimo, o en cada PR
- **Mínimo privilegio**: containers sin root, puertos mínimos, IAM restrictivo
- **Defense in depth**: firewall → WAF → auth → app → DB
- **Rotación de secrets**: automática, no manual

## Anti-patrones

- Ignorar findings por "ya lo voy a arreglar después"
- Secrets en variables de entorno del CI sin encriptar
- Docker corriendo como root en producción
- Dependencias sin escanear (supply chain attack)
- Escanear una vez y asumir que está todo bien después
