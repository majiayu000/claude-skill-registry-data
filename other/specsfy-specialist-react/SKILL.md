---
name: specsfy-specialist-react
description: Projetar, implementar e revisar interfaces React com composição, estado, efeitos, concorrência, acessibilidade, performance e testes. Use quando a tarefa envolve componentes React, hooks, context, forms ou renderização cliente; use a skill Next.js quando o framework definir fronteiras server/client.
---

# React

## Fluxo

1. Confirmar versão, renderer, framework, convenções e estratégia de testes.
2. Modelar estados visíveis, eventos, dados remotos e ownership.
3. Projetar uma árvore de componentes com responsabilidades e props pequenas.
4. Manter estado no owner mais próximo e derivar valores durante render.
5. Usar effects apenas para sincronização com sistemas externos.
6. Implementar semântica e teclado antes do acabamento visual.
7. Testar comportamento observável e medir performance quando houver evidência.

## Padrões

- Preferir composição a componentes com dezenas de flags.
- Não copiar props para state nem usar effect para computação derivável.
- Tornar loading, empty, error, stale, optimistic e success explícitos.
- Preservar identidade com keys estáveis; nunca índice quando a ordem muda.
- Isolar context por frequência e responsabilidade para evitar acoplamento global.
- Evitar memoização sem medição e callbacks estáveis sem consumidor sensível.
- Testar pela experiência do usuário, não por detalhes de hooks.

## Validação

- Interações por teclado e leitor de tela na superfície alterada.
- Testes de estados, erros, concorrência e recuperação.
- Verificação de warnings, hydration quando aplicável e cleanup.
- Profiling ou bundle analysis somente quando a hipótese exigir.

Leia [references/standards.md](references/standards.md) para estado, effects,
composição, acessibilidade, testes e performance.
