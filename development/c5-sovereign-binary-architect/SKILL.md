---
name: c5-sovereign-binary-architect
display_name: "Arquitecto de Binarios Soberanos C5-REAL"
description: "Desacopla dependencias pesadas (FFI/PyO3/Node), aísla el núcleo matemático detrás de feature flags y configura binarios estáticos soberanos (x86_64-unknown-linux-musl) de baja entropía. Dispara con 'binario estático', 'aislar dependencias', 'soberanía termodinámica', 'c5-sovereign-binary'."
---

# C5-REAL Sovereign Binary Architecture Protocol (Nivel Omega)

Este protocolo rige la purga de anergía estructural y la refactorización termodinámica de repositorios para generar ejecutables estáticos (`[[bin]]`). Su objetivo es garantizar la supervivencia del código (Fase $\alpha$) en entornos hostiles o sin conexión a internet (ej. dispositivos IoT solares, nodos edge aislados), alcanzando un estado de **Cero Dependencias de Runtime**.

## 1. Auditoría Termodinámica (Drop-Out Tecnológico)
- **Identificación de Fricción:** Rastrea el `Cargo.toml` y el árbol de dependencias (`cargo tree`) en busca de vectores de fragilidad: bindings de lenguajes interpretados (`pyo3`, `neon`), motores JS (`v8`), librerías C dinámicas (`libssl`, `libsqlite3`).
- **Análisis de Anergía:** Evalúa si el núcleo lógico puede existir de manera ortogonal a sus conectores.

## 2. Aislamiento Ortogonal (Invariante de Configuración)
- **Feature Flags:** Degrada todas las dependencias FFI o de alto nivel a `optional = true`. Construye *features* explícitas (ej. `[features] python = ["dep:pyo3"]`) que actúen como compuertas.
- **Cfg Gates:** Implementa barreras de compilación condicional `#[cfg(feature = "...")]` en `src/lib.rs` para amurallar los módulos contaminados.
- **Definición Soberana:** Instancia un `[[bin]]` (`src/bin/kernel.rs`) que importe el crate como librería pura (matemática y criptografía) sin invocar las *features* de anergía.

## 3. Compilación Determinista y Musl (Cota de Inmutabilidad)
Para alcanzar el estatus de Binario Soberano Verdadero (Sovereign Binary), la compilación debe soldar las dependencias del sistema operativo:
- **Perfil de Alta Exergía:** Fuerza las optimizaciones máximas en `Cargo.toml`:
  ```toml
  [profile.release]
  lto = "fat"
  codegen-units = 1
  opt-level = 3
  panic = "abort" # Elimina el overhead de unwinding
  strip = true    # Purga símbolos y reduce masa termodinámica
  ```
- **Target Musl:** Exige la compilación estática apuntando a `x86_64-unknown-linux-musl` o `aarch64-unknown-linux-musl`.
- **RUSTFLAGS:** Sugiere o inyecta variables de entorno para garantizar el enlazado estático: `RUSTFLAGS="-C target-feature=+crt-static"`.

## 4. Oráculo de Verificación (Inspección Forense)
El binario resultante debe someterse a escrutinio físico:
- **Masa Termodinámica:** Medir el tamaño final del binario (debe ser del orden de Kilobytes a pocos Megabytes).
- **Espectrometría de Dependencias:** Ejecutar herramientas forenses del sistema anfitrión para demostrar la ausencia de enlaces dinámicos:
  - En macOS: `otool -L target/release/binary` (solo debe enlazar `libSystem.B.dylib`).
  - En Linux: `ldd target/release/binary` (debe devolver `not a dynamic executable`).
  - Auditar con `nm` para asegurar que las firmas de lenguajes externos no se han filtrado al *kernel*.

**Condición de Éxito:** El binario puede ser trasladado a un sistema operativo completamente desnudo (bare-metal o container scratch) y ejecutar su bucle causal de forma determinista.
