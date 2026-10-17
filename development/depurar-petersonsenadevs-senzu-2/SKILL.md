---
name: depurar
description: "Método para arreglar bugs sin dar palos de ciego: reproducir, test que falla, hipótesis, acotar, arreglar y verificar. Úsala cuando algo falla o no funciona mientras construyes (tests en rojo, excepción, error 500, resultado incorrecto)."
---

# depurar (Senzu)

Un bug se arregla **entendiéndolo**, no probando cambios hasta que deje de fallar. Cambiar cosas al
azar arregla el síntoma, esconde la causa y rompe otra cosa. Esta skill se usa en dos momentos:
- **Mientras construyes** (una función, un endpoint, un componente): en cuanto un test sale en rojo o
  algo no hace lo esperado, para y aplica el método antes del siguiente cambio.
- **Ante un bug reportado** (`/depurar <síntoma>`): el mismo método desde el paso 1.

## El método (en orden, sin saltarse pasos)
1. **Reproducir**: el error exacto (mensaje, traza, entrada que lo provoca). Sin reproducción fiable no
   se arregla nada: si no se reproduce, lo primero es conseguirlo (datos, pasos, entorno).
2. **Test que falla**: escribe el test más pequeño que reproduce el bug y comprueba que falla por el
   motivo correcto. Será la prueba del arreglo y la red contra regresiones.
3. **Leer el error de verdad**: la traza completa, desde la primera línea del código propio. El mensaje
   suele decir la causa; léelo antes de formular teorías.
4. **Hipótesis explícita**: "falla porque X". Una sola, escrita, con qué la confirmaría o la descartaría.
5. **Acotar**: divide el problema a la mitad (entrada, capa, commit) hasta aislar dónde nace. Herramientas
   y técnicas por stack: `references/tecnicas-por-stack.md`.
6. **Arreglar la causa**, no el síntoma: el cambio mínimo que la resuelve. Si el arreglo es un `try/catch`
   que silencia el error, un `if` que esquiva el caso o un `sleep`, casi seguro no es la causa.
7. **Verificar**: el test del paso 2 en verde, la suite completa en verde (`/verificar`) y el caso real
   reproducido del paso 1 funcionando.
8. **Documentar**: causa en una frase, arreglo y test en el devlog. Si el mismo tipo de bug puede volver
   en otros sitios, búscalo ahora (mismo patrón en el resto del código).

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Depuradores, logs temporales y bisección por stack | `references/tecnicas-por-stack.md` |
| Síntomas típicos y su causa habitual (no reinventar) | `references/sintomas-frecuentes.md` |

## Reglas duras
- **Tres intentos fallidos = parar.** Si tras tres cambios sigue fallando, la hipótesis es mala: vuelve
  al paso 3 y 4 con lo aprendido, o pide contexto al usuario. No sigas cambiando cosas.
- **Un cambio cada vez**, con el test ejecutado después. Varios cambios juntos = no sabes cuál arregló.
- **Logs temporales**: permitidos durante la depuración con el comentario `senzu-allow`
  (el hook de higiene lo exige) y **se quitan antes de cerrar**.
- **No toques el test para que pase.** Si el test estaba mal, dilo y explica por qué; si no, el que está
  mal es el código.
- **No desactives la validación, la seguridad ni los tests** para "ver si así funciona".
- Si el bug está en una dependencia: confírmalo con una reproducción mínima fuera del proyecto antes de
  culparla, y busca si ya está reportado o arreglado en una versión posterior.

## Relación con otras skills
- Tests → `code-quality/references/testing.md`. Errores y logs → `code-quality/references/errors-logging.md`.
- Bug de rendimiento → `code-quality/references/performance.md` (medir antes de cambiar).
- Bug que destapa un problema de diseño → anótalo para `/auditar` o `/refactor`; no lo arregles de paso.
