---
name: veronica
description: Conduzir projetos extensos ou retomar trabalho interrompido com estado local, dependências e evidências de conclusão. Tarefas pontuais seguem diretamente.
metadata:
  version: "1.2.0"
---

# Veronica

Conduza o objetivo até entregas verificáveis, preservando requisitos completos e próximo passo. Os helpers registram estado e artefatos; o agente e as ferramentas do host executam o trabalho e avaliam sua qualidade.

## Iniciar e retomar

Use o núcleo quando dependências, entregas ou tentativas precisam sobreviver à conversa. Uma tarefa curta pode usar apenas um checkpoint Markdown. Defina critérios observáveis e tarefas úteis, sem detalhar antecipadamente etapas que dependem de descobertas.

Na continuação, procure `work/veronica/veronica.db` e `RETOMAR.md` no workspace e leia a retomada antes de replanejar. Confira insumos, capacidades e efeitos atuais. `context` recupera o projeto completo; seleção por tarefa e paginação explícita estão em [economia.md](references/economia.md). Visões menores não substituem os registros. `resume --full` recupera todas as notas sem corte de caracteres.

## Estado e evidências

Consulte [operacao.md](references/operacao.md) ao operar `scripts/veronica.py`. Use Python 3.10+ disponível, workspace real e comandos JSON UTF-8.

- Inicialize objetivo e tarefas com critérios, dependências necessárias e áreas de escrita.
- Escolha tarefa pronta em `status`; `task.claim` devolve reserva e token privado do executor. Renove antes de expirar.
- Execute e registre descobertas que mudam a direção, falhas relevantes e próximo passo.
- Após verificar, anexe evidências por critério. `task.complete` exige evidências atuais; hashes e validade não substituem julgamento semântico.
- Antes de transferir ou encerrar, gere `checkpoint` com motivo e informe entregas, pendências e próxima ação.

Anexe os insumos que poderiam invalidar uma evidência, como código, dados e configuração. Alteração, prazo vencido ou nova tentativa exige revalidação. Cobertura depende dos insumos declarados. Leia [references/aceitacao.md](references/aceitacao.md) para escolher provas por domínio; mantenha preparação, execução e observação humana distintas.

Preserve pedidos e insumos detalhados em arquivos quando uma síntese puder perder informação; referencie os originais nas tarefas. Para diagnóstico, reconciliação ou transferência, consulte [recuperacao.md](references/recuperacao.md). Checkpoint do ledger e pacote de recuperação têm escopos diferentes; nenhum restaura aplicativos ou login.

## Eficiência com autonomia

Elimine trabalho redundante, preservando requisitos, dados exatos e liberdade de aprofundar. A otimização não impõe quota de tokens/tempo, modelo menor, menor esforço, respostas telegráficas ou menos verificações.

Considere agentes, skills, conectores, plugins, CLIs, bibliotecas e execução direta diante de uma ineficiência. Reuse capacidades verificadas; uma lacuna justifica descoberta dirigida. Compare preparação, contexto, chamadas adicionais, recursos locais e qualidade. Escolha a alternativa suficiente e amplie conforme necessário; disponibilidade não obriga uso.

Consulte [economia.md](references/economia.md) ao operar `scripts/preserve.py`, escolher integração ou medir vantagem. Originais byte-exatos permanecem acessíveis por leitura integral, recuperação e consulta literal. Compacidade é opcional, reversível e verificada. Nenhum artefato é apagado automaticamente. Busca sem resultado não prova ausência de um fato. Preserve formatos de pipelines, parsers e âncoras de edição.

Projetos novos usam `max_attempts: 0` e `repeat_failure: 0`, sem teto de tentativas ou bloqueio por repetição. Preserve configurações existentes; ajuste limites com motivo quando autorizado. Diagnóstico orienta a estratégia sem encerrar trabalho por economia presumida. Reservas protegem áreas de escrita e recursos de executores cooperantes.

Para efeitos externos, use `effect.*` do guia antes da chamada real e consulte o destino após um resultado incerto. O registro não executa ações, fornece idempotência ou amplia autorização.

## Agentes e avaliação

Consulte [coordenacao.md](references/coordenacao.md) ao delegar ou transferir. Delegue quando autorizado e quando a vantagem justificar contexto duplicado, preparação e integração. Defina entrega, critérios e área de escrita; use isolamento do host quando necessário e verifique o conjunto integrado.

Aprendizados ficam no projeto; mudanças globais de memória ou skill dependem de pedido do usuário. Leia [references/avaliacao.md](references/avaliacao.md) para comparar métodos e [references/origens.md](references/origens.md) apenas para consultar fontes de desenho. Separe tokens observados, estimativas, dinheiro, bytes e tempo; testes locais não comprovam economia faturada nem qualidade geral do modelo.
