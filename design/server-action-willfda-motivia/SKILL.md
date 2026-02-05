---
name: server-action
description: Crée des Server Actions pour Motivia. Utilise ce skill quand l'utilisateur demande une action serveur, une mutation, un CRUD, ou une opération base de données. Suit le pattern next-safe-action avec gestion d'erreurs typée.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Server Actions Motivia

## Structure des fichiers

```
app/actions/
├── user-api-key.ts          # Gestion clés API
├── user-cv.ts               # Upload/gestion CV
├── user-degrees.ts          # Diplômes
├── user-experiences.ts      # Expériences pro
├── user-informations.ts     # Infos profil
├── user-links.ts            # Liens portfolio
├── user-motivation-letters.ts  # Lettres de motivation
└── preferences.ts           # Préférences utilisateur
```

## Deux patterns disponibles

### 1. `authQuery` - Pour les lectures simples

Utilisé pour les requêtes de lecture sans validation d'input:

```typescript
"use server";

import { authQuery } from "@/lib/auth-session";
import { prisma } from "@/lib/prisma";

export const getAllUserItems = async () =>
  authQuery(async (userId) => {
    try {
      const response = await prisma.item.findMany({
        where: { userId },
        orderBy: { createdAt: "desc" },
        select: {
          id: true,
          name: true,
          createdAt: true,
        },
      });
      return response;
    } catch (error) {
      console.error("Database error:", error);
      throw new Error("FAILED_TO_FETCH_ITEMS");
    }
  });
```

### 2. `authActionClient` - Pour les mutations avec validation

Utilisé pour les mutations (create, update, delete) avec validation Zod:

```typescript
"use server";

import z from "zod/v4";
import { prisma } from "@/lib/prisma";
import { ActionError, authActionClient } from "@/lib/safe-action";

// Action sans input
export const getCount = authActionClient.action(
  async ({ ctx: { userId } }) => {
    try {
      const response = await prisma.user.findUnique({
        where: { id: userId },
        select: { count: true },
      });
      return response?.count;
    } catch (error) {
      console.error("Database error:", error);
      throw new ActionError("FAILED_TO_FETCH_COUNT");
    }
  }
);

// Action avec input simple (string, number)
export const deleteItem = authActionClient
  .inputSchema(z.string())
  .action(async ({ parsedInput: id, ctx: { userId } }) => {
    try {
      const response = await prisma.item.delete({
        where: { id, userId },
      });
      return response;
    } catch (error) {
      console.error("Database error:", error);
      throw new ActionError("FAILED_TO_DELETE_ITEM");
    }
  });

// Action avec input objet
export const createItem = authActionClient
  .inputSchema(
    z.object({
      id: z.string().optional(),
      name: z.string().min(1),
      description: z.string().optional(),
    })
  )
  .action(async ({ parsedInput, ctx: { userId } }) => {
    try {
      const { id, name, description } = parsedInput;

      if (id) {
        // Update
        return prisma.item.update({
          where: { id, userId },
          data: { name, description },
        });
      }

      // Create
      return prisma.item.create({
        data: { name, description, userId },
      });
    } catch (error) {
      console.error("Database error:", error);
      throw new ActionError("FAILED_TO_SAVE_ITEM");
    }
  });
```

## Conventions de nommage

| Opération | Préfixe | Exemple |
|-----------|---------|---------|
| Lecture unique | `get` | `getUserProfile` |
| Lecture multiple | `getAll` | `getAllUserExperiences` |
| Création | `create` / `add` | `createExperience` |
| Mise à jour | `update` | `updateUserInfo` |
| Création/MAJ | `save` | `saveMotivationLetter` |
| Suppression | `delete` | `deleteExperience` |
| Action métier | verbe | `decrementFreeLetters` |

## Gestion des erreurs

### Codes d'erreur standards

```typescript
// Format: ACTION_FAILED_TO_VERB_ENTITY
throw new ActionError("FAILED_TO_FETCH_USER");
throw new ActionError("FAILED_TO_CREATE_EXPERIENCE");
throw new ActionError("FAILED_TO_UPDATE_PROFILE");
throw new ActionError("FAILED_TO_DELETE_LETTER");
```

### Traduction côté client

Les codes d'erreur sont traduits via i18n dans `locales/fr.ts` et `locales/en.ts`.

## Schémas Zod

Placer les schémas réutilisables dans `utils/schemas.ts`:

```typescript
// utils/schemas.ts
import z from "zod/v4";

export const experienceSchema = z.object({
  id: z.string().optional(),
  job: z.string().min(1),
  companyName: z.string().min(1),
  description: z.string().optional(),
  startDate: z.date(),
  endDate: z.date().optional(),
  isCurrent: z.boolean().default(false),
});

export type ExperienceInput = z.infer<typeof experienceSchema>;
```

## Utilisation côté client

```typescript
"use client";

import { useAction } from "next-safe-action/hooks";
import { deleteItem } from "@/app/actions/items";

export const ItemList = () => {
  const { execute, isPending } = useAction(deleteItem, {
    onSuccess: () => {
      // Refresh data
    },
    onError: (error) => {
      // Handle error
    },
  });

  return (
    <button
      type="button"
      disabled={isPending}
      onClick={() => execute("item-id")}
    >
      Delete
    </button>
  );
};
```

## Checklist nouvelle action

1. [ ] Fichier commence par `"use server";`
2. [ ] Import depuis `@/lib/safe-action` ou `@/lib/auth-session`
3. [ ] Schéma Zod pour validation input (si mutation)
4. [ ] Try/catch avec `console.error` et `ActionError`
5. [ ] Code d'erreur en SCREAMING_SNAKE_CASE
6. [ ] `select` explicite pour Prisma (pas de `select: *`)
7. [ ] Toujours vérifier `userId` dans les clauses `where`
