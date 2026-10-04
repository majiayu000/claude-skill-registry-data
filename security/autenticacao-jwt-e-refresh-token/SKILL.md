---
name: autenticacao-jwt-e-refresh-token
description: Implementa autenticação stateless com JWT de curta duração e refresh token rotativo em HTTPOnly cookie. Ativar ao implementar ou auditar o sistema de login, registro, logout e proteção de rotas da plataforma SaaS.
---

# autenticacao-jwt-e-refresh-token

## Descrição
A skill `autenticacao-jwt-e-refresh-token` especifica o fluxo completo de autenticação stateless para a plataforma SaaS de escrita criativa. Ela define a geração de Access Tokens JWT (15 minutos de validade) e Refresh Tokens rotativos (30 dias, armazenados em HTTPOnly cookie), a estratégia de revogação de sessões e a proteção contra roubo de token via rotação obrigatória.

## Quando usar
Gatilhos concretos e observáveis:
- Implementação do módulo `autenticacao_perfil` (UC-129, UC-130, UC-214).
- Revisão de segurança do fluxo de login/logout.
- Implementação do login social (Google, GitHub) via OAuth 2.0 (UC-237).

Quando NÃO usar:
- Para controle de permissões por recurso (usar skill `autorizacao-rbac-por-recurso`).
- Para criptografia de dados em repouso no banco (escopo de infraestrutura, não de autenticação).

## Pré-requisitos
- Biblioteca JWT: `jsonwebtoken` (Node.js) ou `python-jose` (FastAPI).
- Banco de dados com tabela `refresh_tokens` (campos: `token_hash`, `user_id`, `expires_at`, `revoked`, `family_id`).
- HTTPS obrigatório em produção (Refresh Token em HTTPOnly cookie é inútil sem TLS).

## Processo (passo a passo executável)
1. **Login (Geração de Par de Tokens):**
   - Validar credenciais do usuário (email/senha com bcrypt).
   - Gerar Access Token JWT: `{ sub: user_id, role, tenant_id, exp: now+15min }` assinado com `RS256` (chave privada).
   - Gerar Refresh Token: UUID aleatório criptograficamente seguro (`crypto.randomUUID()`).
   - Persistir o hash SHA-256 do Refresh Token na tabela `refresh_tokens` com `family_id` (UUID único por família de sessão).
   - Retornar o Access Token no corpo da resposta JSON e o Refresh Token em cookie `Set-Cookie: refreshToken=<value>; HttpOnly; Secure; SameSite=Strict; Path=/api/auth/refresh; Max-Age=2592000`.

2. **Uso do Access Token (Rotas Protegidas):**
   - Middleware de autenticação extrai o Bearer token do header `Authorization`.
   - Verificar a assinatura com a chave pública RS256 e a expiração.
   - Injetar `{ user_id, role, tenant_id }` no contexto da requisição.

3. **Renovação (Refresh Token Rotation):**
   - Endpoint `POST /api/auth/refresh` lê o cookie `refreshToken`.
   - Buscar o hash do token na tabela `refresh_tokens`. Se não encontrado ou revogado → retornar 401.
   - **Rotação:** Revogar o Refresh Token usado e gerar um novo par (Access + Refresh) com o mesmo `family_id`.
   - Se o mesmo Refresh Token for usado duas vezes (roubo detectado): revogar **toda a família** de tokens (todos os registros com o mesmo `family_id`).

4. **Logout:**
   - Revogar o Refresh Token atual (`revoked = true`) na tabela.
   - Limpar o cookie `refreshToken` com `Set-Cookie: refreshToken=; Max-Age=0`.

## Parâmetros e configuração
| Parâmetro | Descrição | Padrão |
|---|---|---|
| `ACCESS_TOKEN_TTL` | Duração do Access Token JWT | `15min` |
| `REFRESH_TOKEN_TTL` | Duração do Refresh Token | `30d` |
| `JWT_ALGORITHM` | Algoritmo de assinatura JWT | `RS256` |
| `COOKIE_SAMESITE` | Política SameSite do cookie de refresh | `Strict` |

## Armadilhas e como evitá-las
- **Armadilha:** Armazenar o Refresh Token no `localStorage` do navegador, expondo-o a ataques XSS que podem roubar e usar o token indefinidamente.
  **Mitigação:** Armazenar o Refresh Token **exclusivamente** em cookie `HttpOnly; Secure; SameSite=Strict`. O JavaScript da página nunca terá acesso ao valor. O Access Token (de curta duração) pode ficar em memória (variável JavaScript) sem persistência em storage.

- **Armadilha:** Não implementar a detecção de roubo por reuso de Refresh Token. Se um token for comprometido, o atacante consegue renovar sessões indefinidamente sem ser detectado.
  **Mitigação:** Implementar a revogação de família completa: ao detectar o reuso de um Refresh Token já rotacionado, revogar todos os tokens da família (`family_id`) imediatamente, forçando o usuário legítimo a fazer login novamente.

## Critérios de validação (Definition of Done)
- [ ] O Access Token expira em 15 minutos e não pode ser renovado sem um Refresh Token válido.
- [ ] O reuso de um Refresh Token rotacionado revoga toda a sessão da família em 100% dos testes de detecção de roubo.
- [ ] O cookie de Refresh Token possui os atributos `HttpOnly`, `Secure` e `SameSite=Strict` em produção.

## Exemplos
**Login bem-sucedido:**
```json
Response body: { "accessToken": "eyJhbGci..." }
Set-Cookie: refreshToken=<uuid>; HttpOnly; Secure; SameSite=Strict; Path=/api/auth/refresh; Max-Age=2592000
```
**Detecção de roubo:**
Token da família F-001 já foi rotacionado (B → C). Atacante envia token B novamente.
Sistema revoga tokens B, C e quaisquer outros da família F-001. Usuário legítimo é desconectado na próxima requisição.
