from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import intent_classifier_node, movie_fetcher_node, responder_node

def route_by_intent(state: dict) -> str:
    """Decides next node based on intent"""
    intent = state.get("intent", "general")
    if intent in ["recommendation", "review"]:
        return "movie_fetcher"
    return "responder"  # General questions skip fetcher

def build_graph():
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("intent_classifier", intent_classifier_node)
    graph.add_node("movie_fetcher", movie_fetcher_node)
    graph.add_node("responder", responder_node)

    # Entry point
    graph.set_entry_point("intent_classifier")

    # Conditional edge — routes based on intent
    graph.add_conditional_edges(
        "intent_classifier",
        route_by_intent,
        {
            "movie_fetcher": "movie_fetcher",
            "responder": "responder"
        }
    )

    # After fetching, always respond
    graph.add_edge("movie_fetcher", "responder")

    # Responder is the end
    graph.add_edge("responder", END)

    return graph.compile()

# Single compiled instance reused across requests
movie_agent = build_graph()


