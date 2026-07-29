import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq #ChatGroq- LangChain wrapper around Groq.
from langchain_core.messages import SystemMessage, HumanMessage  #SystemMessage- Instructions for the AI. HumanMessage Represents user input.
from langchain_mcp_adapters.client import MultiServerMCPClient   #MultiServerMCPClient- Connects to MCP servers. Your TMDB server exposes tools like: search_movies(),get_movie_details(),get_similar_movies() through MCP.

load_dotenv()

# Initialize Groq
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

# MCP client pointing to your TMDB server
#This launches: python tmdb_server.py as an MCP server.
mcp_client = MultiServerMCPClient({
    "tmdb": {
        "command": "python",
        "args": ["mcp_servers/tmdb_server.py"],
        "transport": "stdio"
    }
})

async def intent_classifier_node(state: dict) -> dict:
    """Decides if user wants a recommendation or a review"""

    last_message = state["messages"][-1].content   #Gets latest user message.

    prompt = f"""You are classifying user intent for a movie chatbot.
    
User message: "{last_message}"

Reply with exactly one word:
- "recommendation" if they want movie suggestions
- "review" if they want a review or details about a specific movie
- "general" if it's a general movie question

Just the one word, nothing else."""

    response = await llm.ainvoke([HumanMessage(content=prompt)])  #Gemini analyzes the prompt.
    intent = response.content.strip().lower()

    # Fallback if model returns unexpected output
    if intent not in ["recommendation", "review", "general"]:
        intent = "general"

    return {"intent": intent}


async def movie_fetcher_node(state: dict) -> dict:
    """Calls TMDB tools based on intent"""

    last_message = state["messages"][-1].content
    intent = state.get("intent", "general")
    tools = await mcp_client.get_tools()
    llm_with_tools = llm.bind_tools(tools)

    if intent == "recommendation":
        prompt = f"""The user wants a movie recommendation. 
Use the search_movies or get_similar_movies tool to find relevant movies.
User request: {last_message}"""

    elif intent == "review":
        prompt = f"""The user wants a movie review or details.
Use search_movies to find the movie first, then get_movie_details and get_watch_providers.
User request: {last_message}"""

    else:
        # General question — no tool needed
        return {"movie_data": {}}

    response = await llm_with_tools.ainvoke([HumanMessage(content=prompt)])

    # Extract tool results if any
    movie_data = {}
    if hasattr(response, "tool_calls") and response.tool_calls: #Checks whether Gemini requested tools and if list is not empty.
        movie_data = {"tool_calls": response.tool_calls}

    return {"movie_data": movie_data}


async def responder_node(state: dict) -> dict:  #Produces user-facing response.
    """Formats the final response to the user"""

    user_name = state.get("user_name", "there")
    intent = state.get("intent", "general")
    movie_data = state.get("movie_data", {})
    conversation = state["messages"]

    system_prompt = f"""You are Movie Companion, a direct and knowledgeable AI cinema guide.
You're talking to {user_name}.

STRICT RULES:
- ALWAYS recommend specific movie titles, never be vague
- NEVER say things like "there are many options" or "it depends on your mood"
- Get straight to the recommendations immediately

If intent is "recommendation":
- Recommend exactly 3 movies
- For each movie state:
  1. Title and year
  2. One sentence on why it matches what they asked
  3. IMDb-style rating from your knowledge
  4. Genre tags
- End with: "Want details or streaming info on any of these?"

If intent is "review":
- State the movie title, year, director
- Rating out of 10 with one line justification
- 2 sentence plot summary (no spoilers)
- Top 3 cast members
- Who should watch it and who shouldn't

If intent is "general":
- Answer directly in 2-3 sentences max

Movie data from tools: {movie_data}
Current intent: {intent}"""

    messages = [SystemMessage(content=system_prompt)] + list(conversation)
    response = await llm.ainvoke(messages)

    return {"messages": [response]}