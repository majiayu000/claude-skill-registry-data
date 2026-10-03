---
name: git-workflow
description: Automatiza la creación de commits y el push al repositorio remoto en GitHub usando GitHub CLI (gh).
---

### Instrucciones para el Agente:
1. Revisa el estado del repositorio mediante `git status`.
2. Si el proyecto no está inicializado en Git, ejecuta `git init` y crea el repositorio remoto con `gh repo create epk-dashboard --public --source=. --remote=origin`.
3. Haz staging de los archivos modificados/creados (`git add .`).
4. Genera un mensaje de commit siguiendo el formato Conventional Commits (ej. `feat:`, `fix:`, `docs:`).
5. Sube los cambios a la rama principal mediante `git push origin main`.