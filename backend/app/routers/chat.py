import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agent.graph import movie_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_name: str
    session_id: str

async def event_generator(message: str, user_name: str):
    """Streams the agent response as SSE events"""
    try:
        # Invoke the agent
        result = await movie_agent.ainvoke({
            "messages": [HumanMessage(content=message)],
            "user_name": user_name,
            "intent": "",
            "movie_data": {}
        })

        # Get final response
        final_message = result["messages"][-1].content

        # Stream word by word for a typing effect
        words = final_message.split(" ")
        for word in words:
            chunk = {"type": "token", "content": word + " "}
            yield f"data: {json.dumps(chunk)}\n\n"

        # Signal completion
        yield f"data: {json.dumps({'type': 'end'})}\n\n"

    except Exception as e:
        error = {"type": "error", "content": str(e)}
        yield f"data: {json.dumps(error)}\n\n"

@router.post("/chat")
async def chat(request: ChatRequest):
    return StreamingResponse(
        event_generator(request.message, request.user_name),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )