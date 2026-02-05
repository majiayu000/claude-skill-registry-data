---
name: joke-fetcher
description: Fetch random jokes from JokeAPI using a Bun CLI script. Use when users ask for a random joke, want jokes by category, or need a quick joke via the JokeAPI endpoint.
---

# Joke Fetcher

Fetch a random joke from JokeAPI via a Bun CLI script.

## Guidelines

- Run the script as a black box; do not read or modify its internals.
- For API details or new endpoints, read `./references/jokeapi.md`.

## Usage

Run the script with Bun. Optionally pass a category or safe flag.

## Actions

### Get a random joke

Note: `./get-joke.js` is relative to `SKILL.md`

```shell
bun ./get-joke.js
```

### Get a joke from a category

```shell
bun ./get-joke.js Programming
```

### Get a safer joke

```shell
bun ./get-joke.js --category Programming --safe
```