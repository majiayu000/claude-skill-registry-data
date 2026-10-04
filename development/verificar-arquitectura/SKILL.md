---
name: verificar-arquitectura
description: Verifica que el código respete las reglas de Arquitectura Limpia del proyecto — que domain/ no importe framework, que los controladores no tengan lógica de negocio y que no se expongan entidades en la API. Úsala antes de abrir un Pull Request, al revisar código de otro, o cuando se agregue una clase nueva al backend.
---

# Verificar Arquitectura Limpia

Revisa el código del backend contra las reglas no negociables de AguaVigía CTG y reporta violaciones
con ubicación exacta y cómo corregirlas.

## Las reglas

### 1. `domain/` es Java puro — CERO framework

Ninguna clase bajo `backend/src/main/java/com/aguavigia/ctg/domain/` puede importar:

- `org.springframework.*`
- `com.mongodb.*` · `org.bson.*`
- `jakarta.persistence.*` · `jakarta.validation.*`
- `com.fasterxml.jackson.*`
- `lombok.*`

**Es la regla más importante del proyecto.** Si se rompe, la build falla por ArchUnit.

### 2. `application/` no conoce tecnología

Puede importar `domain.*` y anotaciones mínimas de Spring para inyección. **No** puede importar
`com.mongodb`, `org.bson`, ni clases del paquete `infrastructure`.

### 3. Los controladores no tienen lógica de negocio

Un método de `@RestController` debe: recibir un DTO → llamar **un** caso de uso → devolver un DTO.
Señales de alarma: `if` con reglas de negocio, cálculos, bucles sobre entidades, llamadas directas a
repositorios.

### 4. No se exponen entidades de dominio en la API

Ningún método de controlador devuelve ni recibe una clase de `domain.model`. Siempre DTOs.

### 5. Los objetos de valor validan en el constructor

Todo `record` en `domain/vo/` valida sus invariantes al construirse (una `Coordenada` fuera de rango
o una `VentanaTiempo` que termina antes de empezar deben lanzar excepción).

## Cómo ejecutar la verificación

1. **Busca violaciones de la regla 1** (la crítica):

   ```
   Grep: pattern="^import (org\.springframework|com\.mongodb|org\.bson|jakarta|lombok)"
         path="backend/src/main/java/com/aguavigia/ctg/domain"
         output_mode="content"
   ```

   Cualquier resultado es una violación crítica.

2. **Busca violaciones de la regla 2**:

   ```
   Grep: pattern="^import com\.aguavigia\.ctg\.infrastructure"
         path="backend/src/main/java/com/aguavigia/ctg/application"
   ```

3. **Revisa los controladores** (regla 3 y 4): lee cada archivo en `api/rest/` y verifica que los
   métodos solo deleguen.

4. **Revisa los value objects** (regla 5): lee `domain/vo/` y confirma que cada `record` valide.

5. **Si existe el test de ArchUnit**, ejecútalo:
   `./mvnw test -Dtest=ArquitecturaTest`

## Formato del reporte

Para cada violación:

- **Archivo y línea** (`ruta:línea`)
- **Regla rota** (número y nombre)
- **Por qué importa** — la consecuencia real, no la regla repetida
- **Cómo se corrige** — la acción concreta

Si no hay violaciones, dilo claramente y no inventes hallazgos menores para llenar el reporte.

## Lo que NO es tarea de esta skill

- Estilo, formato o nombres de variables
- Buscar bugs de lógica
- Sugerir refactorizaciones que no estén relacionadas con las capas
