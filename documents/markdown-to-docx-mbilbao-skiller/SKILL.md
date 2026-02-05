---
name: markdown-to-docx
description: Convierte archivos Markdown a DOCX con formato profesional usando pandoc. Incluye portada con título, tabla de contenidos, cabeceras y estilos corporativos. Usar cuando se necesite generar documentos Word desde Markdown, exportar documentación, o crear informes en formato .docx.
---

# Markdown a DOCX

Convierte archivos Markdown a documentos Word (DOCX) con formato profesional.

## Características

- **Portada con título**: Genera portada automática con título, autor y fecha
- **Tabla de contenidos**: Índice automático con profundidad configurable
- **Cabecera en páginas**: Configurable en la plantilla
- **Código con fondo gris**: Bloques de código resaltados
- **Estilos profesionales**: Tipografía y formato corporativo

## Instrucciones

Para convertir un archivo Markdown a DOCX:

1. Asegúrate de que **pandoc** está instalado en el sistema
2. Usa el script `scripts/convert.sh` para la conversión
3. Especifica título y autor para generar portada

## Uso básico

```bash
# Conversión simple (con TOC por defecto)
./scripts/convert.sh archivo.md

# Con título y autor (genera portada)
./scripts/convert.sh archivo.md --title "Mi Documento" --author "Mi Nombre"

# Sin tabla de contenidos
./scripts/convert.sh archivo.md --no-toc

# Con plantilla personalizada
./scripts/convert.sh archivo.md --template mi-plantilla.docx
```

## Opciones del script

| Opción | Descripción |
|--------|-------------|
| `-o, --output` | Nombre del archivo de salida |
| `-t, --template` | Plantilla DOCX de referencia para estilos |
| `--title "TITULO"` | Título del documento (para portada) |
| `--author "AUTOR"` | Autor del documento |
| `--date "FECHA"` | Fecha del documento |
| `--toc` | Incluir tabla de contenidos (por defecto: sí) |
| `--no-toc` | No incluir tabla de contenidos |
| `--toc-depth N` | Profundidad del índice (por defecto: 2) |
| `-h, --help` | Mostrar ayuda |

## Metadatos YAML en Markdown

Puedes incluir metadatos al inicio del archivo Markdown:

```yaml
---
title: "Título del Documento"
author: "Nombre del Autor"
date: "2024-01-15"
---

# Contenido del documento...
```

## Ejemplos

### Generar documento con portada e índice

```bash
./scripts/convert.sh informe.md --title "Informe Técnico Q4" --author "Equipo Dev" -o informe_final.docx
```

### Documento sin índice

```bash
./scripts/convert.sh notas.md --no-toc --title "Notas de Reunión"
```

### Índice con 3 niveles

```bash
./scripts/convert.sh manual.md --toc-depth 3 --title "Manual de Usuario"
```

## Personalización de estilos

Para personalizar:
- Cabecera en cada página
- Código con fondo gris
- Limitar bullets a 2 niveles
- Estilos de títulos y fuentes

Consulta la guía detallada: [TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md)

### Resumen rápido

1. Abre `templates/reference.docx` en Word
2. Modifica los estilos:
   - **Source Code**: Añadir fondo gris
   - **Encabezado de página**: Añadir título
   - **Compact3+**: Quitar bullets
3. Guarda y reemplaza la plantilla

## Plantilla de referencia

La plantilla `templates/reference.docx` define:

- **Heading 1-6**: Estilos de encabezados
- **Body Text**: Texto del cuerpo
- **Source Code**: Bloques de código (fondo gris)
- **Table**: Estilos de tablas
- **Encabezado/Pie**: Cabecera y numeración

## Dependencias

- **pandoc** >= 2.0: `brew install pandoc` (macOS) o `apt install pandoc` (Linux)

## Verificar instalación de pandoc

```bash
pandoc --version
```

## Notas

- Las imágenes referenciadas en el Markdown se incrustan automáticamente
- Los enlaces se preservan como hipervínculos
- Las tablas Markdown se convierten a tablas Word
- El código se formatea con fuente monoespaciada y fondo (si la plantilla lo define)
- La tabla de contenidos se genera automáticamente con 2 niveles por defecto
