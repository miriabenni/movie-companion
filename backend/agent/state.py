from typing import Annotated  #Annotated lets you attach extra metadata to a type. Using this we can reuse the rule through out in code.
from langgraph.graph.message import add_messages  #add_messages tells LangGraph: "Don't overwrite the old messages. Append the new messages to the conversation history."
from langchain_core.messages import BaseMessage  #Imports the base class for all chat messages.
from typing_extensions import TypedDict #A TypedDict lets you define the expected structure:
#class Person(TypedDict):
    #name: str
    #age: int  #Now tools and type checkers know what fields should exist.

class AgentState(TypedDict): #This describes the data that flows through your LangGraph. Every node in the graph can read or update this state.
    
    messages: Annotated[list[BaseMessage], add_messages]  # Full conversation history
    #list[BaseMessage]

    #Means:
#[
    #HumanMessage(...),
    #AIMessage(...),
    #HumanMessage(...),
#]
    
    user_name: str # Name of the user
    
    intent: str  # intent is what LangGraph uses to decide which path to take — recommendation vs review
    
    movie_data: dict  # movie_data carries TMDB results between nodes so we don't call the API twice