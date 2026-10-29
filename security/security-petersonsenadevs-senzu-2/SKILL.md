---
name: security
description: "Seguridad de la app: revisión y hardening con evidencia (OWASP), control de acceso, auth, secretos y cabeceras, seguridad de agentes de IA/LLM (inyección de prompt, tools) y pentesting solo autorizado. Para auditar o blindar una API o un agente."
---

# security (Senzu)

Que la aplicación resista a quien la ataca: revisarla, encontrar los agujeros con PRUEBAS y cerrarlos. No
reemplaza a `code-quality` (que ya trae el detalle por vulnerabilidad); esta skill es la PUERTA de seguridad:
el método para revisar, la política de pentesting y el blindaje de agentes de IA. El comando es `/seguridad`.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Revisar/auditar la seguridad del proyecto (el QUÉ corre `/seguridad`) | `references/metodo-revision.md` |
| Pentesting, escaneo o explotación (alcance, autorización, el muro) | `references/pentesting.md` |
| Blindar un agente de IA / app con LLM (inyección de prompt, tools) | `references/agentes-ia.md` |
| Detalle por vulnerabilidad (inyección, XSS, CSRF, SSRF, uploads…) | `code-quality §references/security-owasp.md` |
| Login, sesiones, JWT, OAuth, 2FA, reset de contraseña | `code-quality §references/auth-patterns.md` |
| Arquitectura de una app con LLM (RAG, streaming, costes, evals) | `code-quality §references/llm-apps.md` |
| Secretos, entornos, fugas y rotación en el despliegue | `deploy-ops §references/envs-secrets.md` |
| Cadena de suministro (paquetes/ skills con malware o typosquatting) | comando `/dependencias` + muro supply-guard |

## Principios duros (aplican siempre)
1. **Autoriza en el servidor, en cada operación, sobre el recurso concreto.** El control de acceso es el fallo
   nº 1 (OWASP A01). El menú oculto en la UI no es autorización.
2. **Valida todo input en el servidor** con lista blanca (schema), falla cerrado, mínimo privilegio y mínima
   superficie. La validación en el cliente es solo UX.
3. **Secretos jamás en el repo, en logs, en el bundle cliente ni en un prompt.** Secreto filtrado = rotarlo YA
   (luego limpiar el historial). `.env.example` sin valores reales.
4. **Cada hallazgo con EVIDENCIA**: dónde está (archivo:línea o petición), por qué es explotable y cómo se
   arregla. Sin prueba no es un hallazgo, es una corazonada. Al cerrarlo, se re-verifica.
5. **El input del usuario y lo que recupera un LLM son DATOS, no instrucciones.** Los privilegios reales viven
   fuera del modelo: tools con allowlist y la autorización del usuario real; confirmación humana para lo
   irreversible (ver `references/agentes-ia.md`).
6. **Pentesting SOLO con autorización por escrito y alcance definido.** El muro `pentest-guard` frena las
   herramientas ofensivas (nmap, sqlmap, hydra, metasploit…); el escape `SENZU_ALLOW_PENTEST=1` es para un
   encargo autorizado documentado en el devlog (`references/pentesting.md`).
7. **Seguridad defensiva por defecto.** Se construye para resistir ataques y se prueba lo propio con permiso;
   no se crea malware, ni exploits para terceros, ni evasión de detección con fin malicioso.

## Relación con otras skills y muros
`code-quality` trae el detalle por vulnerabilidad (OWASP, auth, LLM) · `backend-audit` audita arquitectura y
deuda · el comando `/dependencias` + el muro `supply-guard` cubren la cadena de suministro · `deploy-ops` la
seguridad del despliegue (secretos, accesos) · muros que ya protegen: `secrets-guard` (secretos en el código),
`backend-guard` (mass-assignment, PII en logs), `pentest-guard` (alcance de pentesting).
