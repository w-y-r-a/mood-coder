# Dev Docs
## Table of contents

* [Ollama](#ollama)
    * [Creating Ollama client](#creating-ollama-clients)
        * [1. Normal / Synchronous](#1-normal--synchronous)
        * [2. Asynchronous](#2-asynchronous)
    * [Using `ollama.list()`](#using-ollamalist)
* [Contributors to this document](#contributors-to-this-document)

---

## Ollama

### Creating Ollama clients
Creating Ollama Clients is useful indeed, here are two types of clients:

#### 1. Normal / Synchronous
```python
from ollama import Client
client = Client(
  host='<http or https>://<host>:<port>',
  headers={'headers': 'some-value'}
)
```

#### 2. Asynchronous
```python
import asyncio
from ollama import AsyncClient

client = AsyncClient(
    host='<http or https>://<host>:<port>',
    headers={'headers': 'some-value'}
)

async def chat():
  message = {'role': 'user', 'content': 'Why is the sky blue?'}
  async for part in await client.chat(model='llama3.2', messages=[message], stream=True):
    print(part['message']['content'], end='', flush=True)
```

### Using `ollama.list()`
Returns 
```
models=[Model(model='deepseek-r1:latest', modified_at=datetime.datetime(2025, 4, 9, 22, 53, 5, 183793, tzinfo=TzInfo(-05:00)), digest='0a8c266910232fd3291e71e5ba1e058cc5af9d411192cf88b6d30e92b6e73163', size=4683075271, details=ModelDetails(parent_model='', format='gguf', family='qwen2', families=['qwen2'], parameter_size='7.6B', quantization_level='Q4_K_M')), Model(model='nomic-embed-text:latest', modified_at=datetime.datetime(2025, 4, 9, 22, 48, 0, 189364, tzinfo=TzInfo(-05:00)), digest='0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f', size=274302450, details=ModelDetails(parent_model='', format='gguf', family='nomic-bert', families=['nomic-bert'], parameter_size='137M', quantization_level='F16')), Model(model='qwen2.5-coder:1.5b-base', modified_at=datetime.datetime(2025, 4, 9, 22, 47, 39, 197814, tzinfo=TzInfo(-05:00)), digest='02e0f2817a890a6de385d534465c04c5d0980abddc83615c09e79cee2c094446', size=986060385, details=ModelDetails(parent_model='', format='gguf', family='qwen2', families=['qwen2'], parameter_size='1.5B', quantization_level='Q4_K_M')), Model(model='llama3.1:8b', modified_at=datetime.datetime(2025, 4, 9, 22, 46, 53, 79422, tzinfo=TzInfo(-05:00)), digest='46e0c10c039e019119339687c3c1757cc81b9da49709a3b3924863ba87ca666e', size=4920753328, details=ModelDetails(parent_model='', format='gguf', family='llama', families=['llama'], parameter_size='8.0B', quantization_level='Q4_K_M')), Model(model='deepseek-r1:14b', modified_at=datetime.datetime(2025, 3, 14, 18, 44, 43, 370530, tzinfo=TzInfo(-05:00)), digest='ea35dfe18182f635ee2b214ea30b7520fe1ada68da018f8b395b444b662d4f1a', size=8988112040, details=ModelDetails(parent_model='', format='gguf', family='qwen2', families=['qwen2'], parameter_size='14.8B', quantization_level='Q4_K_M')), Model(model='deepseek-r1:8b', modified_at=datetime.datetime(2025, 3, 14, 16, 29, 18, 824987, tzinfo=TzInfo(-05:00)), digest='28f8fd6cdc677661426adab9338ce3c013d7e69a5bea9e704b364171a5d61a10', size=4920738407, details=ModelDetails(parent_model='', format='gguf', family='llama', families=['llama'], parameter_size='8.0B', quantization_level='Q4_K_M'))]
```
I don't know how to use it right now, but that's fine!

## Contributors to this document
- [Arnay Kumar](https://github.com/I4LYT/)