---
name: epub-translate
description: A skill for creating bilingual EPUB books by adding translated text alongside the original content while preserving the original formatting and structure.
---

# EPUB Bilingual Translate Skill

## Overview
This skill creates bilingual EPUB files by adding translated text alongside the original content while preserving the original formatting and structure. It follows a 4-step workflow: extract, translate, update metadata, and reassemble.

## Functionality
- Extracts content from EPUB archives
- Creates bilingual text content in HTML/XHTML files by adding translations alongside original text
- Updates metadata to reflect the bilingual nature of the content
- Reassembles bilingual content into a valid EPUB archive
- Preserves original formatting, structure, and non-text content
- Unzips and parses EPUB files to identify navigation and content files
- Supports multiple target languages for bilingual output

## Workflow
1. **Extract**: Unzip the EPUB file to access its contents (HTML files, metadata, etc.)
2. **Translate**: Identify text content in HTML/XHTML files and add translations alongside original text
3. **Update Metadata**: Modify language settings in content.opf and other relevant files to reflect bilingual content
4. **Reassemble**: Zip the bilingual files back into a valid EPUB archive

## Implementation Details
- Reads EPUB as a zip archive (mimetype, META-INF/, EPUB/ folder structure)
- Parses HTML/XHTML files to extract translatable text while preserving tags
- Updates DC metadata language field in content.opf to indicate bilingual content
- Maintains the original file structure and properties during reassembly
- Validates the final EPUB file to ensure it's a properly formatted archive
- Uses `unzip -d` command to extract the EPUB file to a temporary directory
- Opens each file in the extracted EPUB folder to examine its content
- Adds translated text alongside the original text in each file
- Preserves the original text while adding translations
- Compresses the bilingual files back into an EPUB file

## Usage
1. Extract the source EPUB using `unzip`
2. Add translated text alongside original content in HTML files while keeping the markup intact
3. Update language metadata in content.opf to indicate bilingual content
4. Reassemble using `zip` command with proper options to maintain EPUB format
5. Verify the result with `unzip -t` to ensure integrity

## Usage Examples
```
Create a bilingual English-Chinese book about mybook.epub, and save it to mybook_bilingual.epub.
```

## Key Considerations
- EPUB files are essentially ZIP archives with a specific structure
- The mimetype file must be the first file in the archive and stored without compression
- Language attributes in HTML files and metadata should reflect the bilingual nature
- All original file paths and structures must be preserved during reassembly
- Original text content must be preserved alongside the new translations
- No automated scripts should be created for translation; instead, create a TODO list of files that need translation
- Directly read file content and perform modifications on the files rather than using automated processes

## Bilingual Formatting Standards
To ensure optimal reading experience in bilingual EPUB files:
- Use paragraph-by-paragraph comparison format, with translated text immediately following the corresponding original paragraph
- Maintain consistent formatting for both languages throughout the document
- Preserve the original document structure while integrating translated content
- Use appropriate language tags (lang attributes) for both original and translated text
- Clearly separate original and translated content with visual indicators (e.g., different text colors, spacing, or containers)
- Ensure proper text direction and typography for both languages
- Maintain consistent font sizes and styles that work well for both languages
- Follow a structured approach: original paragraph, then translated paragraph, maintaining the logical flow of content
