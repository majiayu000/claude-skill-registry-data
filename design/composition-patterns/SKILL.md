---
name: composition-patterns
description: Padroes de composicao React que escalam. Usar quando refatorar componentes com muitas props booleanas, construir bibliotecas de componentes, ou projetar APIs reutilizaveis.
---

# Padroes de Composicao React -- Padrao DME

Substituir proliferacao de props booleanas por composicao.

## Padroes recomendados

### 1. Compound Components
Componente pai + filhos com estado compartilhado via Context.
Usar quando: componente tem multiplas partes opcionais.

### 2. Hooks Customizados
Extrair logica reutilizavel em hooks.
Usar quando: logica se repete entre componentes.

### 3. Polymorphic as Prop
Componente que renderiza como qualquer elemento HTML.
Usar quando: precisa flexibilidade de semantica.

## Regras DME

- Preferir composicao sobre configuracao
- Maximo 5 props por componente (fora children e className)
- Se tem mais de 3 variantes booleanas, refatorar pra compound component
- Nunca usar any nos tipos
- Sem emojis em nenhum texto de UI
- Icones via Lucide/Heroicons, nunca emojis
