---
name: docker-engineer
description: >
  Containeriza aplicaciones con Docker — Dockerfiles multi-stage, Compose,
  registries y K8s. Optimiza imágenes, seguridad y entornos.
  Trigger: Cuando necesitás containerizar, optimizar imágenes Docker, armar un docker-compose.yml o debuggear contenedores.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Skill: docker-engineer

Containerización profesional. Dockerfiles que no son una vergüenza.

## Trigger

- Necesitás empaquetar una app en Docker
- Hay que optimizar una imagen que pesa 2GB
- Querés levantar un entorno dev con Docker Compose
- Vas a deployar con K8s y necesitás los manifests
- Un contenedor no arranca y hay que debuggear

## Workflow LEND

```
1. ANALIZAR
   ├── Lenguaje y runtime (Python 3.12, Node 20, Go, etc.)
   ├── Dependencias (requirements.txt, package.json, go.mod)
   ├── Puertos, volúmenes, variables de entorno
   └── ¿Es para dev, staging o prod?

2. OFRECER (Menú del Senior)
   ├── A) Simple: Dockerfile de una etapa, compose básico
   ├── B) Multi-stage: builder + runner, Alpine/distroless
   └── C) K8s-ready: multi-stage + healthcheck + non-root + K8s manifests

3. ELEGIR → el usuario confirma

4. HACER
   ├── Dockerfile optimizado (capas ordenadas por frecuencia de cambio)
   ├── .dockerignore (no mandar .venv, node_modules, .git)
   ├── docker-compose.yml (dev con hot-reload si aplica)
   ├── Healthcheck, labels, non-root user
   └── Si aplica: K8s deployment + service + ingress

5. VERIFICAR
   ├── docker build --no-cache pasa
   ├── docker run funciona y responde healthcheck
   └── Escaneo de vulnerabilidades (trivy si está disponible)
```

## Patrones

- **Multi-stage siempre**: no tiene sentido mandar el compilador a prod
- **Orden de capas**: lo que menos cambia primero (dependencias → código)
- **Imagen base**: Alpine (Python/Go) o distroless (Node/Java)
- **Non-root**: `USER nobody` o crear un user dedicado
- **Healthcheck**: `HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/health`
- **Labels**: `maintainer`, `version`, `description`
- **Compose para dev**: bind mount del código + puertos mapeados

## Anti-patrones

- Usar `latest` como tag de imagen base
- Copiar `node_modules` o `.venv` dentro de la imagen
- Correr como root en producción
- Imágenes de 1GB+ sin multi-stage
- Hardcodear secrets en el Dockerfile
