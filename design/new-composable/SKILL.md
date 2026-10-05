---
name: new-composable
description: Use this skill when the user asks to create a new composable (useX) for the TrackGrowth app — reusable reactive logic such as frequency evaluation, streak calculation, theme, or backup. Triggers on "criar composable", "novo composable", "new composable", "useX".
---

# Criar novo composable

Segue as convenções documentadas em [docs/context/06-file-structure-conventions.md](../../../docs/context/06-file-structure-conventions.md) e [docs/context/05-architecture.md](../../../docs/context/05-architecture.md) (divisão Pinia vs `useStorage`).

## Passos

1. **Local do arquivo**: pasta própria `src/composables/useX/`, nome em `camelCase` prefixado com `use` (ex: `composables/useHabitFrequency/`, `composables/useStreak/`), contendo:

   ```
   composables/
     useX/
       index.ts
       tests/
         useX.spec.ts
       models/          # opcional, só se houver tipos locais ao composable
   ```

2. **Antes de criar, decida se é realmente um composable ou deveria ser um store Pinia** (use a skill `/new-store` nesse caso):
   - **Composable**: lógica reativa reutilizável sem necessidade de estado compartilhado entre componentes distantes na árvore, ou wrapper fino sobre `useStorage` do VueUse para uma preferência simples de UI (tema, filtro selecionado).
   - **Store Pinia**: dados de domínio que precisam ser acessados/mutados por múltiplos componentes não relacionados (hábitos, check-ins, tags, gamificação).

3. **Estrutura do `index.ts`:**

   ```ts
   import { computed, ref } from "vue";

   export function useX() {
     const state = ref();

     const derived = computed(() => {
       // lógica derivada
     });

     function action() {
       // lógica de ação
     }

     return { state, derived, action };
   }
   ```

   - Se o composable envolve lógica de negócio pura (cálculo de streak, avaliação de `FrequencyRule`), extraia a função pura para `src/utils/` (ex: `frequency-evaluator.ts`) e deixe o composable como uma casca reativa fina em cima dela — facilita testar a lógica isoladamente sem montar um componente Vue.
   - Se o composable precisa de tipos próprios além dos já definidos em `src/types/`, adicione-os lá, não inline no composable.

4. **Composables de preferência de UI** (ex: `useTheme`): usar `useStorage` do VueUse diretamente, com uma chave de `localStorage` clara e namespaced (ex: `trackgrowth:theme`), para não colidir com as chaves usadas pelo `pinia-plugin-persistedstate` dos stores de domínio.

5. **Após criar `index.ts`**, criar `tests/useX.spec.ts` cobrindo o estado/derivações/ações expostos — não é opcional. Depois, rode `yarn lint:fix`.

## O que não fazer

- Não crie um composable que só reexporta um store Pinia sem adicionar lógica — importe o store diretamente no componente nesse caso.
- Não guarde dados de domínio (hábitos, check-ins) dentro de um composable com `useStorage` — isso é responsabilidade dos stores Pinia persistidos, que oferecem getters/ações compartilhados.
