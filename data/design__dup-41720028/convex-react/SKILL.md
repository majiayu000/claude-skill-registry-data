---
name: convex-react
description: Convex React client - hooks, real-time updates, optimistic updates, pagination, and UI patterns
globs:
  - "**/*.tsx"
  - "**/*.ts"
  - "src/**/*"
triggers:
  - useQuery
  - useMutation
  - useAction
  - usePaginatedQuery
  - convex/react
  - ConvexProvider
  - ConvexReactClient
  - optimistic
  - skip
  - real-time
  - loading state
---

# Convex React Client Guide

Complete React client guidelines for Convex, including hooks, real-time updates, optimistic updates, and best practices for building reactive UIs.

---

# Basic React Integration

## Complete Example

```tsx
import React, { useState } from "react";
import { useMutation, useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

export default function App() {
  const messages = useQuery(api.messages.list) || [];

  const [newMessageText, setNewMessageText] = useState("");
  const sendMessage = useMutation(api.messages.send);

  const [name] = useState(() => "User " + Math.floor(Math.random() * 10000));

  async function handleSendMessage(event: React.FormEvent) {
    event.preventDefault();
    await sendMessage({ body: newMessageText, author: name });
    setNewMessageText("");
  }

  return (
    <main>
      <h1>Convex Chat</h1>
      <p className="badge">
        <span>{name}</span>
      </p>
      <ul>
        {messages.map((message) => (
          <li key={message._id}>
            <span>{message.author}:</span>
            <span>{message.body}</span>
            <span>{new Date(message._creationTime).toLocaleTimeString()}</span>
          </li>
        ))}
      </ul>
      <form onSubmit={handleSendMessage}>
        <input
          value={newMessageText}
          onChange={(event) => setNewMessageText(event.target.value)}
          placeholder="Write a message..."
        />
        <button type="submit" disabled={!newMessageText}>
          Send
        </button>
      </form>
    </main>
  );
}
```

---

# useQuery Hook

## Real-time Updates

The `useQuery()` hook is live-updating! It causes the React component to rerender automatically when data changes. Convex is a perfect fit for collaborative, live-updating websites.

## Return Values

- `undefined` - Query is loading
- `null` - Query returned null (e.g., user not found)
- `data` - Query returned data

```tsx
function UserProfile({ userId }: { userId: Id<"users"> }) {
  const user = useQuery(api.users.get, { userId });

  // Loading state
  if (user === undefined) {
    return <div>Loading...</div>;
  }

  // Not found
  if (user === null) {
    return <div>User not found</div>;
  }

  // Data loaded
  return <div>{user.name}</div>;
}
```

---

# Conditional Queries with "skip"

## CRITICAL: Never Use Hooks Conditionally

```tsx
// WRONG - Will cause React hook errors!
const avatarUrl = profile?.avatarId
  ? useQuery(api.profiles.getAvatarUrl, { storageId: profile.avatarId })
  : null;

// CORRECT - Use "skip" to conditionally skip the query
const avatarUrl = useQuery(
  api.profiles.getAvatarUrl,
  profile?.avatarId ? { storageId: profile.avatarId } : "skip"
);
```

## More Examples

```tsx
function Dashboard() {
  const user = useQuery(api.auth.loggedInUser);

  // Skip queries until we have user data
  const userPosts = useQuery(
    api.posts.getByUser,
    user ? { userId: user._id } : "skip"
  );

  const userSettings = useQuery(
    api.settings.get,
    user ? { userId: user._id } : "skip"
  );

  if (user === undefined) {
    return <Loading />;
  }

  if (user === null) {
    return <LoginPrompt />;
  }

  return (
    <div>
      <PostList posts={userPosts || []} />
      <Settings settings={userSettings} />
    </div>
  );
}
```

---

# useMutation Hook

## Basic Usage

```tsx
function CreatePost() {
  const createPost = useMutation(api.posts.create);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      await createPost({ title, content });
      setTitle("");
      setContent("");
    } catch (error) {
      console.error("Failed to create post:", error);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Title"
        disabled={isSubmitting}
      />
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Content"
        disabled={isSubmitting}
      />
      <button type="submit" disabled={isSubmitting || !title || !content}>
        {isSubmitting ? "Creating..." : "Create Post"}
      </button>
    </form>
  );
}
```

---

# useAction Hook

```tsx
import { useAction } from "convex/react";
import { api } from "../convex/_generated/api";

function AIChat() {
  const generateResponse = useAction(api.ai.generateResponse);
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setIsLoading(true);

    try {
      const result = await generateResponse({ prompt });
      setResponse(result);
    } catch (error) {
      console.error("AI generation failed:", error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Ask AI..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !prompt}>
          {isLoading ? "Thinking..." : "Ask"}
        </button>
      </form>
      {response && <p>{response}</p>}
    </div>
  );
}
```

---

# Importing the API Object

When writing a UI component and you want to use a Convex function, you MUST import the `api` object:

```tsx
import { api } from "../convex/_generated/api";
```

You can use the `api` object to call any public Convex function.

Always make sure:
1. The functions you are calling are defined in the `convex/` directory
2. Use the `api` object for public functions
3. You are using the correct arguments for convex functions
4. If arguments are not optional, make sure they are not null

---

# Pagination with usePaginatedQuery

```tsx
import { usePaginatedQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function InfiniteMessageList({ channelId }: { channelId: Id<"channels"> }) {
  const { results, status, loadMore } = usePaginatedQuery(
    api.messages.list,
    { channelId },
    { initialNumItems: 20 }
  );

  return (
    <div>
      {results.map((message) => (
        <div key={message._id}>{message.content}</div>
      ))}

      {status === "CanLoadMore" && (
        <button onClick={() => loadMore(20)}>Load More</button>
      )}

      {status === "LoadingMore" && <div>Loading...</div>}

      {status === "Exhausted" && <div>No more messages</div>}
    </div>
  );
}
```

---

# Optimistic Updates

```tsx
import { useMutation, useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function TodoList() {
  const todos = useQuery(api.todos.list) || [];
  const toggleTodo = useMutation(api.todos.toggle).withOptimisticUpdate(
    (localStore, args) => {
      const currentTodos = localStore.getQuery(api.todos.list);
      if (currentTodos !== undefined) {
        const updatedTodos = currentTodos.map((todo) =>
          todo._id === args.id
            ? { ...todo, completed: !todo.completed }
            : todo
        );
        localStore.setQuery(api.todos.list, {}, updatedTodos);
      }
    }
  );

  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo._id}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => toggleTodo({ id: todo._id })}
          />
          {todo.title}
        </li>
      ))}
    </ul>
  );
}
```

---

# Error Handling

```tsx
function PostForm() {
  const createPost = useMutation(api.posts.create);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(data: FormData) {
    setError(null);

    try {
      await createPost({
        title: data.get("title") as string,
        content: data.get("content") as string,
      });
    } catch (e) {
      if (e instanceof Error) {
        setError(e.message);
      } else {
        setError("An unexpected error occurred");
      }
    }
  }

  return (
    <form action={handleSubmit}>
      {error && <div className="error">{error}</div>}
      {/* form fields */}
    </form>
  );
}
```

---

# Loading States Pattern

```tsx
function DataComponent() {
  const data = useQuery(api.data.get);

  // Pattern 1: Simple loading check
  if (data === undefined) {
    return <Skeleton />;
  }

  // Pattern 2: With null check
  if (data === null) {
    return <NotFound />;
  }

  return <DataView data={data} />;
}
```

---

# File Upload Pattern

```tsx
function ImageUploader() {
  const generateUploadUrl = useMutation(api.files.generateUploadUrl);
  const saveFile = useMutation(api.files.save);
  const [uploading, setUploading] = useState(false);

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);

    try {
      // Step 1: Get upload URL
      const uploadUrl = await generateUploadUrl();

      // Step 2: Upload file
      const result = await fetch(uploadUrl, {
        method: "POST",
        headers: { "Content-Type": file.type },
        body: file,
      });

      if (!result.ok) {
        throw new Error("Upload failed");
      }

      const { storageId } = await result.json();

      // Step 3: Save reference to database
      await saveFile({ storageId, fileName: file.name });

    } catch (error) {
      console.error("Upload error:", error);
    } finally {
      setUploading(false);
    }
  }

  return (
    <input
      type="file"
      onChange={handleFileChange}
      disabled={uploading}
    />
  );
}
```

---

# Image Display with Storage URLs

```tsx
function ImageGallery() {
  const images = useQuery(api.images.list) || [];

  return (
    <div className="grid grid-cols-3 gap-4">
      {images.map((image) => (
        <ImageWithUrl key={image._id} storageId={image.storageId} />
      ))}
    </div>
  );
}

function ImageWithUrl({ storageId }: { storageId: Id<"_storage"> }) {
  const url = useQuery(api.files.getUrl, { storageId });

  if (url === undefined) {
    return <div className="animate-pulse bg-gray-200 h-48" />;
  }

  if (url === null) {
    return <div>Image not found</div>;
  }

  return <img src={url} alt="" className="w-full h-48 object-cover" />;
}
```

---

# Provider Setup

```tsx
// main.tsx or _app.tsx
import { ConvexProvider, ConvexReactClient } from "convex/react";
import { ConvexAuthProvider } from "@convex-dev/auth/react";

const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

function App() {
  return (
    <ConvexAuthProvider client={convex}>
      <YourApp />
    </ConvexAuthProvider>
  );
}
```

---

# Best Practices

## 1. Never Call Hooks Conditionally

```tsx
// WRONG
if (isLoggedIn) {
  const data = useQuery(api.data.get);
}

// CORRECT
const data = useQuery(api.data.get, isLoggedIn ? {} : "skip");
```

## 2. Handle All States

```tsx
function DataDisplay() {
  const data = useQuery(api.data.get);

  // Always handle: undefined (loading), null (not found), and data
  if (data === undefined) return <Loading />;
  if (data === null) return <NotFound />;
  return <Content data={data} />;
}
```

## 3. Use TypeScript Properly

```tsx
import { Id } from "../convex/_generated/dataModel";

interface Props {
  userId: Id<"users">;  // Use Id<> type, not string
}
```

## 4. Avoid Prop Drilling with Queries

```tsx
// Instead of passing data through many components,
// query it where needed
function DeepNestedComponent({ itemId }: { itemId: Id<"items"> }) {
  // Query directly in the component that needs it
  const item = useQuery(api.items.get, { id: itemId });
  // ...
}
```

## 5. Do NOT Use External UI Libraries Unless Specified

If you want to use a UI element, you MUST create it. DO NOT use external libraries like Shadcn/UI unless explicitly asked.

## 6. Do NOT Use sharp for Image Compression

Always use `canvas` for image compression, not `sharp`.
