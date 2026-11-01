# LangGraph State and Reducers

Source: https://docs.langchain.com/oss/python/langgraph/graph-api

State is the shared data contract for a LangGraph workflow. Nodes receive the
current state and return partial updates. A state schema makes the values used
by the graph explicit and helps define how updates are combined.

## Define a state schema

Python `TypedDict` is one way to describe graph state:

```python
from typing import TypedDict
from langgraph.graph import END, START, StateGraph


class ResearchState(TypedDict):
    question: str
    answer: str


def draft_answer(state: ResearchState) -> dict:
    return {"answer": f"Research question: {state['question']}"}


builder = StateGraph(ResearchState)
builder.add_node("draft_answer", draft_answer)
builder.add_edge(START, "draft_answer")
builder.add_edge("draft_answer", END)
research_graph = builder.compile()
```

The initial input provides the state needed by the first node. A node generally
returns only the keys it changes; the graph applies those updates to the shared
state as execution proceeds.

## Default update behavior

Without a reducer, a state key is updated by replacing its previous value. This
works well for values such as the current query or a final answer, where the
latest node result should become the value used by later nodes.

When multiple parallel nodes update the same key, define how those updates
should be combined. Otherwise, the graph cannot safely infer the intended
combination.

## Accumulate values with a reducer

A reducer combines a new update with the existing value. For example,
`operator.add` can append node results to a list:

```python
import operator
from typing import Annotated, TypedDict


class ResearchState(TypedDict):
    question: str
    notes: Annotated[list[str], operator.add]


def collect_note(state: ResearchState) -> dict:
    return {"notes": ["A note relevant to " + state["question"]]}
```

With this schema, a node can return new notes and the reducer combines them
with the notes already in state. Reducers are useful for message history,
retrieval results, and execution logs that should accumulate across steps.

Choose the reducer to match the field's intended behavior. Appending duplicates
may be undesirable for some data, while replacing an answer is usually more
appropriate than accumulating every draft.

## Keep state focused

Include fields that graph nodes need to read or update, such as the original
question, the active search query, retrieved documents, retry counters, and the
answer. Prefer explicit state keys and clear reducer behavior so routing and
parallel updates remain understandable.

## Official reference

- Graph API: https://docs.langchain.com/oss/python/langgraph/graph-api
