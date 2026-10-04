---
name: vetorizacao-e-contexto-de-escrita
description: Compila assincronamente o contexto de escrita do autor em vetor unificado (CAC) para alimentar motores de recomendacao locais.
---
# vetorizacao-e-contexto-de-escrita

## Descrição
A skill `vetorizacao-e-contexto-de-escrita` compila assincronamente o estado dinâmico atual da sessão de escrita do autor em um vetor de contexto de escrita (CAC - Contextual Authoring Context). Esse vetor unifica a semântica do texto recente, as relações ativas da cena no grafo de lore, a posição estrutural do livro e o histórico de aceitação de sugestões do escritor, servindo de payload básico para alimentar motores locais de recomendação de enredo e personagens.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor digita um caractere de quebra de parágrafo (tecla `Enter`) no editor de texto.
- Ocorre o acionamento de um atalho de teclado associado a sugestões contextuais (ex: `Ctrl+Space`).
- O cursor de digitação permanece estacionário por mais de `5` segundos na mesma linha (trigger de idle).

Quando NÃO usar:
- A cada caractere pressionado de digitação ativa (tecla-a-tecla), sob o risco de travar a interface.
- Durante a importação offline global de arquivos (onde a indexação em lote estática é aplicada).

## Pré-requisitos
- Modelo de embeddings local carregado em memória.
- Acesso à fila em memória das últimas 100 ações de aceitação/rejeição de sugestões de IA.
- Grafo local do romance (GUF) instanciado para recuperar as entidades da cena ativa.

## Processo (passo a passo executável)
1. **Extração e Vetorização do Texto Recente ($c_1$):**
   - Recuperar as últimas 512 palavras escritas no cursor do editor.
   - Enviar a string para o modelo de embeddings local, gerando o vetor textual $c_1$.
2. **Extração de Estado do Grafo ($c_2$):**
   - Ler no outline do romance quais nós de personagens e locais estão associados à cena ativa.
   - Extrair os vetores de atributos desses nós do banco de grafos local e calcular a média ponderada, resultando no vetor de estado narrativo $c_2$.
3. **Mapeamento de Posição Estrutural ($c_3$):**
   - Obter a quantidade de palavras atual do livro ($W_{atual}$) e o limite planejado ($W_{total}$).
   - Calcular a fração de conclusão: $P = \frac{W_{atual}}{W_{total}}$ (faixa de $0.0$ a $1.0$).
   - Multiplicar $P$ por um vetor de pesos estruturais pré-definidos para gerar $c_3$.
4. **Processamento do Feedback do Autor ($c_4$):**
   - Obter o histórico das últimas 100 interações de recomendação.
   - Computar a média vetorial ponderada dos embeddings das sugestões aceitas, aplicando decaimento temporal de $0.95$ por passo para priorizar preferências recentes. Rótulo: $c_4$.
5. **Combinação Assíncrona de Variáveis (Vetor CAC):**
   - Concatenar ou calcular a média ponderada dos componentes lógicos:
     \[\mathbf{c}_{CAC} = w_1 c_1 + w_2 c_2 + w_3 c_3 + w_4 c_4\]
     Onde os pesos sugeridos são $w_1 = 0.50$, $w_2 = 0.30$, $w_3 = 0.10$ e $w_4 = 0.10$.
   - Executar a concatenação de forma debounced em um worker de background (thread separada).

## Parâmetros e configuração
- `CAC_DEBOUNCE_DELAY_MS`: Tempo de debounce para atrasar o cálculo após a última tecla. Padrão: `1000` (1 segundo).
- `RECENT_WORDS_COUNT`: Quantidade de palavras recentes capturadas no editor para $c_1$. Padrão: `512`.
- `WEIGHT_TEXT_RECENT`: Peso da semântica recente $w_1$ no vetor final. Padrão: `0.50`.

## Armadilhas e como evitá-las
- **Armadilha:** Processamento Síncrono no Editor: computar o embedding e fazer queries de grafos a cada caractere pressionado de forma síncrona na thread principal trava o renderizador da página (FPS cai a zero), gerando travamentos ("lag") severos e inviabilizando a escrita.
  **Mitigação:** Desacoplar a geração de contexto da thread principal. O cálculo do vetor CAC deve ser executado obrigatoriamente dentro de um Web Worker de forma debounced, disparando apenas quando o autor pausar a digitação (`CAC_DEBOUNCE_DELAY_MS = 1000`) ou digitar quebras de parágrafo explícitas.

## Critérios de validação (Definition of Done)
- [ ] A latência total de compilação e consolidação do vetor CAC em background é inferior a 50ms na máquina local.
- [ ] O cálculo do vetor não gera perda de quadros (frames dropped) no editor visual da interface principal.

## Fundamentação científica
- RecSys Survey (2022) - A Survey on Conversational Recommender Systems - arXiv 2022
- Sequential RecSys (SEQUENTIAL RECSYS GROUP, 2021) - Sequential Recommender Systems: A Survey - ACM CSUR
- SCORE (SCORE GROUP, 2025) - Story Coherence and Retrieval Enhancement for AI Narratives - arXiv 2025

## Requisitos do projeto relacionados
- RF-30 (contexto implícito)
- RF-81 (sugestões inline)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: O acoplamento dinâmico de pesos de feedback do autor ($w_4$) e estados de grafos ($w_2$) pode gerar desvios vetoriais (drift) caso o autor mude repentinamente a direção estilística do romance.*
*Fallback para v1:* Configurar o vetor CAC para utilizar estritamente a semântica recente do texto ($c_1$), desativando as dependências de grafos locais e histórico de aceitações de IA na v1 da ferramenta.

## Exemplos
**Entrada (Metadados locais):**
- Últimas palavras: "Kael ergueu a lâmpada..."
- Personagem na cena: "Kael"
- Posição da obra: 10% concluída.
**Saída esperada (Vetor CAC):**
```json
{
  "vector_dimensions": 768,
  "status": "COMPILED",
  "meta": {
    "active_scene_entities": ["char_kael"],
    "completion_ratio": 0.10
  }
}
```
**Caso de falha conhecido:**
O sistema disparar o recálculo do vetor CAC de 768 dimensões a cada tecla digitada pelo escritor, paralisando a digitação no navegador.
