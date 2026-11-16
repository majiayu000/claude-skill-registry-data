---
name: instructor-structured-output
description: "Use when extracting structured data (JSON, typed objects) from LLM responses with validation and retries. Triggers on: 'instructor', 'structured output', 'extract JSON from LLM', 'pydantic llm', 'LLM return JSON', 'trích xuất dữ liệu từ LLM', 'LLM trả về JSON', 'parse LLM output', 'validated LLM output', 'schema extraction'."
---

# Instructor Structured Output Skill

Lấy JSON có type-safe và validated từ bất kỳ LLM nào — tự động retry khi fail.
Source: [instructor-ai/instructor](https://github.com/instructor-ai/instructor) (Apache 2.0)

## Install

```bash
pip install instructor
# JS/TS
npm install @instructor-ai/instructor zod
```

## Workflow Python

### Step 1 — Define schema với Pydantic

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class Person(BaseModel):
    name: str
    age: int
    email: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
```

### Step 2 — Wrap client

```python
import instructor
from anthropic import Anthropic

client = instructor.from_anthropic(Anthropic())

# Hoặc OpenAI
# from openai import OpenAI
# client = instructor.from_openai(OpenAI())
```

### Step 3 — Extract

```python
person = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Trích xuất thông tin: Nguyễn Văn An, 25 tuổi, email: an@gmail.com, biết Python và React"
    }],
    response_model=Person,
)
print(person.name)    # "Nguyễn Văn An"
print(person.age)     # 25
print(person.skills)  # ["Python", "React"]
```

## Use cases phổ biến

### Extract danh sách

```python
from typing import List

class ProductList(BaseModel):
    products: List[Product]
    total_count: int

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

result = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[{"role": "user", "content": f"Parse sản phẩm từ: {raw_text}"}],
    response_model=ProductList,
)
```

### Partial streaming (hiện dần dần)

```python
import instructor
from instructor import Partial

person_stream = client.messages.create_partial(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}],
    response_model=Person,
)

for partial_person in person_stream:
    print(partial_person.name)   # hiện ngay khi có
```

### Validation với custom rules

```python
from pydantic import field_validator

class Email(BaseModel):
    address: str

    @field_validator('address')
    @classmethod
    def must_be_email(cls, v):
        if '@' not in v:
            raise ValueError('Không phải email hợp lệ')
        return v

# Instructor tự retry nếu validation fail
```

### Nested + complex schema

```python
class Address(BaseModel):
    street: str
    city: str
    country: str = "Vietnam"

class Company(BaseModel):
    name: str
    founded_year: int
    headquarters: Address
    employees: List[Person]

result = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[{"role": "user", "content": raw_company_description}],
    response_model=Company,
)
```

## TypeScript (Zod)

```typescript
import Instructor from '@instructor-ai/instructor'
import Anthropic from '@anthropic-ai/sdk'
import { z } from 'zod'

const client = Instructor({
  client: new Anthropic(),
  mode: 'TOOLS',
})

const UserSchema = z.object({
  name: z.string(),
  age: z.number().int().positive(),
  email: z.string().email().optional(),
})

const user = await client.chat.completions.create({
  model: 'claude-sonnet-4-6',
  max_tokens: 512,
  messages: [{ role: 'user', content: 'An is 25, email: an@gmail.com' }],
  response_model: { schema: UserSchema, name: 'User' },
})
// user.name, user.age — fully typed
```

## Config retry

```python
client = instructor.from_anthropic(
    Anthropic(),
    max_retries=3,        # retry tối đa 3 lần khi validation fail
)
```

## Providers được support

| Provider | Import |
|----------|--------|
| Anthropic | `instructor.from_anthropic(Anthropic())` |
| OpenAI | `instructor.from_openai(OpenAI())` |
| Google | `instructor.from_gemini(genai.GenerativeModel(...))` |
| Ollama | `instructor.from_openai(OpenAI(base_url="http://localhost:11434/v1"))` |
| LiteLLM | `instructor.from_litellm(litellm.completion)` |
