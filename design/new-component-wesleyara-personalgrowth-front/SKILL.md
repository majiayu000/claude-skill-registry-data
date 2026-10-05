---
name: new-component
description: Use this skill when the user asks to create a new Vue component for the TrackGrowth app (habit, dashboard, gamification, common UI, or a page/view). Triggers on "criar componente", "novo componente", "nova view", "nova página", "new component", "new view".
---

# Criar novo componente Vue

Segue as convenções documentadas em [docs/context/06-file-structure-conventions.md](../../../docs/context/06-file-structure-conventions.md) e no styleguide ONR (https://styleguide.onr.org.br/v2/guide/best-practices/).

## Passos

1. **Determine o tipo e local do arquivo:**
   - Página/rota completa → arquivo único `src/views/<Nome>View.vue`, e adicionar a rota correspondente em `src/router.ts`. Views **não** seguem o padrão pasta-por-item abaixo.
   - Componente de domínio → pasta própria `src/components/<domínio>/<Nome>/`, onde `<domínio>` é um de `habit`, `dashboard`, `gamification` ou `common` (genérico/reutilizável, sem lógica de domínio). Se a pasta do domínio ainda não existir, crie-a. Estrutura:

     ```
     components/
       <dominio>/
         <Nome>/
           components/
             <Nome>.vue
           tests/
             <Nome>.spec.ts
           index.ts        # barrel: export { default } from "./components/<Nome>.vue";
           models/          # opcional, só se houver tipos locais ao componente
     ```
   - Se não estiver claro qual domínio o componente pertence, pergunte ao usuário antes de criar o arquivo.

2. **Nome do componente**: sempre `PascalCase`, descritivo do que o componente faz (não do domínio, já que a pasta cobre isso) — ex: `StreakCard` dentro de `dashboard/`, não `DashboardStreakCard`.

3. **Estrutura do `.vue`** (dentro de `<Nome>/components/<Nome>.vue`, ou diretamente em `src/views/<Nome>View.vue` para views) — use `<script setup lang="ts">`, tipar props/emits explicitamente quando existirem:

   ```vue
   <script setup lang="ts">
   interface Props {
     // props tipadas aqui, se houver
   }

   defineProps<Props>();
   </script>

   <template>
     <div></div>
   </template>
   ```

   - Não adicionar `<style scoped>` a menos que Tailwind não seja suficiente para o caso (raro) — este projeto usa Tailwind utility-first.
   - Emits, quando existirem, com `defineEmits<{ eventName: [payload: Tipo] }>()`.

4. **Classes Tailwind**: escreva na ordem natural, o `eslint-plugin-tailwindcss` corrige a ordem automaticamente no lint — não perca tempo ordenando manualmente. Use os tokens de cor já definidos em `tailwind.config.js` (`bluewood`, `brand-blue`) em vez de cores arbitrárias, a menos que o usuário peça uma nova cor (nesse caso, sugira adicionar ao `tailwind.config.js` em vez de usar valor arbitrário inline).

5. **Se o componente precisar de estado de domínio** (hábitos, check-ins, tags, gamificação), importe o store Pinia correspondente (ver skill `/new-store` se o store ainda não existir) — não duplique lógica de negócio dentro do componente; lógica de cálculo (streak, frequência devida, etc.) pertence a composables/utils, não à camada de view.

6. **Após criar o `.vue`**, criar o `index.ts` (barrel) e, para componentes de domínio (não views), `tests/<Nome>.spec.ts` — não é opcional. Depois, rode `yarn lint:fix` para aplicar ordenação de imports e classes Tailwind automaticamente.

## O que não fazer

- Não crie componentes fora da estrutura de pastas por domínio sem justificativa.
- Não use Options API — este projeto é 100% Composition API com `<script setup>`.
- Não adicione dependências novas (bibliotecas de UI, ícones extras) sem confirmar com o usuário — o projeto já usa `oh-vue-icons` para ícones.
