---
name: python-environment
description: >
  Gestión de entornos Python — venv, pip, poetry, conda. Entornos
  reproducibles y dependencias sin conflictos.
  Trigger: Cuando necesitás crear o gestionar un entorno Python, instalar dependencias, o configurar variables de entorno para un proyecto.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T1-ultra-fast
---

# Skill: python-environment

Entornos Python. Que funcione en tu máquina Y en la mía.

## Trigger

- Arrancás un proyecto nuevo y necesitás un entorno limpio
- Un requirements.txt no funciona y hay conflictos
- Necesitás aislar dependencias entre proyectos
- Vas a deployar y necesitás frozen requirements

## Workflow LEND

```
1. ANALIZAR
   ├── Proyecto: ¿nuevo o existente? ¿tiene requirements.txt/pyproject.toml?
   ├── Python: ¿qué versión? (3.10, 3.11, 3.12)
   ├── OS: Windows (WSL), Linux, Mac
   └── Destino: ¿local, CI, Docker, producción?

2. OFRECER (Menú del Senior)
   ├── A) venv + pip — estándar, liviano, viene con Python
   ├── B) Poetry — dependencias + build + publish en una herramienta
   └── C) Conda — cuando necesitás librerías no-Python (C++, CUDA, R)

3. ELEGIR → confirmación

4. HACER
   ├── python -m venv .venv && source .venv/bin/activate
   ├── pip install -r requirements.txt
   ├── poetry new/pip install poetry
   ├── requirements.txt congelado: pip freeze > requirements.txt (solo para prod)
   ├── .gitignore: .venv/, __pycache__/, *.pyc, .env
   └── Variables de entorno: .env + python-dotenv, nunca hardcodeadas

5. VERIFICAR
   ├── python --version es la correcta
   ├── pip list muestra las dependencias esperadas
   └── El proyecto corre sin errores de import
```

## Patrones

- **Entorno aislado**: nunca instalar dependencias globales. Siempre .venv por proyecto.
- **requirements.txt**: freeze solo para producción. Para dev, usar requirements.in o pyproject.toml.
- **Poetry**: si el proyecto crece, Poetry maneja versionado, build y publish.
- **.env para config**: credenciales, rutas, puertos. Nunca hardcodeados.
- **Python version explícita**: .python-version o runtime.txt para pyenv.

## Anti-patrones

- ❌ pip install global — rompés el sistema eventualmente
- ❌ pip freeze sin .venv activado — mezcla dependencias del sistema
- ❌ No .gitignore .venv — mandás 100MB de librerías al repo
- ❌ Versiones sin fijar — "funciona hoy" se rompe mañana
- ❌ Archivos .env commiteados — credenciales al mundo
