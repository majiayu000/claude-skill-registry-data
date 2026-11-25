---
name: ads-concorrencia
description: Pesquisa de concorrência na Biblioteca de Anúncios da Meta pelo Meta Ads MCP. Use quando o usuário pedir para ver o que os concorrentes anunciam, o que as clínicas da cidade estão rodando, um raio-x antes de reunião com prospect, referências de criativo ou matéria-prima para copy de harmonização, odontologia ou outro nicho.
---

# Raio-x de concorrência (Biblioteca de Anúncios)

**Uso:**
- abrir reunião com prospect ("olha o que as clínicas da tua cidade estão anunciando");
- buscar referência de gancho e formato para a copy.

É só leitura de dados públicos.

## Passo a passo
1. **Definir o recorte com o usuário:** nicho (ex.: harmonização facial, implante, lente de resina), cidade ou região e, se houver, nomes ou páginas dos concorrentes.
2. **Buscar:** `ads_library_search` com:
   - `search_terms`: o termo do nicho, de preferência com a cidade (ex.: "harmonização facial Porto Alegre");
   - `countries=["BR"]`;
   - `ad_active_status=ACTIVE` (o que está no ar agora);
   - `limit=50` (é o máximo);
   - `page_ids`: quando já se conhece a página do concorrente;
   - mais o `client_conversation_id`, o `client_model` e o `advertiser_request` de sempre.
3. Repetir com 2 ou 3 variações de termo. **Não usar para varredura em massa:** a própria ferramenta proíbe extração em lote.
4. **Analisar o que se repete:**
   - ganchos e primeiras linhas;
   - oferta (avaliação, condição, prova social);
   - formato (vídeo do profissional, antes e depois, carrossel);
   - destino (WhatsApp, site, formulário);
   - tempo no ar (anúncio antigo ainda ativo costuma ser vencedor).
5. **Separar o que é copiável do que fere as regras da casa:** promoção agressiva, "avaliação gratuita" e urgência falsa não servem para cliente premium da agência.

## Armadilhas
- Precisa de pelo menos um entre `search_terms`, `page_ids` e `countries`.
- O país vai em ISO-2 (`BR`).
- A biblioteca mostra o criativo, não a performance. Não afirmar que um anúncio "converte".
