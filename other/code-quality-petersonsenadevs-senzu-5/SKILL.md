---
name: code-quality
description: "Buenas prácticas de código (Laravel/PHP, TypeScript, React/Next, Vue, Astro, Python): tipado, tests, errores/logs, seguridad, rendimiento, APIs, PR. Úsala al escribir o refactorizar lógica, testear, revisar PR o diseñar endpoints."
---

# code-quality (Senzu)

Referencias por tema en `references/`. **No las leas todas**: cada una empieza con un índice; lee solo
la sección que necesites (Read con offset/limit o Grep). Una referencia por tarea salvo que la tarea cruce temas.

¿No sabes qué referencia abrir? Rápido: árbol B2 de `skill-router/references/decision-trees.md`.
Completo: **`references/backend-catalog.md`** (tarea/síntoma → receta §sección, como el catálogo de efectos).

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Escribir/refactorizar código Laravel | `references/php-laravel.md` (sección del tema: Eloquent, colas, validación…) |
| Código TS de lógica (Next server, Node, utilidades) | `references/typescript.md` |
| Componentes/rutas Next.js | `references/react-next.md` (+ `ui-ux-pro-max` si hay UI) |
| Componentes/composables Vue | `references/vue.md` |
| Astro (islands, collections, endpoints) | `references/astro.md` |
| Python / FastAPI / LangGraph | `references/python.md` |
| WordPress / WooCommerce (theme o plugin a medida) | `references/wordpress.md` |
| API Node (Express / NestJS) | `references/node-api.md` (+ `references/typescript.md`) |
| Nuxt (páginas, server routes, useFetch) | `references/nuxt.md` (+ `references/vue.md`) |
| SvelteKit / Svelte 5 (runes, load, form actions) | `references/sveltekit.md` |
| Go (servicios, CLIs, concurrencia) | `references/go.md` |
| Java / Spring Boot | `references/java.md` |
| C# / .NET / ASP.NET Core | `references/csharp.md` |
| Auth: login, registro, reset, OAuth, 2FA, API keys | `references/auth-patterns.md` |
| Colas, jobs, emails en background, cron | `references/jobs-and-queues.md` |
| Caché (qué, claves, invalidación, stampede) | `references/caching.md` |
| Esquema de BD, índices, migraciones seguras, full-text | `references/database-design.md` |
| Tiempo real: websockets, SSE, broadcasting, presencia | `references/realtime.md` |
| Uploads, S3/R2, imágenes en servidor, URLs firmadas | `references/files-media.md` |
| Chat/IA en el producto: RAG, streaming, costes, evals | `references/llm-apps.md` |
| Dinero, fechas/zonas, race conditions, únicos, soft delete | `references/data-integrity.md` |
| APIs externas, webhooks, pagos, email transaccional | `references/integrations.md` |
| Crear o arreglar tests | `references/testing.md` §pirámide + §stack correspondiente |
| Manejo de errores, logs, reintentos | `references/errors-logging.md` |
| Auth, inputs externos, uploads, secretos, LLM | `references/security-owasp.md` (checklist final) |
| "Va lento" / consultas / caché | `references/performance.md` §medir + §capa afectada |
| Diseñar o cambiar un endpoint/API | `references/api-design.md` |
| Web multiidioma (ES/CA/EN), hreflang, locales | `references/i18n.md` |
| Abrir o revisar un PR, commits | `references/git-and-reviews.md` §checklist |
| Qué API/sintaxis permite la versión del stack, upgrades, EOL | `references/stack-versions.md` (la versión REAL manda) |
| Proyecto heredado: adoptar sus convenciones (/adoptar) | `references/adopt-conventions.md` |
| Arquitectura: capas, servicios, DTO, carpetas, hexagonal o DDD declarados (`senzu/arquitectura/capas.json`) | `references/arquitectura-declarada.md` + `scripts/arquitectura.mjs` (`--detectar`, `--plantilla`, `--comprobar`) |
| Auditar el backend, deuda técnica, refactor grande (/auditar, /refactor) | skill `backend-audit` (encuentra con pruebas; las recetas de aquí lo arreglan) |
| Explicar un proyecto a quien llega nuevo: estructura, flujos, dónde tocar (/mapa) | `references/mapa-proyecto.md` |
| Algo falla o no funciona mientras construyes | skill `depurar` (método: reproducir, test que falla, hipótesis, acotar) |
| Verificar el proyecto tras TUS cambios | `scripts/verify-build.mjs` desde la raíz (lint+types+tests+build; corrige hasta 0 fallos). En monorepos verifica cada paquete con cambios en su carpeta y lenguaje (JS con su gestor, Python con uv/poetry, PHP, Go); `--plan` enseña qué ejecutaría, `--paquete apps/web`, `--todos`, `--sin-build`. Entiende también Rust, Ruby, Maven/Gradle, .NET, Deno, Python con requirements.txt y Makefile/justfile. **Sin manifiesto no es un build**: ejecuta las suites propias del repo (`tools/test-*`, `check-*`), la sintaxis de lo cambiado y los enlaces de los `.md` cambiados (`--rapido` sin suites) |

## Principios transversales (aplican siempre, sin leer nada más)
1. **Lee antes de escribir**: imita naming, estructura y estilo del código vecino; no introduzcas patrones nuevos sin motivo. Si existe `senzu/conventions.md` (adoptado con `/adoptar`), es ley.
2. **Tipado estricto** en todos los lenguajes (`declare(strict_types=1)`, `strict: true`, mypy/pyright estricto). Sin `any`/`mixed` sin justificar.
3. **Validar en el borde, confiar dentro**: entrada externa (HTTP, colas, LLM, ficheros) se valida y se convierte a tipos; el núcleo asume datos válidos.
4. **Funciones pequeñas, una responsabilidad, nombres que digan qué hacen**. Sin comentarios que repitan el código; sí comentarios de "por qué".
5. **Errores explícitos**: excepciones de dominio con mensaje accionable; nunca `catch` vacío; nunca loguear secretos/PII.
6. **Tests que protegen comportamiento**, no implementación: happy path + errores + bordes; rápidos en dominio, integración acotada.
7. **Seguridad por defecto**: autorización en cada acción sensible, consultas parametrizadas, secretos en entorno, dependencias auditadas.
8. **Rendimiento medido**: sin optimizar a ciegas; N+1, índices, paginación y caché son lo primero que se revisa.
9. **Cambios pequeños y reversibles**: PR < 400 líneas, Conventional Commits, sin co-autores, push solo a la rama de trabajo (nunca a una principal ni forzado).
10. **Verifica antes de afirmar**: lint + tests + tipos del stack (`commands` en `stack.json`) antes de decir "hecho"; pega la salida.

## Checklist de PR (bloqueante)
- [ ] Lint/format, tipos y tests del stack en verde (salida pegada en el devlog).
- [ ] Nuevo comportamiento cubierto por tests; tests antiguos no borrados sin justificación.
- [ ] Sin `any`/`mixed`, sin `dd()`/`console.log`/`print` de depuración, sin TODOs sin issue.
- [ ] Entrada externa validada; autorización comprobada; sin secretos en código ni logs.
- [ ] Consultas sin N+1; paginación en listados; índices para filtros nuevos.
- [ ] Errores con mensaje accionable; logs con contexto y nivel correcto.
- [ ] Devlog actualizado (skill `devlog`); commit con Conventional Commits.

## Reglas aprendidas (extensible)
Si detectas una regla GENERAL del stack o lenguaje (error repetido en proyectos, convención del equipo),
no la dejes morir en el devlog: propón añadirla a Senzu y, con el ok del usuario, escríbela en
`stacks/<stack>/rules/<tema>.md` (se anexa al CLAUDE.md/AGENTS.md de los proyectos al correr `sync.ps1`)
o como sección nueva de la referencia del lenguaje (`references/<lenguaje>.md`). Regla + porqué + ejemplo mínimo.

## Relación con otras skills
- UI, estilos, accesibilidad visual → `ui-ux-pro-max`. Dominio complejo, módulos, puertos/adaptadores → `ddd-hexagonal`.
- Documentación del paso → `devlog`. Si el proyecto tiene `stacks/<x>/best-practices.md` en `CLAUDE.md`, prevalece lo específico del proyecto.
