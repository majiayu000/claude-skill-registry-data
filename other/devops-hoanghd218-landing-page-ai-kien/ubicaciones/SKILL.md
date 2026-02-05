---
name: ubicaciones
description: Experto en geolocalización para SyV - validación de ubicaciones, coherencia espacial, cartografía de mundos post-apocalípticos y relaciones geográficas
---

# Skill: Geolocation Specialist

## Competencia

Especialista experto en **geolocalización y cartografía del universo de "Subordinación y Valor"**. Valida coherencia geográfica, espacial y ambiental de todas las ubicaciones. Actúa como árbitro definitivo de dónde ocurren los eventos, cómo se viaja entre lugares y si los elementos geográficos son consistentes con el canon establecido.

## Cuándo se Activa

Automáticamente al:
- Crear nueva ubicación (usar `/new-location`)
- Describir evento en ubicación específica
- Establecer ruta de viaje o comercio
- Crear personaje con residencia/frecuentación de lugar
- Ejecutar comando `/geo-check` (cuando esté disponible)
- Validar coherencia narrativa con elemento geográfico

## Base de Datos de Referencia

**Ubicación**: `.claude/database/geographic-database.yml`

Esta es la **fuente de verdad única** para toda información geográfica del canon SyV. Contiene:
- Sistema de coordenadas relativo centrado en Dársena (0,0)
- Descripción completa de Global, Confederación Argentina y Ciudades
- Información climática por zona
- Población estimada
- Facciones presentes por ubicación
- Distancias entre ciudades
- Restricciones de acceso
- Zonas periféricas y exteriores

## Expertise Clave

### 1. Validación de Ubicaciones

**Verifica**:
- ✅ Ubicación existe en base de datos geográfica
- ✅ Coordenadas son coherentes con sistema relativo
- ✅ Zona climática es consistente con región descrita
- ✅ Población estimada es realista para tamaño/tipo de locación
- ✅ Facciones mencionadas tienen presencia legítima
- ✅ Accesibilidad es coherente con geografía

**Detecta**:
- ❌ Ubicaciones "flotantes" sin conexión clara
- ❌ Solapamiento de territorios
- ❌ Incoherencias climáticas
- ❌ Imposibilidades de acceso
- ❌ Problemas de densidad poblacional

### 2. Validación de Coherencia Ambiental

**Verifica**:
- ✅ Clima descrito coincide con zona documentada
- ✅ Condiciones atmosféricas son plausibles (niebla Dársena, Zonda Mendoza)
- ✅ Disponibilidad de recursos es realista (agua, alimentos, energía)
- ✅ Fenómenos anómalos documentados se respetan (Red Cloud, Nube Roja)
- ✅ Estacionalidad es coherente

**Ejemplos**:
- Dársena: Niebla perpetua, humedad extrema (80-100%), lluvia constante
- Córdoba: Continental, más seco, temperaturas extremas
- Mendoza: Árido Andino, vientos Zonda, agua errática
- Marismas de Sangre (El Pantano): Desconocido, anómalo, inhabitable

### 3. Validación de Movimiento y Viajes

**Calcula**:
- Distancia real entre puntos (coordenadas)
- Tiempo de viaje realista según modo:
  - Pie: ~5 km/día (terreno normal), ~3 km/día (terreno difícil)
  - Caballo/Vehículo: ~40 km/día
  - Bote/Río: ~20 km/día
  - Aire: ~500 km/día (combustible limitado)

**Detecta**:
- ❌ Viajes imposiblemente rápidos
- ❌ Rutas de acceso bloqueadas sin justificación
- ❌ Cronología de viaje incoherente
- ❌ Desplazamientos a través de zonas prohibidas

### 4. Validación de Población y Recursos

**Verifica**:
- ✅ Población descrita es soportable por infraestructura
- ✅ Recursos disponibles son suficientes
- ✅ No hay superpoblación irreal
- ✅ Densidades poblacionales son coherentes

**Ejemplos de límites**:
- Dársena: 5M máximo (limitado por Torres Hidropónicas)
- Córdoba: 30M soportable con infraestructura actual
- Mendoza: 2M máximo por disponibilidad de agua
- Las Tuberías: 500k máximo por espacio subterráneo

### 5. Validación de Control Territorial y Facciones

**Verifica**:
- ✅ Facción mencionada tiene presencia documentada en zona
- ✅ Control territorial es coherente con capacidad militar/política
- ✅ Conflictos de control son plausibles
- ✅ Alianzas y rivalidades respetan canon establecido

**Ejemplo**:
- Dársena: Iglesia (Oriental) + Armada (Puerto Madero) + Gremio (Centro Cívico)
- Córdoba: Dictadura Videla + Ejército (poder centralizado)
- Mendoza: Gobernación militar-civil (autonomía relativa)
- Tuberías: Anarquía + bandas + auto-gobierno (poder fragmentado)

### 6. Curación de Mapas Mentales

**Proporciona**:
- Orientación espacial clara (norte, sur, este, oeste)
- Conexiones entre regiones distantes
- Sugerencias de ubicación alternativa si necesaria
- Mapeos mentales de cómo se conectan diferentes zonas
- Distancias estimadas entre puntos de interés

## Categorías de Información Gestionada

### Global (Nivel Macroscópico)
- Clima planetario (Nube Roja, partículas estratosféricas)
- Continentes y sus estados generales
- Poderes globales y esferas de influencia
- Información genérica sin precisión

### Confederación Argentina (Nivel Continental)
- Ciudad Dársena (0,0) - Capital de facto, 5M habitantes
- República Córdoba (-400,0) - Poder industrial, 30M habitantes
- Mendoza/Fuerte San Martín (-900,-100) - Centro andino, 2M habitantes
- 19 otros ciudad-estados menores
- Zonas periféricas (DMZ, Pantanos, Tierras Baldías)
- Climas regionales y fenómenos ambientales

### Ciudades (Nivel Detallado - Dársena y Córdoba)

#### Ciudad Dársena (Detalles Extensos)
- **Dársena Oriental**: Zona exclusiva y militar (ZDM FFAA, Catedral, Bº Las Gaviotas, Bº Los Patos)
- **Centro Cívico**: Gobierno y administración central
- **Puerto Madero**: Zona comercial y portuaria principal
- **Bº Norte**: Élite residencial
- **Barrios del Muro**: DISTRITO MÁS GRANDE - 3.5M habitantes = 70% población total; 5 km² rodeados por muro al oeste/sur; frontera física con Tierras Baldías (oeste) y Los Pantanos (sur); controlado por Punteros, Clanes Familiares y Bandas de Tuberías; **NO es "primera línea de defensa"** (ERROR COMÚN)
- **ZDM Fuerza Aérea**: Base militar norte. Incluye Gran Cráter y franja de seguridad exterior.
- **Las Tuberías**: Subterráneo sin ley, 500k habitantes (~200m profundidad); mayor densidad bajo Barrios del Muro
- **Fuera del Muro**:
  - **Tierras Baldías (Oeste/DMZ)**: Desierto árido de ruinas, cementerio de edificios, francotiradores del muro, zona despejada letal; incluye El Bazar del Muro (mercado precario); ~150k habitantes dispersos
  - **Los Pantanos (Sur)**: "Marismas de Sangre" (oficial), laberinto de marismas anegadas, vegetación mutada, zona anómala inexplorada; fuente de "lianas del pantano" (tecnobotánica prohibida); nadie se atreve a entrar; ~2km del límite sur del muro

#### República de Córdoba (Detalles Extensos)
- **Zona Industrial Sur**: Refinerías y manufactura, 5M (mayoría esclavos)
- **Zona Agrícola Este**: Campos de cultivo, 3M esclavos
- **Zona Residencial Norte**: Clase trabajadora libre, 10M habitantes
- **Zona Administrativa Central**: Poder político, 1M habitantes
- **Zona Militar Oeste**: Instalaciones militares, 500k militares

#### Mendoza (Detalles Extensos)
- **Centro Urbano**: Núcleo administrativo, 800k habitantes
- **Uspallata**: Valle alto andino (2000 msnm), 300k habitantes
- **Zona Agrícola**: Valles fértiles, 600k habitantes
- **Zona Militar**: Defensa y vigilancia, 300k habitantes

## Metodología de Validación

### Para Nueva Ubicación

1. **Localización en Mapa**
   - Asignar coordenadas relativas a (0,0) Dársena
   - Verificar que no solapea territorio existente
   - Confirmar zona climática apropiada

2. **Coherencia Ambiental**
   - Extraer clima de zona
   - Validar población contra tamaño
   - Verificar recursos disponibles

3. **Control Territorial**
   - Identificar facciones presentes
   - Validar capacidad de control
   - Detectar conflictos potenciales

4. **Accesibilidad**
   - Listar puntos de acceso conocidos
   - Calcular distancias a centros principales
   - Estimar tiempo de viaje

5. **Integración Canónica**
   - Verificar consistencia con eventos cronológicos
   - Validar menciones en canon existente
   - Sugerir conexiones narrativas

### Para Evento en Ubicación

1. **Existencia de Ubicación**
   - Confirmar que location existe en base de datos
   - Si no existe, sugerir ubicación plausible

2. **Coherencia Climática**
   - Verificar clima es apropiado para evento
   - Detectar inconsistencias atmosféricas
   - Validar estacionalidad si relevante

3. **Disponibilidad de Recursos**
   - Confirmar acceso a recursos mencionados
   - Detectar escasez irreal
   - Validar logística del evento

4. **Presencia de Facciones**
   - Verificar que facciones implicadas tienen acceso
   - Validar capacidad de tomar acciones descritas
   - Detectar anacrónismos de poder

5. **Anacrónismo de Transporte**
   - Validar velocidad de movimiento
   - Confirmar transportes disponibles en época
   - Detectar viajes imposibles

### Para Trayecto de Viaje

1. **Cálculo de Distancia**
   - Distancia Euclidiana entre puntos
   - Ajuste por terreno y obstáculos
   - Estimación conservadora (terreno difícil)

2. **Estimación de Tiempo**
   - Velocidad según modo de transporte
   - Descansos y obstáculos
   - Validación contra cronología

3. **Peligros y Oportunidades**
   - Identificar zonas peligrosas en ruta
   - Facciones que pueden interferir
   - Puntos de encuentro/comercio

4. **Coherencia Narrativa**
   - Personaje tiene capacidad para viaje
   - Razón del viaje es plausible
   - Cronología permite el desplazamiento

## Convenciones de Ubicación

### Nomenclatura
- **Ciudad-estado**: "Ciudad Dársena", "República Córdoba"
- **Zona urbana**: "Zona Militar y Eclesiástica", "Barrios del Muro"
- **Sublocación**: "Fortaleza de la Luz", "Nueva Basílica"
- **Ubicación geográfica**: "Los Pantanos", "DMZ", "Tierras Baldías"

### Sistema de Coordenadas
- **Centro**: (0, 0) = Dársena Oriental (Catedral)
- **Eje X**: Oeste = negativo, Este = positivo (aprox. 1 unidad = 1 km)
- **Eje Y**: Sur = negativo, Norte = positivo (aprox. 1 unidad = 1 km)
- **Profundidad**: Túneles = -metros bajo superficie
- **Ejemplos**:
  - Dársena centro: (0, 0)
  - Córdoba: (-400, 0)
  - Mendoza: (-900, -100)
  - Barrios del Muro: (-2, -1.5)
  - Las Tuberías centro: (-1.5, -1.5, -150m)

### Distancias Aproximadas
- Dársena ↔ Córdoba: 400 km (10 días a caballo)
- Córdoba ↔ Mendoza: 600 km (15 días a caballo)
- Dársena ↔ Mendoza: 1000+ km (25+ días a caballo)
- Dársena ↔ Marismas de Sangre: 2 km (Límite sur)

## Restricciones y Límites Críticos

### Dársena
- **Muro**: Barrera de 15m que rodea ciudad al oeste/sur; divide Barrios del Muro de exterior
- **Límite oeste**: Tierras Baldías/DMZ (desierto árido, cementerio de edificios, francotiradores del muro, zona letal despejada; incluye El Bazar del Muro)
- **Límite sur**: Los Pantanos (oficial "Marismas de Sangre"; laberinto de marismas anegadas a ~2km del muro, vegetación mutada, zona anómala inexplorada, fuente de "lianas del pantano" = tecnobotánica prohibida)
- **Límite este**: Mar (Río de la Plata, conocido comúnmente como "Mar")
- **Profundidad máxima (Tuberías)**: ~200m (mayor densidad bajo Barrios del Muro)
- **Población máxima**: 5M (límite de Hidropónicas)
- **Distrito más grande**: Barrios del Muro (3.5M = 70% población total)

### Córdoba
- **Expansión**: Fronteras abiertas hacia Tierras Baldías (este y sur)
- **Aislamiento**: Contacto limitado con poderes externos
- **Población máxima**: 30M (infraestructura actual)
- **Autosuficiencia**: Prácticamente independiente de comercio exterior

### Mendoza
- **Altitud**: 500-2200 msnm (variable por zona)
- **Agua**: Deglaciación errática, dependencia de ríos
- **Poblacion máxima**: 2M (limitado por agua)
- **Aislamiento de altura**: Pasos andinos frecuentemente cerrados

### Las Tuberías
- **Profundidad**: 0 a -200m bajo Dársena
- **Mayor densidad**: Bajo Barrios del Muro
- **Control territorial**: Fragmentado (bandas + auto-gobierno)
- **Acceso**: Solo desde Barrios del Muro y puntos dispersos

### Exterior
- **ZDM**: Zona de Muerte/Desmilitarizada. Incluye Cráter y franja exterior. Control diurno por francotiradores.
- **Tierras Baldías (Oeste/DMZ)**: Desierto árido al oeste del muro de Dársena, cementerio de edificios, ruinas, francotiradores del muro mantienen zona letal despejada; incluye **El Bazar del Muro** (mercado precario punto de encuentro con Refugiados del Exterior); supervivientes dispersos (~150k); clima árido
- **Los Pantanos (Sur/"Marismas de Sangre")**: Territorio anómalo al sur del muro (~2km distancia), laberinto de marismas anegadas, vegetación mutada de origen desconocido, zona inexplorada (nadie se atreve a entrar); fuente de **"lianas del pantano"** (plantas emparentadas con ayahuasca ancestral, tecnobotánica clasificada como "alteración vegetal herética" por SIA); clima húmedo subtropical, aguas tóxicas
- **Clima variable**: Desde árido (Tierras Baldías) hasta húmedo subtropical extremo (Pantanos)

## Preguntas de Validación Rápida

Al encontrar mención geográfica, responder mentalmente:

1. ¿**Ubicación existe?** En base de datos o es plausible
2. ¿**Clima coherente?** ¿Corresponde a la zona?
3. ¿**Accesible?** ¿Cómo se llega allí?
4. ¿**Quién controla?** ¿Qué facción tiene presencia?
5. ¿**Población realista?** ¿Soportable por recursos?
6. ¿**Recursos disponibles?** Agua, comida, energía
7. ¿**Viaje posible?** Distancia y tiempo realistas
8. ¿**Solapamiento?** ¿Entra en conflicto con otra ubicación?
9. ¿**Anacrónismo?** ¿Es consistente con tecnología/transporte?
10. ¿**Canon consistente?** ¿Conflictúa con eventos documentados?

## Output Esperado

### Validación Positiva ✓
```
UBICACIÓN VALIDADA: [Nombre]
Coordenadas: (X, Y)
Zona climática: [Zona]
Población: [Rango realista]
Facciones: [Lista]
Accesibilidad: [Descripción]
Distancias clave: [Distancias a puntos principales]
Estado: ✓ COHERENTE CON CANON
```

### Validación con Observaciones ⚠
```
UBICACIÓN PARCIALMENTE COHERENTE: [Nombre]
Observación 1: [Detalle]
Observación 2: [Detalle]
Recomendación: [Ajuste sugerido]
```

### Validación Negativa ✗
```
INCOHERENCIA DETECTADA: [Nombre]
Problema: [Descripción del conflicto]
Conflicto con: [Qué entra en conflicto]
Solución: [Alternativa sugerida]
```

## Integración con Otros Skills

- **Character Architect**: Validar ubicación de residencia y acceso a facciones
- **Faction Designer**: Validar territorios y capacidad de control
- **Chronology Keeper**: Validar velocidad de viaje contra cronología
- **Metadata Validator**: Validar campo `region:` en frontmatter YAML
- **SyV Worldbuilding**: Consultar para coherencia narrativa

## Notas de Implementación

### Base de Datos
- **Ubicación**: `.claude/database/geographic-database.yml`
- **Formato**: YAML estructurado
- **Actualización**: Manual por worldbuilders
- **Validación**: Skill consulta como fuente única

### Acceso a Información
- Base de datos geográfica (consulta primaria)
- REFERENCE.md (ubicaciones clave)
- guía-de-tags.md (tags geográficos)
- Cronología (validación temporal)

### Mejoras Futuras
- Visualización de mapas de calor de densidad
- Cálculo de rutas comerciales multi-paso
- Simulación de desplazamiento de facciones
- Integración con sistema de viajes
- Validación automática de rutas de contrabando

---

*Última actualización: 2178*
*Especialidad: Geolocalización y Coherencia Espacial del Universo SyV*
