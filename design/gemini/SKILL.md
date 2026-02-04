---
name: gemini
description: "All-purpose Gemini 3 Pro client with Thinking enabled. Query, analyze files (MP4, PDF, images), YouTube videos, generate/edit images. Uses browser cookies - no API key required."
---

<gemini_skill>
  <persona>Gemini 3 Pro Assistant</persona>
  <primary_goal>Provide access to Gemini 3 Pro with Thinking for queries, file analysis, and image generation</primary_goal>

  <overview>
    A comprehensive Gemini 3 Pro skill using gemini-webapi for cookie-based authentication.
    Supports text queries, file analysis (video, PDF, images), YouTube analysis, and image generation/editing.
    Uses "Thinking with 3 Pro" mode by default for enhanced reasoning.
  </overview>

  <capabilities>
    <capability name="Text Queries">General questions with Thinking enabled for complex reasoning</capability>
    <capability name="Video Analysis">Upload MP4 files for summarization, timestamp finding, content extraction</capability>
    <capability name="YouTube Analysis">Pass YouTube URLs for video understanding via extension</capability>
    <capability name="Document Analysis">Upload PDFs and documents for summarization and Q&A</capability>
    <capability name="Image Analysis">Upload images for description, OCR, analysis</capability>
    <capability name="Image Generation">Create images from text prompts</capability>
    <capability name="Image Editing">Modify existing images with natural language</capability>
    <capability name="Google Search Grounding">Automatic web search for current information</capability>
    <capability name="Thinking Access">View model's reasoning process with --show-thoughts</capability>
  </capabilities>

  <prerequisites>
    <requirement>Chrome browser logged into gemini.google.com</requirement>
    <requirement>First time setup: cd ~/.claude/skills/gemini && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt</requirement>
    <requirement>On macOS, allow Keychain access when prompted (first run)</requirement>
  </prerequisites>

  <usage>
    Text query:
    ```bash
    ~/.claude/skills/gemini/webapi "Explain quantum computing"
    ```

    Analyze video file:
    ```bash
    ~/.claude/skills/gemini/webapi "Summarize this video" --file video.mp4
    ```

    Analyze YouTube video:
    ```bash
    ~/.claude/skills/gemini/webapi "What are the key points?" --youtube "https://youtube.com/watch?v=..."
    ```

    Analyze document:
    ```bash
    ~/.claude/skills/gemini/webapi "Summarize this report" --file report.pdf
    ```

    Generate image:
    ```bash
    ~/.claude/skills/gemini/webapi "A sunset over mountains" --generate-image sunset.png
    ```

    Edit image:
    ```bash
    ~/.claude/skills/gemini/webapi "Make the sky purple" --edit photo.jpg --output edited.png
    ```

    Show thinking process:
    ```bash
    ~/.claude/skills/gemini/webapi "Solve step by step: What is 15% of 240?" --show-thoughts
    ```
  </usage>

  <cli_options>
    | Option | Description |
    |--------|-------------|
    | `--file, -f FILE` | Input file (MP4, PDF, PNG, JPG, etc.) |
    | `--youtube URL` | YouTube video URL to analyze |
    | `--generate-image FILE` | Generate image and save to FILE |
    | `--edit IMAGE` | Edit existing image (use with --output) |
    | `--output, -o FILE` | Output file path for image operations |
    | `--aspect RATIO` | Aspect ratio for images (16:9, 1:1, 4:3, 3:4) |
    | `--show-thoughts` | Display model's thinking process |
    | `--model MODEL` | Model to use (default: gemini-3.0-pro) |
    | `--json` | Output response as JSON |
    | `--retries N` | Number of retries for transient failures (default: 3) |
    | `--timeout SECS` | Client initialization timeout in seconds (default: 120) |
    | `--help, -h` | Show help |
  </cli_options>

  <reliability>
    The client includes several reliability improvements:
    - **Retry with backoff**: Transient errors (timeouts, rate limits, 5xx) trigger automatic retries with exponential backoff
    - **Response stability checks**: Image generation waits for stable response before saving
    - **Extended timeouts**: Video file analysis automatically uses longer timeouts (180s)
    - **Detailed diagnostics**: Error messages include troubleshooting suggestions
  </reliability>

  <workflow>
    1. User requests analysis, generation, or query
    2. Determine appropriate mode (query, file analysis, image gen)
    3. Construct command with appropriate flags
    4. Run webapi script
    5. Process and present results
  </workflow>

  <examples>
    <example name="Complex reasoning with thinking">
      ```bash
      ~/.claude/skills/gemini/webapi "What are the implications of quantum computing for cryptography? Think through this carefully." --show-thoughts
      ```
    </example>

    <example name="Video meeting summary">
      ```bash
      ~/.claude/skills/gemini/webapi "Create meeting notes: attendees, topics, decisions, action items" --file meeting.mp4
      ```
    </example>

    <example name="YouTube tutorial extraction">
      ```bash
      ~/.claude/skills/gemini/webapi "List all steps with timestamps" --youtube "https://youtube.com/watch?v=VIDEO_ID"
      ```
    </example>

    <example name="Current events (grounded)">
      ```bash
      ~/.claude/skills/gemini/webapi "What are the latest developments in AI this week? Search the web."
      ```
    </example>

    <example name="Image generation with aspect ratio">
      ```bash
      ~/.claude/skills/gemini/webapi "A cyberpunk cityscape at night" --generate-image city.png --aspect 16:9
      ```
    </example>

    <example name="Document analysis">
      ```bash
      ~/.claude/skills/gemini/webapi "Extract the key findings and recommendations" --file research_paper.pdf
      ```
    </example>
  </examples>

  <troubleshooting>
    <issue name="Error initializing client">
      <symptom>Cookie or initialization errors, repeated init failures</symptom>
      <solution>
        1. Ensure you're logged into gemini.google.com in Chrome
        2. On macOS, allow Keychain access when prompted
        3. Try closing Chrome completely and reopening gemini.google.com
        4. Clear Chrome cookies for gemini.google.com and re-login
        5. Try increasing --timeout if failures are intermittent
      </solution>
    </issue>

    <issue name="Transient/timeout errors">
      <symptom>Timeout, connection reset, or 5xx errors</symptom>
      <solution>The client automatically retries with backoff. If failures persist, try --retries 5 or --timeout 180. Check your network connection.</solution>
    </issue>

    <issue name="No images generated">
      <symptom>Script runs but no image output after retries</symptom>
      <solution>
        1. Rephrase prompt to be more explicit about wanting an image
        2. Some content may be filtered by safety systems
        3. Try simpler prompts first to verify the client works
        4. Check if the model returned text (may indicate why image failed)
      </solution>
    </issue>

    <issue name="Module not found">
      <symptom>ImportError for gemini_webapi</symptom>
      <solution>Run: cd ~/.claude/skills/gemini && source .venv/bin/activate && pip install -r requirements.txt</solution>
    </issue>

    <issue name="YouTube not working">
      <symptom>Cannot analyze YouTube video</symptom>
      <solution>Ensure YouTube extension is enabled in your Gemini web settings at gemini.google.com</solution>
    </issue>

    <issue name="No thinking shown">
      <symptom>--show-thoughts returns nothing</symptom>
      <solution>Thinking may be skipped for trivial queries. Try a more complex question, or the model may have used code execution instead.</solution>
    </issue>

    <issue name="Rate limiting">
      <symptom>Repeated failures with rate limit errors</symptom>
      <solution>Wait a few minutes before retrying. Consider spacing out requests. The client uses exponential backoff automatically.</solution>
    </issue>
  </troubleshooting>

  <important_notes>
    <note>Always uses "Thinking with 3 Pro" mode for enhanced reasoning</note>
    <note>Google Search grounding is automatic - just ask about current events</note>
    <note>YouTube extension must be enabled in gemini.google.com settings</note>
    <note>Cookie-based auth - no API key needed, uses your Google account quota</note>
    <note>First run on macOS prompts for Keychain access</note>
  </important_notes>
</gemini_skill>
