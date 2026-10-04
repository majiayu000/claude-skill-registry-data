---
name: conformidade-com-lgpd-e-gdpr-por-design
description: Implementa exclusao fisica permanente, portabilidade estruturada e log imutavel de consentimento para conformidade LGPD/GDPR.
---
# conformidade-com-lgpd-e-gdpr-por-design

## Descrição
A skill `conformidade-com-lgpd-e-gdpr-por-design` especifica as rotinas de exclusão física permanente de dados (Hard-Delete), portabilidade estruturada de conteúdo literário e registro imutável de consentimento para sistemas SaaS multi-tenant sujeitos à Lei Geral de Proteção de Dados (LGPD) brasileira e ao Regulamento Geral de Proteção de Dados (GDPR) europeu. Ela garante que o direito ao esquecimento e à portabilidade de dados do escritor sejam implementados de forma tecnicamente completa e auditável.

## Quando usar
Gatilhos concretos e observáveis:
- Um escritor ou organização solicita o encerramento permanente da conta e exclusão dos dados.
- O time jurídico ou de compliance solicita um relatório de auditoria de tratamento de dados.
- Um usuário ativa o download e exportação portável do seu projeto literário.

Quando NÃO usar:
- Para exclusões lógicas temporárias de rascunhos (usar `is_draft = false` sem deletar fisicamente).
- Em backups operacionais de banco de dados que são gerenciados por políticas separadas de retenção de infraestrutura.

## Pré-requisitos
- PostgreSQL configurado com restrições em cascata (`ON DELETE CASCADE`) em todas as tabelas filhas vinculadas a `tenant_id`.
- Exportador JSON/YAML das fichas de lore e grafos do GUF implementado.
- Tabela de log de consentimento configurada como `APPEND-ONLY` (sem permissão de UPDATE/DELETE).

## Processo (passo a passo executável)
1. **Hard-Delete em Cascata (Direito ao Esquecimento):**
   - Receber a confirmação de exclusão permanente do usuário autenticado.
   - Executar a deleção física do registro raiz do tenant:
     ```sql
     DELETE FROM tenants WHERE id = 'tenant-uuid-a-excluir';
     ```
   - Graças às restrições `ON DELETE CASCADE` configuradas em todas as tabelas filhas (`manuscritos`, `notas`, `entidades`, `chunks_vetoriais`, `grafo_arestas`), o banco executa automaticamente a remoção em cascata de todos os dados do tenant em todas as tabelas.
2. **VACUUM Físico (Remoção de Traços em Disco):**
   - Após a deleção lógica das linhas, executar a rotina de compactação física do PostgreSQL para sobrescrever os blocos de disco liberados:
     ```sql
     VACUUM FULL ANALYZE manuscritos;
     VACUUM FULL ANALYZE notas;
     -- Repetir para cada tabela sensível
     ```
3. **Exportação Portável Estruturada (Portabilidade):**
   - Ao receber solicitação de exportação, compilar um pacote `.zip` contendo:
     - `manuscritos.json`: Textos em formato aberto.
     - `wiki.json`: Fichas de personagens, locais e facções.
     - `grafo.json`: Nós e arestas do GUF em formato GraphML/JSON-LD.
     - `timeline.json`: Eventos e linhas do tempo.
   - Gerar um link de download seguro e temporário (válido por 24h) protegido por token de autenticação do usuário.
4. **Log de Consentimento Imutável:**
   - Registrar cada ação de aceite ou revogação de termos e cada deleção física executada na tabela protegida:
     ```sql
     INSERT INTO consent_audit_log (tenant_id, action, timestamp, ip_address)
     VALUES ('tenant-uuid', 'DATA_DELETION_COMPLETED', NOW(), '...ip...');
     ```
   - A tabela deve ser configurada sem permissão de `UPDATE` ou `DELETE` para qualquer role no sistema (incluindo superusuários de aplicação).

## Parâmetros e configuração
- `EXPORT_LINK_TTL_HOURS`: Tempo de validade do link de exportação portável. Padrão: `24` horas.
- `CASCADE_DELETE_TABLES`: Lista das tabelas que possuem `ON DELETE CASCADE` vinculadas ao `tenant_id`. Padrão: `["manuscritos", "notas", "entidades", "chunks_vetoriais", "grafo_nos", "grafo_arestas"]`.
- `AUDIT_LOG_TABLE`: Nome da tabela imutável de consentimento. Padrão: `"consent_audit_log"`.

## Armadilhas e como evitá-las
- **Armadilha:** Deleção Lógica como Solução de Privacidade: implementar apenas a marcação de linhas com `is_deleted = true` ou `deleted_at = timestamp` e considerar isso suficiente para o direito ao esquecimento da LGPD. Os dados permanecem inteiros e legíveis nos blocos físicos de disco e em backups de banco.
  **Mitigação:** O direito ao apagamento sob LGPD/GDPR exige que os dados pessoais e o conteúdo literário proprietário sejam removidos fisicamente dos blocos de disco do servidor. A deleção lógica via flag `is_deleted` pode ser usada para operações temporárias de recycle-bin, mas **não é uma implementação legal suficiente** para responder a solicitações formais de exclusão (GDPR Multi-Tenant, 2023).

## Critérios de validação (Definition of Done)
- [ ] A deleção física em cascata elimina 100% das linhas e chunks vinculados ao tenant em todas as tabelas indexadas após a requisição de exclusão.
- [ ] O log de auditoria de consentimento registra todos os eventos de deleção com timestamp e IP, sendo imutável mesmo com credenciais de superusuário.

## Fundamentação científica
- GDPR Multi-Tenant (2023) - GDPR Compliance Patterns in Multi-Tenant Cloud Applications - IEEE CLOUD 2023
- LGPD Compliance SaaS (2024) - Implementação da LGPD em plataformas SaaS: desafios e padrões - SBC 2024
- Zero Trust Architecture Group (2024) - Zero Trust Architecture for Multi-Tenant AI Systems - NIST SP 2024

## Requisitos do projeto relacionados
- RF-128 (conformidade LGPD)
- RF-129 (dados criptografados)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*Os padrões SQL de Hard-Delete e VACUUM no PostgreSQL são estáveis. O risco de engenharia reside em mapear completamente todas as tabelas filhas vinculadas para garantir zero dados residuais.*

## Exemplos
**Fluxo de exclusão (Direito ao Esquecimento):**
1. Usuário clica em "Excluir Conta Permanentemente" e confirma com senha.
2. Sistema executa `DELETE FROM tenants WHERE id = 'tenant-A-uuid'`.
3. Cascata remove 1200 manuscritos, 4000 entidades, 80.000 chunks vetoriais do tenant A.
4. VACUUM FULL executado em background.
5. Log: `{action: "DATA_DELETION_COMPLETED", timestamp: "2026-01-01T12:00:00Z"}` registrado.
**Caso de falha conhecido:**
O sistema marcar `deleted_at = NOW()` e considerar o processo concluído, mas os dados continuarem acessíveis via backup diário do banco de dados do servidor.
