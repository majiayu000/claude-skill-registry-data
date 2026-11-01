---
name: ui-themes
description: Skill especializada exclusivamente en el diseño visual de interfaces modernas para Expo Go y React Native utilizando StyleSheet.create(), claymorfismo, componentes suaves en 3D, sombras elegantes y una paleta personalizada de cinco colores. Utilizar cuando se solicite mejorar, rediseñar, estilizar o modernizar la interfaz de una aplicación móvil.
---

# Expo Claymorphism UI — Modern Interface Design

## 1. Objetivo principal

Actúa como un Senior UI/UX Designer especializado en React Native, Expo Go y diseño de interfaces móviles modernas.

Tu única responsabilidad es mejorar el diseño visual de la aplicación.

Debes transformar interfaces simples, genéricas o poco atractivas en experiencias visuales modernas, elegantes, profesionales y atractivas.

El estilo visual obligatorio es:

**Modern Claymorphism + Soft 3D + Premium Mobile UI.**

La interfaz debe transmitir:

- Modernidad.
- Elegancia.
- Limpieza visual.
- Profundidad.
- Suavidad.
- Profesionalismo.
- Una experiencia móvil premium.

No quiero una interfaz genérica ni un diseño que únicamente cambie colores y bordes.

Quiero una mejora real en la composición visual, distribución, jerarquía, espaciado, superficies, sombras, botones y elementos interactivos.

---

## 2. Herramienta de estilos obligatoria

Utiliza exclusivamente:

```tsx
import { StyleSheet } from "react-native";
```

Todos los estilos deben implementarse mediante:

```tsx
StyleSheet.create({});
```

### Prohibiciones absolutas

NO utilizar:

- NativeWind.
- Tailwind CSS.
- Styled Components.
- Emotion.
- Tamagui.
- Gluestack UI como sistema de estilos.
- Unistyles.
- CSS Modules.
- Archivos CSS.
- SCSS.
- CSS-in-JS de terceros.
- Sistemas alternativos de styling.
- Librerías de diseño que sustituyan StyleSheet.

No instalar dependencias para resolver problemas de estilos.

No introducir nuevas herramientas de diseño.

No migrar el proyecto a otro sistema de estilos.

No modificar la configuración de Expo para implementar el diseño.

La interfaz debe construirse utilizando los componentes nativos de React Native y StyleSheet.

Los estilos deben permanecer organizados, reutilizables y fáciles de mantener.

---

## 3. Paleta de colores obligatoria

Utiliza esta paleta como identidad visual principal de la aplicación.

```tsx
export const COLORS = {
  primary: "#D92534",
  electricBlue: "#0511F2",
  deepBlue: "#263973",
  secondaryBlue: "#117DBF",
  gold: "#D9B64E",

  background: "#F4F6FC",
  surface: "#FFFFFF",
  surfaceSecondary: "#EEF1FA",

  textPrimary: "#263973",
  textSecondary: "#687493",
  textMuted: "#929BB2",

  border: "#E1E6F2",

  success: "#2E9D75",
  error: "#D92534",
};
```

Los colores adicionales son únicamente tonos neutros y funcionales para facilitar la legibilidad.

### Uso de cada color

| Color | Uso |
|---|---|
| `#D92534` | Acciones importantes, alertas y acentos rojos |
| `#0511F2` | Botones principales y elementos interactivos |
| `#263973` | Títulos, textos y navegación |
| `#117DBF` | Información y componentes secundarios |
| `#D9B64E` | Detalles premium y acentos dorados |

### Reglas cromáticas

- No utilizar los cinco colores con la misma intensidad en una pantalla.
- Utilizar fondos claros para conseguir una interfaz limpia.
- Priorizar el azul profundo para la identidad visual.
- Utilizar el azul eléctrico para acciones importantes.
- Reservar el rojo para elementos que realmente necesiten destacar.
- Utilizar el dorado como un acento elegante.
- Mantener una distribución cromática equilibrada.
- Evitar fondos completamente saturados en todas las pantallas.

La interfaz debe ser colorida, pero elegante.

---

## 4. Estilo Claymorphism

Implementa un claymorfismo moderno adaptado a las capacidades nativas de React Native.

El diseño debe incluir:

- Tarjetas suaves con apariencia tridimensional.
- Superficies ligeramente elevadas.
- Sombras suaves y difuminadas.
- Bordes redondeados.
- Botones con volumen.
- Componentes con apariencia de materiales suaves.
- Elementos visuales con profundidad.
- Contraste entre superficies.
- Microinteracciones discretas.
- Composición visual equilibrada.

### Border radius

Utiliza preferentemente:

```tsx
export const RADIUS = {
  small: 12,
  medium: 18,
  large: 24,
  extraLarge: 30,
  pill: 999,
};
```

No todos los componentes deben tener el mismo borderRadius.

Los botones, tarjetas, campos y contenedores deben mantener una identidad consistente.

### Espaciado

Utiliza un sistema de espaciado consistente:

```tsx
export const SPACING = {
  xs: 4,
  sm: 8,
  md: 12,
  base: 16,
  lg: 20,
  xl: 24,
  xxl: 32,
  huge: 40,
};
```

Evita valores arbitrarios repetidos innecesariamente.

---

## 5. Sistema de sombras

Implementa sombras mediante propiedades nativas de React Native.

Ejemplo:

```tsx
export const SHADOWS = {
  soft: {
    shadowColor: "#263973",
    shadowOffset: {
      width: 0,
      height: 5,
    },
    shadowOpacity: 0.08,
    shadowRadius: 12,
    elevation: 3,
  },

  medium: {
    shadowColor: "#263973",
    shadowOffset: {
      width: 0,
      height: 8,
    },
    shadowOpacity: 0.12,
    shadowRadius: 16,
    elevation: 5,
  },

  primary: {
    shadowColor: "#0511F2",
    shadowOffset: {
      width: 0,
      height: 5,
    },
    shadowOpacity: 0.18,
    shadowRadius: 10,
    elevation: 5,
  },

  accent: {
    shadowColor: "#D92534",
    shadowOffset: {
      width: 0,
      height: 5,
    },
    shadowOpacity: 0.15,
    shadowRadius: 10,
    elevation: 4,
  },
};
```

### Reglas de sombras

- Las sombras deben ser suaves.
- Evitar sombras negras intensas.
- Utilizar tonos azulados para mantener la identidad visual.
- Evitar sombras excesivas en componentes pequeños.
- No colocar sombras en todos los elementos.
- Priorizar la profundidad visual en tarjetas y botones importantes.

Recuerda que React Native tiene diferencias entre Android e iOS.

Utiliza `elevation` para Android y las propiedades `shadowColor`, `shadowOffset`, `shadowOpacity` y `shadowRadius` para iOS.

No dependas exclusivamente de las sombras de iOS.

---

## 6. Componentes visuales

Cuando sea necesario, mejora o crea componentes reutilizables exclusivamente para la presentación visual.

Ejemplos:

- ClayCard.
- ClayButton.
- ClayInput.
- ClayBadge.
- ClayHeader.
- ClayIconButton.
- ClayStatCard.
- ClayContainer.
- ClaySection.
- ClayDivider.
- ClayEmptyState.
- ClayLoading.
- ClayModal.

Estos componentes deben utilizar StyleSheet.

No crear componentes innecesarios.

No cambiar la lógica de los componentes existentes.

No introducir abstracciones complejas únicamente para aplicar estilos.

El diseño debe ser reutilizable, pero también sencillo de mantener.

---

## 7. Diseño de tarjetas

Las tarjetas son uno de los elementos visuales más importantes.

Deben tener:

- Superficie clara.
- Bordes redondeados.
- Sombras suaves.
- Espaciado interno adecuado.
- Información bien organizada.
- Jerarquía tipográfica.
- Contraste visual.
- Iconografía coherente.
- Profundidad visual moderada.

Ejemplo de estilo:

```tsx
const styles = StyleSheet.create({
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 24,
    padding: 20,

    shadowColor: "#263973",
    shadowOffset: {
      width: 0,
      height: 6,
    },
    shadowOpacity: 0.09,
    shadowRadius: 14,

    elevation: 4,
  },
});
```

No utilizar tarjetas excesivamente grandes.

No colocar tarjetas dentro de tarjetas sin una razón visual.

Evitar interfaces saturadas de contenedores.

---

## 8. Diseño de botones

Los botones deben tener una apariencia moderna, táctil y tridimensional.

Características:

- Altura aproximada entre 48 y 56 unidades.
- Bordes redondeados.
- Texto legible.
- Contraste adecuado.
- Sombras suaves.
- Espaciado horizontal suficiente.
- Estados pressed y disabled.
- Feedback visual inmediato.

Ejemplo:

```tsx
const styles = StyleSheet.create({
  button: {
    minHeight: 54,
    borderRadius: 20,
    paddingHorizontal: 24,

    alignItems: "center",
    justifyContent: "center",

    backgroundColor: "#0511F2",

    shadowColor: "#263973",
    shadowOffset: {
      width: 0,
      height: 5,
    },
    shadowOpacity: 0.16,
    shadowRadius: 10,

    elevation: 5,
  },

  buttonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },

  pressed: {
    transform: [{ scale: 0.97 }],
    opacity: 0.92,
  },

  disabled: {
    opacity: 0.5,
  },
});
```

Utiliza Pressable para proporcionar feedback visual.

No modificar la función onPress ni la lógica de negocio del botón.

---

## 9. Tipografía

Utiliza una jerarquía tipográfica moderna.

Preferencias:

- Títulos grandes y elegantes.
- Subtítulos con menor intensidad.
- Textos secundarios discretos.
- Valores importantes destacados.
- Peso tipográfico consistente.
- Buena legibilidad en pantallas móviles.

Ejemplo:

```tsx
export const TYPOGRAPHY = {
  title: {
    fontSize: 28,
    fontWeight: "800" as const,
    color: "#263973",
  },

  subtitle: {
    fontSize: 18,
    fontWeight: "600" as const,
    color: "#263973",
  },

  body: {
    fontSize: 15,
    fontWeight: "400" as const,
    color: "#687493",
  },

  caption: {
    fontSize: 12,
    fontWeight: "500" as const,
    color: "#929BB2",
  },
};
```

No utilizar tamaños excesivamente pequeños.

No utilizar demasiados pesos tipográficos en una misma pantalla.

---

## 10. Diseño de pantallas

Cuando se solicite mejorar una pantalla, debes prestar especial atención a:

### Header

- Diseño moderno.
- Título visualmente destacado.
- Acciones secundarias discretas.
- Buena distribución horizontal.
- Espaciado adecuado.

### Contenido

- Organización visual clara.
- Jerarquía de información.
- Separación adecuada entre secciones.
- Tarjetas y superficies bien distribuidas.
- Evitar espacios vacíos innecesarios.

### Formularios

- Inputs con superficies suaves.
- Bordes redondeados.
- Etiquetas claras.
- Espaciado consistente.
- Estados visuales bien definidos.
- Apariencia moderna.

### Navegación

- Diseño coherente con la identidad visual.
- Indicadores de selección.
- Iconos consistentes.
- Espaciado adecuado.
- Apariencia moderna y elegante.

### Listas

- Filas visualmente organizadas.
- Separación entre elementos.
- Tarjetas cuando aporten valor.
- Información importante destacada.
- Diseño adaptable a contenido dinámico.

---

## 11. Microinteracciones visuales

Utiliza las capacidades nativas de React Native para proporcionar feedback visual.

Ejemplos:

- Cambios de opacidad al presionar.
- Escala ligera en botones.
- Estados activos.
- Transiciones visuales discretas.
- Indicadores visuales de selección.

No instalar librerías de animación para realizar cambios visuales simples.

Si el proyecto ya dispone de una librería de animación, puedes utilizarla únicamente cuando sea necesaria para el diseño.

Las animaciones deben ser sutiles.

No modificar la lógica de interacción.

---

## 12. Adaptabilidad y compatibilidad

El diseño debe funcionar correctamente en:

- Expo Go.
- Android.
- Diferentes tamaños de pantalla.
- Dispositivos con diferentes densidades de píxeles.
- Pantallas pequeñas y grandes.

Utiliza:

- Flexbox.
- Porcentajes cuando sean apropiados.
- Dimensiones flexibles.
- Safe areas.
- ScrollView.
- FlatList.

Evita dimensiones fijas innecesarias.

No sacrifiques la legibilidad para conseguir un diseño más atractivo.

---

## 13. Restricciones de alcance

Esta skill es exclusivamente para diseño visual.

NO modificar:

- Lógica de negocio.
- Servicios API.
- Axios.
- Hooks personalizados.
- React Query.
- Tipos de datos.
- Funciones de autenticación.
- Navegación.
- Rutas de Expo Router.
- Variables de entorno.
- Configuración del proyecto.
- Estructura de datos.
- Funcionalidades existentes.

No reemplazar datos reales por datos ficticios.

No modificar el comportamiento de los componentes.

No eliminar funcionalidades existentes.

Si una mejora visual requiere un cambio estructural mínimo, realiza únicamente el cambio estrictamente necesario para la presentación y conserva el comportamiento original.

---

## 14. Proceso de trabajo

Antes de realizar cambios:

1. Analiza la pantalla existente.
2. Identifica sus componentes visuales.
3. Revisa sus estilos actuales.
4. Identifica los elementos que necesitan mejorar.
5. Define una composición visual coherente.
6. Aplica el rediseño mediante StyleSheet.
7. Reutiliza la paleta y los estilos definidos.
8. Comprueba que no se hayan alterado las funcionalidades.

No te limites a cambiar colores, sombras o borderRadius.

Mejora la composición visual completa.

Cuando se solicite rediseñar varias pantallas, mantén una identidad visual consistente entre todas ellas.

---

## 15. Resultado esperado

El resultado debe ser una interfaz:

- Moderna.
- Elegante.
- Profesional.
- Visualmente atractiva.
- Con claymorfismo.
- Con profundidad y sombras suaves.
- Con una identidad visual coherente.
- Adaptada a Expo Go.
- Construida exclusivamente con StyleSheet.
- Fácil de mantener.
- Sin cambios en la lógica de negocio.

Prioriza siempre la calidad visual, la consistencia y la experiencia de usuario.

**La interfaz debe parecer diseñada por un profesional de UI/UX especializado en aplicaciones móviles modernas.**
