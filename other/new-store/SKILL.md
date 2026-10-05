---
name: new-store
description: Use this skill when the user asks to create a new Pinia store for TrackGrowth domain data (habits, check-ins, tags, gamification profile). Triggers on "criar store", "novo store", "new store", "novo pinia store".
---

# Criar novo store Pinia

Segue as convenções documentadas em [docs/context/06-file-structure-conventions.md](../../../docs/context/06-file-structure-conventions.md), [docs/context/02-domain-model.md](../../../docs/context/02-domain-model.md) (entidades) e [docs/context/05-architecture.md](../../../docs/context/05-architecture.md) (Pinia + `pinia-plugin-persistedstate`).

## Passos

1. **Confirme que `pinia-plugin-persistedstate` já está instalado e registrado** no `main.ts` (`pinia.use(piniaPluginPersistedstate)`). Se ainda não estiver, adicione a dependência e o registro antes de criar o store — não crie stores "persist: true" sem o plugin configurado, pois falham silenciosamente.

2. **Local do arquivo**: pasta própria `src/stores/<entidade>/`, no plural quando a entidade é uma coleção (ex: `stores/habits/`, `stores/checkins/`, `stores/tags/`) ou singular quando é um perfil único (ex: `stores/gamification/`), contendo:

   ```
   stores/
     entidade/
       index.ts        # exporta useEntidadeStore (defineStore)
       tests/
         entidade.spec.ts
   ```

3. **Estrutura do arquivo** (Setup Store, consistente com o resto do projeto usar Composition API) — vai em `stores/entidade/index.ts`:

   ```ts
   import { defineStore } from "pinia";
   import { computed, ref } from "vue";

   import type { Entidade } from "@/types/entidade.types";

   export const useEntidadeStore = defineStore(
     "entidade",
     () => {
       const items = ref<Entidade[]>([]);

       const activeItems = computed(() => items.value.filter(item => item.status === "active"));

       function add(item: Entidade) {
         items.value.push(item);
       }

       return { items, activeItems, add };
     },
     {
       persist: true,
     },
   );
   ```

   - O primeiro argumento de `defineStore` (id) deve ser único e em `camelCase`/`kebab-case` simples, sem prefixo `use` (isso é o nome exportado da função, não o id).
   - Use o tipo já definido em [02-domain-model.md](../../../docs/context/02-domain-model.md) (`src/types/`) para o estado — não redeclare a interface dentro do store.
   - Getters derivados (ex: streak, % de conclusão) que dependem de **múltiplos** stores (ex: `habits` + `checkins`) não devem morar dentro de um único store — extraia para um composable que combina os stores (ex: `useStreak/`), mantendo cada store focado na sua própria entidade.

4. **Regras de negócio com validação** (ex: janela de edição retroativa de 7 dias, ver [02-domain-model.md](../../../docs/context/02-domain-model.md#3-edição-retroativa-janela-de-7-dias)) devem ser aplicadas dentro das actions do store, não confiadas à camada de UI — a UI pode desabilitar botões como reforço visual, mas a validação real fica na action.

5. **Após criar `index.ts`**, criar `tests/<entidade>.spec.ts` cobrindo getters e actions — não é opcional. Depois, rode `yarn lint:fix`.

## O que não fazer

- Não use a Options API do Pinia (`state`/`getters`/`actions` como objeto) — este projeto usa exclusivamente Setup Stores, consistente com `<script setup>` no restante do código.
- Não persista estado derivado/computado — apenas o estado bruto (`ref`) deve ser persistido; `computed` é sempre recalculado a partir dele.
- Não crie um store para preferências simples de UI (tema, filtro selecionado) — isso é papel de um composable com `useStorage` do VueUse (ver skill `/new-composable`).
