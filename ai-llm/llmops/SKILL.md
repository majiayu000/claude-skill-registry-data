---
name: llmops
description: "LLMOps — RAG 운영, 프롬프트 버전 관리, Ragas 기반 LLM 평가, NeMo 가드레일. Use when LLM 앱을 운영 환경에서 품질 평가하고 프롬프트 변경을 관리하거나 가드레일을 붙일 때."
---

# LLMOps 가이드

RAG 운영, 프롬프트 버전 관리, LLM 평가(Ragas), 가드레일(NeMo)

## LLMOps: RAG 운영

### RAG 아키텍처

```
+------------------------------------------------------------------+
|                         RAG Pipeline                               |
+------------------------------------------------------------------+
|                                                                    |
|  사용자 쿼리                                                        |
|       |                                                            |
|       v                                                            |
|  +-------------+                                                   |
|  | Embedding   |                                                   |
|  | Model       |                                                   |
|  +-------------+                                                   |
|       |                                                            |
|       v                                                            |
|  +-------------+     +-------------+                               |
|  | Vector      |<--->| Document    |                               |
|  | Store       |     | Store       |                               |
|  | (Pinecone,  |     | (S3, etc.)  |                               |
|  |  Weaviate)  |     +-------------+                               |
|  +-------------+                                                   |
|       |                                                            |
|       v (Top-K 문서)                                               |
|  +-------------+                                                   |
|  | LLM         |                                                   |
|  | (GPT-4,     |                                                   |
|  |  Claude)    |                                                   |
|  +-------------+                                                   |
|       |                                                            |
|       v                                                            |
|  응답 생성                                                          |
|                                                                    |
+------------------------------------------------------------------+
```

### LangChain RAG 구현

```python
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Weaviate
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import weaviate

# 벡터 스토어 연결
client = weaviate.Client(
    url="http://weaviate:8080",
    auth_client_secret=weaviate.AuthApiKey(api_key="...")
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Weaviate(
    client=client,
    index_name="Documents",
    text_key="content",
    embedding=embeddings
)

# RAG Chain 구성
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

prompt_template = """다음 컨텍스트를 사용하여 질문에 답하세요.
컨텍스트에 답이 없으면 "정보를 찾을 수 없습니다"라고 답하세요.

컨텍스트:
{context}

질문: {question}

답변:"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    chain_type_kwargs={"prompt": PROMPT},
    return_source_documents=True
)

# 실행
result = qa_chain.invoke({"query": "API 인증 방법은?"})
print(result["result"])
```

### 벡터 스토어 Kubernetes 배포

```yaml
# Weaviate 배포
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: weaviate
  namespace: llmops
spec:
  serviceName: weaviate
  replicas: 1
  selector:
    matchLabels:
      app: weaviate
  template:
    metadata:
      labels:
        app: weaviate
    spec:
      containers:
        - name: weaviate
          image: semitechnologies/weaviate:1.27.0
          ports:
            - containerPort: 8080
          env:
            - name: QUERY_DEFAULTS_LIMIT
              value: "25"
            - name: AUTHENTICATION_APIKEY_ENABLED
              value: "true"
            - name: AUTHENTICATION_APIKEY_ALLOWED_KEYS
              valueFrom:
                secretKeyRef:
                  name: weaviate-secrets
                  key: api-key
            - name: PERSISTENCE_DATA_PATH
              value: "/var/lib/weaviate"
            - name: DEFAULT_VECTORIZER_MODULE
              value: "text2vec-openai"
            - name: ENABLE_MODULES
              value: "text2vec-openai,generative-openai"
          volumeMounts:
            - name: data
              mountPath: /var/lib/weaviate
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 2
              memory: 4Gi
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 50Gi
```

---

## 프롬프트 버전 관리

### LangSmith 연동

```python
import os
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "..."
os.environ["LANGCHAIN_PROJECT"] = "my-llm-app"

client = Client()

# 프롬프트 저장
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 유용한 AI 어시스턴트입니다."),
    ("human", "{input}")
])

client.push_prompt("my-prompt", object=prompt)

# 프롬프트 로드 (버전 관리)
prompt_v1 = client.pull_prompt("my-prompt:v1")
prompt_latest = client.pull_prompt("my-prompt")
```

### 프롬프트 템플릿 관리 (Git 기반)

```yaml
# prompts/qa_prompt.yaml
name: qa_prompt
version: "1.0.0"
description: "Question answering prompt for RAG"

template: |
  You are a helpful assistant. Answer the question based on the context.

  Context:
  {context}

  Question: {question}

  Answer:

input_variables:
  - context
  - question

metadata:
  model: gpt-4-turbo
  temperature: 0
  max_tokens: 1000
```

---

## LLM 평가 & 가드레일

### Ragas 평가

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from datasets import Dataset

# 평가 데이터셋 준비
eval_data = {
    "question": ["API 인증 방법은?", "에러 처리는?"],
    "answer": ["OAuth2 토큰 인증을 사용합니다.", "try-catch로 처리합니다."],
    "contexts": [
        ["OAuth2를 사용한 인증...", "Bearer 토큰..."],
        ["예외 처리 가이드...", "에러 핸들러..."]
    ],
    "ground_truth": ["OAuth2 Bearer 토큰", "예외 처리"]
}

dataset = Dataset.from_dict(eval_data)

# 평가 실행
result = evaluate(
    dataset,
    metrics=[
        faithfulness,      # 응답이 컨텍스트에 충실한가
        answer_relevancy,  # 응답이 질문과 관련있는가
        context_precision, # 검색된 컨텍스트가 정확한가
        context_recall     # 필요한 컨텍스트를 모두 검색했는가
    ]
)

print(result)
# {'faithfulness': 0.92, 'answer_relevancy': 0.88, ...}
```

### 가드레일 (NeMo Guardrails)

```python
from nemoguardrails import LLMRails, RailsConfig

config = RailsConfig.from_path("./guardrails_config")

rails = LLMRails(config)

# 안전한 응답 생성
response = rails.generate(messages=[{
    "role": "user",
    "content": "비밀번호를 알려줘"
}])
# 가드레일이 부적절한 요청 차단
```

```yaml
# guardrails_config/config.yml
models:
  - type: main
    engine: openai
    model: gpt-4-turbo

rails:
  input:
    flows:
      - check topic  # 주제 확인
      - check jailbreak  # 탈옥 시도 감지

  output:
    flows:
      - check facts  # 사실 확인
      - check hallucination  # 환각 감지

prompts:
  - task: self_check_input
    content: |
      이 메시지가 부적절하거나 유해한 내용을 요청하는지 확인하세요.
      메시지: {{ user_input }}
      결과 (yes/no):
```

### 출력 검증

```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class StructuredResponse(BaseModel):
    answer: str = Field(description="질문에 대한 답변")
    confidence: float = Field(ge=0, le=1, description="신뢰도 (0-1)")
    sources: list[str] = Field(description="참조 문서 목록")

parser = PydanticOutputParser(pydantic_object=StructuredResponse)

# 프롬프트에 포맷 지시 추가
prompt = prompt.partial(format_instructions=parser.get_format_instructions())

# 응답 파싱 및 검증
chain = prompt | llm | parser
result = chain.invoke({"question": "..."})  # StructuredResponse 객체
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 실험 추적 없음 | 재현 불가 | MLflow/W&B 사용 |
| 모델 버전 미관리 | 롤백 불가 | Model Registry |
| RAG 평가 생략 | 품질 저하 모름 | Ragas 정기 평가 |
| 가드레일 없음 | 유해 응답 생성 | NeMo Guardrails |
| 프롬프트 하드코딩 | 관리 어려움 | 버전 관리 시스템 |
| 비용 모니터링 없음 | 예산 초과 | 토큰 사용량 추적 |

---

## 체크리스트

### MLOps
- [ ] Kubeflow 또는 MLflow 설치
- [ ] 파이프라인 정의 (학습/배포)
- [ ] 모델 레지스트리 설정
- [ ] KServe 배포

### LLMOps
- [ ] 벡터 스토어 설정
- [ ] RAG 파이프라인 구축
- [ ] 프롬프트 버전 관리

### 평가
- [ ] Ragas 평가 파이프라인
- [ ] 가드레일 설정
- [ ] 출력 검증 스키마

### 모니터링
- [ ] 토큰 사용량 추적
- [ ] 응답 품질 메트릭
- [ ] 비용 알림 설정

**관련 skill**: `/ai:ml-serving`, `/k8s:k8s-gpu`, `/sre:finops`

---

## Sources

- [Kubeflow Documentation](https://www.kubeflow.org/docs/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [KServe](https://kserve.github.io/website/)
- [LangChain RAG](https://python.langchain.com/docs/tutorials/rag/)
- [Ragas Evaluation](https://docs.ragas.io/)
- [NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/)
- [MLOps Guide 2026](https://rahulkolekar.com/mlops-in-2026-the-definitive-guide-tools-cloud-platforms-architectures-and-a-practical-playbook/)
- [LLMOps Roadmap](https://medium.com/@sanjeebmeister/the-complete-mlops-llmops-roadmap-for-2026-building-production-grade-ai-systems-bdcca5ed2771)

## 참조 스킬

- `/ai:mlops` - MLOps 기본 (Kubeflow, KServe)
- `/ai:mlops-tracking` - MLflow 실험 추적, 모델 레지스트리
- `/ai:ml-serving` - ML 서빙 심화
