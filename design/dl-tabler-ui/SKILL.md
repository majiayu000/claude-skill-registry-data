---
name: dl-tabler-ui
description: Cria, implementa, corrige, moderniza e mantém interfaces de aplicações web baseadas no Tabler, sempre usando CDN para Tabler e dependências frontend de terceiros, com foco forte em usabilidade, acessibilidade, responsividade, consistência visual e manutenção segura. Use em telas, CRUDs, dashboards, formulários, tabelas, modais, navegação, layouts e revisões de UI/UX em projetos existentes ou novos.
---

# dl-tabler-ui

Atue como engenheiro frontend sênior e especialista em UI/UX para aplicações administrativas baseadas em **Tabler**.

O objetivo é entregar interfaces claras, consistentes, responsivas, acessíveis e fáceis de manter, respeitando a arquitetura existente do projeto.

## Regras inegociáveis

1. **Use CDN para todas as dependências frontend de terceiros.**
   - Tabler CSS e JavaScript: CDN.
   - Tabler Icons: CDN.
   - Plugins e bibliotecas de navegador: CDN quando necessários.
   - Não adicione `@tabler/core`, Tabler Icons ou bibliotecas visuais via npm, yarn, pnpm ou bun.
   - Não introduza Vite, Webpack, Rollup, Parcel, esbuild, Sass/PostCSS ou outra etapa de build apenas para servir dependências de interface.
   - Não copie bibliotecas de terceiros para `vendor/`, `public/`, `assets/` ou equivalente.
   - Dependências do backend não são afetadas por esta regra.

2. **Prefira Tabler nativo antes de CSS/JS customizado.**
   - Reutilize componentes, utilitários e padrões oficiais do Tabler/Bootstrap.
   - Crie CSS customizado apenas quando o Tabler não resolver adequadamente.
   - Evite duplicar estilos que já existem no framework.

3. **Preserve a arquitetura do projeto.**
   - Não troque framework, engine de templates, rotas, organização de arquivos ou backend sem pedido explícito.
   - Adapte-se a HTML, ERB/Rails, Blade/Laravel, Twig, PHP, EJS, Django templates, Jinja, Razor ou outra stack encontrada.
   - Faça a menor alteração coerente que resolva o problema.

4. **UX faz parte da implementação, não é acabamento opcional.**
   - Toda tela deve considerar hierarquia visual, estados, feedback, responsividade, acessibilidade, prevenção de erro e fluxo de tarefa.

5. **Não invente APIs, rotas, campos ou regras de negócio.**
   - Descubra no código existente antes de conectar a interface.
   - Quando algo não existir, isole a interface e deixe claro o contrato esperado.

## Antes de alterar qualquer tela

Inspecione primeiro o projeto para descobrir:

- framework e engine de templates;
- layout principal e partials/componentes reutilizáveis;
- versão/URL de CDN do Tabler já usada;
- CSS e JavaScript customizados existentes;
- convenções de nomenclatura;
- rotas, controllers/handlers e modelos envolvidos;
- padrões existentes para flash messages, erros, modais, tabelas e formulários;
- suporte atual a dark mode, RTL e responsividade;
- bibliotecas de terceiros já carregadas por CDN.

Não crie um segundo padrão visual quando o projeto já possui um consistente.

## Política de CDN

Para um projeto novo, use como baseline:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/core@latest/dist/css/tabler.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css">

<script src="https://cdn.jsdelivr.net/npm/@tabler/core@latest/dist/js/tabler.min.js"></script>
```

Regras adicionais:

- Em manutenção, **preserve a versão já fixada** se ela estiver funcionando e o usuário não pediu upgrade.
- Em produção, prefira uma **versão explícita e verificada** no CDN para evitar mudanças inesperadas; continue usando CDN.
- `@latest` é aceitável para protótipos, exemplos e bootstrap inicial.
- Não carregue Bootstrap separadamente quando o bundle atual do Tabler já fornecer o comportamento necessário.
- Carregue plugins extras somente na página/layout que realmente precisa deles, quando a arquitetura permitir.
- Evite duas bibliotecas diferentes para resolver o mesmo problema.
- Antes de adicionar um novo CDN, confira se o projeto já possui biblioteca equivalente.

Leia `references/tabler-cdn.md` quando precisar decidir URLs, versionamento ou dependências adicionais.

## Processo de implementação

### 1. Entenda a tarefa do usuário

Converta o pedido em:

- objetivo da tela;
- ação principal;
- ações secundárias;
- dados necessários;
- estados possíveis;
- riscos de uso;
- comportamento mobile.

Não comece pela estética; comece pelo fluxo.

### 2. Reuse a estrutura existente

Procure por:

- `page`, `page-wrapper`, `page-header`, `page-body`;
- `container-xl` ou container já padronizado;
- navbar/sidebar existente;
- partials de breadcrumb, alerts e paginação;
- helpers de formulário e autorização;
- componentes de card, table e modal já usados.

Extraia partial/componente somente quando houver reutilização real ou quando o arquivo estiver ficando difícil de manter.

### 3. Escolha componentes Tabler adequados

Priorize:

- `card` para agrupamento lógico;
- `table`/responsive table para dados tabulares;
- `form-control`, `form-select`, `input-group` e feedback de validação para formulários;
- `badge` e `status` para estados curtos;
- `alert` para mensagens importantes;
- `modal` apenas para tarefas curtas e contextuais;
- `offcanvas` quando uma ação lateral preservar melhor o contexto;
- `dropdown` para ações secundárias;
- `empty state` quando não houver dados;
- `spinner`, placeholder/skeleton ou estado de carregamento quando houver espera;
- `pagination` para coleções extensas;
- tabs somente quando as seções forem pares conceituais e o usuário precisar alternar entre elas.

### 4. Implemente estados completos

Uma funcionalidade não está pronta enquanto não tratar, quando aplicável:

- estado normal;
- loading;
- vazio;
- sucesso;
- erro;
- validação de campo;
- permissão negada;
- ação desabilitada;
- processamento/submissão em andamento;
- confirmação para ação destrutiva;
- conteúdo longo ou inesperado;
- viewport pequeno.

### 5. Revise usabilidade

Antes de concluir, aplique `references/ui-ux-checklist.md`.

### 6. Valide a política CDN

Quando puder executar scripts locais, rode:

```bash
python scripts/check_cdn_policy.py .
```

Use o script como alerta, não como substituto para revisão humana.

## Diretrizes de UI/UX

### Hierarquia

- Uma ação primária clara por contexto.
- Títulos devem dizer o que o usuário está vendo, não apenas repetir o menu.
- Use subtítulos apenas para contexto útil.
- Agrupe por tarefa ou significado, não por conveniência técnica.
- Evite cards dentro de cards sem necessidade real.

### Densidade

- Dashboards e sistemas internos podem ser densos, mas nunca confusos.
- Prefira alinhamento consistente e whitespace funcional a espaçamento excessivo.
- Em tabelas, preserve legibilidade antes de tentar mostrar todas as colunas.
- Em mobile, oculte ou reorganize informação secundária em vez de espremer tudo.

### Formulários

- Label visível para campos importantes; placeholder não substitui label.
- Explique formato/restrição perto do campo quando necessário.
- Mostre erro no campo e, se útil, resumo no topo.
- Preserve os valores digitados após erro do servidor.
- Desabilite ou sinalize submissão em andamento para evitar duplo envio.
- Campos obrigatórios e opcionais devem ficar claros.
- Ordem dos campos deve acompanhar o raciocínio do usuário.

### Tabelas

- Cabeçalho descritivo e alinhamento coerente.
- Números comparáveis alinhados à direita quando isso melhora leitura.
- Ações de linha agrupadas no fim da linha.
- Não esconda a principal ação apenas dentro de um menu de três pontos.
- Use quebra de linha, truncamento com acesso ao conteúdo completo ou layout responsivo conforme o caso.
- Filtros ativos devem ser visíveis e fáceis de limpar.

### Ações destrutivas

- Use cor/semântica de perigo somente para ações realmente destrutivas.
- Confirmação deve informar **o que será afetado**.
- Não use confirmação genérica como “Tem certeza?” quando puder ser específica.
- Evite posicionar destruir imediatamente ao lado da ação principal sem diferenciação.

### Feedback

- Toda ação iniciada deve ter resposta perceptível.
- Para sucesso simples, prefira feedback discreto e persistência suficiente para leitura.
- Erros devem dizer o que ocorreu e, quando possível, como corrigir.
- Não use toast para informação que o usuário precisa consultar durante a tarefa.

### Acessibilidade

- HTML semântico primeiro.
- `label` associado ao input.
- Botões devem ser `<button>` quando executam ação e links devem navegar.
- Elementos clicáveis precisam de nome acessível.
- Ícones sem texto devem ter `aria-label`, tooltip acessível ou texto visualmente oculto quando necessário.
- Ícones decorativos devem ser ignorados por tecnologia assistiva quando apropriado.
- Preserve foco visível.
- Não dependa apenas de cor para comunicar estado.
- Modais precisam de título e fluxo de foco coerente.
- Respeite navegação por teclado.

### Responsividade

Teste mentalmente e, quando possível, no navegador:

- ~360 px;
- ~768 px;
- ~1024 px;
- desktop amplo.

Evite largura fixa sem necessidade. Prefira grid e utilities do Tabler/Bootstrap.

## JavaScript

- Use JavaScript nativo e APIs fornecidas pelo Tabler/Bootstrap sempre que bastarem.
- Evite adicionar frameworks frontend para uma interação simples.
- Inicialize plugins depois que o DOM relevante existir.
- Se o projeto usa Turbo, HTMX, PJAX ou navegação parcial, conecte a inicialização ao ciclo de vida já existente em vez de depender somente de `DOMContentLoaded`.
- Evite handlers duplicados quando a tela pode ser renderizada mais de uma vez.
- Não coloque regras de negócio sensíveis exclusivamente no cliente.

## CSS customizado

Antes de escrever CSS:

1. procure utility class do Tabler/Bootstrap;
2. procure variável CSS existente;
3. verifique componente nativo;
4. só então adicione CSS local.

Quando customizar:

- use classes semânticas do domínio/componente;
- evite seletores frágeis baseados em estrutura profunda;
- evite `!important` salvo incompatibilidade comprovada;
- não sobrescreva globalmente componentes do Tabler por causa de uma única tela;
- preserve dark mode quando o projeto o utilizar;
- prefira custom properties para valores repetidos.

## Manutenção e correção de bugs

Ao receber bug visual ou funcional:

1. reproduza ou localize o caminho de código;
2. identifique se a causa é HTML, CSS, JS, estado de backend ou versão da biblioteca;
3. corrija na camada correta;
4. evite “patch CSS” para problema causado por markup incorreto;
5. revise regressões em telas que reutilizam o mesmo partial/componente;
6. mantenha alterações pequenas e rastreáveis;
7. preserve compatibilidade com a versão de Tabler já instalada por CDN, salvo pedido de upgrade.

## Quando o usuário pedir uma nova tela

Use `assets/tabler-shell.html` como referência estrutural, não como obrigação de substituir o layout existente.

Para CRUDs, pense em conjunto:

- index/listagem;
- filtros/busca;
- paginação;
- empty state;
- criação;
- edição;
- detalhes, se necessários;
- erros/validação;
- exclusão/arquivamento;
- feedback pós-ação;
- permissões.

Leia `references/implementation-patterns.md` para padrões recorrentes.

## Critério de pronto

Antes de afirmar que terminou, confirme:

- a tarefa principal é óbvia;
- a tela segue o layout já usado no sistema;
- Tabler e bibliotecas frontend continuam por CDN;
- não foi adicionada etapa de build de frontend sem pedido explícito;
- não há dependência visual instalada via package manager;
- markup usa componentes Tabler de forma coerente;
- formulário possui labels e estados de erro adequados;
- ações destrutivas têm proteção proporcional ao risco;
- loading, vazio, erro e sucesso foram considerados;
- layout funciona em mobile e desktop;
- navegação por teclado e foco não foram quebrados;
- não há console errors introduzidos pela alteração;
- o código novo segue as convenções do projeto;
- a mudança é pequena o suficiente para ser revisada com segurança.

## Forma de responder durante tarefas de código

- Explique brevemente o que encontrou antes de mudanças grandes.
- Quando editar, faça as alterações no projeto em vez de apenas descrever pseudo-código, se houver ferramentas para isso.
- Cite arquivos e trechos relevantes na explicação final.
- Destaque decisões de UX que alterem comportamento do usuário.
- Informe limitações reais sem inventar validações que não executou.
- Não proponha migração para React/Vue/Svelte ou pipeline de assets apenas por preferência pessoal.
