---
name: documentar-aplicacion
description: >-
  Producir, al cerrar una aplicación o un slice, dos entregables profesionales desde el Cerebro: la
  GUÍA DE USO para personas (empezar en pocos pasos, cada flujo con pantallas y paso a paso, glosario,
  preguntas frecuentes) y la DOCUMENTACIÓN TÉCNICA Y FUNCIONAL completa (resumen, módulos, modelo de
  datos, API, flujos, catálogo de reglas, integraciones, decisiones, pruebas, pendientes, aprendizajes,
  bitácora, glosario, diagramas). Primero el script bin/generar-documentacion.py (índice y diagramas
  SVG), después se pule la prosa SOLO con lo que está en el Cerebro; pantallas de Stitch y diagramas de
  Archify enlazados. Usar cuando se pida "documentá la app", "armá el manual", "la guía de uso", "la
  bitácora técnica", "el entregable de documentación", "/documentar-aplicacion". No inventa. Español
  (Argentina).
---

# Documentar la aplicación

Dos documentos, dos lectores. La **guía de uso** le dice a una persona *cómo* usar la aplicación, en
pasos cortos y con la pantalla a la vista. La **documentación técnica y funcional** le dice al equipo
*qué* es, *cómo* está construida y *por qué*, con índice, diagramas y bitácora. Las dos salen del
Cerebro: lo que no está ahí, **no se inventa**: se marca y se pregunta.

## Flujo

1. **Encuadre** (un turno): módulo, repositorio de código para la radiografía, y cuál de los dos
   documentos (o los dos). Si la aplicación tiene pantallas sin maqueta citada, se avisa: la guía va a
   salir con huecos hasta pasar por [[disenar-con-stitch]].
2. **Primero el script**, que arma estructura, índice, diagramas y marca en amarillo lo que falta:

   ```bash
   python -B bin/generar-documentacion.py --tipo manual --modulo <slug>
   python -B bin/generar-documentacion.py --tipo tecnica --modulo <slug> --app <ruta del repo>
   ```

   Deja `borrador/documentacion/guia-de-uso.html` y `documentacion-tecnica.html`, con las pantallas que las
   fichas citan en `fuente_maqueta` embebidas y los diagramas de `borrador/diagramas/` enlazados. Un script
   que no corrió es `SIN DATOS`.
3. **Completar lo marcado `<completar>`** leyendo el Cerebro (fichas, contexto, decisiones, `aplicacion/`).
   Lo que el Cerebro no tiene se pregunta **en una sola tanda** o queda `⚠`; nunca se rellena con una
   suposición. Para la guía, la prosa va en criollo: frases cortas, **un paso por acción**, el verbo
   primero, sin siglas en la cara del lector; el porqué no va en la guía, va en la técnica.
4. **Pantallas y diagramas**: una pantalla sin maqueta → [[disenar-con-stitch]]; un diagrama de
   secuencia o de arquitectura que valga la pena mostrar → `archify` a `borrador/diagramas/` (se enlaza);
   el grafo de módulos y el modelo de datos salen de la radiografía. Nada se dibuja «de memoria».
5. **Revisión** (checklist, un veredicto por documento):
   - índice completo y cada sección con contenido o con su `⚠` declarado;
   - cada flujo con pasos **y** pantalla; cada regla citada existe en la ficha;
   - sin PHI (capturas incluidas), sin datos inventados, sin hexadecimales sueltos;
   - la guía se puede seguir sin leer la técnica.
   **OK** si todo cierra; **HALLAZGO** por cada falta, con la sección; **SIN DATOS** si el script no corrió.
6. **Promover** con un «sí» a `entregables/documentacion/` (y la entrada en `log.md` por `cerebro-curator`).
7. **Retroalimentación**: cada hueco que apareció es un `P-nnn` en `pendientes.md`; lo que se descubrió
   de la aplicación al documentarla es un `AP-nnn`. Nada se queda en el documento.

## Barreras

- **No inventa**: pasos, reglas, nombres y comportamientos salen de las fichas y del código radiografiado.
- **Sin PHI** en textos, ejemplos y capturas.
- **No reemplaza el `README.md` del repositorio** (cómo se construye y se corre): lo cita.
- Se regenera después de cada slice; el documento promovido se reemplaza, no se parchea a mano.
- Todo en español (Argentina).
