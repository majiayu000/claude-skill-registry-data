---
name: taxonomy
description: Design and maintain a knowledge taxonomy of concepts, terms, categories, relationships, synonyms, and ownership so information remains findable without forcing one rigid hierarchy onto every use case.
---
# Knowledge Taxonomy

Use when inconsistent naming or categorization makes knowledge difficult to search, connect, or maintain.

## Procedure
1. Inventory the audience language, recurring concepts, product areas, processes, entities, and queries the taxonomy must support.
2. Define canonical terms and relationships while recording important synonyms, abbreviations, deprecated terms, and aliases used in existing material.
3. Separate hierarchical relationships from tags, facets, and cross-domain relationships where one tree cannot represent the knowledge accurately.
4. Keep categories mutually understandable and avoid catch-all buckets that hide ownership or meaning.
5. Define rules for adding, renaming, merging, and retiring terms and identify downstream search, links, analytics, or automation affected by changes.
6. Map terms to authoritative owners or source systems where terminology has formal product, legal, technical, or business meaning.
7. Test the taxonomy against real search and filing tasks and note where users consistently choose a different concept than the designer expected.
8. Review for drift as products, teams, and language evolve.

## Decision rules
- Taxonomy should support retrieval and shared meaning, not model the organization for its own sake.
- Synonyms are valuable evidence about how people actually search.
- One item can need several facets without belonging to several contradictory canonical categories.
- Renames can be compatibility changes for links, search, and automation.

## Quality gate
The taxonomy is ready when common concepts have clear canonical names and useful aliases, relationships fit real retrieval needs, ambiguous catch-alls are minimized, change governance exists, and users can classify and find content with fewer competing interpretations.