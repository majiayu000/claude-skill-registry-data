---
name: codigo-html
description: Garante padrões de código HTML limpo, semântico e consistente. Use quando criar ou modificar arquivos HTML, estruturar páginas, ou o usuário mencionar HTML, tags, atributos, ou estrutura de código.
---

# Skill: Padrões de Código HTML

Esta skill garante código HTML limpo, semântico, bem-estruturado e consistente em todo o projeto.

## Quando Usar

- Ao criar novos arquivos HTML
- Ao modificar estrutura de páginas existentes
- Quando o usuário mencionar "HTML", "tags", "estrutura"
- Ao revisar ou refatorar código
- Ao corrigir problemas de formatação

## Estrutura Básica Obrigatória

Toda página HTML deve seguir esta estrutura:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Título Descritivo da Página]</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <!-- Conteúdo da página -->

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

## Regras de Formatação

### 1. Indentação

**Padrão: 4 espaços**

```html
<!-- ✅ Correto -->
<div class="container">
    <div class="row">
        <div class="col-12">
            <p>Conteúdo</p>
        </div>
    </div>
</div>

<!-- ❌ Incorreto (2 espaços ou tabs) -->
<div class="container">
  <div class="row">
      <div class="col-12">
          <p>Conteúdo</p>
      </div>
  </div>
</div>
```

**Regras:**
- Use 4 espaços, nunca tabs
- Mantenha consistência em todo o arquivo
- Indente cada nível de aninhamento
- Elementos inline podem ficar na mesma linha quando curtos

### 2. Comentários HTML

Use comentários para separar seções principais:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <!-- Head content -->
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">...</nav>

    <!-- Header Section -->
    <section class="bg-dark">...</section>

    <!-- Card Details -->
    <div class="container my-5">...</div>

    <!-- Footer -->
    <footer class="bg-dark">...</footer>

    <!-- Scripts -->
    <script src="..."></script>
</body>
</html>
```

**Boas práticas:**
- Comentários descritivos e concisos
- Em inglês para consistência
- Não comente código óbvio
- Use para delimitar seções grandes

### 3. Atributos

**Ordem recomendada:**
1. `class`
2. `id`
3. `data-*`
4. `type`
5. `href` / `src`
6. `title`
7. `alt`
8. `aria-*`
9. `role`

**Exemplos:**

```html
<!-- ✅ Correto -->
<button class="btn btn-primary"
        id="submitBtn"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#collapse1"
        aria-label="Abrir seção">

<img class="img-fluid rounded"
     src="image.jpg"
     alt="Descrição da imagem">

<!-- ❌ Incorreto (ordem aleatória) -->
<button type="button"
        aria-label="Abrir seção"
        class="btn btn-primary"
        data-bs-toggle="collapse"
        id="submitBtn">
```

**Regras de atributos:**
- Sempre use aspas duplas (`"`)
- Um atributo por linha se muitos atributos
- Valores booleanos explícitos quando necessário
- Sem espaços extras ao redor do `=`

### 4. Semântica HTML5

**Use tags apropriadas:**

```html
<!-- ✅ Correto - Tags semânticas -->
<nav>Navegação</nav>
<header>Cabeçalho</header>
<main>Conteúdo principal</main>
<section>Seção</section>
<article>Artigo independente</article>
<aside>Conteúdo lateral</aside>
<footer>Rodapé</footer>

<!-- ❌ Incorreto - Divs para tudo -->
<div class="navigation">...</div>
<div class="header">...</div>
<div class="main-content">...</div>
```

**Hierarquia de Headings:**

```html
<!-- ✅ Correto -->
<h1>Título Principal</h1>
    <h2>Seção</h2>
        <h3>Subseção</h3>
    <h2>Outra Seção</h2>
        <h3>Subseção</h3>

<!-- ❌ Incorreto - Pula níveis -->
<h1>Título</h1>
    <h3>Subseção</h3>  ❌
```

**Lista de tags semânticas:**
- `<nav>` - Navegação principal
- `<header>` - Cabeçalho de página ou seção
- `<main>` - Conteúdo principal (se aplicável)
- `<section>` - Seção temática de conteúdo
- `<article>` - Conteúdo independente
- `<aside>` - Conteúdo complementar/lateral
- `<footer>` - Rodapé de página ou seção
- `<figure>` - Conteúdo referenciado (imagens com legenda)
- `<figcaption>` - Legenda de figure
- `<time>` - Datas e horários

### 5. Links e Navegação

**Links relativos:**

```html
<!-- ✅ Correto - Caminho relativo correto -->
<a href="../index.html">Voltar</a>
<img src="../assets/image.jpg">

<!-- ❌ Incorreto - Caminho absoluto desnecessário -->
<a href="/home/user/projeto/index.html">Voltar</a>
```

**Texto descritivo:**

```html
<!-- ✅ Correto -->
<a href="charizard.html">Ver detalhes do Charizard</a>
<a href="index.html">Voltar ao Portfólio</a>

<!-- ❌ Incorreto -->
<a href="charizard.html">Clique aqui</a>
<a href="index.html">Voltar</a>
```

**Target e rel:**

```html
<!-- Links externos -->
<a href="https://exemplo.com" target="_blank" rel="noopener noreferrer">
    Link externo
</a>

<!-- Links internos -->
<a href="../index.html">Link interno</a>
```

### 6. Imagens

**Atributo alt obrigatório:**

```html
<!-- ✅ Correto - Alt descritivo -->
<img src="carta.jpg" alt="Carta Charizard Base Set graduada nota 9">

<!-- ✅ Correto - Imagem decorativa -->
<img src="decoration.png" alt="">

<!-- ❌ Incorreto - Sem alt -->
<img src="carta.jpg">
```

**Classes e estilos:**

```html
<!-- ✅ Correto -->
<img src="carta.jpg"
     alt="Carta Pikachu"
     class="w-100 rounded border"
     style="height: 400px; object-fit: contain;">

<!-- ❌ Incorreto - Estilo inline desnecessário -->
<img src="carta.jpg"
     alt="Carta Pikachu"
     style="width: 100%; border-radius: 5px; border: 1px solid #ccc;">
```

### 7. Formulários (Se Aplicável)

**Labels obrigatórios:**

```html
<!-- ✅ Correto -->
<label for="nome">Nome:</label>
<input type="text" id="nome" name="nome" class="form-control">

<!-- ❌ Incorreto - Sem label -->
<input type="text" name="nome" placeholder="Nome">
```

**Estrutura de formulário:**

```html
<form action="/submit" method="POST">
    <div class="mb-3">
        <label for="email" class="form-label">Email:</label>
        <input type="email"
               id="email"
               name="email"
               class="form-control"
               required>
    </div>
    <button type="submit" class="btn btn-primary">Enviar</button>
</form>
```

## Padrões Específicos do Projeto

### Navbar Padrão

```html
<!-- Navigation -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand fw-bold" href="../index.html">Cartas Graduadas</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link" href="../index.html">Voltar ao Portfólio</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

### Footer Padrão

```html
<!-- Footer -->
<footer class="bg-dark text-white py-4 mt-5 border-top border-secondary">
    <div class="container">
        <div class="row">
            <div class="col-md-6">
                <p class="mb-0 text-secondary">&copy; 2025 Cartas Pokémon TCG Graduadas</p>
            </div>
            <div class="col-md-6 text-md-end">
                <p class="mb-0 text-secondary">Laudo gerado em: DD/MM/YYYY</p>
            </div>
        </div>
    </div>
</footer>
```

### Modal Padrão

```html
<!-- Modal -->
<div class="modal fade" id="modalId" tabindex="-1" aria-labelledby="modalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content bg-dark">
            <div class="modal-header border-secondary">
                <h5 class="modal-title text-white" id="modalLabel">Título</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Fechar"></button>
            </div>
            <div class="modal-body text-center p-0">
                <img src="image.jpg" alt="Descrição" class="img-fluid">
            </div>
        </div>
    </div>
</div>
```

## O Que Evitar

### ❌ CSS Inline ou Tags Style

```html
<!-- ❌ Incorreto -->
<style>
    .custom-class {
        color: red;
    }
</style>

<div style="margin: 10px; padding: 20px; background: blue;">
```

**Exceções permitidas:**
- Width de progress bars: `style="width: 85%;"`
- Height de progress bars: `style="height: 25px;"`
- Object-fit de imagens: `style="object-fit: contain;"`

### ❌ JavaScript Inline

```html
<!-- ❌ Incorreto -->
<button onclick="alert('Hello')">Clique</button>

<!-- ✅ Correto -->
<button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal">
    Clique
</button>
```

**Exceção:** Atributos `data-bs-*` do Bootstrap são permitidos.

### ❌ Tabelas para Layout

```html
<!-- ❌ Incorreto -->
<table>
    <tr>
        <td>Menu</td>
        <td>Conteúdo</td>
    </tr>
</table>

<!-- ✅ Correto -->
<div class="row">
    <div class="col-md-3">Menu</div>
    <div class="col-md-9">Conteúdo</div>
</div>
```

**Exceção:** Tabelas são OK para dados tabulares reais.

### ❌ Divs Desnecessárias

```html
<!-- ❌ Incorreto -->
<div>
    <div>
        <div>
            <p>Texto</p>
        </div>
    </div>
</div>

<!-- ✅ Correto -->
<p>Texto</p>
```

### ❌ IDs Duplicados

```html
<!-- ❌ Incorreto -->
<div id="item">Item 1</div>
<div id="item">Item 2</div>

<!-- ✅ Correto -->
<div id="item1">Item 1</div>
<div id="item2">Item 2</div>
```

### ❌ Mistura de Idiomas

```html
<!-- ❌ Incorreto -->
<h1>Pokemon Cards</h1>
<p>Bem-vindo ao portfólio</p>

<!-- ✅ Correto -->
<h1>Cartas Pokémon</h1>
<p>Bem-vindo ao portfólio</p>
```

**Exceções:** Nomes próprios e termos técnicos (ex: "Base Set", "Gem Mint").

## Checklist de Código HTML

Ao criar ou modificar HTML:

**Estrutura:**
- ✅ `<!DOCTYPE html>` no início
- ✅ `<html lang="pt-BR">`
- ✅ Meta charset e viewport no `<head>`
- ✅ Título descritivo
- ✅ CDN do Bootstrap (CSS e JS)

**Formatação:**
- ✅ Indentação de 4 espaços consistente
- ✅ Comentários para seções principais
- ✅ Ordem de atributos padronizada
- ✅ Aspas duplas em todos os atributos

**Semântica:**
- ✅ Tags HTML5 semânticas (`<nav>`, `<section>`, `<footer>`)
- ✅ Hierarquia de headings correta
- ✅ Alt em todas as imagens
- ✅ Labels em inputs (se houver)

**Boas Práticas:**
- ✅ Links relativos corretos
- ✅ Texto descritivo em links
- ✅ Sem CSS inline (exceto exceções)
- ✅ Sem JavaScript inline
- ✅ Sem divs desnecessárias
- ✅ IDs únicos
- ✅ Idioma consistente (português)

## Validação

**Ferramentas:**
- [W3C HTML Validator](https://validator.w3.org/)
- [Nu Html Checker](https://validator.w3.org/nu/)
- Extensão "HTMLHint" para VS Code

**Validação mínima:**
- Sem erros críticos
- Sem warnings importantes
- Estrutura bem-formada

## Integração com Outras Skills

Esta skill trabalha em conjunto com:
- **bootstrap-guidelines:** Para classes e componentes Bootstrap
- **acessibilidade:** Para HTML acessível
- **estrutura-paginas:** Para layout consistente

Código HTML limpo é a base para um projeto de qualidade. Mantenha os padrões!
