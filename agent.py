"""
agent.py — LangChain agent that answers fitness queries using user context.

Architecture (simple & effective):
  - SystemMessage: injects the user's data summary so the LLM is grounded
  - HumanMessage: the user's actual question
  - No tool-calling needed — context is pre-fetched and injected directly,
    which is cheaper, faster, and avoids hallucination loops.
"""

import json
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
MODEL_NAME     = os.environ.get("LLM_MODEL")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY environment variable is required but not set")
if not MODEL_NAME:
    raise RuntimeError("LLM_MODEL environment variable is required but not set")

_SYSTEM_TEMPLATE = """\
You are FitBot, a helpful and encouraging personal fitness assistant for the FitForge platform.
You have access to the following data for the current user. Use it to give personalised, \
data-driven answers. Do NOT reveal information about other users. \
If the data is empty, acknowledge it and give general advice instead.

--- USER DATA ---
{user_data}
--- END DATA ---

Guidelines:
- Be concise and friendly.
- Reference specific workouts, nutrition figures, or progress metrics from the data above when relevant.
- If the question is unrelated to fitness, politely redirect the conversation.
"""


def get_llm() -> ChatGoogleGenerativeAI:
    """Return a ChatGoogleGenerativeAI instance for gemini-2.5-flash-lite."""
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.5,
    )


async def chat_with_agent(user_question: str, user_context: dict) -> str:
    """
    Run a single-turn LangChain LLM call grounded with the user's fitness data.

    Args:
        user_question: Natural-language question from the user.
        user_context:  Dict returned by data_fetcher.fetch_user_context().

    Returns:
        The assistant's reply as a plain string.
    """
    llm = get_llm()

    system_content = _SYSTEM_TEMPLATE.format(
        user_data=json.dumps(user_context, indent=2, default=str)
    )

    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=user_question),
    ]

    response = await llm.ainvoke(messages)
    return response.content
