---
name: browser
description: remotely orchestrate a (chromium) browser to utilize web apps
---

# Browser

Uses [browser-use](https://github.com/browser-use/browser-use) (via Chrome DevTools Protocol) to browse any website.
Remotely orchestrate a browser, to navigate the web.
Meaning any task that can be accomplished via a browser.

## Instructions

- read `README.md` to understand this project

## QUICK REFERENCE

These are CLI commands you may use.

| Task | Command | Purpose |
|------|---------|---------|
| Start Browser Server | `browser server start` | Start background browser server |
| Stop Browser Server | `browser server stop` | Stop background server |
| Server Status | `browser server status` | Check server status and latest logs summary |
| View Live Logs | `browser server logs --follow` | Tail live server logs |
| Get Page Status | `browser client status` | Get current page URL and title |
| Navigate to URL | `browser client navigate URL` | Navigate browser to specified URL |
| Execute JavaScript | `browser client execute JAVASCRIPT` | Execute JavaScript code (arrow function) |
| Get DOM Content | `browser client dom [SELECTOR]` | Get HTML content of element (default: body) |
| Fill Input Field | `browser client fill SELECTOR VALUE` | Fill form input field with value |
| Click Element | `browser client click SELECTOR` | Click on specified element |
| Click at Coordinates | `browser client click-at X Y` | Click at specific coordinates |
| Visualize Elements | `browser client visualize [--csv]` | Generate Set-of-Marks visualization |
| Detect Objects | `browser client detect [--csv]` | Run YOLO object detection |
| Segment Objects | `browser client segment` | Run SAM segmentation |

## Examples

Sample user prompt:

> let's test this project:
> - start browser service
> - use client scripts to 
>   - navigate to google.com
>   - type `hamster dance` into search box
>   - click search button
>   - read first 3 search results
>   - summarize them in your response to me
>   - stop the server

Sample agent output (ie. `Gemini 3 Flash`):

```
GitHub Copilot: Created 6 todos

Starting: *Start browser service* (1/6)

Ran terminal command: browser server start

Stdout:
Starting browser server...
✅ Server started in background (PID 12345)
Logs: /home/user/.browser_agent/server.log

Starting: *Navigate to Google* (2/6)

Ran terminal command: browser client navigate "https://www.google.com"

Stdout:
✅ Navigated to https://www.google.com

Starting: *Type search query* (3/6)

Ran terminal command: browser client fill "[name='q']" "hamster dance"

Stdout:
✅ Filled [name='q']

Starting: *Click search button* (4/6)

Ran terminal command: browser client click "[name='btnK']"

Stdout:
✅ Clicked [name='btnK']

Starting: *Read search results* (5/6)

Ran terminal command: browser client execute "() => Array.from(document.querySelectorAll('#search h3')).slice(0, 3).map(h3 => ({title: h3.innerText, link: h3.closest('a')?.href}))"

Stdout:
Result: [{"title": "Hampton the Hamster \"The Hamsterdance Song\"", "link": "https://www.youtube.com/watch?v=1qN72LEQnaU"}, ...]

Starting: *Stop server* (6/6)

Ran terminal command: browser server stop

Stdout:
✅ Server stopped (PID 12345)

Completed: *Summarize results*

The browser service was successfully started, and I performed the requested search for "hamster dance" on Google. Here are the first three search results:

1.  **Hampton the Hamster "The Hamsterdance Song"**
    - [https://www.youtube.com/watch?v=1qN72LEQnaU](https://www.youtube.com/watch?v=1qN72LEQnaU)
2.  **Hampton the Hamster - The Hamsterdance Song (Official Video ...**
    - [https://www.youtube.com/watch?v=6WpMlwVwydo](https://www.youtube.com/watch?v=6WpMlwVwydo)
3.  **Hamster Dance - Wikipedia**
    - [https://en.wikipedia.org/wiki/Hamster_Dance](https://en.wikipedia.org/wiki/Hamster_Dance)
```


### Visual Grounding Example

Sample user prompt:

> Find the "Sign in" button on this page using vision and click it.

Sample agent output:

```bash
# 1. Get visual coordinates of interactive elements (CSV is default)
browser client visualize | grep -i "Sign in"
# Output: 1194,28,5,Sign in

# 2. Click at the identified coordinates
browser client click-at 1194 28
```

**Example Output:**
![Visualized Elements](docs/visualized_example.png)

**CSV Representation (truncated):**
```csv
44,30,0,About
99,30,1,Store
1010,28,2,Gmail
1066,28,3,Images
1124,28,4,
1194,28,5,Sign in
```

### Object Detection Example (YOLOv8)

Sample user prompt:

> Detect people and bicycles in the current image search results.

```bash
browser client detect
# Output:
# 256,180,0,person
# 240,320,1,bicycle
# ...
```

**Example Output:**
![Detected Objects](docs/detected_example.png)

### Image Segmentation Example (SAM)

Sample user prompt:

> Segment the visual regions of the current page and click on the main logo (Segment 0).

```bash
# 1. Run segmentation to get IDs and coordinates
browser client segment
# Output:
# 450,300,0,segment
# 120,50,1,segment
# ...

# 2. Click at the coordinates corresponding to ID 0
browser client click-at 450 300
```

**Example Output:**
![Segmented Regions](docs/segmented_example.png)

**How it works:**
The `segment` command returns a CSV mapping (`x,y,id,label`). The `id` in the CSV matches the large number shown in the `segmented_*.png` image. An AI agent can look at the image to identify which segment it wants to interact with, find that ID in the CSV, and use the provided `x,y` coordinates for a `click-at` command.
