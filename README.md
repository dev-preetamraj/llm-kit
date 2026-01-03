# llm-kit-pro

**llm-kit-pro** is a unified, async-first Python toolkit for interacting with multiple Large Language Model (LLM) providers through a consistent, provider-agnostic API.

It is designed for developers who need to switch between providers (OpenAI, Gemini, Anthropic/Bedrock) without rewriting their core application logic, with a heavy emphasis on **structured data** and **multimodal inputs**.

---

## ✨ Features

- **Unified API**: One interface for OpenAI, Gemini, and AWS Bedrock.
- **Pydantic-First Structured Output**: Pass Pydantic models directly to get validated, type-safe dictionaries back.
- **Native "Strict Mode"**: Automatically handles OpenAI's Structured Outputs requirements.
- **Multimodal Inputs**: First-class support for PDF, PNG, JPEG, and Text files across all supported providers.
- **Async-First**: Built from the ground up for high-performance asynchronous Python applications.
- **Provider-Agnostic Inputs**: Use `LLMFile` to handle different file types without worrying about provider-specific formatting.

---

## 📦 Installation

```bash
pip install llm-kit-pro
```

Install with specific provider support:

```bash
# For OpenAI
pip install "llm-kit-pro[openai]"

# For Google Gemini
pip install "llm-kit-pro[gemini]"

# For AWS Bedrock (Anthropic/Llama/etc)
pip install "llm-kit-pro[bedrock]"
```

---

## 🚀 Quick Start

### 1. Simple Text Generation

```python
from llm_kit_pro.providers.openai import OpenAIClient, OpenAIConfig

client = OpenAIClient(OpenAIConfig(api_key="your-key"))

text = await client.generate_text(
    prompt="Explain quantum entanglement like I'm five."
)
print(text)
```

### 2. Structured Data with Pydantic

Instead of messy regex or manual JSON parsing, define your schema as a Pydantic model. `llm-kit-pro` handles the schema injection, strict mode enforcement, and final validation.

```python
from pydantic import BaseModel
from llm_kit_pro.providers.gemini import GeminiClient, GeminiConfig

class MovieReview(BaseModel):
    title: str
    rating: int
    summary: str
    sentiment: str

client = GeminiClient(GeminiConfig(api_key="your-key"))

# Pass the class directly!
data = await client.generate_json(
    prompt="Review the movie 'Inception'",
    schema=MovieReview
)

print(data["rating"])
```

### 3. Multimodal: Extracting from a PDF

`llm-kit-pro` treats files as first-class citizens. You can pass images or PDFs directly to the model.

```python
from llm_kit_pro.core.inputs import LLMFile
from pydantic import BaseModel

class Invoice(BaseModel):
    vendor: str
    amount: float
    due_date: str

# Load your file
with open("invoice.pdf", "rb") as f:
    pdf = LLMFile(
        content=f.read(),
        mime_type="application/pdf",
        filename="invoice.pdf"
    )

# Extract structured data from the document
data = await client.generate_json(
    prompt="Extract the invoice details",
    schema=Invoice,
    files=[pdf]
)
```

---

## 🧠 Core Abstractions

### `BaseLLMClient`

Every provider implements this interface, ensuring your code remains portable.

- `generate_text(prompt, files=None, **kwargs)` -> `str`
- `generate_json(prompt, schema, files=None, **kwargs)` -> `dict`

### `LLMFile`

A simple container for file-based inputs.

- `content`: Raw bytes.
- `mime_type`: e.g., `application/pdf`, `image/jpeg`.
- `filename`: Optional metadata.

---

## 🔌 Supported Providers

| Provider          | Installation Extra | Status     | Structured Output  | Multimodal           |
| :---------------- | :----------------- | :--------- | :----------------- | :------------------- |
| **OpenAI**        | `[openai]`         | ✅ Stable  | Native Strict Mode | Images               |
| **Google Gemini** | `[gemini]`         | ✅ Stable  | Native JSON Schema | Images, PDF          |
| **AWS Bedrock**   | `[bedrock]`        | ✅ Stable  | Schema Injection   | Images, PDF (Claude) |
| **Anthropic**     | `[anthropic]`      | 🏗️ Planned | -                  | -                    |

---

## 📍 Status

🚧 **Under active development**

The public API is stabilizing. We are currently focusing on adding more Bedrock adapters (Llama 3, Titan) and a native Anthropic provider.

---

## 📄 License

MIT License
