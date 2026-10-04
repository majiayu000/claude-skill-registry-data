---
name: remotion-web-player-integration
description: Embedding videos in React with @remotion/player. Use when rendering dynamic video components inside interactive web applications or portfolios using Remotion web players.
version: "1.0.0"
verified_date: 2026-06-01
category: core
---

# Remotion Web Player Integration

## Purpose
Provide copy-pasteable React recipes and parameters for embedding, styling, and controlling dynamic video components inside standard React/Next.js pages using the `@remotion/player` module.

## When to Use This Skill
- Embedding React-animated video compositions directly inside web pages.
- Providing custom video playback controls, frame scrubbing, or trigger actions based on video playback state.
- Structuring high-performance video players with dynamic rendering widths and heights.

## Output Format / Delivery
Deliver highly optimized, client-isolated video player components. Ensure components utilize standard `@remotion/player` variables, handles, and fallback skeletons.

## Behavior Rules
1. **Never load player assets on Server Components directly** — isolate all video rendering contexts inside client files.
2. **Always provide precise composition dimension bounds** (width, height) and frame rates matching the template context.
3. **Never allow unmounted or raw layouts to layout shift** — reserve spatial bounds using responsive layout heights.
4. **Always verify frame limits match composition duration properties**.

## Maintenance Notes
This skill is locked for Remotion core player integration. Update if newer `@remotion/player` APIs introduce structural interface changes.

---

## Phase 1: Player Setup

```tsx
"use client";
import { Player } from "@remotion/player";
import { CoffeeVideo } from "./CoffeeVideo";

export function VideoPlayerSection() {
  return (
    <div className="w-full max-w-4xl mx-auto overflow-hidden rounded-xl border border-zinc-800 bg-black aspect-video">
      <Player 
        component={CoffeeVideo} 
        durationInFrames={150} 
        fps={30} 
        width={1920} 
        height={1080} 
        style={{
          width: "100%",
          height: "100%",
        }}
        controls
        loop
      />
    </div>
  );
}
```