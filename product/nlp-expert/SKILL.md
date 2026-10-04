---
name: nlp-expert
description: Natural Language Processing expertise from Google AI. Use when building text processing pipelines, implementing sentiment analysis, creating chatbots, working with embeddings (Word2Vec, BERT, sentence-transformers), fine-tuning language models, building search/retrieval systems, implementing named entity recognition (NER), or integrating LLM APIs for text tasks. Triggers on NLP, text processing, sentiment analysis, embeddings, tokenization, language models, or text classification.
---

# NLP Expert - Natural Language Processing

**Purpose**: Build NLP applications with text processing, embeddings, transformers, and language models

**Agent**: Google AI Researcher
**Use When**: Building chatbots, text classification, sentiment analysis, or language understanding systems

---

## Text Preprocessing

```python
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remove special characters
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    return ' '.join(tokens)

# Example
text = "I'm loving the new features! Check out https://example.com"
clean = preprocess_text(text)  # "love new feature check"
```

---

## Text Classification (Sentiment Analysis)

```python
from transformers import pipeline

# Pre-trained sentiment analysis
classifier = pipeline('sentiment-analysis')

result = classifier("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# Batch processing
texts = [
    "This is great!",
    "This is terrible.",
    "Not sure about this."
]
results = classifier(texts)

# Custom model (fine-tuned)
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
model = AutoModelForSequenceClassification.from_pretrained(
    'distilbert-base-uncased',
    num_labels=2
)

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)

    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

    positive_score = predictions[0][1].item()
    return 'positive' if positive_score > 0.5 else 'negative'
```

---

## Named Entity Recognition (NER)

```python
from transformers import pipeline

ner = pipeline('ner', aggregation_strategy='simple')

text = "Apple Inc. was founded by Steve Jobs in Cupertino, California."
entities = ner(text)

for entity in entities:
    print(f"{entity['word']}: {entity['entity_group']} ({entity['score']:.2f})")

# Output:
# Apple Inc.: ORG (0.99)
# Steve Jobs: PER (0.99)
# Cupertino: LOC (0.99)
# California: LOC (0.99)
```

---

## Text Embeddings

```python
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
sentences = [
    "The cat sits on the mat",
    "A dog plays in the park",
    "The feline rests on the rug"
]

embeddings = model.encode(sentences)

# Compute similarity
from sklearn.metrics.pairwise import cosine_similarity

similarities = cosine_similarity(embeddings)
print(similarities)
# [[1.00, 0.45, 0.82],  # cat & mat similar to feline & rug
#  [0.45, 1.00, 0.48],
#  [0.82, 0.48, 1.00]]

# Semantic search
def semantic_search(query, documents):
    query_embedding = model.encode([query])
    doc_embeddings = model.encode(documents)

    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

    # Sort by similarity
    results = sorted(
        zip(documents, similarities),
        key=lambda x: x[1],
        reverse=True
    )

    return results

# Usage
docs = [
    "Python is a programming language",
    "The cat is sleeping",
    "Machine learning with Python"
]

results = semantic_search("coding in Python", docs)
# [("Python is a programming language", 0.85),
#  ("Machine learning with Python", 0.72),
#  ("The cat is sleeping", 0.12)]
```

---

## Question Answering

```python
from transformers import pipeline

qa = pipeline('question-answering')

context = """
Python is a high-level programming language created by Guido van Rossum
in 1991. It emphasizes code readability and simplicity.
"""

question = "Who created Python?"

answer = qa(question=question, context=context)
print(answer['answer'])  # "Guido van Rossum"
print(f"Confidence: {answer['score']:.2f}")
```

---

## Text Generation (GPT)

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def generate_text(prompt, max_length=100):
    inputs = tokenizer.encode(prompt, return_tensors='pt')

    outputs = model.generate(
        inputs,
        max_length=max_length,
        num_return_sequences=1,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text

# Usage
prompt = "Once upon a time"
story = generate_text(prompt)
print(story)
```

---

## Chatbot (RAG - Retrieval Augmented Generation)

```python
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# 1. Load documents and create vector store
documents = [
    "Our store is open Monday to Friday, 9 AM to 5 PM.",
    "We offer free shipping on orders over $50.",
    "Returns are accepted within 30 days of purchase."
]

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(documents, embeddings)

# 2. Create retrieval QA chain
llm = ChatOpenAI(temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# 3. Ask questions
response = qa_chain({"query": "What are your store hours?"})
print(response['result'])
# "Our store is open Monday to Friday, 9 AM to 5 PM."
```

---

## Language Detection

```python
from langdetect import detect

texts = [
    "Hello, how are you?",
    "Bonjour, comment allez-vous?",
    "Hola, ¿cómo estás?"
]

for text in texts:
    lang = detect(text)
    print(f"{text} -> {lang}")

# Output:
# Hello, how are you? -> en
# Bonjour, comment allez-vous? -> fr
# Hola, ¿cómo estás? -> es
```

---

## Text Summarization

```python
from transformers import pipeline

summarizer = pipeline('summarization', model='facebook/bart-large-cnn')

article = """
Natural language processing (NLP) is a subfield of linguistics, computer
science, and artificial intelligence concerned with the interactions between
computers and human language. NLP techniques are used in many applications
including machine translation, sentiment analysis, and question answering.
Modern NLP systems use deep learning models like transformers.
"""

summary = summarizer(article, max_length=50, min_length=25)
print(summary[0]['summary_text'])
# "Natural language processing is concerned with interactions between
#  computers and human language. Modern NLP uses deep learning transformers."
```

---

## Best Practices

- Preprocess text consistently
- Use pre-trained models when possible (transfer learning)
- Fine-tune on domain-specific data
- Handle multiple languages if needed
- Cache embeddings for efficiency
- Monitor model performance on real data
- Consider ethical implications (bias, privacy)
- Use GPU for faster inference

---

**Remember**: Language is complex. Start with pre-trained models, fine-tune for your domain, and always validate on real data.

**Created**: 2026-02-04
**Maintained By**: Google AI Researcher
