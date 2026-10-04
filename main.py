import asyncio
import logging
import os

from dotenv import load_dotenv

from llm_manager import AsyncLLMManager
from schemas import ChatMessage, ModelConfig, Role

load_dotenv()
logging.basicConfig(level=logging.WARNING, format="%(levelname)s | %(name)s | %(message)s")

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

QUESTION = "¿Qué es la entropía?"

DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-sonnet-20241022",
    "gemini": "gemini-3.8-flash",
}


def build_messages(question: str) -> list[ChatMessage]:
  
    return [
        ChatMessage(role=Role.SYSTEM, content="Sos un asistente técnico. Respondé en 3 líneas como máximo."),
        ChatMessage(role=Role.USER, content=question),
    ]


async def run_normal(manager: AsyncLLMManager) -> None:
    print(f"{YELLOW}\n--- Modo normal (ainvoke) ---\n{RESET}")
    response = await manager.generate(build_messages(QUESTION))
    if response.error:
        print(f"{RED}Error controlado: {response.error}")
        return
    print(f"\n{GREEN}{response.content}{RESET}\n")
    print(f"{YELLOW}(finish_reason={response.finish_reason}, tokens in/out={response.input_tokens}/{response.output_tokens}){RESET}")


async def run_streaming(manager: AsyncLLMManager) -> None:
    print(f"{YELLOW}\n--- Modo streaming ---\n{RESET}")
    print(GREEN, end="", flush=True)
    async for chunk in manager.stream(build_messages(QUESTION)):
        print(chunk, end="", flush=True)
    print(RESET)
    # EOF
    print()


async def main() -> None:
    provider = os.getenv("LLM_PROVIDER", "gemini")
    model = os.getenv("LLM_MODEL", DEFAULT_MODELS[provider])
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.3"))

    config = ModelConfig(provider=provider, model=model, temperature=temperature, max_tokens=2048)
    manager = AsyncLLMManager(config)
    await run_normal(manager)
    await run_streaming(manager)


# Event loop
if __name__ == "__main__":
    asyncio.run(main())