---
name: querying-influxdb-18
description: Ejecuta consultas de lectura (queries) en InfluxDB 1.8 mediante la API HTTP usando curl. Permite verificar datos, detectar errores, crear resúmenes estadísticos y analizar valores en bases de datos de series temporales. Usa exclusivamente operaciones SELECT y SHOW en InfluxQL. Configura IP y puerto de forma flexible. No requiere autenticación.
---

# Consultas InfluxDB 1.8

Este skill permite ejecutar consultas de lectura en InfluxDB versión 1.8 usando la API HTTP mediante curl.  **Solo operaciones de lectura - sin escritura.**

## Configuración básica

La instancia de InfluxDB se accede mediante:
- **URL base**: `http://IP:PUERTO` (configurable)
- **Puerto por defecto**: 8086
- **Endpoint**: `/query`
- **Autenticación**: No requerida en esta configuración

## Estructura de comandos curl

Todas las consultas usan este formato base:
```bash
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=CONSULTA_INFLUXQL"
```


**Elementos clave:**
- `-G` especifica método GET
- `--data-urlencode` codifica correctamente la query
- `db=` especifica la base de datos objetivo
- `q=` contiene la consulta InfluxQL

## Parámetros opcionales útiles

Agrega estos parámetros a la URL según necesidad:

- `pretty=true` - Formatea JSON legible (útil para debugging)
- `epoch=s` - Timestamps en segundos Unix (opciones: ns, us, ms, s, m, h)
- `chunked=true` - Transmite resultados grandes en bloques

**Ejemplo con parámetros:**
```bash
curl -G 'http://192.168.1.100:8086/query?db=mydb&pretty=true&epoch=s' \
  --data-urlencode "q=SELECT * FROM cpu LIMIT 10"
```

## Flujo de trabajo recomendado

Cuando el usuario solicite información de InfluxDB, sigue este proceso:

### 1. Obtener configuración
Pregunta al usuario por la IP, puerto y nombre de base de datos si no están especificados.

### 2. Explorar esquema
Ejecuta estos comandos para entender la estructura:
```bash
# Listar bases de datos disponibles
curl -G 'http://IP:PUERTO/query' \
  --data-urlencode "q=SHOW DATABASES"

# Listar mediciones en una DB
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SHOW MEASUREMENTS"

# Ver campos y tipos de una medición
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SHOW FIELD KEYS FROM nombre_medicion"

# Ver tags disponibles
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SHOW TAG KEYS FROM nombre_medicion"
```

### 3. Consultar datos
Una vez comprendido el esquema, ejecuta las consultas apropiadas.

## Consultas comunes por caso de uso

### Verificación de datos

**Contar puntos totales:**
```bash
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SELECT COUNT(*) FROM medicion"
```

**Ver datos más recientes:**
```bash
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SELECT * FROM medicion ORDER BY time DESC LIMIT 10"
```

**Verificar rango temporal de datos:**
```bash
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SELECT FIRST(*), LAST(*) FROM medicion"
```

### Detección de errores y gaps

**Detectar intervalos sin datos (usar fill(0) para identificar gaps):**
```bash
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SELECT COUNT(campo) FROM medicion WHERE time > now() - 24h GROUP BY time(5m) fill(0)"
```

Los intervalos con COUNT=0 indican ausencia de datos.

**Identificar valores fuera de rango:**
```bash
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SELECT * FROM medicion WHERE campo > 100 AND time > now() - 1h"
```

### Resúmenes estadísticos

**Resumen completo de un campo:**
```bash
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SELECT COUNT(valor) AS puntos, MEAN(valor) AS promedio, MEDIAN(valor) AS mediana, STDDEV(valor) AS desviacion, MIN(valor) AS minimo, MAX(valor) AS maximo FROM medicion WHERE time > now() - 24h"
```

**Promedios por hora:**
```bash
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SELECT MEAN(valor) FROM medicion WHERE time > now() - 7d GROUP BY time(1h)"
```

**Máximos y mínimos diarios:**
```bash
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SELECT MIN(temp), MAX(temp) FROM sensores WHERE time > now() - 30d GROUP BY time(1d)"
```


### Análisis de valores

**Valores por encima/debajo de umbral:**
```bash
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SELECT * FROM medicion WHERE valor > 80 AND time > now() - 1h"
```

**Distribución por tags:**
```bash
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SELECT MEAN(valor) FROM medicion WHERE time > now() - 24h GROUP BY ubicacion"
```

**Tendencias temporales con múltiples métricas:**
```bash
curl -G 'http://IP:PUERTO/query?db=NOMBRE_DB' \
  --data-urlencode "q=SELECT MEAN(valor) AS promedio, MIN(valor) AS min, MAX(valor) AS max FROM medicion WHERE time > now() - 24h GROUP BY time(1h), region"
```

## Sintaxis InfluxQL esencial

### Filtros temporales

**Formato absoluto (RFC3339):**
```sql
WHERE time >= '2024-01-01T00:00:00Z' AND time < '2024-01-02T00:00:00Z'
```

**Formato relativo (recomendado):**
```sql
WHERE time > now() - 1h   -- última hora
WHERE time > now() - 24h  -- últimas 24 horas
WHERE time > now() - 7d   -- últimos 7 días
```

**Unidades de tiempo:**
- `ns` nanosegundos
- `us` o `µ` microsegundos
- `ms` milisegundos
- `s` segundos
- `m` minutos
- `h` horas
- `d` días
- `w` semanas

### Funciones de agregación

- `COUNT(campo)` - cuenta puntos no nulos
- `MEAN(campo)` - promedio aritmético
- `SUM(campo)` - suma total
- `MIN(campo)` - valor mínimo
- `MAX(campo)` - valor máximo
- `MEDIAN(campo)` - mediana
- `STDDEV(campo)` - desviación estándar
- `SPREAD(campo)` - rango (max - min)

### GROUP BY time()

Agrupa datos en intervalos temporales:
```sql
GROUP BY time(5m)   -- intervalos de 5 minutos
GROUP BY time(1h)   -- intervalos de 1 hora
GROUP BY time(1d)   -- intervalos de 1 día
```


**Con fill() para manejar gaps:**
```sql
GROUP BY time(10m) fill(0)        -- llenar con 0
GROUP BY time(10m) fill(previous) -- usar valor anterior
GROUP BY time(10m) fill(linear)   -- interpolación lineal
GROUP BY time(10m) fill(none)     -- omitir intervalos vacíos
```

### Reglas de sintaxis importantes

1. **Identificadores** (nombres de mediciones, campos, tags con caracteres especiales o palabras reservadas) van entre **comillas dobles**: `"measurement_name"`, `"field-with-dash"`

2. **Valores de strings y tags** van entre **comillas simples**: `WHERE location = 'us-west'`

3. **El SELECT debe incluir al menos un campo** (no puede ser solo tags)

4. **ORDER BY solo acepta `time`**: `ORDER BY time DESC`

## Formato de respuesta JSON

Las respuestas siguen esta estructura:
```json
{
  "results": [
    {
      "statement_id": 0,
      "series": [
        {
          "name": "nombre_medicion",
          "columns": ["time", "campo1", "tag1"],
          "values": [
            ["2024-01-01T00:00:00Z", 45.2, "valor_tag"],
            ["2024-01-01T00:01:00Z", 46.1, "valor_tag"]
          ]
        }
      ]
    }
  ]
}
```


**En caso de error:**
```json
{
  "results": [
    {
      "statement_id": 0,
      "error": "database not found: mydb"
    }
  ]
}
```


## Códigos HTTP de respuesta

- **200 OK** - Consulta ejecutada (revisar JSON para errores específicos)
- **400 Bad Request** - Sintaxis de query inválida
- **404 Not Found** - Base de datos no existe
- **500 Internal Server Error** - Error del servidor

**Importante:** Un código 200 no garantiza éxito - siempre verifica el campo `error` en la respuesta JSON.

## Mejores prácticas

### Optimización de performance
1. **Siempre especifica rangos temporales** - evita `SELECT * FROM measurement` sin WHERE
2. **Usa LIMIT para exploración** - `LIMIT 100` al investigar datos nuevos
3. **Selecciona campos específicos** - evita `SELECT *` cuando solo necesitas algunos campos
4. **Usa agregaciones** con GROUP BY time() en lugar de puntos individuales para visualización

### Manejo de errores
1. **Verifica existencia de DB primero** con `SHOW DATABASES`
2. **Explora esquema antes de consultar** con SHOW MEASUREMENTS, SHOW FIELD KEYS
3. **Valida respuestas** - chequea tanto código HTTP como campo `error` en JSON
4. **Usa pretty=true durante desarrollo** para debugging más fácil

### Codificación de URLs
1. **Siempre usa `--data-urlencode`** - maneja automáticamente caracteres especiales
2. **Escapa comillas en shell** cuando sea necesario
3. **Para queries complejas** considera guardarlas en archivos y usar `@archivo.txt`

## Ejemplo completo de workflow
```bash
# 1. Verificar que InfluxDB responde
curl -I 'http://192.168.1.100:8086/ping'

# 2. Listar bases de datos
curl -G 'http://192.168.1.100:8086/query?pretty=true' \
  --data-urlencode "q=SHOW DATABASES"

# 3. Ver mediciones disponibles
curl -G 'http://192.168.1.100:8086/query?db=telegraf&pretty=true' \
  --data-urlencode "q=SHOW MEASUREMENTS"

# 4. Inspeccionar estructura de una medición
curl -G 'http://192.168.1.100:8086/query?db=telegraf' \
  --data-urlencode "q=SHOW FIELD KEYS FROM cpu"

curl -G 'http://192.168.1.100:8086/query?db=telegraf' \
  --data-urlencode "q=SHOW TAG KEYS FROM cpu"

# 5. Obtener muestra de datos
curl -G 'http://192.168.1.100:8086/query?db=telegraf&pretty=true' \
  --data-urlencode "q=SELECT * FROM cpu LIMIT 5"

# 6. Análisis estadístico
curl -G 'http://192.168.1.100:8086/query?db=telegraf&epoch=s' \
  --data-urlencode "q=SELECT COUNT(usage_idle), MEAN(usage_idle), MIN(usage_idle), MAX(usage_idle) FROM cpu WHERE time > now() - 1h"

# 7. Detectar gaps (fill(0) muestra intervalos sin datos)
curl -G 'http://192.168.1.100:8086/query?db=telegraf' \
  --data-urlencode "q=SELECT COUNT(usage_idle) FROM cpu WHERE time > now() - 1h GROUP BY time(1m) fill(0)"
```

## Limitaciones y consideraciones

### Versión específica
- **Este skill es SOLO para InfluxDB 1.8** (no compatible con 2.x)
- InfluxDB 2.x usa API y sintaxis diferentes (Flux en lugar de InfluxQL)

### Operaciones permitidas
- ✅ SELECT queries (lectura de datos)
- ✅ SHOW commands (exploración de esquema)
- ❌ INSERT/WRITE (escritura de datos)
- ❌ CREATE/DROP (administración de schema)
- ❌ DELETE (eliminación de datos)

### Precisión temporal
- Timestamps se almacenan en UTC
- Precisión por defecto: nanosegundos
- Usa parámetro `epoch` para otras precisiones

### Tipos de datos
- **Funciones numéricas** (MEAN, SUM, etc.): solo int64 y float64
- **COUNT**: funciona con todos los tipos
- Los campos pueden tener diferentes tipos entre shards (evitar)

## Troubleshooting común

**Error: "database not found"**
- Verifica nombre exacto con `SHOW DATABASES`
- Nombres son case-sensitive

**Error: "error parsing query"**
- Revisa sintaxis InfluxQL
- Verifica comillas: dobles para identificadores, simples para valores
- Usa `--data-urlencode` para codificación correcta

**Respuesta vacía con 200 OK**
- Verifica que existan datos en el rango temporal
- Comprueba filtros WHERE (tags, valores)
- Usa `SELECT COUNT(*)` para verificar existencia de datos

**Query muy lenta**
- Reduce rango temporal con WHERE time
- Usa agregaciones con GROUP BY time() en lugar de puntos individuales
- Considera usar LIMIT

## Referencias adicionales

Para referencia técnica completa de InfluxQL, consulta [REFERENCE.md](REFERENCE.md) en esta carpeta (si existe).

**Documentación oficial InfluxDB 1.8:**
- API HTTP: https://docs.influxdata.com/influxdb/v1.8/tools/api/
- InfluxQL: https://docs.influxdata.com/influxdb/v1.8/query_language/

---

**Versión del skill**: 1.0
**Compatible con**: InfluxDB OSS 1.8.x
**Última actualización**: Basado en documentación InfluxDB 1.8
