---
name: swm-react-native-best-practices
description: "Software Mansion's best practices for React Native and Expo on the New Architecture: Reanimated 4 animations, Gesture Handler, react-native-svg, and react-native-worklets threading. Read the sub-skill in references/ that matches the topic."
license: MIT
metadata:
  opencode/autoinvoke: false
---

# React Native Best Practices

Software Mansion's production patterns for React Native apps on the New Architecture.

Read the relevant sub-skill for the topic at hand. All sub-skills are in `references/`.

Apex vendors four of upstream's nine sub-skills, the ones for libraries in `apps/mobile`'s booth binary; see `SOURCE.md`.

## Sub-skills

| Sub-skill                            | When to use                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `references/animations/index.md`     | CSS transitions, CSS animations, CSS pseudo-selectors and callbacks, shared value animations, GPU shader animations (WebGPU, TypeGPU), layout animations (entering/exiting, transitions, keyframes), scroll-driven animations, animation functions (withSpring, withTiming, withDecay), core hooks (useSharedValue, useAnimatedStyle), interpolation, particle systems, procedural noise, SDF rendering, animation performance, 120fps, accessibility, Reanimated 4 |
| `references/gestures/index.md`       | Tap, pan, pinch, rotation, swipe, long press, fling, hover, drag, Pressable, RectButton, Swipeable, DrawerLayout, VirtualGestureDetector, gesture composition, gesture testing -- any touch interaction with Gesture Handler                                                                                                                                                                                                                                        |
| `references/svg/index.md`            | Vector graphics, icons, charts, illustrations using React Native SVG                                                                                                                                                                                                                                                                                                                                                                                                |
| `references/multithreading/index.md` | Multithreading, react-native-worklets, background processing, Worker Runtimes, UI thread, scheduleOnUI, scheduleOnRN, Serializable, Synchronizable, offloading computation from the JS thread                                                                                                                                                                                                                                                                       |
