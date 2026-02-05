---
name: dev-swarm-screen-snapshot
description: Capture and inspect specific screen regions (e.g., mobile simulators, app windows) using a background streaming process. Use for UI debugging and troubleshooting.
---

# Screen Snapshot

This skill allows an AI agent to inspect a mobile app, an iOS/Android simulator, or any specific part of the screen.

## When to Use This Skill

- User needs to debug UI issues in mobile simulator or app
- User wants AI agent to inspect specific screen region
- User asks to capture and analyze app window or UI element
- User needs visual feedback for troubleshooting GUI applications

## Your Roles in This Skill

- **QA Engineer**: Set up screen capture tools for UI inspection and debugging. Configure capture regions to focus on relevant UI elements. Verify screen capture functionality and troubleshoot capture issues. Guide users through window positioning and configuration.
- **DevOps Engineer**: Execute Python script to run screen streaming server. Manage background processes for screen capture. Handle server port configuration and accessibility. Verify system permissions for screen recording.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

1.  **Start the Screen Stream Process**:
    Run the following shell command as a background process to start the screen streaming server:

    ```bash
    uv run --directory {PROJECT-ROOT}/dev-swarm/py_scripts screen_stream.py --monitor -1 --background --fps 30 --host 127.0.0.1 --port 9090
    ```

2.  **Instruct the User**:
    Once the process is running, instruct the user to configure the capture area:

    > "I have started a screen capture tool. A light gray window should appear.
    > 1. Please move and resize this window to cover the area you want me to see (e.g., your mobile simulator or app window).
    > 2. Place the target content ON TOP of this light gray window.
    > 3. You can verify what I see by visiting http://127.0.0.1:9090 in your browser.
    > 4. Once you are satisfied with the view, you can close the preview page."

3.  **Capture Snapshot**:
    To see the screen content, fetch a snapshot from the local server:
    
    *   **URL**: `http://127.0.0.1:9090/snapshot.png`
    *   **Action**: Use a tool (like `web_fetch` or similar, depending on available tools) to retrieve/view this image.

## Usage Notes

*   **monitor -1**: This flag tells the script to use a transparent overlay window to define the capture region, rather than capturing a full monitor.
*   **Background Process**: Ensure the script continues running in the background while you need to take snapshots.
*   **Troubleshooting**: If the snapshot is blank or black, ensure the user has placed the content *on top* of the capture window and that screen recording permissions are granted to the terminal application.
