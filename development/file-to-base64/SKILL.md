---
name: file-to-base64
description: Convert files (PDF, images) to Base64 encoding with MIME type detection for API attachments. Use when you need to prepare file attachments for the FreeAgent API or any other API that requires Base64-encoded files.
---

# File to Base64 Converter

This skill converts files to Base64-encoded strings and detects their MIME types, which is essential for attaching files to FreeAgent expenses, timeslips, and other API operations that require file uploads.

## When to Use This Skill

Use this skill when:
- Preparing attachments for FreeAgent API calls (expenses, timeslips)
- Converting PDFs or images to Base64 format
- Detecting MIME types for file uploads
- Validating file formats and sizes for API requirements

## Supported File Formats

### FreeAgent Supported Formats
- PDF (`.pdf`) - `application/pdf`
- PNG (`.png`) - `image/png`
- JPEG (`.jpg`, `.jpeg`) - `image/jpeg`
- GIF (`.gif`) - `image/gif`

### Additional Common Formats (for reference)
- Text files (`.txt`) - `text/plain`
- Word documents (`.doc`, `.docx`)
- Excel files (`.xls`, `.xlsx`)

## File Size Limits

- **FreeAgent API**: Maximum 5MB per file

## How to Use

### 1. Convert a Single File

```bash
# Read the file and convert to Base64
base64 /path/to/file.pdf

# Get MIME type from extension
# For .pdf -> application/pdf
# For .png -> image/png
# For .jpg/.jpeg -> image/jpeg
# For .gif -> image/gif
```

### 2. Check File Size

```bash
# Check file size in bytes
stat -f%z /path/to/file.pdf  # macOS
stat -c%s /path/to/file.pdf  # Linux

# Convert to MB for comparison
# 5MB = 5242880 bytes
```

### 3. Validate File Before Conversion

```bash
# Check if file exists and is readable
test -r /path/to/file.pdf && echo "File is readable" || echo "Cannot read file"

# Get file extension
basename /path/to/file.pdf | sed 's/.*\.//'
```

## Example Workflow

### Prepare an Attachment for FreeAgent Expense

```bash
# 1. Validate file exists
FILE_PATH="/path/to/receipt.pdf"
test -f "$FILE_PATH" || exit 1

# 2. Check file size (must be < 5MB = 5242880 bytes)
FILE_SIZE=$(stat -f%z "$FILE_PATH")
if [ $FILE_SIZE -gt 5242880 ]; then
  echo "Error: File size exceeds 5MB limit"
  exit 1
fi

# 3. Get filename
FILE_NAME=$(basename "$FILE_PATH")

# 4. Determine MIME type from extension
EXT="${FILE_PATH##*.}"
case "$EXT" in
  pdf) MIME_TYPE="application/pdf" ;;
  png) MIME_TYPE="image/png" ;;
  jpg|jpeg) MIME_TYPE="image/jpeg" ;;
  gif) MIME_TYPE="image/gif" ;;
  *) echo "Unsupported format"; exit 1 ;;
esac

# 5. Convert to Base64
BASE64_DATA=$(base64 "$FILE_PATH")

# 6. Output in format ready for API
echo "Attachment prepared:"
echo "- file_name: $FILE_NAME"
echo "- content_type: $MIME_TYPE"
echo "- data: [Base64 string - ${#BASE64_DATA} characters]"
```

### Multiple Files

```bash
# Process multiple files
for FILE in /path/to/receipts/*.pdf; do
  if [ -f "$FILE" ]; then
    SIZE=$(stat -f%z "$FILE")
    if [ $SIZE -le 5242880 ]; then
      BASE64=$(base64 "$FILE")
      echo "File: $(basename "$FILE") - Ready"
    else
      echo "File: $(basename "$FILE") - Too large"
    fi
  fi
done
```

## MIME Type Reference

| Extension | MIME Type |
|-----------|-----------|
| .pdf | application/pdf |
| .png | image/png |
| .jpg, .jpeg | image/jpeg |
| .gif | image/gif |
| .txt | text/plain |
| .doc | application/msword |
| .docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document |
| .xls | application/vnd.ms-excel |
| .xlsx | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet |

## Error Handling

### Common Issues

1. **File not found**
   ```bash
   test -f "$FILE_PATH" || echo "Error: File does not exist"
   ```

2. **File too large**
   ```bash
   SIZE=$(stat -f%z "$FILE_PATH")
   MAX_SIZE=5242880  # 5MB
   [ $SIZE -gt $MAX_SIZE ] && echo "Error: File exceeds 5MB limit"
   ```

3. **Unsupported format**
   ```bash
   EXT="${FILE_PATH##*.}"
   case "$EXT" in
     pdf|png|jpg|jpeg|gif) echo "Supported" ;;
     *) echo "Error: Unsupported format. Use: pdf, png, jpg, jpeg, gif" ;;
   esac
   ```

4. **Permission denied**
   ```bash
   test -r "$FILE_PATH" || echo "Error: Cannot read file (check permissions)"
   ```

## Tips for Large Files

- Compress images before converting (use ImageMagick, etc.)
- For PDFs, ensure they're optimized/compressed
- Consider resizing images to reasonable dimensions
- Remove unnecessary metadata from images

## Platform Differences

### macOS vs Linux Commands

| Task | macOS | Linux |
|------|-------|-------|
| File size | `stat -f%z file` | `stat -c%s file` |
| Base64 encode | `base64 file` | `base64 file` |
| Base64 (no wrap) | `base64 file` | `base64 -w 0 file` |

## Integration with FreeAgent API

When using this skill to prepare attachments for FreeAgent:

1. Convert file to Base64 using this skill
2. Detect MIME type from extension
3. Include in API payload as:
   ```json
   {
     "attachment": {
       "data": "base64_encoded_string",
       "file_name": "receipt.pdf",
       "content_type": "application/pdf",
       "description": "Receipt for office supplies"
     }
   }
   ```

## Notes

- Base64 encoding increases file size by approximately 33%
- Ensure you have enough memory for large file conversions
- For very large batches, consider processing files in chunks
- Always validate files before attempting conversion
