"""Refactorización a LCEL asíncrono: prompt | modelo | parser."""
import asyncio
import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-sonnet-5-5",
    "gemini": "gemini-3.8-flash",
}


def build_model(provider: str, model: str, temperature: float) -> BaseChatModel:
    """Reemplaza los clientes manuales del Módulo 1 por modelos de LangChain."""
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model, temperature=temperature)
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=model, temperature=temperature)
    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=model, temperature=temperature, google_api_key=os.getenv("GEMINI_API_KEY")
        )
    raise ValueError(f"Proveedor no soportado: '{provider}'. Usá uno de: {', '.join(DEFAULT_MODELS)}")


prompt = ChatPromptTemplate.from_messages([
    ("system", "Sos un asistente técnico. Respondé en 3 líneas como máximo."),
    ("human", "{pregunta}"),
])

model = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.3)
chain = prompt | model | StrOutputParser()

async def main() -> None:
    try:
        response = await chain.ainvoke({"pregunta": "¿Qué es la entropía?"})
    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    asyncio.run(main())

