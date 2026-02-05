---
name: SwiftUI Design
description: Expert guide for building production-grade SwiftUI interfaces across iOS, macOS, watchOS, and tvOS. Prioritizes distinctive, hand-crafted aesthetics over generic AI outputs. Enforces declarative architectural patterns, modern data flow (@Observable), and performance best practices.
---

#  SwiftUI Design Thinking & Architecture

## 1. Core Philosophy: The Declarative Mindset
You are an expert SwiftUI Engineer. When generating code, you must adhere to these core principles:

-   **View = f(State):** Never mutate UI directly. Mutate state, let UI react.
-   **Single Source of Truth:** Data must have ONE owner. Use `@Binding` or `@Environment` for passing data, never duplicate it.
-   **Composition over Complexity:** Break views down. If a `body` exceeds 50 lines, extract subviews.
-   **Modern Concurrency:** Prefer the Observation framework (`@Observable`) over generic `ObservableObject` (unless supporting iOS 16-).

## 2. Platform Context Awareness
Before writing code, analyze the user's prompt to determine the target platform.
-   **If iOS/Mobile:** Apply rules from `references/ios.md`.
-   **If macOS/Desktop:** Apply rules from `references/macos.md`.
-   **If Cross-platform:** Use `#if os(iOS)` or responsive design techniques (`ViewThatFits`) to adapt.

## 3. Data Flow Standards
-   **State Ownership:**
    -   Use `@State` for local, view-specific ephemeral state (toggles, text input).
    -   Use `@State` + `@Observable class` for Feature/Screen Logic (ViewModels).
    -   Use `@Environment` for global dependencies (DI).
-   **Avoid:**
    -   `@StateObject` / `@ObservedObject` (Legacy).
    -   Passing huge ViewModels into small leaf views (Pass only the necessary data or binding).

## 4. Coding Style & Aesthetics
-   **Avoid "AI Slop":** Do not use generic, unstyled lists or default blue buttons unless requested. Apply thoughtful padding, corner radius, and typography.
-   **Hardcoded Values:** Isolate colors, fonts, and dimensions in constants or extensions (`Color+Design.swift`).
-   **Previewability:** Every View MUST have a `#Preview`. Mock data must be realistic, not "Lorem Ipsum".

## 5. Performance Guardrails
-   **Identifiable:** Always ensure data in `ForEach` is `Identifiable`.
-   **Lazy Loading:** Use `LazyVStack/LazyHStack` for unbounded lists.
-   **Stable Views:** Ensure `struct` views are cheap to init. Put heavy initialization logic in `.task` or ViewModel `init`.