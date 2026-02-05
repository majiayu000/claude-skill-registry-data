---
name: bootstrap-guidelines
description: Garante uso correto do Bootstrap 5 sem CSS customizado. Use quando criar ou modificar HTML, estilizar componentes, ajustar layout, ou o usuário mencionar Bootstrap, grid, responsividade, ou classes CSS.
---

# Skill: Bootstrap 5 Guidelines

Esta skill garante o uso correto do Bootstrap 5.3.0, seguindo o princípio fundamental do projeto de **ZERO CSS customizado**.

## Princípio Fundamental

**🚫 NUNCA use CSS customizado. SOMENTE classes Bootstrap.**

Toda estilização deve ser feita usando classes nativas do Bootstrap. Se algo não puder ser feito com Bootstrap, reconsidere o design.

## Quando Usar

- Ao criar novas páginas HTML
- Ao adicionar componentes (cards, badges, alerts, etc)
- Ao ajustar layout e responsividade
- Quando o usuário mencionar "estilizar", "layout", "responsivo"
- Ao trabalhar com grid system
- Quando precisar de cores, espaçamento, ou tipografia

## Sistema de Grid

### Container

```html
<!-- Largura fixa responsiva (recomendado) -->
<div class="container">

<!-- 100% da largura -->
<div class="container-fluid">
```

### Grid System

```html
<div class="row">
    <div class="col-12 col-md-6 col-lg-4">
        <!-- Conteúdo -->
    </div>
</div>
```

### Breakpoints

- `col-` : Extra small (< 576px) - Mobile
- `col-sm-` : Small (≥ 576px)
- `col-md-` : Medium (≥ 768px) - Tablet
- `col-lg-` : Large (≥ 992px) - Desktop
- `col-xl-` : Extra large (≥ 1200px)
- `col-xxl-` : Extra extra large (≥ 1400px)

### Exemplos de Grid

```html
<!-- 2 colunas em desktop, 1 em mobile -->
<div class="row">
    <div class="col-12 col-lg-6">Coluna 1</div>
    <div class="col-12 col-lg-6">Coluna 2</div>
</div>

<!-- 3 colunas em desktop, 1 em mobile -->
<div class="row">
    <div class="col-12 col-md-6 col-lg-4">Col 1</div>
    <div class="col-12 col-md-6 col-lg-4">Col 2</div>
    <div class="col-12 col-md-12 col-lg-4">Col 3</div>
</div>

<!-- Proporções diferentes (5-7) -->
<div class="row">
    <div class="col-lg-5">Coluna menor</div>
    <div class="col-lg-7">Coluna maior</div>
</div>
```

## Componentes Principais

### Cards

```html
<div class="card">
    <div class="card-header">Título</div>
    <div class="card-body">
        <h5 class="card-title">Título do Card</h5>
        <p class="card-text">Conteúdo</p>
    </div>
    <div class="card-footer">Rodapé</div>
</div>

<!-- Card com sombra e borda -->
<div class="card shadow border-secondary">
```

### Badges

```html
<span class="badge bg-primary">Primário</span>
<span class="badge bg-success">Sucesso</span>
<span class="badge bg-danger">Perigo</span>
<span class="badge bg-warning text-dark">Aviso</span>
<span class="badge bg-info">Info</span>
<span class="badge bg-dark">Escuro</span>

<!-- Tamanhos -->
<span class="badge bg-primary fs-6">Grande</span>
```

### Alerts

```html
<div class="alert alert-info">
    <h6 class="alert-heading">Título</h6>
    <p class="mb-0">Conteúdo do alerta</p>
</div>

<!-- Outros tipos -->
<div class="alert alert-primary">Primário</div>
<div class="alert alert-success">Sucesso</div>
<div class="alert alert-danger">Perigo</div>
<div class="alert alert-warning">Aviso</div>
<div class="alert alert-light border">Light com borda</div>
<div class="alert alert-dark">Escuro</div>
```

### Progress Bars

```html
<div class="progress" style="height: 25px;">
    <div class="progress-bar bg-success"
         role="progressbar"
         style="width: 85%;"
         aria-valuenow="85"
         aria-valuemin="0"
         aria-valuemax="100">
        <span class="fw-bold">85%</span>
    </div>
</div>

<!-- Diferentes cores -->
<div class="progress-bar bg-success">Verde</div>
<div class="progress-bar bg-warning">Amarelo</div>
<div class="progress-bar bg-danger">Vermelho</div>
<div class="progress-bar bg-secondary">Cinza</div>
```

### Accordion

```html
<div class="accordion accordion-flush" id="accordionExample">
    <div class="accordion-item border-bottom">
        <h2 class="accordion-header">
            <button class="accordion-button bg-light"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#collapse1">
                Título
            </button>
        </h2>
        <div id="collapse1" class="accordion-collapse collapse show">
            <div class="accordion-body bg-white small">
                Conteúdo
            </div>
        </div>
    </div>
</div>
```

### Navbar

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand fw-bold" href="index.html">Título</a>
        <button class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link" href="#">Link</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

### Modals

```html
<div class="modal fade" id="modalId" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content bg-dark">
            <div class="modal-header border-secondary">
                <h5 class="modal-title text-white">Título</h5>
                <button type="button" class="btn-close btn-close-white"
                        data-bs-dismiss="modal" aria-label="Fechar"></button>
            </div>
            <div class="modal-body text-center p-0">
                Conteúdo
            </div>
        </div>
    </div>
</div>
```

## Utility Classes Essenciais

### Spacing (Margin e Padding)

**Sintaxe:** `{property}{sides}-{size}` ou `{property}{sides}-{breakpoint}-{size}`

**Properties:**
- `m` : margin
- `p` : padding

**Sides:**
- `t` : top
- `b` : bottom
- `s` : start (left em LTR)
- `e` : end (right em LTR)
- `x` : horizontal (left + right)
- `y` : vertical (top + bottom)
- (vazio) : todos os lados

**Sizes:**
- `0` : 0
- `1` : 0.25rem (4px)
- `2` : 0.5rem (8px)
- `3` : 1rem (16px)
- `4` : 1.5rem (24px)
- `5` : 3rem (48px)
- `auto` : auto

**Exemplos:**
```html
<div class="mt-3">      <!-- margin-top: 1rem -->
<div class="mb-4">      <!-- margin-bottom: 1.5rem -->
<div class="p-2">       <!-- padding: 0.5rem -->
<div class="px-3">      <!-- padding horizontal: 1rem -->
<div class="my-5">      <!-- margin vertical: 3rem -->
<div class="mx-auto">   <!-- margin horizontal: auto (centralizar) -->
```

### Cores

**Background:**
```html
<div class="bg-primary">    <!-- Azul -->
<div class="bg-secondary">  <!-- Cinza -->
<div class="bg-success">    <!-- Verde -->
<div class="bg-danger">     <!-- Vermelho -->
<div class="bg-warning">    <!-- Amarelo -->
<div class="bg-info">       <!-- Azul claro -->
<div class="bg-light">      <!-- Cinza claro -->
<div class="bg-dark">       <!-- Preto -->
<div class="bg-white">      <!-- Branco -->
```

**Text:**
```html
<p class="text-primary">    <!-- Texto azul -->
<p class="text-secondary">  <!-- Texto cinza -->
<p class="text-success">    <!-- Texto verde -->
<p class="text-danger">     <!-- Texto vermelho -->
<p class="text-warning">    <!-- Texto amarelo -->
<p class="text-info">       <!-- Texto azul claro -->
<p class="text-dark">       <!-- Texto escuro -->
<p class="text-white">      <!-- Texto branco -->
<p class="text-muted">      <!-- Texto cinza claro -->
```

### Texto

**Alinhamento:**
```html
<p class="text-start">      <!-- Alinhado à esquerda -->
<p class="text-center">     <!-- Centralizado -->
<p class="text-end">        <!-- Alinhado à direita -->

<!-- Responsivo -->
<p class="text-start text-md-center">  <!-- Esquerda em mobile, centro em md+ -->
```

**Peso:**
```html
<span class="fw-bold">      <!-- Negrito -->
<span class="fw-normal">    <!-- Normal -->
<span class="fw-light">     <!-- Leve -->
<span class="fst-italic">   <!-- Itálico -->
```

**Tamanho:**
```html
<p class="fs-1">            <!-- Maior -->
<p class="fs-2">
<p class="fs-3">
<p class="fs-4">
<p class="fs-5">
<p class="fs-6">            <!-- Menor -->

<!-- Display headings (grandes) -->
<h1 class="display-1">      <!-- Muito grande -->
<h1 class="display-4">      <!-- Grande -->

<!-- Monospace -->
<code class="font-monospace">P0000254</code>
```

### Bordas

```html
<!-- Adicionar bordas -->
<div class="border">
<div class="border-top">
<div class="border-bottom">
<div class="border-start">
<div class="border-end">

<!-- Cores de borda -->
<div class="border border-primary">
<div class="border border-secondary">
<div class="border border-success">

<!-- Arredondamento -->
<img class="rounded">           <!-- Cantos arredondados -->
<img class="rounded-circle">    <!-- Círculo -->
<div class="rounded-pill">      <!-- Pílula -->
```

### Sombras

```html
<div class="shadow-sm">     <!-- Sombra pequena -->
<div class="shadow">        <!-- Sombra média -->
<div class="shadow-lg">     <!-- Sombra grande -->
```

### Display

```html
<div class="d-none">        <!-- Escondido -->
<div class="d-block">       <!-- Bloco -->
<div class="d-inline">      <!-- Inline -->
<div class="d-flex">        <!-- Flex -->

<!-- Responsivo -->
<div class="d-none d-md-block">     <!-- Escondido em mobile, visível em md+ -->
<div class="d-block d-lg-none">     <!-- Visível até lg, escondido em lg+ -->
```

### Flexbox

```html
<div class="d-flex justify-content-start">      <!-- Início -->
<div class="d-flex justify-content-center">     <!-- Centro -->
<div class="d-flex justify-content-end">        <!-- Fim -->
<div class="d-flex justify-content-between">    <!-- Espaço entre -->

<div class="d-flex align-items-start">          <!-- Topo -->
<div class="d-flex align-items-center">         <!-- Centro -->
<div class="d-flex align-items-end">            <!-- Base -->

<!-- Combinado -->
<div class="d-flex justify-content-between align-items-center">
```

### Largura

```html
<div class="w-25">      <!-- 25% -->
<div class="w-50">      <!-- 50% -->
<div class="w-75">      <!-- 75% -->
<div class="w-100">     <!-- 100% -->

<button class="btn btn-primary w-100">  <!-- Botão largura total -->
```

### Altura

```html
<div class="h-25">      <!-- 25% -->
<div class="h-50">      <!-- 50% -->
<div class="h-75">      <!-- 75% -->
<div class="h-100">     <!-- 100% -->
```

## Botões

```html
<!-- Estilos -->
<button class="btn btn-primary">Primário</button>
<button class="btn btn-secondary">Secundário</button>
<button class="btn btn-success">Sucesso</button>
<button class="btn btn-danger">Perigo</button>
<button class="btn btn-warning">Aviso</button>
<button class="btn btn-dark">Escuro</button>

<!-- Outline -->
<button class="btn btn-outline-primary">Outline</button>

<!-- Tamanhos -->
<button class="btn btn-primary btn-sm">Pequeno</button>
<button class="btn btn-primary">Normal</button>
<button class="btn btn-primary btn-lg">Grande</button>

<!-- Largura total -->
<button class="btn btn-primary w-100">Largura Total</button>
```

## Tabelas

```html
<table class="table">
    <tbody>
        <tr>
            <td>Célula</td>
        </tr>
    </tbody>
</table>

<!-- Variações -->
<table class="table table-sm">              <!-- Compacta -->
<table class="table table-borderless">      <!-- Sem bordas -->
<table class="table table-striped">         <!-- Zebrada -->
<table class="table table-hover">           <!-- Hover -->
```

## Gaps (Espaçamento em Grid)

```html
<div class="row g-2">       <!-- Gap de 0.5rem -->
<div class="row g-3">       <!-- Gap de 1rem -->
<div class="row g-4">       <!-- Gap de 1.5rem -->

<!-- Gaps direcionais -->
<div class="row gx-3">      <!-- Gap horizontal -->
<div class="row gy-3">      <!-- Gap vertical -->
```

## Cores para Tipos Pokémon (Sugestões)

```html
<!-- Fogo -->
<div class="bg-danger text-white">
<div class="bg-warning text-dark">

<!-- Água -->
<div class="bg-info text-white">
<div class="bg-primary text-white">

<!-- Planta -->
<div class="bg-success text-white">

<!-- Elétrico -->
<div class="bg-warning text-dark">

<!-- Psíquico -->
<div class="bg-primary text-white">

<!-- Normal/Lutador/Metal -->
<div class="bg-secondary text-white">

<!-- Fantasma -->
<div class="bg-dark text-white">
```

## Regras de Ouro

1. ✅ **Use APENAS classes Bootstrap nativas**
2. ✅ **Combine classes para obter o efeito desejado**
3. ✅ **Use o sistema de grid responsivo**
4. ✅ **Aproveite as utility classes**
5. ❌ **NUNCA crie CSS customizado**
6. ❌ **NUNCA use tags `<style>`**
7. ⚠️ **Style inline APENAS para:**
   - Width de progress bars (`style="width: 85%;"`)
   - Height de progress bars (`style="height: 25px;"`)
   - Object-fit de imagens (`style="object-fit: contain;"`)

## Checklist Bootstrap

Ao criar ou modificar HTML:

- ✅ CDN do Bootstrap 5.3.0 no `<head>`
- ✅ Bootstrap JS no final do `<body>`
- ✅ Container (`container` ou `container-fluid`)
- ✅ Grid system com breakpoints apropriados
- ✅ Componentes usando classes Bootstrap
- ✅ Spacing com utility classes (m-*, p-*)
- ✅ Cores com utility classes (bg-*, text-*)
- ✅ Responsividade testada
- ✅ Zero CSS customizado
- ✅ Zero tags `<style>`

## CDN do Bootstrap

**No `<head>`:**
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
```

**No final do `<body>`:**
```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

## Recursos

- [Bootstrap 5.3 Documentation](https://getbootstrap.com/docs/5.3/)
- [Bootstrap Grid System](https://getbootstrap.com/docs/5.3/layout/grid/)
- [Bootstrap Utilities](https://getbootstrap.com/docs/5.3/utilities/spacing/)
- [Bootstrap Components](https://getbootstrap.com/docs/5.3/components/)

## Integração com Outras Skills

Esta skill trabalha em conjunto com:
- **acessibilidade:** Para garantir componentes acessíveis
- **codigo-html:** Para estrutura HTML limpa
- **estrutura-paginas:** Para layout consistente

Lembre-se: Bootstrap 5 já inclui muitas práticas de acessibilidade por padrão. Mantenha-as!
