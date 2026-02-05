---
name: linkedin-postagem-mcp
description: Esta skill deve ser usada quando o usuário quiser criar, gerenciar ou otimizar posts no LinkedIn. Utiliza o MCP do LinkedIn para criar posts via API oficial, sem necessidade de automação de navegador. Ideal para criar conteúdo profissional, técnico ou promocional com boas práticas de engajamento.
---

# LinkedIn Postagem MCP

## Visão Geral

Esta skill automatiza a criação de posts no LinkedIn usando o MCP oficial do LinkedIn (API). Diferente de automação via navegador, esta abordagem é mais rápida, confiável e permite criar posts programaticamente.

## Ferramentas MCP Disponíveis

### Leitura
- `mcp__linkedin__get_my_info` - Obtém informações do perfil autenticado (author_id, nome, email)
- `mcp__linkedin__get_company_info` - Lista empresas que o usuário administra

### Escrita
- `mcp__linkedin__create_linked_in_post` - Cria um novo post
- `mcp__linkedin__delete_linked_in_post` - Deleta um post existente

## Fluxo de Trabalho Principal

### 1. Obter Author ID

Antes de criar qualquer post, obter o author_id do usuário:

```
mcp__linkedin__get_my_info
```

Resposta contém:
- `author_id`: URN do usuário (ex: `urn:li:person:MTJ1egdrII`)
- `name`: Nome completo
- `email`: Email verificado

### 2. Criar Post

Usar `mcp__linkedin__create_linked_in_post` com os parâmetros:

**Obrigatórios:**
- `author`: URN do autor (obtido no passo 1)
- `commentary`: Texto do post

**Opcionais:**
- `visibility`: PUBLIC (padrão), CONNECTIONS, LOGGED_IN
- `lifecycleState`: PUBLISHED (padrão), DRAFT
- `isReshareDisabledByAuthor`: true/false

### 3. Verificar Resultado

A resposta contém:
- `share_id`: ID do post criado (ex: `urn:li:share:7403648621042208769`)
- `status_code`: 201 = sucesso

**Link do post:** `https://www.linkedin.com/feed/update/{share_id}`

## Boas Práticas para Posts de Alto Engajamento

### Estrutura do Hook (Primeiras 2-3 linhas)

O LinkedIn corta o texto e mostra "ver mais". As primeiras linhas são CRÍTICAS:

**✅ BOM - Hook que entrega valor imediato:**
```
Minha IA agora consulta banco de dados, posta no LinkedIn e controla o navegador sozinha.
```

**❌ RUIM - Hook vago que não entrega valor:**
```
Descobri algo poderoso no Claude Code.

O que é MCP?
```

### Regras do Hook Perfeito

1. **Primeira linha deve ser uma afirmação impactante completa**
2. **Evitar perguntas no início** (ficam cortadas)
3. **Mostrar resultado/benefício antes de explicar o "como"**
4. **Usar números concretos quando possível**

### Estrutura Recomendada

```
[HOOK - Resultado impactante em 1 linha]

[CONTEXTO - O que é e por que importa - 2-3 linhas]

[LISTA - Pontos principais com → ou •]
→ Ponto 1
→ Ponto 2
→ Ponto 3

[CTA ou REFLEXÃO - 1 linha final]

#Hashtag1 #Hashtag2 #Hashtag3
```

### Formatação

- **Linhas curtas**: Máximo 60-80 caracteres por linha
- **Espaçamento**: Linha em branco entre seções
- **Emojis**: Usar com moderação (1-3 no máximo)
- **Hashtags**: 3-5 no final, relevantes ao tema
- **Listas**: Usar → ou • para bullet points

### Tamanho Ideal

- **Mínimo**: 100 caracteres
- **Ideal**: 500-1200 caracteres
- **Máximo**: 3000 caracteres (limite do LinkedIn)

## Templates por Tipo de Conteúdo

### Template: Compartilhar Aprendizado Técnico

```
[Resultado que você conseguiu em 1 linha]

[Tecnologia/método usado - 1-2 linhas]

O que aprendi:
→ [Insight 1]
→ [Insight 2]
→ [Insight 3]

[Próximo passo ou reflexão]

#Tech #Dev #[Tecnologia]
```

### Template: Anunciar Projeto/Feature

```
[Nome do projeto] agora faz [benefício principal].

[Contexto breve do problema que resolve]

Funcionalidades:
→ [Feature 1]
→ [Feature 2]
→ [Feature 3]

[Link ou CTA]

#Launch #Tech #[Área]
```

### Template: Reflexão Profissional

```
[Afirmação provocativa ou contra-intuitiva]

[Explicação do contexto - por que isso importa]

[Sua experiência/evidência]

[Conclusão ou pergunta para engajamento]

#Carreira #[Área] #Reflexão
```

## Tratamento de Erros

### Post Não Aparece Completo

**Problema**: LinkedIn corta o texto
**Solução**: Reescrever com hook melhor nas primeiras linhas

### Edição de Post

**Problema**: API não permite editar posts
**Solução**:
1. Deletar post: `mcp__linkedin__delete_linked_in_post(share_id)`
2. Criar novo com texto corrigido

### Rate Limiting

**Problema**: Muitas requisições
**Solução**: Aguardar alguns minutos entre posts

## Exemplos de Uso

### Exemplo 1: Post técnico simples

**Usuário:** "Crie um post sobre MCP servers"

**Ação:**
1. Obter author_id
2. Criar post com hook impactante sobre MCP
3. Retornar link do post

### Exemplo 2: Post sobre projeto

**Usuário:** "Faça um post sobre este projeto [caminho]"

**Ação:**
1. Ler e entender o projeto
2. Extrair pontos principais
3. Criar post com estrutura de anúncio
4. Retornar link do post

### Exemplo 3: Corrigir post

**Usuário:** "O post ficou ruim, melhore"

**Ação:**
1. Deletar post anterior
2. Reescrever com melhor estrutura
3. Criar novo post
4. Retornar novo link

## Checklist Pré-Publicação

- [ ] Hook entrega valor na primeira linha?
- [ ] Texto faz sentido se cortado após 2 linhas?
- [ ] Formatação com espaçamento adequado?
- [ ] Hashtags relevantes (3-5)?
- [ ] Tamanho adequado (500-1200 chars ideal)?
- [ ] Sem erros de português?
- [ ] Visibilidade correta (PUBLIC/CONNECTIONS)?

## Notas Importantes

- **Não é possível editar** posts via API - apenas criar e deletar
- **Author ID** deve ser obtido antes de criar posts
- **Share ID** é retornado na criação e necessário para deletar
- **Visibilidade PUBLIC** é o padrão e recomendado para alcance
- Posts criados via API aparecem normalmente no feed
