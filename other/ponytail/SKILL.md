---
name: ponytail
description: Convierte una lista de tareas o un informe de errores en un plan de trabajo priorizado y verificable, separando lo que es un bug real de lo que solo parece un bug. Usar cuando el usuario entregue un plan externo (otro modelo, otro agente) y haya que decidir que se adopta, cuando una lista de "problemas" deba convertirse en un alcance, o antes de tocar varios ficheros para decidir el orden y el reparto de ownership.
---

# Ponytail

Un plan que llega de otro sitio no es un encargo. Es un documento con su propia
probabilidad de estar equivocado, y algunos de sus puntos pueden estar
inventando bugs que no existen. Adoptarlo entero es tan malo como ignorarlo
entero: en ambos casos se pierde el trabajo de quien lo escribio y el contexto
de quien revisa.

Esta skill es el filtro. Su trabajo es separar las tres cosas que se mezclan en
cualquier lista de trabajo:

1. **Bug real**: se puede escribir un test que falla antes del arreglo.
2. **Feature ausente**: el codigo esta bien, lo que falta es funcionalidad.
3. **Alucinacion**: el supuesto no se sostiene contra el codigo.

La mayoria del tiempo de una revision se va en separar la 3 de la 1. Es
invertido respecto a lo que parece.

## Procedimiento

### 1. Verificar cada punto antes de Adoptarlo

Por cada punto del plan, en un comando: buscar el fichero, leer las lineas
citadas, y decidir en cual de las tres categorias cae. **Citar linea.** Un
punto sin linea verificable no se adopta: se anota como dudoso y se pregunta.

El fallo tipico es aceptar el punto porque "suena a bug". Suena igual de
convincente un bug real, una feature pedida y una suposicion falsa sobre codigo
que nadie ha leido. El unico filtro que funciona es abrir el fichero.

### 2. Buscar el efecto en cascada

Corregir un bug suele destapar otro, porque el primero estaba enmascarandolo.
Presupuestar una segunda iteracion es parte del analisis, no un imprevisto.

Ejemplo real de este repo: al arreglar la persistencia de las pistas hijas de un
release, aparecio que la duracion del padre se quedaba en el valor guardado en
BD. El arreglo del primer bug no era incorrecto; era incompleto, y solo se vio
al probarlo.

### 3. Fijar el contrato de cada cambio

Para cada fichero: quien lo escribe, que se espera de el, y que test lo
comprueba. Un cambio sin test observador se documenta, no se cierra.

### 4. Cerrar con lo que queda fuera

El entregable de la revision no es solo la lista de arreglos. Es tambien la
lista de lo que se **decidio no hacer**, con el motivo. Sin ella, el siguiente
que lea el plan va a intentar lo mismo otra vez.

## Cuando el plan propone añadir infraestructura

Un plan externo tiende a proponer cosas grandes — un MCP de terceros, un
endpoint nuevo, un campo de configuracion — para resolver algo que todavia no se
ha aislado. Cuestionar la dimension antes de construir.

Dos criterios:

- **¿El dato es verificable con lo que ya hay?** Si la fuente canonica no lo
  da, buscarlo mas lejos no lo hace fiable: lo convierte en candidato, no en
  hecho.
- **¿Hay un modo de fallo silencioso?** Una dependencia extra que degrada en
  silencio es peor que no tenerla.

Ejemplo real: un plan propuso un MCP de busqueda de YouTube para encontrar el
canal oficial de un artista. El MCP devuelve el canal que el buscador considera
relevante, no el canal verificado del artista. Anadido tal cual, habria metido
en el perfil del artista el canal equivocado, con su catalogo y sus
suscriptores, y nada en el resultado habria parecido un error.

## Errores tipicos

- **Aceptar el punto sin abrir el fichero.** Es el error principal. Todo lo demas
  es consecuencia.
- **Confundir "no lo he encontrado" con "no existe".** Ausencia de evidencia no
  es evidencia de ausencia.
- **Dar por bueno un arreglo que no se puede volver a romper.** Si no hay un test
  que falle al revertir el arreglo, no hay nada protegido. Un check que siempre
  pasa no protege de nada.
- **Ejecutar el plan al pie de la letra y perder el contexto.** El plan se hizo
  sin acceso al estado real de los datos. Esa informacion la tiene quien revisa,
  y es la parte mas valiosa de la revision.
