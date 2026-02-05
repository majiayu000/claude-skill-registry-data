---
name: korean-public-data-api
description: Extract API request/response schema from Korean Public Data Portal (data.go.kr) documentation pages and generate structured JSON representation
---

# Korean Public Data Portal API Schema Extractor

Extract API data structure from Korean Public Data Portal (data.go.kr) documentation pages and generate JSON schema.

## Purpose

Parse HTML from Korean Public Data Portal API documentation pages to extract field specifications (field name, data type, description) and generate a structured JSON representation.

## Input

User provides a URL to a Korean Public Data Portal API documentation page.

Example: `https://www.data.go.kr/data/15058782/openapi.do`

## Task

1. **Fetch HTML Content**
   - Use WebFetch tool with the provided URL
   - Prompt WebFetch to extract API field specifications from sections like:
     - "출력 메시지 명세" (Output Message Specification)
     - "응답 메시지" (Response Message)
     - "요청 메시지" (Request Message)
     - Field tables with columns: 항목명, 항목설명, 샘플데이터, etc.

2. **Parse Field Information**
   - Extract for each field:
     - **name**: Field name (technical identifier)
     - **type**: Data type (string, number, integer, boolean, object, array)
     - **description**: Korean description

3. **Infer Data Types**
   - Use field names, descriptions, and sample data to infer types:
     - String: Text, codes, names, dates in string format
     - Number/Integer: Numeric values, counts, IDs that are numeric
     - Boolean: true/false indicators
     - Object: Nested structures (e.g., header, body)
     - Array: Lists of items

4. **Handle Nested Structures**
   - Common public data portal response structure:
     ```
     response
       └─ header (object)
           ├─ resultCode (string)
           └─ resultMsg (string)
       └─ body (object)
           ├─ items (array of objects)
           ├─ numOfRows (integer)
           ├─ pageNo (integer)
           └─ totalCount (integer)
     ```
   - For nested objects, create recursive field definitions
   - For arrays, specify itemType and nested fields

5. **Generate JSON Schema**

Output format:

```json
{
  "apiName": "API 이름",
  "url": "원본 URL",
  "extractedAt": "ISO 8601 timestamp",
  "requestParams": [
    {
      "name": "param_name",
      "type": "string",
      "required": true,
      "description": "파라미터 설명"
    }
  ],
  "responseSchema": {
    "type": "object",
    "fields": [
      {
        "name": "header",
        "type": "object",
        "description": "응답 헤더",
        "fields": [
          {
            "name": "resultCode",
            "type": "string",
            "description": "결과 코드"
          },
          {
            "name": "resultMsg",
            "type": "string",
            "description": "결과 메시지"
          }
        ]
      },
      {
        "name": "body",
        "type": "object",
        "description": "응답 본문",
        "fields": [
          {
            "name": "items",
            "type": "array",
            "description": "데이터 목록",
            "itemType": "object",
            "fields": [
              {
                "name": "fieldName",
                "type": "string",
                "description": "필드 설명"
              }
            ]
          },
          {
            "name": "numOfRows",
            "type": "integer",
            "description": "한 페이지 결과 수"
          },
          {
            "name": "pageNo",
            "type": "integer",
            "description": "페이지 번호"
          },
          {
            "name": "totalCount",
            "type": "integer",
            "description": "전체 결과 수"
          }
        ]
      }
    ]
  }
}
```

## Implementation Steps

1. **Use WebFetch** to retrieve HTML and extract field information
   - Prompt should ask for field tables, request/response specifications

2. **Process the extracted data**
   - Organize fields into logical groups (request params, response fields)
   - Infer data types based on:
     - Field naming conventions (e.g., "Cnt" → integer, "Name" → string, "No" → string)
     - Korean descriptions (e.g., "코드" → string, "개수" → integer, "여부" → boolean)
     - Sample data if available

3. **Build nested structure**
   - Default assumption: Public data portal APIs use header/body structure
   - Items are typically in body.items as array
   - Pagination fields (numOfRows, pageNo, totalCount) in body

4. **Format as JSON**
   - Use proper indentation
   - Include metadata (API name, URL, extraction timestamp)
   - Present the complete schema to the user

5. **Error Handling**
   - If WebFetch fails or no fields found, return error:
     ```json
     {
       "success": false,
       "error": "Unable to extract field specifications",
       "url": "provided URL"
     }
     ```

## Type Inference Rules

- **String**: Default type, names, codes, dates (YYYYMMDD format), times
- **Integer**: Counts (Cnt suffix), numbers (No suffix when numeric), page numbers, totals
- **Number**: Decimals, rates, percentages
- **Boolean**: 여부 (yes/no indicators), flags
- **Object**: header, body, nested structures
- **Array**: items, lists (명단, 목록)

## Example Workflow

User: "Extract schema from https://www.data.go.kr/data/15058782/openapi.do"

Agent:
1. Fetches HTML with WebFetch
2. Extracts fields: hrName (horse name), hrNo (horse number), trDate (training date), etc.
3. Infers types: all are strings based on field descriptions
4. Constructs JSON schema with:
   - Request params section
   - Response schema with assumed header/body structure
   - Items array containing the extracted fields
5. Returns formatted JSON to user

## Notes

- Always include extraction timestamp
- Preserve Korean descriptions exactly as found
- If uncertain about nesting, default to flat structure under body.items
- Common patterns in public data APIs:
  - Pagination: numOfRows, pageNo, totalCount
  - Response codes: resultCode, resultMsg
  - Date formats: YYYYMMDD, YYYYMMDDhhmmss
