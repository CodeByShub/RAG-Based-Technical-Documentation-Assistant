# LangGraph Streaming

Source: https://docs.langchain.com/oss/python/langgraph/streaming

Streaming lets an application observe a graph while it runs instead of waiting for
the final result from `invoke()`. It is useful for showing progress in a user
interface, displaying generated tokens, and inspecting intermediate state updates.

## Stream state updates

Use `stream()` with the `updates` mode to receive updates produced by graph nodes.
Each yielded item identifies the node that produced the update:

```python
for update in graph.stream(
    {"question": "How does graph state work?"},
    stream_mode="updates",
):
    for node_name, state_update in update.items():
        print(node_name, state_update)
```

Use the `values` mode when consumers need the full state after each graph step,
rather than just the values changed by that step:

```python
for state in graph.stream(
    {"question": "How does graph state work?"},
    stream_mode="values",
):
    print(state)
```

Streaming exposes intermediate information. Applications should select a mode
that fits their interface and avoid sending internal state to clients unless it
is intended to be public.

## Stream model messages

For token-by-token output from language models used inside a graph, use the
`messages` stream mode. It yields message chunks together with metadata that can
identify the node producing them:

```python
for message_chunk, metadata in graph.stream(
    {"question": "Explain conditional edges."},
    stream_mode="messages",
):
    if message_chunk.content:
        print(message_chunk.content, end="", flush=True)
```

A graph may contain nodes that do not call a model. Consumers can use the
metadata to distinguish model output from other graph activity.

## Async streaming

In asynchronous applications, use `astream()` and iterate asynchronously:

```python
async for update in graph.astream(
    {"question": "Explain graph execution."},
    stream_mode="updates",
):
    print(update)
```

Choose one or more stream modes based on the information the client needs. For
example, a progress view can consume node updates, while an answer view can
consume model message chunks.

## Streaming and persistence

Streaming controls how execution output is delivered; it does not by itself
persist graph state. Configure a checkpointer and provide a thread identifier
when the application also needs state to continue across invocations. See the
LangGraph persistence guide for checkpoint and thread behavior.

## Official reference

- Streaming: https://docs.langchain.com/oss/python/langgraph/streaming
