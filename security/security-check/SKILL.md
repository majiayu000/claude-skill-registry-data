---
name: security-check
description: Faz a verificação de segurança completa do projeto - análise estática (bandit), auditoria de dependências (pip-audit, npm audit), revisão OWASP Top 10 do código alterado e pentest da API rodando localmente (injeção/SQLi, upload malicioso, arquivos gigantes, headers forjados, métodos inesperados, CORS). Corrige o que encontrar e cria teste de regressão para cada falha. Use antes de abrir PR que mexa em endpoint, upload, banco ou autenticação, ou quando pedirem "pentest", "teste de segurança", "teste de invasão".
---

# security-check

Verificação de segurança do projeto OCR de Placas. **Escopo: só o próprio código e a API
rodando em `localhost`.** Nunca aponte ferramentas ou payloads para hosts externos, para o
deploy de produção ou para qualquer serviço de terceiros.

## 1. Mapear a superfície de ataque

- Liste os endpoints atuais (`backend/app/routers/*.py`) e o que mudou nesta branch
  (`git diff origin/main...HEAD --stat`).
- Para cada endpoint anote: método, entrada (path/query/body/upload), se toca banco, se chama
  algo pesado (OCR), se devolve dado do usuário.

## 2. Análise estática e dependências

```bash
cd backend
source .venv/Scripts/activate   # Linux/macOS: .venv/bin/activate
bandit -r app -q
pip-audit -r requirements.txt
```

Se `frontend/package.json` existir:

```bash
cd frontend
npm audit --audit-level=high
```

Triagem: achado de severidade média/alta no nosso código → corrigir. CVE em dependência →
atualizar a versão (se não houver versão corrigida, registrar no PR o motivo e o impacto real).
Falso positivo → justificar no PR, não silenciar com `# nosec` sem explicação.

## 3. Revisão manual (OWASP Top 10) do código alterado

Leia o diff e procure, no mínimo:

- **Injeção**: SQL montado com f-string/concatenação/`text()` com entrada do usuário;
  `eval`/`exec`/`pickle`/`subprocess`/`os.system` com dado externo; path traversal ao montar
  caminho de arquivo com entrada do usuário.
- **Upload**: tipo, tamanho (`MAX_UPLOAD_BYTES`) e resolução (`MAX_IMAGE_PIXELS`) validados;
  arquivo nunca salvo com o nome original do cliente.
- **Reflexão/XSS**: header, nome de arquivo ou texto do cliente devolvido sem tratamento;
  `dangerouslySetInnerHTML` no React.
- **Exposição de dados**: stack trace, caminho interno ou segredo em resposta/log; segredo
  hardcoded no código.
- **Controle de acesso / CORS**: rota sem proteção que deveria ter; `allow_origins=["*"]`.
- **DoS**: loop/processamento proporcional à entrada sem limite.

## 4. Pentest da API local

Suba a API em outro processo (`uvicorn app.main:app --port 8002`, em background) e ataque
**apenas `http://127.0.0.1:8002`**. Para cada endpoint relevante, tente:

| Ataque | Exemplo | Esperado |
|---|---|---|
| Tipo de arquivo forjado | `.php`, `.html`, `.svg` com `Content-Type: image/jpeg` | 400, nada executado/salvo |
| Arquivo não-imagem | PDF, GIF, bytes aleatórios, arquivo vazio | 400 |
| Arquivo gigante | > `MAX_UPLOAD_BYTES` | 413, sem estourar memória |
| Decompression bomb | PNG pequeno declarando dimensões enormes | 400 |
| Header refletido | `Content-Type` com `<script>` | resposta sem o payload |
| Nome de arquivo malicioso | `../../etc/passwd`, `a"<svg onload=1>.jpg` | não usado em caminho; escapado na UI |
| Injeção (SQLi) | `' OR '1'='1`, `1; DROP TABLE x;--` em todo parâmetro que chegue ao banco | tratado como texto comum, sem erro 500 |
| Método inesperado | `GET`/`PUT`/`DELETE` em rota `POST` | 405 |
| JSON malformado / campos extras / tipos errados | | 422, sem stack trace |
| CORS | `Origin: https://evil.example` | origem não autorizada não recebe `Access-Control-Allow-Origin` |
| Erro interno | forçar exceção | 500 genérico, sem detalhes internos |

Use `curl` ou um script Python com `httpx` salvo no scratchpad (não commitar o script de
ataque em si — o que vai para o repo são os testes de regressão). Pare a API ao terminar.

## 5. Corrigir e provar

Para **cada** falha encontrada:

1. Escreva primeiro o teste que reproduz o ataque em `backend/tests/test_security.py` (ou no
   Playwright, se for no frontend) e confirme que ele falha.
2. Corrija o código com a menor mudança segura.
3. Rode `pytest` completo e confirme que tudo passa.

Se a correção mudar comportamento de negócio (ex: exigir autenticação, mudar contrato da API),
pare e pergunte ao usuário antes.

## 6. Relatório

Resuma para o usuário, e depois na descrição do PR (seção `## Security`):

- Ferramentas rodadas e resultado.
- Vulnerabilidades encontradas → como foram corrigidas → teste que cobre.
- Riscos aceitos/pendentes (com motivo).
