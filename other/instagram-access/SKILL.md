---
name: Instagram Access
description: Permanent capability skill for authenticated Instagram data extraction using instaloader and a reusable session cookie file
recall_keywords: [instagram, instaloader, download post, download reel, instagram profile, instagram research, social media download, shortcode, instagram asset]
---

# Instagram Access — Permanent Capability Skill

## What This Skill Enables
- Download posts, reels, and stories from any public Instagram profile
- Download from private profiles the logged-in user follows
- Fetch post metadata (caption, likes, comments, date, type)
- Explore profiles (follower count, bio, post count, recent posts)
- Search by hashtag or location
- Download specific posts by shortcode or URL
- Batch scan captions for content categorization

## Authentication

### First-Time Setup
You need a dedicated Instagram account for scraping (DO NOT use your main account — Instagram may rate-limit or ban scraper accounts). Create a secondary account, then:

1. Install instaloader:
   ```bash
   pip install instaloader --break-system-packages  # Linux/WSL
   pip install instaloader                          # Windows/macOS
   ```

2. Generate a session cookie file (run in a separate terminal, NOT through Claude Code's Bash tool):
   ```powershell
   instaloader --login <your-scraper-username>
   ```

3. Instaloader stores the session at:
   - **Windows**: `%LOCALAPPDATA%\Instaloader\session-<username>.pg` (e.g. `C:\Users\<you>\AppData\Local\Instaloader\session-<username>.pg`)
   - **macOS/Linux**: `~/.config/instaloader/session-<username>.pg`

4. Record the username and session path in your project's configuration (NOT in this skill — keep credentials out of version control).

### If Session Expires
The session eventually expires. When instaloader throws `LoginRequiredException` or `ConnectionException` with "redirected to login":

1. Tell the user: "Instagram session expired. Please re-authenticate."
2. User runs in a separate terminal (NOT through Claude Code's Bash):
   ```powershell
   instaloader --login <username>
   ```
3. User enters password interactively (Bash tool cannot handle password prompts)
4. Session file is refreshed automatically
5. Resume operations

**NEVER** attempt interactive login through the Bash tool. It cannot handle password prompts.

## How to Use — Code Patterns

### Load Session (always start with this)
```python
import instaloader
L = instaloader.Instaloader(
    download_videos=True,
    download_video_thumbnails=False,
    compress_json=False,
    save_metadata=False,
    download_geotags=False,
    download_comments=False,
    post_metadata_txt_pattern=""
)
# Replace <username> with the scraper account username
L.load_session_from_file("<username>")
```

### Get Profile Info
```python
profile = instaloader.Profile.from_username(L.context, "<target-username>")
print(f"Followers: {profile.followers}, Posts: {profile.mediacount}")
print(f"Bio: {profile.biography}")
```

### Get Post by Shortcode
```python
post = instaloader.Post.from_shortcode(L.context, "<shortcode>")
print(f"Date: {post.date_utc}, Likes: {post.likes}, Type: {post.typename}")
print(f"Caption: {post.caption}")
```

### Download a Single Post
```python
L.download_post(post, target="output_directory")
```

### Iterate Profile Posts
```python
for post in profile.get_posts():
    print(post.shortcode, post.caption[:50])
    time.sleep(2)
```

### Search by Hashtag
```python
hashtag = instaloader.Hashtag.from_name(L.context, "<hashtag>")
for post in hashtag.get_posts():
    print(post.shortcode)
    time.sleep(2)
```

### Extract Shortcode from URL
```python
import re
url = "https://www.instagram.com/p/<shortcode>/"
shortcode = re.search(r'/(p|reel)/([A-Za-z0-9_-]+)', url).group(2)
```

## Windows-Specific Handling

### UTF-8 Encoding (required for non-Latin captions)
Always add at the top of any script:
```python
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
os.environ["PYTHONIOENCODING"] = "utf-8"
```

### Filename Safety
Instaloader creates files with timestamps containing colons — invalid on Windows. Always sanitize filenames:
```python
import re
safe_name = re.sub(r'[<>:"/\\|?*]', '_', original_name)
```

### File Writing with Non-Latin Content
```python
with open(filepath, "w", encoding="utf-8") as f:
    f.write(caption_with_non_latin)
```

## Safety Rules
1. **NEVER** store passwords in any file
2. **NEVER** open Chrome or any browser
3. **NEVER** create directory junctions
4. Add 2-3 second delays between API calls (reels: 3-5 seconds)
5. If rate limited (429 or "Please wait"): wait 60 seconds, retry once, then skip
6. If session expired: tell the user to re-authenticate in a separate terminal
7. **NEVER** download from accounts the user does not follow (respect privacy)
8. **NEVER** use Instagram data for purposes other than what the user requests
9. All filenames must be plain ASCII — replace special characters with hyphens
10. ZERO non-Latin characters in terminal commands or filenames

## Common Tasks

### "Download photos from @someprofile"
```python
profile = instaloader.Profile.from_username(L.context, "someprofile")
for post in profile.get_posts():
    L.download_post(post, target="downloads")
    time.sleep(3)
```

### "Get captions from recent 20 posts of @profile"
```python
profile = instaloader.Profile.from_username(L.context, "profile")
for i, post in enumerate(profile.get_posts()):
    if i >= 20: break
    print(f"{post.shortcode}: {post.caption[:100]}")
    time.sleep(1.5)
```

### "Download this specific post: [URL]"
```python
shortcode = re.search(r'/(p|reel)/([A-Za-z0-9_-]+)', url).group(2)
post = instaloader.Post.from_shortcode(L.context, shortcode)
L.download_post(post, target="downloads")
```

### "Research competitor @profile"
```python
profile = instaloader.Profile.from_username(L.context, "competitor")
info = {
    "username": profile.username,
    "full_name": profile.full_name,
    "bio": profile.biography,
    "followers": profile.followers,
    "following": profile.followees,
    "posts": profile.mediacount,
    "is_verified": profile.is_verified,
    "is_business": profile.is_business_account,
    "business_category": profile.business_category_name,
}
# Get engagement stats from recent 20 posts
likes, comments = [], []
for i, post in enumerate(profile.get_posts()):
    if i >= 20: break
    likes.append(post.likes)
    comments.append(post.comments)
    time.sleep(1.5)
info["avg_likes"] = sum(likes) / len(likes) if likes else 0
info["avg_comments"] = sum(comments) / len(comments) if comments else 0
```

## Recall Keywords
instagram, instaloader, download post, download reel, instagram profile,
instagram research, social media download, shortcode, instagram asset
