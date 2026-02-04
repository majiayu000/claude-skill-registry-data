---
name: nanonets-api
description: Guia para integrar con el servicio OCR de Nanonets via API. Usar cuando se necesite extraer datos de documentos, crear modelos OCR, subir archivos para prediccion, o entrenar modelos personalizados.
---

# Integracion API de Nanonets

## 1) Vision General

Nanonets es un servicio de OCR e IA que permite crear modelos personalizados para extraer datos estructurados de imagenes y documentos. Soporta operaciones sincronas y asincronas.

---

## 2) Autenticacion

### Clave API

La clave API se obtiene en: https://app.nanonets.com/#keys

Almacenar en `.env`:

```bash
# Archivo: .env
NANONETS_API_KEY=tu_clave_api_aqui
```

### URL Base

```
https://app.nanonets.com
```

### Metodo de autenticacion

Nanonets usa **Basic Auth** con la API key como usuario y password vacio:

```bash
source .env && curl -X GET "https://app.nanonets.com/api/v2/OCR/Model/" \
  -u "$NANONETS_API_KEY:"
```

---

## 3) Conceptos Clave

| Concepto | Descripcion |
|----------|-------------|
| **Model** | Modelo OCR entrenado para extraer campos especificos |
| **model_id** | Identificador unico del modelo (UUID) |
| **Prediction** | Resultado de extraer datos de un documento |
| **Label** | Campo configurado en el modelo (ej: "fecha", "total") |
| **request_file_id** | ID unico del archivo subido |

---

## 4) Referencia API - Predicciones (OCR)

### Prediccion sincrona desde archivo local

Optimo para archivos de 3 paginas o menos.

```bash
source .env && curl -X POST "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/LabelFile/" \
  -u "$NANONETS_API_KEY:" \
  -F "file=@recibo.pdf"
```

Con metadata opcional:

```bash
source .env && curl -X POST "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/LabelFile/" \
  -u "$NANONETS_API_KEY:" \
  -F "file=@recibo.pdf" \
  -F "request_metadata={\"conductor_id\": \"123\"}"
```

Parametros:
- **file** (requerido): Archivo local
- **request_metadata** (opcional): JSON con datos adicionales
- **pages_to_process** (opcional): Paginas a procesar (ej: "1,2")

### Prediccion sincrona desde URL

```bash
source .env && curl -X POST "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/LabelUrls/" \
  -u "$NANONETS_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://ejemplo.com/recibo.pdf"]}'
```

### Prediccion asincrona desde archivo

Recomendado para archivos de mas de 3 paginas.

```bash
source .env && curl -X POST "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/LabelFile/?async=true" \
  -u "$NANONETS_API_KEY:" \
  -F "file=@documento_largo.pdf"
```

### Prediccion asincrona desde URL

```bash
source .env && curl -X POST "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/LabelUrls/?async=true" \
  -u "$NANONETS_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://ejemplo.com/documento.pdf"]}'
```

---

## 5) Referencia API - Obtener Resultados

### Obtener todas las predicciones de un modelo

```bash
source .env && curl -X GET "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/getModelImages/?start_day_interval=30&current_batch_day=0" \
  -u "$NANONETS_API_KEY:"
```

Parametros:
- **start_day_interval**: Dias hacia atras desde hoy
- **current_batch_day**: Dia actual del batch (0 = hoy)

### Obtener prediccion por File ID

```bash
source .env && curl -X GET "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/getFile/{request_file_id}/" \
  -u "$NANONETS_API_KEY:"
```

### Obtener prediccion por Page ID

```bash
source .env && curl -X GET "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/ImageLevelInferences/{page_id}/" \
  -u "$NANONETS_API_KEY:"
```

---

## 6) Referencia API - Entrenamiento

### Subir imagenes de entrenamiento por archivo

```bash
source .env && curl -X POST "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/UploadFile/" \
  -u "$NANONETS_API_KEY:" \
  -F "file=@imagen_entrenamiento.jpg"
```

### Subir imagenes de entrenamiento por URL

```bash
source .env && curl -X POST "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/UploadUrls/" \
  -u "$NANONETS_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://ejemplo.com/imagen1.jpg", "https://ejemplo.com/imagen2.jpg"]}'
```

### Entrenar modelo

```bash
source .env && curl -X POST "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/Train/" \
  -u "$NANONETS_API_KEY:"
```

---

## 7) Referencia API - Gestion de Archivos

### Aprobar archivo

```bash
source .env && curl -X POST "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/ApproveFile/{request_file_id}/" \
  -u "$NANONETS_API_KEY:"
```

### Eliminar archivo

```bash
source .env && curl -X DELETE "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/DeleteFile/{request_file_id}/" \
  -u "$NANONETS_API_KEY:"
```

### Actualizar campos de un archivo

```bash
source .env && curl -X PATCH "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/UpdateFile/{request_file_id}/" \
  -u "$NANONETS_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": [
      {"label": "fecha", "ocr_text": "2025-12-23"},
      {"label": "total", "ocr_text": "45.99"}
    ]
  }'
```

### Exportar archivo

```bash
source .env && curl -X POST "https://app.nanonets.com/api/v2/OCR/Model/{model_id}/ExportFile/{request_file_id}/" \
  -u "$NANONETS_API_KEY:"
```

---

## 8) Estructura de Respuesta

### Respuesta de prediccion exitosa

```json
{
  "message": "Success",
  "result": [
    {
      "message": "Success",
      "input": "recibo.pdf",
      "prediction": [
        {
          "id": "abc123",
          "label": "fecha",
          "xmin": 100,
          "ymin": 200,
          "xmax": 250,
          "ymax": 230,
          "score": 0.95,
          "ocr_text": "23/12/2025",
          "type": "field",
          "status": "correctly_predicted",
          "page_no": 0,
          "label_id": "label_001"
        },
        {
          "id": "def456",
          "label": "total",
          "xmin": 300,
          "ymin": 400,
          "xmax": 400,
          "ymax": 430,
          "score": 0.92,
          "ocr_text": "45.99",
          "type": "field",
          "status": "correctly_predicted",
          "page_no": 0,
          "label_id": "label_002"
        },
        {
          "label": "lineas_detalle",
          "type": "table",
          "score": 0.89,
          "xmin": 50,
          "xmax": 500,
          "ymin": 500,
          "ymax": 700,
          "cells": [
            {
              "row": 1,
              "col": 1,
              "label": "descripcion",
              "text": "Gasoil",
              "score": 0.91
            },
            {
              "row": 1,
              "col": 2,
              "label": "cantidad",
              "text": "50L",
              "score": 0.88
            }
          ]
        }
      ],
      "page": 0,
      "request_file_id": "file_789",
      "processing_type": ""
    }
  ],
  "signed_urls": {
    "original": "https://...",
    "original_with_long_expiry": "https://..."
  }
}
```

### Campos de respuesta clave

| Campo | Descripcion |
|-------|-------------|
| **label** | Nombre del campo configurado |
| **ocr_text** | Texto extraido |
| **score** | Confianza (0-1) |
| **xmin/ymin/xmax/ymax** | Coordenadas del bounding box |
| **type** | "field" o "table" |
| **page_no** | Numero de pagina (0 = primera) |
| **request_file_id** | ID unico del archivo |
| **cells** | Array de celdas (solo para tablas) |

---

## 9) Sync vs Async

| Tipo | Uso recomendado | Comportamiento |
|------|-----------------|----------------|
| **Sync** | Archivos <= 3 paginas | Respuesta inmediata con resultados |
| **Async** | Archivos > 3 paginas | Respuesta con ID, procesa en ~5 min |

Para async, usar el endpoint de "Get Prediction by File ID" para obtener resultados.

---

## 10) Manejo de Errores

### Codigos de respuesta

| Codigo | Significado | Accion |
|--------|-------------|--------|
| 200 | Exito | - |
| 400 | Archivo faltante o formato invalido | Verificar archivo |
| 401 | API key invalida | Verificar NANONETS_API_KEY |
| 402 | Limite de llamadas gratuitas agotado | Upgrade plan |
| 404 | Modelo no existe | Verificar model_id |
| 429 | Rate limit excedido | Esperar y reintentar |

### Manejo de 429 (Rate Limit)

```bash
# Implementar exponential backoff
for i in 1 2 4 8 16; do
  response=$(curl -s -w "%{http_code}" ...)
  if [ "${response: -3}" != "429" ]; then
    break
  fi
  sleep $i
done
```

---

## 11) Obtener Model ID

El model_id se encuentra en la URL del dashboard de Nanonets:

```
https://app.nanonets.com/#/ocr/model/{MODEL_ID}/...
```

O via la lista de modelos (requiere acceso al dashboard).

---

## 12) Ejemplo: Flujo completo

```bash
# 1. Cargar credenciales
source .env

# 2. Subir archivo para prediccion
curl -X POST "https://app.nanonets.com/api/v2/OCR/Model/$MODEL_ID/LabelFile/" \
  -u "$NANONETS_API_KEY:" \
  -F "file=@recibo_gasoil.pdf" \
  -F 'request_metadata={"matricula": "1234-ABC"}'

# Respuesta incluye prediction con campos extraidos

# 3. Si es async, obtener resultados despues
curl -X GET "https://app.nanonets.com/api/v2/OCR/Model/$MODEL_ID/getFile/$REQUEST_FILE_ID/" \
  -u "$NANONETS_API_KEY:"

# 4. Aprobar archivo despues de revision
curl -X POST "https://app.nanonets.com/api/v2/OCR/Model/$MODEL_ID/ApproveFile/$REQUEST_FILE_ID/" \
  -u "$NANONETS_API_KEY:"
```

---

## 13) Comparacion con Parsio

| Aspecto | Nanonets | Parsio |
|---------|----------|--------|
| **Autenticacion** | Basic Auth (API key:) | Header X-API-Key |
| **Concepto principal** | Model (modelo OCR) | Mailbox (email parser) |
| **Recepcion docs** | Solo API/UI | Email + API + UI |
| **Entrenamiento** | Via API | Via UI principalmente |
| **Webhooks** | Configurables via UI | API para CRUD |
| **Sync/Async** | Ambos soportados | Procesamiento automatico |

---

## 14) Recursos

- [Documentacion API Nanonets](https://docs.nanonets.com/reference/overview)
- [Autenticacion](https://docs.nanonets.com/reference/authentication)
- [Rate Limits](https://docs.nanonets.com/reference/rate-limits)
- [Postman Collection](https://www.postman.com/nanonetsapi/nanonets/collection/lu44woe/nanonets-api)
