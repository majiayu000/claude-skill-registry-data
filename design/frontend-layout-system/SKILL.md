---
name: frontend-layout-system
description: Padroniza o visual e a estrutura das páginas frontend do projeto, incluindo landing page, menu, login, cadastros e operações.
---

# Skill: Frontend Layout System

Use esta skill sempre que for criar ou alterar páginas HTML, CSS, JavaScript, React ou Tailwind neste projeto.

## Objetivo

Manter um padrão visual único para todo o sistema, começando simples agora, mas preparado para evoluir para:

- Landing page
- Menu principal
- Login
- Tela de cadastro
- Listagem de registros
- Operações do sistema
- Dashboard futuro

## Identidade visual

O projeto deve seguir um visual:

- moderno
- limpo
- responsivo
- profissional
- fácil de navegar
- com aparência de produto real, não de exercício escolar

## Layout padrão

Toda página deve ter, quando fizer sentido:

1. Header
2. Menu de navegação
3. Área principal
4. Cards ou seções bem separadas
5. Footer
6. Botões padronizados

## Estrutura visual

Usar preferencialmente:

- container centralizado
- espaçamento generoso
- bordas arredondadas
- sombras leves
- boa hierarquia de títulos
- contraste adequado
- layout mobile first

## Cores padrão

Usar como base:

- Primária: azul escuro
- Secundária: azul médio
- Fundo: cinza muito claro ou branco
- Texto principal: cinza escuro
- Texto secundário: cinza médio
- Erro: vermelho
- Sucesso: verde
- Atenção: amarelo/laranja

## Componentes obrigatórios

Sempre que necessário, criar ou reutilizar componentes para:

### Header

Deve conter:

- nome/logo do projeto
- menu principal
- botão de login ou área do usuário

### Menu

Deve prever links para:

- Início
- Login
- Cadastros
- Operações
- Dashboard futuro

### Botões

Padrões:

- botão primário para ações principais
- botão secundário para ações alternativas
- botão de perigo para excluir/cancelar ações críticas

### Formulários

Todo formulário deve ter:

- label visível
- placeholder claro
- validação básica
- mensagem de erro
- botão de envio
- layout responsivo

### Cards

Usar cards para:

- funcionalidades da landing page
- resumo de cadastros
- operações disponíveis
- indicadores futuros

## Regras de código

- Não usar CSS inline.
- Evitar duplicação visual.
- Separar HTML, CSS e JS quando o projeto for vanilla.
- Se usar React, criar componentes reutilizáveis.
- Nomear arquivos e classes de forma clara.
- Manter estrutura simples.
- Não instalar bibliotecas sem autorização.

## Acessibilidade

Toda tela deve respeitar:

- contraste legível
- texto alternativo em imagens
- labels em inputs
- botões com texto claro
- navegação simples por teclado

## Responsividade

As telas devem funcionar bem em:

- celular
- tablet
- desktop

Nunca criar layout que funcione apenas em tela grande.

## Estrutura futura esperada

O projeto poderá evoluir para algo parecido com:

```
src/
  pages/
    index.html
    login.html
    cadastros.html
    operacoes.html
  css/
    styles.css
  js/
    main.js
  assets/
    images/
```

## Passos para criar uma nova página

1. **Entender o contexto** — qual é a finalidade da página (listagem, formulário, dashboard)?
2. **Reaproveitar o padrão** — usar o mesmo header, menu e footer das outras páginas.
3. **Criar o HTML** no diretório correto dentro de `src/public/` ou `src/pages/`.
4. **Separar o CSS** em `src/css/styles.css` se o projeto já tiver esse arquivo; caso contrário, usar `<style>` no próprio HTML.
5. **Separar o JS** em `src/js/main.js` se o projeto já tiver esse arquivo; caso contrário, usar `<script>` no próprio HTML.
6. **Conectar à API** via `fetch`, seguindo os endpoints documentados no Swagger (`/api-docs`).
7. **Testar nos três tamanhos** — celular, tablet e desktop — antes de considerar pronto.
