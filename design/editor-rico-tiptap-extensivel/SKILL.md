---
name: editor-rico-tiptap-extensivel
description: Configura o editor de texto rico Tiptap/ProseMirror com extensões para escrita literária (notas de rodapé, comentários inline, modo foco, formatação rica). Ativar ao implementar ou estender o módulo core_editor da plataforma.
---

# editor-rico-tiptap-extensivel

## Descrição
A skill `editor-rico-tiptap-extensivel` define a configuração completa do editor Tiptap (baseado em ProseMirror) para a plataforma de escrita criativa literária. Ela especifica o conjunto de extensões necessárias para formatos literários (notas de rodapé, citações, capítulos numerados), as extensões de colaboração (cursores de colaboradores, comentários inline), o modo foco sem distração e a serialização para o formato de armazenamento interno.

## Quando usar
Gatilhos concretos e observáveis:
- Implementação inicial do componente de editor (`core_editor`).
- Adição de novos recursos de formatação solicitados nos RFs (UC-175 formatos ricos, UC-177 notas de rodapé, UC-141 modo foco).
- Integração do editor com o sistema de colaboração em tempo real CRDT.

Quando NÃO usar:
- Para a lógica de autosave e versionamento (ver `autosave-e-historico-de-versoes`).
- Para a implementação do CRDT de colaboração em tempo real (ver `concorrencia-editor-texto-rico-crdt`).

## Pré-requisitos
- `@tiptap/core`, `@tiptap/starter-kit` instalados.
- `@tiptap/extension-collaboration` e `yjs` para colaboração.
- `@tiptap/extension-comment` ou extensão customizada para comentários inline.

## Processo (passo a passo executável)
1. **Conjunto Base de Extensões (StarterKit):**
   ```ts
   import { useEditor } from '@tiptap/react'
   import StarterKit from '@tiptap/starter-kit'
   import { Footnote } from './extensions/Footnote'
   import { InlineComment } from './extensions/InlineComment'
   import { FocusMode } from './extensions/FocusMode'
   import { ChapterNumber } from './extensions/ChapterNumber'

   const editor = useEditor({
     extensions: [
       StarterKit.configure({ history: false }), // desativar history nativo (CRDT gerencia)
       Footnote,
       InlineComment,
       FocusMode,
       ChapterNumber,
       Table.configure({ resizable: true }),
       Image.configure({ allowBase64: false }), // apenas URLs de object storage
     ],
     content: documentoJSON,
     editorProps: {
       attributes: { class: 'prose prose-lg max-w-none literary-editor' }
     }
   })
   ```

2. **Extensão de Nota de Rodapé (Footnote):**
   - Criar mark customizado `Footnote` que ao ser aplicado insere um superscript numerado no texto e adiciona o bloco de texto da nota ao fim do documento num nó `FootnoteList`.
   - Numerar notas automaticamente por ordem de aparição (reindexar ao deletar uma nota).

3. **Extensão de Comentário Inline (InlineComment):**
   - Criar mark `comment` com atributo `{ commentId, authorId, resolvedAt }`.
   - Trechos comentados exibem highlight amarelo claro; ao clicar, abrir painel lateral com thread de comentários.
   - Marcar como resolvido muda a cor do highlight para cinza sem remover o mark do documento.

4. **Modo Foco (FocusMode):**
   - Extensão que ao ser ativada adiciona classe CSS `focus-mode` ao container do editor.
   - CSS aplica `opacity: 0.15` em todos os parágrafos exceto o parágrafo ativo (onde o cursor está), mantendo `opacity: 1.0` no parágrafo atual para destacar o trecho em edição.
   - Ativar/desativar via atalho `Ctrl+Shift+F`.

5. **Serialização para Armazenamento:**
   - Armazenar documentos no banco em formato JSON nativo do ProseMirror (`editor.getJSON()`).
   - Nunca armazenar HTML — usar `editor.getHTML()` apenas para exportações e visualizações.

## Parâmetros e configuração
| Parâmetro | Descrição | Padrão |
|---|---|---|
| `MAX_FOOTNOTES_PER_DOC` | Limite de notas de rodapé por documento | `200` |
| `FOCUS_MODE_SHORTCUT` | Atalho de teclado para modo foco | `Ctrl+Shift+F` |
| `COMMENT_HIGHLIGHT_COLOR` | Cor CSS de destaque de comentário não resolvido | `#FFF3CD` |
| `AUTOFOCUS_ON_OPEN` | Colocar cursor no início do documento ao abrir | `true` |

## Armadilhas e como evitá-las
- **Armadilha:** Armazenar o conteúdo do editor em HTML no banco de dados. HTML é frágil, difícil de migrar entre versões do editor, propenso a inconsistências de serialização e vulnerável a XSS ao renderizar sem sanitização.
  **Mitigação:** Persistir **sempre** em JSON ProseMirror via `editor.getJSON()`. O HTML deve ser gerado sob demanda apenas para exportações e pré-visualizações, usando `generateHTML(docJSON, extensions)` do Tiptap.

## Critérios de validação (Definition of Done)
- [ ] O editor suporta formatos ricos (negrito, itálico, listas, citações, tabelas) conforme UC-175.
- [ ] Notas de rodapé são inseridas, numeradas automaticamente e removíveis sem quebrar a numeração.
- [ ] O modo foco é ativado e desativado via atalho `Ctrl+Shift+F` sem recarregar o documento.

## Exemplos
**Inserção de nota de rodapé:**
Usuário seleciona "Kael¹" → pressiona `Ctrl+Alt+F` → editor insere superscript `¹` inline e abre campo de texto no rodapé do documento para digitar a nota.

**Comentário inline:**
Editor seleciona "a chuva caía" → clica "Comentar" → thread abre na sidebar: "Verificar se é inverno neste capítulo". Colaborador responde e resolve o comentário.
