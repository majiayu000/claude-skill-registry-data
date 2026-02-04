---
name: remote-camera-capture
description: Capture photos remotely from mobile devices for hardware inspection, PCB debugging, chip identification, document capture, or visual analysis. Use when you need to see something in the physical world - circuit boards, chip markings, component labels, error screens, handwritten notes, or any physical object the user mentions.
---

# Remote Camera Capture

Capture and analyze photos from the user's mobile device to help with hardware debugging, visual inspection, documentation, and troubleshooting tasks.

## When to Use This Skill

Use remote camera capture when:

- **Hardware debugging**: Inspecting PCBs, components, chips, sensors, or electronic devices
- **Chip identification**: Reading markings, part numbers, or labels on ICs and components
- **PCB inspection**: Examining trace layouts, solder joints, connections, or physical damage
- **Document capture**: Photographing handwritten notes, diagrams, schematics, or documentation
- **Error messages**: Capturing on-screen errors, status displays, or diagnostic information
- **Physical troubleshooting**: Seeing how something is assembled, connected, or configured
- **Visual comparison**: Comparing physical objects or setups with reference images or specs

The user will mention phrases like "take a photo", "can you see this", "look at this chip", "what's this component", or describe something physical they want help with.

## How Remote Capture Works

The workflow uses two MCP tools: `generate_upload_url` and `poll_for_upload`.

### Step 1: Generate Upload URL

Call the `generate_upload_url` tool with a clear message parameter that tells the user what to photograph:

```
{
  "message": "Take a photo of the chip markings on the main IC"
}
```

This returns:
- `capture_url`: A URL for the user to open on their mobile device
- `session_id`: An identifier for this capture session

### Step 2: Present URL to User

Show the capture URL to the user in a clear, actionable way:

```
I've generated a remote camera capture link for you. Please open this URL on your mobile device to take the photo:

[capture_url]

Instructions: [repeat the message you provided]

The URL will open a camera interface where you can capture the photo. Once you've taken the photo, I'll automatically detect when it's uploaded.
```

### Step 3: Poll for Upload

Immediately after presenting the URL, call `poll_for_upload` with the session_id:

```
{
  "session_id": "[session_id from step 1]",
  "timeout": 120
}
```

This will wait up to 120 seconds (2 minutes) for the user to capture and upload the photo. The tool provides progress updates while waiting.

When the upload completes, you'll receive:
- `download_url`: A presigned URL to download the captured photo
- `etag`: A unique identifier for this specific upload
- `last_modified`: Timestamp of when the photo was uploaded

### Step 4: Analyze the Photo

Use the Read tool to fetch and analyze the downloaded photo:

```
Read the image at [download_url]
```

Then provide your analysis based on what the user asked for - identify chips, explain circuit layouts, read error messages, transcribe handwritten notes, etc.

## Reusing Capture URLs

The same capture URL can be reused multiple times! If the user needs to take additional photos:

1. Tell them they can use the same URL again
2. When polling, use the `not_etag` parameter with the previous photo's etag to detect the new upload:

```
{
  "session_id": "[same session_id]",
  "timeout": 120,
  "not_etag": "[etag from previous upload]"
}
```

This allows efficient multi-photo workflows without generating new URLs each time.

## Crafting Effective Capture Messages

Good capture instructions are specific and actionable:

**Good examples:**
- "Take a close-up photo of the chip markings on the largest IC"
- "Capture the PCB trace layout near the power connector"
- "Photograph the part number printed on the sensor module"
- "Show me the error message displayed on the screen"
- "Take a photo of the wiring connections at the terminal block"

**Less effective:**
- "Take a photo" (too vague)
- "Show me the board" (not specific enough)
- "Photograph the thing" (unclear what to focus on)

Include:
- What to photograph (specific component, area, or feature)
- Where to find it (location or identifying feature)
- What to focus on (markings, connections, labels, etc.)

## Tips for Users

When presenting capture URLs, you can include these tips for better photos:

- **Lighting**: Ensure good lighting on the subject, avoid shadows
- **Focus**: Get close enough to read text or see details clearly
- **Stability**: Hold the device steady to avoid blur
- **Angle**: Photograph straight-on when reading text or markings
- **Context**: Include enough surrounding area to understand what you're looking at

## Common Use Cases

### Chip Identification

"I need to identify this chip on my board."

1. Generate URL: "Take a close-up photo showing the markings on the chip you want to identify"
2. Analyze the photo to read manufacturer, part number, date codes
3. Look up chip specifications and provide information

### PCB Debugging

"This circuit isn't working, can you help debug it?"

1. Generate URL: "Take a photo of your full PCB showing all components and connections"
2. Analyze for incorrect connections, damaged traces, reversed components
3. Request additional photos of specific areas if needed (reuse the URL)

### Error Message Capture

"My device is showing an error but I can't copy the text."

1. Generate URL: "Photograph the error message displayed on your screen"
2. Read and transcribe the error text
3. Provide troubleshooting guidance based on the error

### Documentation Review

"Can you help me understand this schematic?"

1. Generate URL: "Take a photo of the schematic or diagram you need help with"
2. Analyze the schematic and explain key sections
3. Answer specific questions about the design

## Error Handling

If the poll times out:
- The user may not have opened the URL yet - ask them to try
- Network issues may have delayed upload - suggest trying again
- The URL is still valid - they can retry without generating a new one

If you can't analyze the photo:
- Ask for a clearer photo focused on the specific area of interest
- Request better lighting or a different angle
- The capture URL can be reused for retakes

## Technical Notes

- Upload URLs are valid for 7 days
- Download URLs are valid for 7 days
- Maximum file size depends on user's S3 configuration
- Photos are stored in the user's S3 bucket at `remote-camera-mcp/{session_id}`
- The session_id is a UUID that serves as the filename

## Best Practices

1. **Be specific**: Clear instructions get better photos the first time
2. **Set expectations**: Tell users you're waiting for their photo after presenting the URL
3. **Reuse URLs**: For multi-photo sessions, reuse the capture URL with not_etag parameter
4. **Provide context**: After analyzing, reference what you saw to confirm you're looking at the right thing
5. **Guide retakes**: If the photo isn't clear enough, explain what would help and remind them the URL still works
