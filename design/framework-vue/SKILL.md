---
name: "framework-vue"
description: "Fornece padrões de desenvolvimento modular e de alta performance usando o ecossistema Vue 3, cobrindo Composition API, TypeScript, Pinia, Vue Router e otimizações de reatividade."
---

# Habilidade de IA: Engenharia de Vue.js (Vue Specialist)

Esta skill orienta a inteligência artificial a agir como especialista no desenvolvimento de aplicações web modernas e reativas utilizando o ecossistema **Vue 3**. O objetivo principal é guiar a IA e desenvolvedores a desenhar componentes reutilizáveis, gerenciar estados eficientemente com Pinia e aplicar a Composition API de forma performática e tipada.

---

## 🧭 Diretrizes de Desenvolvimento Vue 3

Ao atuar nesta skill, paute o desenvolvimento de código sob as seguintes práticas:

### 1. Composition API & `<script setup>`
- **Prática Padrão**: Sempre utilize a Composition API com a sintaxe `<script setup>` por ser mais limpa, performática e possuir suporte nativo superior para tipagem TypeScript.
- **Reatividade Clara**: Utilize `ref` para dados primitivos reativos isolados e `reactive` exclusivamente para objetos complexos ou estados internos coesos de componentes.
- **Computed vs Watch**:
  - Use `computed` para derivar ou transformar estados de forma síncrona com caching nativo automático.
  - Use `watch` ou `watchEffect` apenas para efeitos colaterais assíncronos ou imperativos externos (ex: chamadas de API, salvar no localStorage).

### 2. Gerenciamento de Estado Global com Pinia
- **Pinia Stores**: Substitua o Vuex antigo pelo Pinia. Defina stores focadas e modulares (ex: `useAuthStore`, `useCartStore`) utilizando a sintaxe de Setup (com `ref` e `computed`) para manter paridade com a Composition API.
- **Desestruturação Segura**: Nunca desestruture propriedades reativas da store diretamente sem utilizar `storeToRefs` do Pinia, para evitar quebrar a reatividade nativa do Vue.

### 3. Otimização de Performance no Vue
- **Ciclo de Vida de Componentes**: Limpe ouvintes de eventos manuais (`window.addEventListener`), timers (`setInterval`) ou conexões Websocket nos hooks `onUnmounted` ou `onBeforeUnmount` para evitar vazamentos de memória.
- **Virtualização de Listas**: Em listas extensas (mais de 100 itens), prefira técnicas de virtualização de DOM (ex: `vue-virtual-scroller`) em vez de renderizar todos os elementos com `v-for`.
- **v-if vs v-show**: Use `v-if` quando a alternância for rara (evitando renderizar o nó no DOM) e `v-show` quando o elemento alternar de visibilidade frequentemente.

---

## 🛠️ Padrões de Código Recomendados (TypeScript Integrado)

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

// Definição de Props tipadas estritamente
const props = defineProps<{
  title: string;
  initialCount?: number;
}>();

// Definição de Emits tipados
const emit = defineEmits<{
  (e: 'update', count: number): void;
}>();

// Estados reativos
const count = ref(props.initialCount ?? 0);

// Estado derivado reativo (Computed)
const doubledCount = computed(() => count.value * 2);

function increment() {
  count.value++;
  emit('update', count.value);
}
</script>

<template>
  <div class="counter-card">
    <h3>{{ title }}</h3>
    <p>Contador: {{ count }} (Dobro: {{ doubledCount }})</p>
    <button @click="increment">Incrementar</button>
  </div>
</template>

<style scoped>
.counter-card {
  padding: 1rem;
  border-radius: 8px;
  background: var(--bg-surface);
}
</style>
```

---

## 🔗 Integração com Outras Skills
- [frontend-developer](../../roles/frontend-developer/SKILL.md): Utiliza as diretrizes Vue para orquestrar componentes e implementar o Design System visual do projeto.
- [tech-typescript](../../languages/lang-typescript/SKILL.md): Fornece os tipos estruturais que validam props e stores do Vue.
