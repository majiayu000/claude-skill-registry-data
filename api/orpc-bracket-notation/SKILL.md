---
name: oRPC Bracket Notation
description: Represent structured data in limited formats such as URL queries and form data.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Bracket Notation

Bracket Notation encodes structured data in formats with limited syntax, like URL queries and form data. It is used by [OpenAPIHandler](/docs/openapi/openapi-handler) and [OpenAPILink](/docs/openapi/client/openapi-link).

## Usage

1. **Same name (>=2 elements) are represented as an array.**

   ```
   color=red&color=blue → { color: ["red", "blue"] }
   ```

2. **Append `[]` at the end to denote an array.**

   ```
   color[]=red&color[]=blue → { color: ["red", "blue"] }
   ```

3. **Append `[number]` to specify an array index (missing indexes create sparse arrays).**

   ```
   color[0]=red&color[2]=blue → { color: ["red", <empty>, "blue"] }
   ```

   > Array indexes must be less than 10,000 by default to prevent memory exhaustion. Configure with `maxBracketNotationArrayIndex`.

4. **Append `[key]` to denote an object property.**

   ```
   color[red]=true&color[blue]=false → { color: { red: true, blue: false } }
   ```

## Limitations

* **Empty Arrays:** Cannot be represented; arrays must have at least one element.
* **Empty Objects:** Cannot be represented. Objects with empty or numeric keys may be interpreted as arrays.

## Examples

### URL Query

```bash
curl http://example.com/api/example?name[first]=John&name[last]=Doe
```

Parsed as:

```json
{ "name": { "first": "John", "last": "Doe" } }
```

### Form Data

```bash
curl -X POST http://example.com/api/example \
  -F 'name[first]=John' \
  -F 'name[last]=Doe'
```

### Complex Example

```bash
curl -X POST http://example.com/api/example \
  -F 'data[names][0][first]=John1' \
  -F 'data[names][0][last]=Doe1' \
  -F 'data[ages][0]=18' \
  -F 'data[ages][2]=25' \
  -F 'data[files][]=@/path/to/file1'
```

Parsed as:

```json
{
  "data": {
    "names": [{ "first": "John1", "last": "Doe1" }],
    "ages": ["18", "<empty>", "25"],
    "files": ["<binary data>"]
  }
}
```
