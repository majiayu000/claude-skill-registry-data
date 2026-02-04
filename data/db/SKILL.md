---
name: db
description: Gère le schéma Prisma et les migrations de Motivia. Utilise ce skill quand l'utilisateur demande de modifier la base de données, ajouter une table, un champ, une relation, ou effectuer une migration. PostgreSQL avec Prisma ORM.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Base de Données Motivia

## Stack technique

- **ORM**: Prisma
- **BDD**: PostgreSQL (Neon)
- **Fichier schema**: `prisma/schema.prisma`

## Commandes Prisma

```bash
# Développement
pnpm prisma generate          # Générer le client Prisma
pnpm prisma migrate dev       # Créer et appliquer une migration
pnpm prisma migrate dev --name add_feature  # Migration nommée
pnpm prisma db push           # Push direct (dev seulement)

# Production
pnpm prisma migrate deploy    # Appliquer les migrations

# Utilitaires
pnpm prisma studio            # Interface graphique
pnpm prisma db seed           # Exécuter le seed
pnpm prisma format            # Formater le schema
```

## Modèles existants

### User (central)

```prisma
model User {
  id                String             @id @default(cuid())
  email             String             @unique
  name              String             @default("")
  firstName         String?
  lastName          String?
  profileTitle      String?
  localisation      String?
  image             String?
  emailVerified     Boolean            @default(false)
  freeLetters       Int                @default(5)
  keyAchievements   String[]
  softSkills        String[]
  technicalSkills   String[]
  createdAt         DateTime           @default(now())
  updatedAt         DateTime           @updatedAt

  // Relations
  accounts          Account[]
  sessions          Session[]
  apiKeys           ApiKey[]
  experiences       Experience[]
  degrees           Degree[]
  links             Link[]
  projects          Project[]
  motivationLetters MotivationLetter[]
  userCV            UserCV?
}
```

### Entités métier

| Modèle | Description | Relation |
|--------|-------------|----------|
| Experience | Expériences pro | User 1:N |
| Degree | Diplômes | User 1:N |
| Project | Projets portfolio | User 1:N |
| Link | Liens sociaux | User 1:N |
| MotivationLetter | Lettres générées | User 1:N |
| UserCV | CV PDF uploadé | User 1:1 |
| ApiKey | Clés API providers | User 1:N |

### Auth (Better Auth)

| Modèle | Description |
|--------|-------------|
| Account | Comptes OAuth/credentials |
| Session | Sessions utilisateur |
| Verification | Tokens de vérification |
| Authenticator | WebAuthn |

## Conventions de schéma

### Champs obligatoires

```prisma
model NouveauModele {
  id        String   @id @default(cuid())
  // ... champs métier
  userId    String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
}
```

### Types courants

| Usage | Type Prisma |
|-------|-------------|
| ID | `String @id @default(cuid())` |
| Email | `String @unique` |
| Texte court | `String` |
| Texte long | `String` (pas de @db.Text nécessaire) |
| Date | `DateTime` |
| Date optionnelle | `DateTime?` |
| Booléen | `Boolean @default(false)` |
| Entier | `Int @default(0)` |
| Liste de strings | `String[]` |

### Relations

```prisma
// 1:N (User a plusieurs Experience)
model User {
  experiences Experience[]
}

model Experience {
  userId String
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
}

// 1:1 (User a un CV)
model User {
  userCV UserCV?
}

model UserCV {
  userId String @unique
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
}
```

### Enum

```prisma
enum ApiProvider {
  OPENAI
  GOOGLE
  ANTHROPIC
  MISTRAL
  XAI
}

model ApiKey {
  provider ApiProvider
}
```

## Workflow modification de schéma

### 1. Modifier le schéma

```prisma
// prisma/schema.prisma
model User {
  // Ajouter un nouveau champ
  newField String?
}
```

### 2. Créer la migration

```bash
pnpm prisma migrate dev --name add_new_field
```

### 3. Mettre à jour le code

- Server actions dans `app/actions/`
- Schémas Zod dans `utils/schemas.ts`

## Ajouter un nouveau modèle

### 1. Définir le modèle

```prisma
model NewEntity {
  id          String   @id @default(cuid())
  name        String
  description String?
  isActive    Boolean  @default(true)
  userId      String
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  user        User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
}
```

### 2. Ajouter la relation dans User

```prisma
model User {
  // ... existing fields
  newEntities NewEntity[]
}
```

### 3. Créer la migration

```bash
pnpm prisma migrate dev --name add_new_entity
```

### 4. Créer les server actions

Créer `app/actions/new-entity.ts` avec le pattern habituel.

## Bonnes pratiques

### Indexes

```prisma
@@index([userId])          // Toujours indexer les FK
@@index([createdAt])       // Si tri fréquent
@@unique([userId, name])   // Contrainte d'unicité
```

### Cascade

Toujours utiliser `onDelete: Cascade` pour les relations avec User afin de supprimer les données orphelines.

### Migrations en production

1. Tester localement avec `migrate dev`
2. Commit des fichiers de migration
3. En production: `migrate deploy` (via script build)

## Checklist nouvelle table

1. [ ] ID avec `@id @default(cuid())`
2. [ ] `createdAt` et `updatedAt`
3. [ ] `userId` avec relation et `onDelete: Cascade`
4. [ ] `@@index([userId])`
5. [ ] Relation ajoutée dans User
6. [ ] Migration créée et testée
7. [ ] Server actions créées
8. [ ] Schéma Zod ajouté
