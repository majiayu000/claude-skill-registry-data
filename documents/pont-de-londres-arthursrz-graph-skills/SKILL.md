---
name: pont-de-londres
description: "Pattern d'intégration pour relier un graphe de domaine (structuré, issu d'un CSV) à un graphe lexical (extrait automatiquement de documents non-structurés via LLM). Utiliser cette skill lorsque Claude doit construire un Knowledge Graph hybride combinant données structurées et extraction automatique, notamment avec neo4j-graphrag et SimpleKGPipeline. Cas d'usage: GraphRAG, ingestion de PDFs avec métadonnées, construction de Knowledge Graphs à partir de sources hétérogènes."
---

# Le Pont de Londres

*Pattern d'intégration Domain Graph / Lexical Graph, formalisé selon Vaishnavi & Kuechler*

## Problème

Dans le roman de Céline, le pont de Londres relie deux rives qui s'ignorent — le chaos de la guerre et la vie qui continue, deux mondes qui coexistent sans se comprendre. Le même problème se pose en architecture de données : comment relier un graphe de domaine (structuré, issu d'un CSV) à un graphe lexical (extrait automatiquement de documents non-structurés), quand ces deux rives parlent des langues différentes ?

## Solution

La solution procède en cinq étapes.

### Étape 1 : Spécifier le schéma du graphe lexical

Avant toute extraction, définir l'ontologie qui guidera le LLM. Cette spécification comprend trois éléments.

**Types de nœuds** — Les entités à extraire. Certains sont de simples labels, d'autres sont enrichis avec une description (pour guider le LLM) et des propriétés typées :

```python
NODE_TYPES = [
    "Technology",
    "Concept",
    "Example",
    "Process",
    "Challenge",
    {"label": "Benefit", "description": "A benefit or advantage of using a technology or approach."},
    {
        "label": "Resource",
        "description": "A related learning resource such as a book, article, video, or course.",
        "properties": [
            {"name": "name", "type": "STRING", "required": True}, 
            {"name": "type", "type": "STRING"}
        ]
    },
]
```

**Types de relations** — Les verbes possibles entre entités :

```python
RELATIONSHIP_TYPES = [
    "RELATED_TO",
    "PART_OF",
    "USED_IN",
    "LEADS_TO",
    "HAS_CHALLENGE",
    "CITES"
]
```

**Patterns** — Les combinaisons valides. Le LLM ne pourra extraire que des triplets conformes :

```python
PATTERNS = [
    ("Technology", "RELATED_TO", "Technology"),
    ("Concept", "RELATED_TO", "Technology"),
    ("Example", "USED_IN", "Technology"),
    ("Process", "PART_OF", "Technology"),
    ("Technology", "HAS_CHALLENGE", "Challenge"),
    ("Concept", "HAS_CHALLENGE", "Challenge"),
    ("Technology", "LEADS_TO", "Benefit"),
    ("Process", "LEADS_TO", "Benefit"),
    ("Resource", "CITES", "Technology"),
]
```

### Étape 2 : Configurer le pipeline d'extraction

Le pipeline assemble le LLM, l'embedder, le text splitter et le schéma :

```python
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter

llm = OpenAILLM(
    model_name="gpt-4o",
    model_params={
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
)

embedder = OpenAIEmbeddings(model="text-embedding-ada-002")
text_splitter = FixedSizeSplitter(chunk_size=500, chunk_overlap=100)

kg_builder = SimpleKGPipeline(
    llm=llm,
    driver=neo4j_driver, 
    neo4j_database=os.getenv("NEO4J_DATABASE"), 
    embedder=embedder, 
    from_pdf=True,
    text_splitter=text_splitter,
    schema={
        "node_types": NODE_TYPES,
        "relationship_types": RELATIONSHIP_TYPES,
        "patterns": PATTERNS
    },
)
```

Le pipeline effectue : PDF → chunks → extraction LLM guidée par le schéma → création des nœuds/relations → embeddings.

### Étape 3 : Transformer le CSV en dictionnaire

Chaque ligne du CSV (qui incarne le graphe de domaine) devient un dictionnaire Python :

```python
docs_csv = csv.DictReader(
    open(os.path.join(data_path, "docs.csv"), encoding="utf8", newline='')
)
# Produit : {"filename": "lesson1.pdf", "url": "https://...", "lesson": "Intro", "module": "M1", "course": "GraphRAG"}
```

### Étape 4 : Ajouter la clé commune au dictionnaire

Le pipeline crée des nœuds `Document` avec une propriété `path`. C'est cette propriété qui servira de pont entre les deux graphes. Enrichir le dictionnaire avec une clé `pdf_path` construite pour correspondre exactement à ce que le pipeline va stocker :

```python
doc["pdf_path"] = os.path.join(data_path, doc["filename"])
# Ajoute : {"pdf_path": "./genai-graphrag-python/data/lesson1.pdf", ...}
```

Cette même valeur est passée au pipeline qui génère le graphe lexical et stocke le chemin dans `Document.path` :

```python
result = asyncio.run(
    kg_builder.run_async(file_path=doc["pdf_path"])
)
```

### Étape 5 : Joindre les deux graphes par Cypher

Une requête utilise la clé commune pour rattacher le graphe de domaine au graphe lexical :

```cypher
MATCH (d:Document {path: $pdf_path})
MERGE (l:Lesson {url: $url})
SET l.name = $lesson,
    l.module = $module,
    l.course = $course
MERGE (d)-[:PDF_OF]->(l)
```

Le dictionnaire enrichi est passé en paramètres :

```python
neo4j_driver.execute_query(cypher, parameters_=doc)
```

## Conséquences

Le pattern fonctionne parce que `doc["pdf_path"]` et `Document.path` contiennent la même valeur. Cette clé implicite relie deux rives : le graphe lexical (entités extraites selon le schéma spécifié) et le graphe de domaine (structure métier issue du CSV). Si ces valeurs divergent, le pont s'effondre silencieusement — et comme chez Céline, personne ne s'en aperçoit.

## Vérification

Pour s'assurer que le pont tient, vérifier que les `Document` sont bien rattachés :

```cypher
// Documents orphelins (pont cassé)
MATCH (d:Document)
WHERE NOT EXISTS { (d)-[:PDF_OF]->(:Lesson) }
RETURN d.path AS orphan

// Leçons sans document (pont jamais construit)
MATCH (l:Lesson)
WHERE NOT EXISTS { (:Document)-[:PDF_OF]->(l) }
RETURN l.name AS missing
```

## Référence complète

Pour un exemple complet d'implémentation, voir `references/full_example.py`.

## Ressources

Ce pattern est documenté et illustré dans le repo de référence : https://github.com/ArthurSrz/graphrag101
