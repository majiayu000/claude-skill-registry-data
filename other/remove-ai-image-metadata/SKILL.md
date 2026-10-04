---
name: remove-ai-image-metadata
description: Inspect, remove, and verify embedded AI-generator or provenance metadata in image files without changing encoded picture data when the format permits. Use for any image-metadata cleanup request involving GPT Image, OpenAI, DALL-E, C2PA, Content Credentials, generative-AI labels, EXIF/XMP generator fields, or similar provenance in individual images or folders, including PNG, JPEG/JPG, WebP, GIF, TIFF, HEIC/HEIF, AVIF, SVG, and other image formats.
---

# Remove AI Image Metadata

Remove explicit embedded AI provenance or generator metadata using a format-aware workflow. Preserve encoded image content and rendering data whenever possible.

## Workflow

1. Resolve the exact files or folder in scope and identify each real file format from its contents.
2. Inspect before writing. For PNG, JPEG/JPG, WebP, and GIF, use the bundled cleaner without a write option:

   ```powershell
   python "<skill-folder>\scripts\clean_image_metadata.py" "<file-or-folder>" --recursive
   ```

3. Review every proposed removal. Default mode removes C2PA/Content Credentials blocks and metadata fields that contain known AI-generator markers.
4. Choose a write mode:

   - Prefer verified copies when replacement was not explicitly requested:

     ```powershell
     python "<skill-folder>\scripts\clean_image_metadata.py" "<file-or-folder>" --recursive --output-dir "<clean-folder>"
     ```

   - Use `--in-place` only when the user wants the originals changed. Add `--backup-dir "<folder-outside-the-publish-folder>"` when a backup is useful.
   - Add `--all-metadata` only when the user asks to remove all removable non-rendering metadata. Preserve color profiles and functional animation data.

5. Confirm every changed file reports `PASS`. The cleaner reparses the written container and confirms that encoded PNG, JPEG, WebP, or GIF image payloads are unchanged.
6. Inspect the cleaned output again when extra verification is appropriate.
7. Report the number of files processed, exact output path, formats handled, and metadata removed.

## Format Routing

- Use the bundled script for byte-preserving PNG, JPEG/JPG, WebP, and GIF cleanup.
- For TIFF, HEIC/HEIF, AVIF, SVG, PSD, or another format, inspect available format-aware tools such as ExifTool or `c2patool`. Work on copies unless in-place replacement was requested. Verify the result with the same tool plus a decoder.
- If no safe handler is available, stop and report the unsupported format. Do not generically re-save or convert the image merely to strip metadata; that may alter pixels, animation, orientation, color, or compression.

## Operational Rules

- Process only images you own or are authorized to modify. Do not remove provenance metadata to misrepresent an image's origin or bypass a platform's disclosure requirements.
- Never claim a cleaned image is undetectable or guaranteed not to be classified as AI-generated. State only which explicit metadata was removed. Pixel-based classifiers may still guess.
- Preserve encoded picture data, ICC profiles, gamma/chromaticity information, JPEG color-transform markers, animation control, and other rendering-related data.
- In default mode, preserve unrelated copyright, authorship, descriptions, and location metadata unless the user requests broader removal.
- Warn when removing a whole EXIF block could also remove orientation or other co-located fields. Prefer a metadata-aware editor when selective EXIF tag deletion is possible.
- Keep backups outside the upload/publish folder so tagged originals are not selected accidentally.
- Stop on malformed containers, failed integrity validation, changed encoded-image hashes, or incomplete post-clean inspection.

## Common Invocations

Inspect supported images:

```powershell
python "<skill-folder>\scripts\clean_image_metadata.py" "C:\path\images" --recursive
```

Clean originals after explicit confirmation:

```powershell
python "<skill-folder>\scripts\clean_image_metadata.py" "C:\path\images" --recursive --in-place
```

Create clean copies:

```powershell
python "<skill-folder>\scripts\clean_image_metadata.py" "C:\path\images" --recursive --output-dir "C:\path\clean-images"
```

The bundled cleaner uses only the Python standard library.
