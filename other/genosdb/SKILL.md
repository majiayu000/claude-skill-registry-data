---
name: genosdb
description: eres un experto usando GenosDB
---

## REGLA: Footer obligatorio en artículos
Todo post/artículo relacionado con GenosDB DEBE incluir al final el contenido de:
`/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosdb-links.md`
Leer ese archivo e insertar su contenido como footer del artículo.

## API Reference & Core Documentation

- 📘 [GDB API Reference](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosdb-api-reference.md) - Detailed API documentation
- ✨ [GenosDB Features](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosdb-features.md) - Comprehensive feature overview and architecture
- 🧪 [GenosDB Examples](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosdb-examples.md) - Live demos and community projects
- 🤝 [Distributed Trust Model](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosdb-distributed-trust-model.md) - P2P trust via cryptographic identity, signed ops, and RBAC enforcement
- 🔒 [Zero Trust Security Model](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/zero-trust-security-model.md) - Understanding GenosDB Zero-Trust Security Model: From Guest to SuperAdmin
- ↔️ [Cursor-Based Pagination](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/cursor‐based-pagination.md) - Efficient paging with $after/$before/$limit
- 📚 [Resources](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosdb-resources.md) - Helpful links: whitepaper, docs, wiki, npm, discussions

## CRUD Operations

- 🛠️ [CRUD Operation Guide](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/crud-operations-guide.md) - Overview of CRUD APIs with links to detailed guides
- 📤 [PUT Guide](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/put-guide.md) - Insert/update nodes; auto ID, persistence, and events
- 📥 [GET Guide](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/get-guide.md) - Retrieve nodes by ID; optional real-time subscription
- 🗺️ [MAP Guide](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/map-guide.md) - Query language, real-time subscriptions, and $edge traversal
- 🗑️ [REMOVE Guide](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/remove-guide.md) - Delete nodes and clean up edges; persistence and notifications
- 🔗 [LINK Guide](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/link-guide.md) - Create directed relationships between nodes

## GenosRTC (P2P Real-time)

- 📡 [GenosRTC API Reference](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosrtc-api-reference.md) - P2P WebRTC API: rooms, data channels, audio/video
- ⚙️ [GenosRTC Architecture](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosrtc-architecture.md) - Technical breakdown of GenosRTC Module architecture, decentralized signaling with Nostr, P2P transport with WebRTC
- 🧭 [GenosRTC Guide](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosrtc-guide.md) - Tutorials for data channels and media streaming
- 🔷 [GenosRTC Cells](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosrtc-cells.md) - Cellular mesh overlay: architecture, bridges, TTL, metrics, and scalability
- 🛰️ [Nostr Relay Deployment Guide](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/nostr-guide.md) - How to run your own Nostr signaling relay for GenosDB/GenosRTC

## Security Manager

- 🔐 [SM API Reference](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/sm-api-reference.md) - RBAC, identity (WebAuthn/mnemonic), signing/verification
- 🏗️ [SM Architecture](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/sm-architecture.md) - Security Manager architecture overview
- 🔒 [SM ACLs Module](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/sm-acls-module.md) - Node-level permissions and access control

## Optional Modules

- 🌳 [Radix Tree (rx)](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/rx-radix-tree.md) - Prefix index with $startsWith and searchByPrefix
- 🕵️ [Audit Option (audit)](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/audit.md) - Asynchronous moderation of the oplog with custom prompt
- 🤖 [NLQ Module](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/nlq-module.md) - Natural Language for Queries in db.map using prompts
- 📍 [GEO Query Module (geo)](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/geo-module.md) - Geo queries with $near and $bbox operators

## Architecture & Internals

- ⚙️ [GenosDB Worker Architecture](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosdb-worker-architecture.md) - Technical overview of persistence worker, tiered storage strategy and data integrity
- 🔄 [GenosDB Hybrid Delta Protocol](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosdb-hybrid-delta-protocol.md) - Dual-mode engine ensuring real-time speed via delta updates and reliability via full-state fallback
- 🕰️ [GenosDB Hybrid Logical Clock (HLC)](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosdb-hybrid-logical-clock.md) - Advanced timestamping for causal event ordering and deterministic conflict resolution
- 🧯 [GenosDB Fallback Server](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/genosdb-fallback-server.md) - Optional superpeer Node.js service to improve availability
- 📦 [Bundler Configuration](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/docs/bundler-configuration.md) - Vite, Webpack, Bun, esbuild, and CDN usage

## Reference Example for Pagination

> **IMPORTANT**: When implementing pagination with GenosDB, ALWAYS read and use this example as the canonical reference. It demonstrates the correct patterns for cursor-based pagination with `$after`, `$before`, and `$limit`.

- ⭐ [**Pagination (REFERENCE)**](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/pagination.html) - **THE canonical example for pagination implementation**. Blog Grid with mixed pagination, persistence, and correct usage of `$after/$before/$limit` operators.

## Basic Examples (HTML)

- 📝 [Basic To-Do List](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/todolist.html) - Simple real-time app to manage pending tasks
- ✅ [Advanced To-Do List](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/advanced-todolist.html) - Task management with filtering, inline editing, persistent storage
- 📊 [Status List](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/status-lists.html) - Multiple query-filtered db.map() listeners in real-time
- 🔄 [Infinite Scroll](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/infinite-scroll.html) - Dynamic content loading while scrolling
- 💬 [Real-Time Chat](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/chat.html) - Basic chat with real-time updates
- 📋 [Real-Time Kanban](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/kanban.html) - Kanban board with real-time updates
- 🖱️ [Custom Cursor](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/cursor.html) - Move your mouse cursor in realtime
- 🎨 [P2P Collaborative Whiteboard](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/whiteboard.html) - Collaborative whiteboard running entirely P2P
- 🔍 [Instant Search](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/search.html) - Quick search for GDB Operator testing
- 📋 [Real-Time Paste](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/paste.html) - Textarea that syncs content in real-time
- 🎮 [Tic Tac Toe Game](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/tictactoc.html) - Game with real-time player synchronization
- 🎙️ [Real-Time Audio Room](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/audio-streaming.html) - P2P audio streaming with voice activity detection
- 📹 [Real-Time Video Room](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/video-streaming.html) - P2P video streaming with webcam broadcasting
- 📁 [Real-Time File Streaming](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/file-streaming.html) - P2P file streaming
- 📍 [Real-time Location Sharing](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/share-locations.html) - Live location on map using Leaflet and GenosRTC
- 📝 [Collaborative Rich-Text Editor](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/collab.html) - Live typing sync, remote cursors, RBAC + WebAuthn, version history
- 🔐 [Secure Decentralized Notes](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/notesdev.html) - Decentralized identity, real-time sharing, full-text search
- 🌡️ [IoT Thermostat Control](/Users/estebanrfp/Projects/Deployments/GDB-Project/GenosDB/examples/thermostat.html) - Real-time P2P thermostat demo with reactive sync
