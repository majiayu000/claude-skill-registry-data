---
name: fizzy
description: Manages Fizzy boards, cards, steps, comments, and reactions. Use when user asks about boards, cards, tasks, backlog or anything Fizzy. 
---

# fizzy

Manage Fizzy boards, cards, steps, comments and reactions.  Run `fizzy --help` for all flags.  Each sub-command also has a `--help` flag.

## Output format 

JSON

## Usage Patterns

**Never dump raw output.** Use jq to reduce tokens.

## File Uploads

```bash
fizzy upload file PATH              # Upload a file for use in cards/comments
```

The upload command returns **two different IDs** for different purposes:

```bash
fizzy upload file /path/to/image.png
# Returns: { "signed_id": "...", "attachable_sgid": "..." }
```

| ID | Use For |
|---|---|
| `signed_id` | Card header/background images (via `--image` flag) |
| `attachable_sgid` | Inline images in rich text fields (descriptions, comments) |

### Default Behavior for Image Uploads

- **Card images:** Use inline (via `attachable_sgid` in description) by default. Only use background/header image (`signed_id` with `--image` flag) when the user explicitly mentions "background" or "header".
- **Comment images:** Always inline (via `attachable_sgid`). Comments do not support background images.

### Card Header/Background Image (only when explicitly requested)

**Important:** When creating a card with a background image, upload the image first to get the `signed_id`, then use it when creating the card.

**Validate the file is an image before uploading** for background images:

```bash
# Step 1: Verify file is a valid image type
MIME=$(file --mime-type -b /path/to/header.png)
if [[ ! "$MIME" =~ ^image/ ]]; then
  echo "Error: File is not a valid image (detected: $MIME)"
  exit 1
fi

# Step 2: Upload the image first to get the signed_id
SIGNED_ID=$(fizzy upload file /path/to/header.png | jq -r '.data.signed_id')

# Step 3: Create the card with the background image
fizzy card create --board BOARD_ID --title "Card" --image "$SIGNED_ID"
```

### Inline Images in Rich Text (Descriptions & Comments)

Use `attachable_sgid` in an `<action-text-attachment>` tag:

```bash
SGID=$(fizzy upload file image.png | jq -r '.data.attachable_sgid')
cat > description.html << EOF
<p>See image:</p>
<action-text-attachment sgid="$SGID"></action-text-attachment>
EOF
fizzy card create --board BOARD_ID --title "Card" --description_file description.html
```

**Important:** Each `attachable_sgid` can only be used once. Upload the file again if you need to attach it to multiple cards or comments.

# Paragraphs in HTML for Card Descriptions and Comments

When creating a card or comment, if there are multiple paragraphs in the card description or comment then place a `<p><br></p>` between the paragraphs. This will add spacing in the view.

# Card Statuses

Cards can have the following statuses:
- `published` - Active/open cards
- `closed` - Completed cards
- `not_now` - Postponed cards (marked as not ready)

# Instructions

1. **Determine the action** - What does the user want to do? (list, create, update, move, close, etc.)
2. **Check for account context** - If the user wants data from a specific account, use `--account=ID` with the numeric account ID
3. **Run the appropriate fizzy command** using the Bash tool
4. **Parse the JSON output** to present results clearly.
5. **Report the outcome** to the user in a readable format include entity identifiers in output so user can copy if needed. 

