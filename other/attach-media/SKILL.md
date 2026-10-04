---
name: attach-media
description: Attach screenshots, recordings, and other media to GitHub issues, pull requests, and comments with `gh --attach`. Use whenever an issue, PR, or comment should carry an image or video the session captured or was given.
---

`gh` uploads media itself: pass `--attach <path>` to `gh issue create|edit|comment` or `gh pr create|edit|comment`, once per file. Needs gh v2.99.0 or later and write access to the repository; GitHub Enterprise Server is unsupported.

## Placement

- **Inline**: reference the local path in the body, `![The login error state](./login.png)`, and pass `--attach ./login.png`. The reference is rewritten in place to the uploaded asset and keeps its alt text.
- **Appended**: attach without referencing it and the file lands at the end of the body. Alt text follows `#` in the path: `--attach './login.png#The login error state'`.

Alt text says what the reader should see in the capture, in the project's own vocabulary.

```bash
gh pr comment 123 --body 'Reproduced on main.' --attach './login.png#Login form after submitting an expired token'
```

## Limits

PNG, JPEG, GIF, WebP, SVG, MP4, MOV, WebM. Images and GIFs up to 10 MB; video up to 10 MB on Free plans, 100 MB on paid. Scale an oversized image before attaching.
