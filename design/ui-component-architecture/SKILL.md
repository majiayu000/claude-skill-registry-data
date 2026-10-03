---
name: ui-component-architecture
description: "Diseña, crea o refactoriza componentes y screens frontend con límites claros, reutilización práctica y composición simple. Usa esta skill cuando se agregue o reorganice UI con responsabilidad propia, cuando una screen o modal concentre demasiada lógica o JSX, o cuando haya que decidir qué vive dentro del componente reusable y qué queda como integración de la feature. Aplica también cuando se agrega JSX nuevo con interacción o estado propio a un componente existente , no solo al crear un archivo nuevo."
---

## Propósito

Crear o refactorizar UI con buena composición, reutilización práctica y separación clara de responsabilidades.

## Cuándo usarla

Usala cuando:

- se crea un componente o screen;
- se refactoriza un componente o screen existente;
- un componente o screen concentra demasiada lógica o JSX;
- conviene decidir límites entre componente reusable y adaptación específica de feature;
- la nueva UI puede reaparecer en otros flujos.

## Cuando el pedido es un refactor

Antes de tocar código, escaneá el archivo en busca de:

- Variables o funciones declaradas y nunca usadas.
- Helpers (`formatDate`, mappers, etc.) duplicados en archivos vecinos — hacé grep antes de extraer a un archivo compartido.
- Interfaces con intersecciones `A & { extra }` que conviene fusionar.
- Bloques de JSX que se repiten en ≥ 2 archivos — extraé un componente solo si supera las 20 líneas o tiene lógica propia.

Extraé solo lo que se reutiliza en más de un lugar o que hace el archivo difícil de leer. No extraigas por reflejo.

## Reglas

- Buscá componentes existentes antes de crear nuevos.
- Reutilizá antes de duplicar.
- Aplicá APD según el patrón real del equipo, no como clasificación burocrática.
- Definí props estables y orientadas al dominio real del componente.
- Evitá mezclar UI reusable con reglas de negocio de un único flujo.
- Si ya existe estado o acciones desde un hook o feature superior, no dupliques fuentes de verdad sin necesidad.
- Mantené responsive de forma proporcional al cambio.
- Usa naming para un componente reutilizable, si es demasiado especifico, dale un naming acorde.

## Qué debe vivir dentro del componente reusable

Cuando el componente represente una **unidad visual completa**, incluí dentro de él:

- wrapper raíz del bloque;
- título o label opcional si forma parte natural de la capacidad;
- helper text o descripción opcional;
- cuerpo interactivo;
- empty/loading/error states propios del componente, si aplican.

Dejá fuera únicamente:

- composición global de la screen;
- layout estrictamente contextual;
- reglas de negocio específicas de la feature.

## Personalización visual

Una vez creado el componente, conservá una UI default y permití personalización de los contenedores iniciales:

- `className` para el root cuando el proyecto use ese patrón;
- `classNames`, `classes` o equivalente por slots si hay múltiples subcontenedores importantes;
- variantes controladas si el design system del repo ya las usa.

Ejemplos de slots posibles:

- `root`
- `label`
- `description`
- `content`
- `item`
- `action`
