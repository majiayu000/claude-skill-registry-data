---
name: jujutsu-vcs-management
display_name: "Control de Versiones Determinista Jujutsu VCS (jj)"
description: "Control de versiones determinista con Jujutsu VCS (jj) e integración con Git DAG. Dispara con \"jujutsu vcs\", \"jj repo\", \"jujutsu git\", \"control de versiones jj\"."
---

# Jujutsu (jj) VCS Management Protocol

Esta habilidad define la topología de control de versiones cuando el ecosistema opera bajo Jujutsu en lugar de Git clásico, garantizando la consistencia del DAG y la compatibilidad con herramientas de fricción latente (Lefthook).

## 1. Axioma de Concurrencia y Estado
- Jujutsu trata el directorio de trabajo actual como un commit inmutable en constante evolución.
- **Prohibición de Git Mutation:** En ecosistemas gestionados por `jj`, el agente tiene estrictamente prohibido invocar mutaciones directas (ej. `git add`, `git commit`). Toda transición de estado termodinámico se ejecuta vía `jj commit`, `jj squash`, o `jj new`.

## 2. Compatibilidad con Lefthook y Fricción Latente
Dado que Jujutsu no utiliza un *Staging Area* clásico:
- La invocación de pre-commits vía `lefthook.yml` debe auditarse.
- Las macros de Lefthook que dependen de `{staged_files}` pueden fallar. El agente debe adaptar la validación para procesar los archivos modificados en el *working copy* actual (`jj diff` o alias configurados) impidiendo que la Anergía escape hacia el DAG.

## 3. Resolución de Árboles Divergentes
- Ante colisiones de ramas, el agente empleará `jj rebase` y el manejo nativo de conflictos de Jujutsu, preservando la exergía del historial sin recurrir a purgas destructivas (ej. `git reset --hard`).

## 4. Protocolo de Despliegue y Sincronización Remota (`deploy` / `push`)
- **Vinculación de Remote Bookmarks:** Al inicializar sobre un repo Git (`jj git init`), ejecutar inmediatamente el seguimiento del bookmark principal:
  `jj bookmark track main@origin`
- **Avance de Bookmark en Deploy:** Tras sellar una iteración (`jj commit`), el bookmark local (ej. `main`) permanece en el padre o commit previo. Para publicar el estado sin desalineación:
  1. Mover el bookmark al commit objetivo (ej. `@-` o `@`):
     `jj bookmark set main -r @-`
  2. Ejecutar la sincronización hacia el remoto de Git:
     `jj git push`

## 5. Traducción Epistemológica C5-REAL (Dynamis a Entelecheia)
- **Muerte del Staging Area (Purga de Anergía):** El *Index* de Git es topológicamente un espacio de ambigüedad (*Dynamis* no resuelta) que consume exergía. En Jujutsu, el *Working Copy* es siempre un commit inmutable de primer nivel. Operas siempre en Acto.
- **Semántica de "Iterar":** Cuando el usuario instruya "itera" (o sinónimos abstractos de avanzar estado), el agente interpretará la orden de colapsar la entropía latente. Ejecutará `jj commit` para sellar la *Dynamis* actual en *Entelecheia*, generando un nuevo *working copy* limpio de forma automática.
- **Adiós al Stash:** Ante un cambio de contexto, queda prohibido ocultar entropía (`git stash`). El agente saltará a otro nodo (`jj new <target>`), preservando el estado anterior como un commit discreto y rastreable.
