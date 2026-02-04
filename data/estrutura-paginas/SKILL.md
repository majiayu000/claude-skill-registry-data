---
name: estrutura-paginas
description: Define a estrutura padrão para páginas individuais de cartas Pokémon TCG. Use quando criar novas páginas de carta, organizar layout de perícia, ou o usuário mencionar estrutura de página, layout de carta, ou template de carta.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Skill: Estrutura de Páginas de Cartas

Esta skill define a estrutura padrão para páginas individuais de cartas Pokémon TCG graduadas, garantindo consistência e qualidade em todo o portfólio.

## Quando Usar

- Ao criar novas páginas de cartas individuais
- Ao revisar estrutura de páginas existentes
- Quando o usuário mencionar "criar página de carta", "layout de perícia"
- Ao refatorar páginas para seguir o padrão
- Ao planejar a estrutura de uma nova carta

**Nota:** Esta skill é complementar à `pericia-template`. Use `pericia-template` para criar novas perícias completas com dados específicos. Use esta skill para entender e aplicar a estrutura padrão.

## Estrutura Padrão Completa

```
1. Navbar (navegação superior)
2. Header Section (cabeçalho com título e certificado)
3. Container Principal
   3.1. Fotos e Identificação (row com 2 colunas)
       - Fotos da Carta (col-lg-6)
       - Identificação (col-lg-6)
   3.2. Graduação (card único)
   3.3. Análise de Condição (card único)
   3.4. Histórico de Proveniência (card único)
   3.5. Observação Importante (alert - opcional)
   3.6. Botão de Voltar
4. Footer (rodapé)
5. Modals (para visualização de fotos)
6. Scripts
```

## Seção 1: Navbar

**Padrão obrigatório:**
- Navbar dark com `bg-dark`
- Link "Cartas Graduadas" voltando para `../index.html`
- Link "Voltar ao Portfólio" no menu
- Responsiva com toggler para mobile

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

## Seção 2: Header Section

**Cores:**
- Fundo: `bg-dark`
- Texto: `text-white`
- Borda: `border-bottom border-secondary`

**Conteúdo:**
- Título: "Laudo de Perícia Técnica"
- Subtítulo: Nome completo da carta com coleção
- Badge: Número do certificado

```html
<!-- Header Section -->
<section class="bg-dark text-white py-4 border-bottom border-secondary">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-md-8">
                <h1 class="h3 mb-2">Laudo de Perícia Técnica</h1>
                <p class="mb-0 text-secondary">[Nome Carta] - [Coleção]</p>
            </div>
            <div class="col-md-4 text-md-end">
                <span class="badge bg-secondary fs-6">Cert: [CERTIFICADO]</span>
            </div>
        </div>
    </div>
</section>
```

## Seção 3.1: Fotos e Identificação

**Layout:**
- Row com 2 colunas iguais em desktop (`col-lg-6`)
- Coluna única em mobile

**Coluna Esquerda - Fotos da Carta:**

```html
<div class="col-lg-6 mb-3 mb-lg-0">
    <div class="card shadow border-secondary h-100">
        <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Fotos da Carta</h5>
        </div>
        <div class="card-body bg-white p-0">
            <div class="row g-0">
                <div class="col-6">
                    <div class="p-3 border-end">
                        <img src="[URL_FRENTE]"
                             alt="[Nome] - Frente"
                             class="w-100 rounded border"
                             style="height: 400px; object-fit: contain; cursor: pointer;"
                             data-bs-toggle="modal"
                             data-bs-target="#modalFrente">
                    </div>
                </div>
                <div class="col-6">
                    <div class="p-3">
                        <img src="[URL_VERSO]"
                             alt="[Nome] - Verso"
                             class="w-100 rounded border"
                             style="height: 400px; object-fit: contain; cursor: pointer;"
                             data-bs-toggle="modal"
                             data-bs-target="#modalVerso">
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

**Coluna Direita - Identificação:**

```html
<div class="col-lg-6">
    <div class="card shadow border-secondary h-100">
        <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Identificação</h5>
        </div>
        <div class="card-body bg-white">
            <table class="table table-sm table-borderless mb-0">
                <tbody>
                    <tr>
                        <td class="fw-bold text-dark" style="width: 40%;">Nome:</td>
                        <td>[Nome]</td>
                    </tr>
                    <tr>
                        <td class="fw-bold text-dark">Número:</td>
                        <td>[Número]</td>
                    </tr>
                    <!-- Mais campos conforme necessário -->
                </tbody>
            </table>
        </div>
    </div>
</div>
```

**Campos obrigatórios de Identificação:**
- Nome
- Número
- Coleção
- Ano
- Raridade (com badge colorido)
- Tipo
- Idioma
- Fabricante
- Ilustrador/Artista

**Campos opcionais:**
- Edição
- Versão
- Lançamento
- Registro AAA (para GBA)

## Seção 3.2: Graduação

**Card header:**
- Cor: `bg-dark text-white`
- Título: "Graduação [Nome Graduadora]"

**Conteúdo obrigatório:**
1. Nota final (display-4)
2. Descrição da nota
3. Nome da graduadora
4. Certificado
5. Data ou programa
6. Ranking/População
7. Links de referência

```html
<div class="card shadow border-secondary mb-4">
    <div class="card-header bg-dark text-white">
        <h5 class="mb-0">Graduação [Graduadora]</h5>
    </div>
    <div class="card-body bg-white">
        <!-- Nota final centralizada -->
        <div class="text-center mb-3">
            <h2 class="display-4 text-dark mb-0">[Nota]</h2>
            <p class="text-secondary mb-0" style="font-size: 1.1rem;">[Descrição]</p>
        </div>
        <hr>
        <!-- Informações da graduadora -->
        <!-- Ranking -->
        <!-- Links -->
    </div>
</div>
```

**Ranking - 3 Colunas:**
1. Mesma Nota
2. Nota Maior
3. Total/População

## Seção 3.3: Análise de Condição

**Card header:**
- Cor: `bg-secondary text-white`
- Título: "Análise de Condição - [Graduadora]"

**Conteúdo obrigatório:**
1. Alert com descrição da escala
2. Classificação geral com progress bar
3. Notas por componente (cards pequenos):
   - Centering
   - Corners
   - Edges
   - Surface
4. Observações técnicas detalhadas
5. Observação de autenticidade

```html
<div class="card shadow border-secondary mb-4">
    <div class="card-header bg-secondary text-white">
        <h5 class="mb-0">Análise de Condição - [Graduadora]</h5>
    </div>
    <div class="card-body bg-white">
        <!-- Alert com escala -->
        <div class="alert alert-secondary mb-4">
            <h6 class="alert-heading fw-bold mb-2">Escala [Graduadora]</h6>
            <p class="small mb-0">[Descrição da escala]</p>
        </div>

        <!-- Progress bar -->
        <div class="mb-4">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="fw-bold text-dark">Classificação Geral:</span>
                <span class="badge [cor] fs-6">[Nota] - [Descrição]</span>
            </div>
            <div class="progress" style="height: 25px;">
                <div class="progress-bar [cor]" style="width: [%]%;">
                    <span class="fw-bold">[Nota]/10</span>
                </div>
            </div>
        </div>

        <!-- Componentes -->
        <h6 class="text-dark mb-3">Análise Detalhada por Componente</h6>
        <!-- Cards com notas de cada componente -->

        <!-- Observações técnicas -->
        <h6 class="text-dark mb-3">Observações Técnicas</h6>
        <!-- Alerts com observações -->
    </div>
</div>
```

**Cores de Progress Bar:**
- Nota 9-10: `bg-success` (verde)
- Nota 8-8.9: `bg-warning` (amarelo)
- Nota < 8: `bg-secondary` (cinza)

## Seção 3.4: Histórico de Proveniência

**Card header:**
- Cor: `bg-dark text-white`
- Título: "Histórico de Proveniência" ou "Histórico e Contexto"

**Estrutura:**
- Accordion flush para eventos históricos
- Alertas ao final para:
  - Informações sobre o artista/ilustrador
  - Notas sobre a graduadora

```html
<div class="card shadow border-secondary">
    <div class="card-header bg-dark text-white">
        <h5 class="mb-0">Histórico de Proveniência</h5>
    </div>
    <div class="card-body bg-white">
        <div class="accordion accordion-flush" id="accordionHistory">
            <!-- Accordion items -->
        </div>

        <!-- Info do artista -->
        <div class="alert alert-dark mt-4 mb-3">
            <h6 class="alert-heading small fw-bold">Sobre o [Artista/Ilustrador]</h6>
            <!-- Conteúdo -->
        </div>

        <!-- Notas da graduadora -->
        <div class="alert alert-secondary mb-0">
            <h6 class="alert-heading small fw-bold">Notas sobre a Graduação [Graduadora]</h6>
            <!-- Conteúdo -->
        </div>
    </div>
</div>
```

**Accordion Items:**
- Cada evento em um `accordion-item`
- IDs únicos (collapse1, collapse2, etc)
- Primeiro item pode iniciar expandido (`collapse show`)
- Formato de título: Data + Descrição curta
- Corpo: Descrição detalhada em fonte `small`

## Seção 3.5: Observação Importante (Opcional)

Para cartas com nota de perícia que pode mudar:

```html
<div class="alert alert-info mt-4">
    <h6 class="alert-heading fw-bold mb-2">Observação Importante</h6>
    <p class="small mb-0">
        O estado de conservação, as notas de graduação e a população apresentados
        neste laudo refletem a condição da carta na data da [avaliação/certificação]
        realizada pela [Graduadora] em <strong>[Data]</strong>.
        Estes dados podem sofrer alterações ao longo do tempo conforme novas cartas
        são graduadas e adicionadas ao sistema.
    </p>
</div>
```

## Seção 3.6: Botão de Voltar

```html
<div class="text-center mt-4">
    <a href="../index.html" class="btn btn-dark btn-lg">Voltar ao Portfólio</a>
</div>
```

## Seção 4: Footer

**Padrão obrigatório:**

```html
<!-- Footer -->
<footer class="bg-dark text-white py-4 mt-5 border-top border-secondary">
    <div class="container">
        <div class="row">
            <div class="col-md-6">
                <p class="mb-0 text-secondary">&copy; 2025 Cartas Pokémon TCG Graduadas</p>
            </div>
            <div class="col-md-6 text-md-end">
                <p class="mb-0 text-secondary">[Texto variável - data ou certificado]</p>
            </div>
        </div>
    </div>
</footer>
```

**Opções de texto variável:**
- "Laudo gerado em: DD/MM/YYYY"
- "Laudo gerado para: [CERTIFICADO]"

## Seção 5: Modals

**Dois modals obrigatórios:**
1. `modalFrente` - Foto da frente
2. `modalVerso` - Foto do verso

```html
<!-- Modal Frente -->
<div class="modal fade" id="modalFrente" tabindex="-1" aria-labelledby="modalFrenteLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content bg-dark">
            <div class="modal-header border-secondary">
                <h5 class="modal-title text-white" id="modalFrenteLabel">[Nome] - Frente</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Fechar"></button>
            </div>
            <div class="modal-body text-center p-0">
                <img src="[URL_FRENTE]" alt="[Nome] - Frente" class="img-fluid">
            </div>
        </div>
    </div>
</div>

<!-- Modal Verso -->
<!-- Estrutura idêntica com IDs e conteúdo do verso -->
```

## Responsividade

**Mobile (< 768px):**
- Layout em coluna única
- Navbar com toggler
- Cards em largura total
- Fotos em grid 2 colunas

**Tablet (≥ 768px):**
- Layout ainda em coluna única
- Melhor espaçamento

**Desktop (≥ 992px):**
- Grid 2 colunas para Fotos e Identificação
- Cards em largura total
- Layout otimizado

**Use classes responsivas:**
- `col-12 col-lg-6` para 2 colunas em desktop
- `mb-3 mb-lg-0` para espaçamento responsivo
- `text-md-end` para alinhamento responsivo

## Cores e Estilos

**Paleta padrão:**
- Background principal: `bg-light`
- Cards: `bg-white`
- Headers primários: `bg-dark text-white`
- Headers secundários: `bg-secondary text-white`
- Bordas: `border-secondary`
- Sombras: `shadow`

**Badges de Raridade:**
- Promocional: `bg-dark`
- Shiny Rare: `bg-dark`
- Hyper Rare: `bg-warning text-dark`
- Secret Rare: `bg-danger`

**Badges de Notas:**
- 9.5-10: `bg-success`
- 9-9.25: `bg-success`
- 8-8.5: `bg-warning text-dark`
- 6-7.5: `bg-secondary`
- < 6: `bg-secondary`

## Checklist de Qualidade

Antes de considerar uma página completa:

**Estrutura:**
- ✅ Navbar funcional
- ✅ Header com título e certificado
- ✅ Fotos da carta (frente e verso)
- ✅ Tabela de identificação completa
- ✅ Card de graduação com ranking
- ✅ Análise de condição detalhada
- ✅ Histórico com accordion
- ✅ Info do artista
- ✅ Notas da graduadora
- ✅ Botão de voltar
- ✅ Footer
- ✅ Modals para fotos

**Conteúdo:**
- ✅ Todas as informações básicas preenchidas
- ✅ Notas detalhadas (Centering, Corners, Edges, Surface)
- ✅ Observações técnicas escritas
- ✅ Pelo menos 2-3 eventos históricos
- ✅ Informações sobre o artista
- ✅ Links de referência funcionando

**Qualidade:**
- ✅ Responsivo em mobile
- ✅ Imagens carregando corretamente
- ✅ Modals funcionando
- ✅ Accordion funcionando
- ✅ Apenas classes Bootstrap
- ✅ HTML válido e semântico
- ✅ Acessibilidade (ARIA, alt text)

## Diferenças por Graduadora

### Manafix
- Campo: "Data da Certificação"
- Ranking label: "Total"
- Pode usar "Artista" em vez de "Ilustrador"
- Campos extras: Edição, Versão

### GBA
- Campo: "Data da Avaliação" ou "Programa"
- Ranking label: "População"
- Campo: "Registro AAA"
- Ilustrador (não Artista)
- Campo extra: Lançamento

## Integração com Outras Skills

Esta skill trabalha em conjunto com:
- **pericia-template:** Para criação automatizada de páginas
- **bootstrap-guidelines:** Para classes e componentes
- **codigo-html:** Para estrutura HTML limpa
- **acessibilidade:** Para HTML acessível

Use esta skill como referência para entender a estrutura. Use `pericia-template` para criar páginas completas.
