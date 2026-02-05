---
name: generate-image
description: "Generate and edit images using Google Gemini (Nano Banana). Use when user asks to create, generate, or edit images. Requires Chrome logged into gemini.google.com."
---

<generate_image_skill>
  <persona>Image Generator</persona>
  <primary_goal>Generate and edit images using Gemini Nano Banana via browser cookies</primary_goal>

  <overview>
    A Python-based image generation skill that uses gemini-webapi to access Google Gemini's
    Nano Banana image model. Authenticates via browser cookies auto-extracted from Chrome.
    No API key required - uses your existing Google account.
  </overview>

  <prerequisites>
    <requirement>Chrome browser logged into gemini.google.com</requirement>
    <requirement>First time setup: cd ~/.claude/skills/generate-image && pip install -r requirements.txt</requirement>
    <requirement>On macOS, allow Keychain access when prompted (first run)</requirement>
  </prerequisites>

  <usage>
    Generate an image:
    ```bash
    ~/.claude/skills/generate-image/scripts/nano-banana "A futuristic cityscape at sunset"
    ```

    With options:
    ```bash
    ~/.claude/skills/generate-image/scripts/nano-banana "A cat in space" --output /tmp/cat.png --aspect 16:9
    ```

    Edit an existing image:
    ```bash
    ~/.claude/skills/generate-image/scripts/nano-banana "Make the sky purple" --input photo.jpg --output /tmp/edited.png
    ```
  </usage>

  <cli_options>
    | Option | Description |
    |--------|-------------|
    | `--output, -o FILE` | Output file path (default: generated.png) |
    | `--input, -i FILE` | Input image for editing mode |
    | `--aspect RATIO` | Aspect ratio hint (e.g., 16:9, 1:1, 4:3, 3:4) |
    | `--retries N` | Number of retries for transient failures (default: 3) |
    | `--timeout SECS` | Client initialization timeout in seconds (default: 90) |
    | `--help, -h` | Show help |

    Model: gemini-3.0-pro (Nano Banana Pro) - hardcoded for best image quality
  </cli_options>

  <reliability>
    The client includes several reliability improvements inspired by Oracle's browser automation:
    - **Retry with exponential backoff**: Transient errors (timeouts, rate limits, 5xx) trigger automatic retries
    - **Response stability checks**: Waits for image response to stabilize before saving (prevents truncated/incomplete images)
    - **Empty response retry**: Automatically retries when no images are returned
    - **Detailed diagnostics**: Error messages include troubleshooting steps for common issues
  </reliability>

  <examples>
    <example name="Generate a simple image">
      ```bash
      ~/.claude/skills/generate-image/scripts/nano-banana "A golden retriever playing in autumn leaves"
      ```
      Output: generated.png (1024x1024)
    </example>

    <example name="Generate with specific aspect ratio">
      ```bash
      ~/.claude/skills/generate-image/scripts/nano-banana "A panoramic mountain landscape" --aspect 16:9 --output /tmp/landscape.png
      ```
    </example>

    <example name="Generate a portrait">
      ```bash
      ~/.claude/skills/generate-image/scripts/nano-banana "A professional headshot photo style portrait" --aspect 3:4 --output /tmp/portrait.png
      ```
    </example>

    <example name="Edit an existing image">
      ```bash
      ~/.claude/skills/generate-image/scripts/nano-banana "Add a rainbow in the sky" --input /tmp/photo.jpg --output /tmp/with-rainbow.png
      ```
    </example>

    <example name="Generate detailed artwork">
      ```bash
      ~/.claude/skills/generate-image/scripts/nano-banana "Detailed oil painting of a forest at dawn" --output /tmp/painting.png
      ```
    </example>
  </examples>

  <workflow>
    1. User requests image generation or editing
    2. Construct appropriate prompt (be descriptive for best results)
    3. Run the nano-banana script with the prompt
    4. Check output file exists and report success
    5. If needed, iterate with refined prompts
  </workflow>

  <prompting_tips>
    <tip>Be specific and descriptive - "A red vintage sports car on a winding mountain road at sunset" works better than "a car"</tip>
    <tip>Include style hints - "in the style of watercolor painting", "photorealistic", "3D render"</tip>
    <tip>Specify lighting - "golden hour lighting", "dramatic shadows", "soft diffused light"</tip>
    <tip>Mention composition - "close-up", "wide angle", "bird's eye view"</tip>
    <tip>For editing, describe the specific change you want, not the full scene</tip>
  </prompting_tips>

  <troubleshooting>
    <issue name="Error initializing client">
      <symptom>Error message about cookies or initialization, repeated init failures</symptom>
      <solution>
        1. Ensure you're logged into gemini.google.com in Chrome
        2. On macOS, allow Keychain access when prompted
        3. Try closing Chrome completely and reopening gemini.google.com
        4. Clear Chrome cookies for gemini.google.com and re-login
        5. Try --timeout 120 if failures are intermittent
      </solution>
    </issue>

    <issue name="Transient/timeout errors">
      <symptom>Timeout, connection reset, or 5xx errors during generation</symptom>
      <solution>The client automatically retries with backoff. If failures persist, try --retries 5. Check your network connection.</solution>
    </issue>

    <issue name="No images generated">
      <symptom>Script runs but no image output after retries</symptom>
      <solution>
        1. Rephrase prompt to be more explicit
        2. Some content may be filtered by safety systems
        3. Try simpler prompts first to verify the client works
        4. Check stderr for model's text response (may explain why image failed)
      </solution>
    </issue>

    <issue name="Module not found">
      <symptom>ImportError for gemini_webapi or browser_cookie3</symptom>
      <solution>Run: cd ~/.claude/skills/generate-image && pip install -r requirements.txt</solution>
    </issue>

    <issue name="Permission denied on macOS">
      <symptom>Error reading Chrome cookies</symptom>
      <solution>Grant Keychain access when macOS prompts. You may need to run the script again after granting access.</solution>
    </issue>

    <issue name="Rate limiting">
      <symptom>Repeated failures with rate limit errors</symptom>
      <solution>Wait a few minutes before retrying. The client uses exponential backoff automatically.</solution>
    </issue>
  </troubleshooting>

  <important_notes>
    <note>Requires Chrome logged into gemini.google.com - cookies are auto-extracted</note>
    <note>First run on macOS will prompt for Keychain access</note>
    <note>Image generation uses your Google account's Gemini quota</note>
    <note>Generated images include SynthID watermark (Google's AI watermark)</note>
    <note>Default output is 1024x1024 PNG</note>
  </important_notes>
</generate_image_skill>
