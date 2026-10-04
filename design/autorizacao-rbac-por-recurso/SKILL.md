---
name: autorizacao-rbac-por-recurso
description: Controle de acesso baseado em papéis (admin/editor/leitor/convidado) com verificação granular por recurso individual (projeto, pasta, texto). Ativar ao implementar permissões de acesso colaborativo, compartilhamento de projetos ou painel administrativo.
---

# autorizacao-rbac-por-recurso

## Descrição
A skill `autorizacao-rbac-por-recurso` implementa o sistema de controle de acesso granular da plataforma, definindo quais papéis (roles) podem executar quais ações em cada recurso específico (projeto, pasta ou texto). Ela vai além de um RBAC global, permitindo que um mesmo usuário seja "editor" num projeto e "leitor" em outro, sem necessitar de schemas separados por tenant.

## Quando usar
Gatilhos concretos e observáveis:
- Implementação dos UC relacionados a compartilhamento (UC-081, UC-083), permissões por pasta (UC-245) e papéis de equipe (UC-256).
- Adição de um novo endpoint de API que modifica dados de outro usuário.
- Implementação do painel administrativo (UC-215, UC-216).

Quando NÃO usar:
- Para o isolamento de dados entre tenants diferentes (usar `isolamento-de-banco-de-dados-com-rls`).
- Para autenticação e geração de tokens (usar `autenticacao-jwt-e-refresh-token`).

## Pré-requisitos
- Tabela `resource_permissions` no banco: `(user_id, resource_type, resource_id, role)`.
- Middleware de autenticação já injetando `user_id` no contexto da requisição.
- Enum de papéis: `ADMIN | OWNER | EDITOR | VIEWER | GUEST`.

## Processo (passo a passo executável)
1. **Definição da Matriz de Permissões:**
   Implementar a matriz de capacidades por papel como constante imutável:
   ```ts
   const PERMISSIONS = {
     ADMIN:  { read: true,  write: true,  delete: true,  manage_members: true  },
     OWNER:  { read: true,  write: true,  delete: true,  manage_members: true  },
     EDITOR: { read: true,  write: true,  delete: false, manage_members: false },
     VIEWER: { read: true,  write: false, delete: false, manage_members: false },
     GUEST:  { read: true,  write: false, delete: false, manage_members: false },
   };
   ```

2. **Middleware de Autorização por Recurso:**
   - Criar função `authorize(action, resourceType)` usada como middleware em cada rota.
   - A função consulta a tabela `resource_permissions` para o par `(user_id, resource_id)`.
   - Verifica se o papel encontrado tem a capacidade `action` na matriz `PERMISSIONS`.
   - Se não houver registro direto, verificar herança: permissão na pasta pai do texto, ou no projeto pai da pasta.

3. **Herança Hierárquica de Permissões:**
   - Permissões propagam do topo para baixo: Projeto → Pasta → Texto.
   - Se um usuário tem papel `EDITOR` no Projeto A, herda `EDITOR` em todas as pastas e textos do Projeto A, a menos que haja uma permissão explícita mais restritiva no recurso filho.

4. **API de Gerenciamento de Permissões:**
   - `POST /api/resources/:id/members` — Adicionar membro com papel (apenas `OWNER` ou `ADMIN` pode fazer).
   - `PATCH /api/resources/:id/members/:userId` — Alterar papel de membro.
   - `DELETE /api/resources/:id/members/:userId` — Remover membro.

## Parâmetros e configuração
| Parâmetro | Descrição | Padrão |
|---|---|---|
| `DEFAULT_NEW_PROJECT_ROLE` | Papel atribuído ao criador do projeto | `OWNER` |
| `DEFAULT_INVITED_ROLE` | Papel padrão para usuários convidados por link | `VIEWER` |
| `PERMISSION_INHERITANCE` | Habilita herança hierárquica de permissões | `true` |

## Armadilhas e como evitá-las
- **Armadilha:** Verificar permissões apenas no frontend (ocultar botões de edição para `VIEWER`), sem validação no backend. Um usuário malicioso pode enviar requisições diretamente à API e modificar dados de outro usuário.
  **Mitigação:** A verificação de autorização DEVE ser executada no middleware de backend em **toda** rota que modifica dados, independentemente de como a UI está configurada. A UI pode ocultar botões para melhor UX, mas nunca como mecanismo de segurança.

## Critérios de validação (Definition of Done)
- [ ] Um usuário com papel `VIEWER` não consegue executar operações de escrita ou deleção via API em 100% dos testes de penetração de autorização.
- [ ] A herança de permissões propaga corretamente do projeto para subpastas e textos sem consultas adicionais ao banco.

## Exemplos
**Cenário de herança:**
- Usuário Maria: `EDITOR` no Projeto "Romance A" (sem registro na pasta "Capítulo 3").
- Maria tenta editar texto "Cena 7" dentro de "Capítulo 3" dentro de "Romance A".
- Sistema: sem registro direto → verifica pasta pai → sem registro → verifica projeto → `EDITOR`. Permissão concedida.

**Cenário de bloqueio:**
- Usuário João: `VIEWER` no Projeto "Romance B".
- João envia `PATCH /api/texts/42` diretamente via curl.
- Middleware `authorize('write', 'text')` consulta permissão → `VIEWER.write = false` → responde `403 Forbidden`.
