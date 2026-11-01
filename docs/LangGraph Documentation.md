# LangGraph Documentation

Source: https://docs.langchain.com/oss/python/langgraph/overview

LangGraph is a low-level orchestration framework for building stateful, long-running
agents. It models an application as a graph, giving developers explicit control over
how work is performed, how state changes, and how execution moves between steps.
LangGraph can be used on its own or with higher-level LangChain components.

## Graph fundamentals

A graph is built from three main concepts:

- **State** is the shared data passed between graph steps. A state schema describes
  the fields available to nodes. State updates can replace values or use reducers
  to combine updates, such as appending messages to a list.
- **Nodes** are Python functions that receive the current state and return updates.
  Nodes commonly call models, retrieve information, validate results, or make
  decisions.
- **Edges** define what runs next. Normal edges connect a node to a fixed next step;
  conditional edges choose the next step from the current state or a routing result.

The `StateGraph` builder supports adding nodes and edges. `START` marks the entry
point and `END` marks completion. Call `compile()` before invoking the graph; compile
time is also where runtime features such as checkpointers can be configured.

```python
from typing_extensions import TypedDict
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    question: str
    answer: str


def answer_question(state: State) -> dict:
    return {"answer": f"You asked: {state['question']}"}


builder = StateGraph(State)
builder.add_node("answer", answer_question)
builder.add_edge(START, "answer")
builder.add_edge("answer", END)
graph = builder.compile()
result = graph.invoke({"question": "What is graph state?", "answer": ""})
```

## Routing and cycles

Conditional edges let a graph branch based on a routing function's result. A node
can also have a normal edge back to an earlier node, creating a loop for retries,
review, or iterative refinement. Every cycle should have a clear stopping condition;
otherwise execution may continue until a configured recursion limit is reached.

For example, an agent can route to a tool node when a model requests a tool call,
then return to the model node with the tool result. A validation workflow can route
an unsuccessful result back to a generation step and finish when it passes review.

## Running a graph

After compilation, use `invoke` for one complete run. Use `stream` or `astream` to
observe events or state updates while a graph runs. A graph invocation accepts an
initial state and can also accept runtime configuration, including a thread
identifier used by persistence.

## Persistence and threads

A checkpointer saves graph state at execution checkpoints. With a `thread_id` in
the invocation configuration, later invocations can resume or inspect state for
that thread. Persistence supports multi-step conversations, recovery, and
human-in-the-loop workflows. A thread identifies a sequence of stateful runs; it
is distinct from a single invocation.

Checkpoint storage is selected when compiling the graph. Production applications
should choose a checkpointer appropriate to their durability and deployment
requirements. In-memory checkpointing is useful for local experiments but does
not persist across process restarts.

## Interrupts and human review

An interrupt pauses graph execution and exposes data for external review. The
application can collect approval or other input and resume the graph using the
same thread. Interrupt-based workflows require a checkpointer so the graph can
restore its state when resumed.

Interrupts are useful for approval before consequential actions, editing a
generated value, or asking for missing user input. Keep the work before an
interrupt safe to repeat, since resuming a checkpoint can re-enter the node that
issued the interrupt.

## Subgraphs

Subgraphs are compiled graphs used as nodes inside a parent graph. They help
organize larger systems into reusable components and can keep their own state
schema. A parent can invoke a subgraph directly when its input and output state
are compatible, or use a wrapper node to translate between schemas.

## Choosing an API

The Graph API exposes state, nodes, edges, and routing explicitly and is suited to
workflows with branching, cycles, or custom orchestration. The Functional API
decorates existing Python functions and is useful when that style is a better fit.
Both APIs can use LangGraph runtime capabilities such as persistence, streaming,
and interrupts.

## Official references

- Overview: https://docs.langchain.com/oss/python/langgraph/overview
- Graph API: https://docs.langchain.com/oss/python/langgraph/graph-api
- Persistence: https://docs.langchain.com/oss/python/langgraph/persistence
- Interrupts: https://docs.langchain.com/oss/python/langgraph/interrupts
- Streaming: https://docs.langchain.com/oss/python/langgraph/streaming
