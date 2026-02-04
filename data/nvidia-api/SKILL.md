---
name: nvidia-api
description: NVIDIA API documentation for integrating NVIDIA services. Use for NVIDIA NIM (NVIDIA Inference Microservices), LLM APIs, visual models, multimodal APIs, retrieval APIs, healthcare APIs, and CUDA-X microservices integration.
---

# Nvidia-Api Skill

Comprehensive assistance with NVIDIA API development, focusing on NIM (NVIDIA Inference Microservices) and cloud-hosted AI endpoints for building prototype and production applications.

## When to Use This Skill

This skill should be triggered when:

### Primary Use Cases
- **LLM Integration**: Working with Large Language Models via NVIDIA NIM API (Llama, Mistral, Gemma, etc.)
- **Chat Completions**: Implementing chat interfaces, chatbots, or conversational AI using NVIDIA-hosted models
- **Code Generation**: Using code-specialized models (CodeLlama, StarCoder, Codestral, Granite)
- **Multimodal AI**: Integrating visual design, image understanding, or vision-language models
- **Retrieval Systems**: Building RAG (Retrieval-Augmented Generation) applications with NVIDIA retrieval APIs
- **Healthcare AI**: Implementing medical AI solutions with NVIDIA healthcare-specific APIs
- **Weather & Simulation**: Working with Earth-2 weather prediction APIs

### Technical Scenarios
- Setting up authentication with NVIDIA API keys
- Migrating from OpenAI API to NVIDIA NIM (OpenAI-compatible endpoints)
- Choosing between different LLM models for specific tasks
- Implementing streaming responses for chat applications
- Building production AI applications with NVIDIA cloud endpoints
- Prototyping AI features before self-hosting NIMs

## Quick Reference

### Authentication Setup

**Get your API key**: Visit [NVIDIA API Catalog](https://build.nvidia.com) to obtain your API key.

```bash
# Set environment variable
export NVIDIA_API_KEY="nvapi-your-key-here"
```

```python
# Python - Using environment variable
import os
api_key = os.environ.get("NVIDIA_API_KEY")
```

### Basic Chat Completion (Python)

```python
import requests

url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "meta/llama3-70b-instruct",
    "messages": [
        {"role": "user", "content": "Explain quantum computing in simple terms"}
    ],
    "max_tokens": 150,
    "temperature": 0.7
}

response = requests.post(url, json=payload, headers=headers)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

### Streaming Chat Response

```python
import requests
import json

url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "mistralai/mixtral-8x7b-instruct",
    "messages": [{"role": "user", "content": "Write a short story"}],
    "stream": True
}

response = requests.post(url, json=payload, headers=headers, stream=True)

for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: '):
            data = line[6:]
            if data != '[DONE]':
                chunk = json.loads(data)
                content = chunk["choices"][0]["delta"].get("content", "")
                print(content, end="", flush=True)
```

### OpenAI-Compatible Integration

```python
from openai import OpenAI

# Drop-in replacement for OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

completion = client.chat.completions.create(
    model="meta/llama3-70b-instruct",
    messages=[{"role": "user", "content": "Hello!"}],
    temperature=0.5,
    max_tokens=100
)

print(completion.choices[0].message.content)
```

### Code Generation Example

```python
# Using code-specialized models
payload = {
    "model": "bigcode/starcoder2-15b",
    "messages": [
        {"role": "system", "content": "You are an expert programmer."},
        {"role": "user", "content": "Write a Python function to calculate Fibonacci numbers"}
    ],
    "temperature": 0.2,  # Lower temperature for code generation
    "max_tokens": 500
}

response = requests.post(url, json=payload, headers=headers)
code = response.json()["choices"][0]["message"]["content"]
```

### Multi-Turn Conversation

```python
conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is machine learning?"},
]

# First response
response1 = requests.post(url, json={"model": "meta/llama3-70b-instruct", "messages": conversation}, headers=headers)
assistant_reply = response1.json()["choices"][0]["message"]["content"]

# Continue conversation
conversation.append({"role": "assistant", "content": assistant_reply})
conversation.append({"role": "user", "content": "Can you give me an example?"})

response2 = requests.post(url, json={"model": "meta/llama3-70b-instruct", "messages": conversation}, headers=headers)
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const url = 'https://integrate.api.nvidia.com/v1/chat/completions';
const apiKey = process.env.NVIDIA_API_KEY;

async function chatCompletion() {
  const response = await axios.post(url, {
    model: "mistralai/mistral-7b-instruct",
    messages: [
      { role: "user", content: "What are the benefits of renewable energy?" }
    ],
    max_tokens: 200
  }, {
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    }
  });

  console.log(response.data.choices[0].message.content);
}

chatCompletion();
```

### cURL Example

```bash
curl https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta/llama3-8b-instruct",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

### Error Handling

```python
try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raise exception for 4xx/5xx status codes
    result = response.json()
except requests.exceptions.HTTPError as e:
    if response.status_code == 401:
        print("Authentication failed. Check your API key.")
    elif response.status_code == 429:
        print("Rate limit exceeded. Please slow down requests.")
    else:
        print(f"HTTP Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

## Available Model Categories

### Large Language Models (LLMs)
Access to top language models for various tasks:

**Meta Models**
- `meta/llama3-70b-instruct` - High-performance instruction-following
- `meta/llama3-8b-instruct` - Efficient smaller model
- `meta/codellama-70b` - Specialized for code generation

**Mistral Models**
- `mistralai/mixtral-8x7b-instruct` - High-quality mixture-of-experts
- `mistralai/mistral-large-2-instruct` - Latest large model
- `mistralai/codestral-22b-instruct-v0.1` - Code generation specialist

**Google Models**
- `google/gemma-2-27b-it` - Instruction-tuned Gemma
- `google/codegemma-7b` - Code understanding and generation
- `google/shieldgemma-9b` - Safety and content filtering

**Other Notable Models**
- `nvidia/llama3-chatqa-1.5-70b` - Optimized for Q&A
- `ibm/granite-34b-code-instruct` - Enterprise code model
- `deepseek-ai/deepseek-r1` - Advanced reasoning model

### Code Generation Models
- `bigcode/starcoder2-15b` - Open-source code completion
- `mistralai/codestral-22b-instruct-v0.1` - Instruction-following for code
- `google/codegemma-7b` - Google's code specialist

### Other API Categories
- **Visual Design** - Image generation and visual models
- **Multimodal** - Vision-language models
- **Retrieval** - Embedding and retrieval APIs for RAG
- **Healthcare** - Medical AI specialized models
- **Weather Prediction** - Earth-2 climate simulation

## Key Concepts

### NVIDIA NIM (NVIDIA Inference Microservices)
Cloud-hosted inference endpoints that provide:
- Simple REST API access to leading AI models
- OpenAI API compatibility for easy migration
- Prototype-friendly with production capabilities
- Support for both cloud endpoints and downloadable containers

### Endpoint Structure
```
Base URL: https://integrate.api.nvidia.com
Endpoint: POST /v1/chat/completions
```

### API Compatibility
NVIDIA NIM APIs follow OpenAI's API specification, making it easy to:
- Migrate existing OpenAI-based applications
- Use OpenAI client libraries with minimal changes
- Maintain familiar request/response patterns

### Authentication
- Uses Bearer token authentication
- API keys obtained from [NVIDIA API Catalog](https://build.nvidia.com)
- Key format: `nvapi-*`

### Response Format
Standard OpenAI-compatible response structure:
```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "meta/llama3-70b-instruct",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Response text here"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  }
}
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

### getting_started.md
- Overview of NVIDIA API platform
- Getting started guide for cloud endpoints
- Authentication and setup instructions
- Links to main API categories

### other.md
- Additional NVIDIA API documentation
- Related services and microservices
- Integration patterns and best practices

**Note**: For detailed API specifications, parameter descriptions, and model-specific information, refer to the official documentation at [docs.api.nvidia.com](https://docs.api.nvidia.com)

## Working with This Skill

### For Beginners
1. **Start with authentication**: Get your API key from [NVIDIA API Catalog](https://build.nvidia.com)
2. **Try simple examples**: Use the Quick Reference curl or Python examples above
3. **Test different models**: Experiment with various models to understand their strengths
4. **Read the docs**: Check `references/getting_started.md` for foundational concepts

### For Intermediate Users
1. **Implement streaming**: Add real-time response streaming for better UX
2. **Optimize parameters**: Experiment with temperature, max_tokens, and other settings
3. **Build conversations**: Maintain context across multiple turns
4. **Handle errors gracefully**: Implement robust error handling and retry logic
5. **Choose optimal models**: Select models based on task requirements (speed vs accuracy)

### For Advanced Users
1. **Production deployment**: Move from prototypes to production-ready applications
2. **Batch processing**: Implement efficient batch inference patterns
3. **Self-hosted NIMs**: Download and deploy container images for local inference
4. **Multi-modal integration**: Combine LLM, vision, and retrieval APIs
5. **Performance optimization**: Fine-tune requests for latency and cost efficiency
6. **RAG implementation**: Build retrieval-augmented generation systems

### Navigation Tips
- **Model selection**: Choose based on task complexity, latency needs, and cost
- **OpenAI migration**: Use the OpenAI-compatible client for seamless migration
- **API documentation**: Access detailed specs at [docs.api.nvidia.com/nim](https://docs.api.nvidia.com/nim)
- **Model catalog**: Browse available models at [build.nvidia.com](https://build.nvidia.com)

## Common Use Cases

### Chatbots & Conversational AI
Use models like `meta/llama3-70b-instruct` or `mistralai/mixtral-8x7b-instruct` for building intelligent conversational interfaces.

### Code Assistants
Use specialized models like `bigcode/starcoder2-15b`, `mistralai/codestral-22b-instruct`, or `ibm/granite-34b-code-instruct`.

### Question Answering
Use `nvidia/llama3-chatqa-1.5-70b` optimized specifically for Q&A tasks.

### Content Generation
Use creative models like `mistralai/mistral-large-2-instruct` with higher temperature settings.

### RAG Applications
Combine LLM APIs with NVIDIA's Retrieval APIs for knowledge-grounded responses.

## Best Practices

### API Key Security
- **Never commit API keys** to version control
- **Use environment variables** for key storage
- **Rotate keys regularly** for security
- **Monitor usage** to detect unauthorized access

### Parameter Tuning
- **Temperature**: Lower (0.1-0.3) for factual/code, higher (0.7-1.0) for creative
- **Max tokens**: Set appropriate limits to control costs and response length
- **Top-p**: Alternative to temperature for controlling randomness
- **Streaming**: Enable for better user experience in interactive applications

### Error Handling
- **Implement retry logic** with exponential backoff
- **Handle rate limits** gracefully (HTTP 429)
- **Validate responses** before using in production
- **Log errors** for debugging and monitoring

### Model Selection
- **Small models** (7B-8B): Fast, cost-effective for simple tasks
- **Medium models** (13B-34B): Balance of performance and efficiency
- **Large models** (70B+): Best quality for complex reasoning and generation

## Resources

### Official Documentation
- **API Docs**: [docs.api.nvidia.com](https://docs.api.nvidia.com)
- **NIM Reference**: [docs.api.nvidia.com/nim](https://docs.api.nvidia.com/nim/reference/llm-apis)
- **Model Catalog**: [build.nvidia.com](https://build.nvidia.com)

### Getting Started
- Get API key at [NVIDIA API Catalog](https://build.nvidia.com)
- Browse available models and try them in the playground
- Read getting started guides in `references/getting_started.md`

### Community & Support
- Check NVIDIA Developer Forums for community support
- Review example applications and integration patterns
- Explore NVIDIA AI Enterprise documentation for production deployments

## Notes

- NVIDIA NIM APIs follow **OpenAI API specifications** for easy integration
- Models are **cloud-hosted** for prototyping; downloadable containers available for production
- API is designed for **both prototyping and production** workloads
- **Multiple language support**: Works with Python, JavaScript, Java, Ruby, PHP, and any HTTP client
- **Streaming support**: Real-time response generation for interactive applications
- Select models available as **self-hosted NIMs** with NVIDIA AI Enterprise entitlement

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest model information and API updates
3. Check for new models and API endpoints in the official documentation
