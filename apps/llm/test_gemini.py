from apps.llm.client import generate_structured
from pydantic import BaseModel


class TestOutput(BaseModel):
    answer: str
    relevant: bool


result = generate_structured(
    """
    Determine whether this document is relevant to the question.

    Question:
    How do conditional edges route execution in LangGraph?

    Document:
    A LangGraph conditional edge selects the next node based on a routing
    function, allowing graph execution to branch based on the current state.

    Return whether the document is relevant and explain why.
    """,
    TestOutput,
)

print(result)