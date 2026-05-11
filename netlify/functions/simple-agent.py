import json
import os
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI()

# Request/Response models
class ChatMessage(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    response: str
    history: List[Dict[str, str]]

# Mock tools (in a real implementation, these would call actual APIs)
def search_tool(query: str) -> str:
    """Mock search tool"""
    return f"Search results for: {query}. This is a mock response showing information about {query}."

def calculator_tool(expression: str) -> str:
    """Mock calculator tool"""
    try:
        # Simple eval for demo - in production use a safe eval
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error in calculation: {str(e)}"

def weather_tool(location: str) -> str:
    """Mock weather tool"""
    return f"Weather in {location}: Sunny, 72°F (mock data)"

# Available tools
TOOLS = {
    "search": search_tool,
    "calculator": calculator_tool,
    "weather": weather_tool
}

def simple_agent_response(user_message: str, history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Simple agent implementation following the perception-reasoning-action-memory loop
    """
    
    # 1. PERCEPTION: Receive and understand the input
    perception_step = {
        "type": "perception",
        "content": f"Received user input: '{user_message}'"
    }
    
    # 2. REASONING: Process the input and decide what to do
    user_lower = user_message.lower()
    reasoning_steps = [perception_step]
    
    # Simple intent detection (in practice, an LLM would do this)
    intent = "general_query"
    selected_tools = []
    
    if any(word in user_lower for word in ["search", "find", "look up", "what is", "who is", "tell me about"]):
        intent = "information_seeking"
        selected_tools.append("search")
        reasoning_steps.append({
            "type": "reasoning",
            "content": "Identified user wants information - will use search tool"
        })
    
    elif any(word in user_lower for word in ["calculate", "compute", "math", "+", "-", "*", "/", "="]):
        intent = "calculation"
        selected_tools.append("calculator")
        reasoning_steps.append({
            "type": "reasoning",
            "content": "Identified user wants to perform a calculation - will use calculator tool"
        })
    
    elif any(word in user_lower for word in ["weather", "temperature", "forecast", "rain", "sun"]):
        intent = "weather_inquiry"
        selected_tools.append("weather")
        reasoning_steps.append({
            "type": "reasoning",
            "content": "Identified user wants weather information - will use weather tool"
        })
    
    else:
        reasoning_steps.append({
            "type": "reasoning",
            "content": "No specific intent detected - treating as general query"
        })
    
    # 3. ACTION: Execute actions based on reasoning
    observations = []
    action_steps = []
    
    for tool_name in selected_tools:
        if tool_name in TOOLS:
            tool_func = TOOLS[tool_name]
            action_steps.append({
                "type": "action",
                "content": f"Executing {tool_name} tool"
            })
            
            # Extract parameters (simplified for demo)
            if tool_name == "search":
                search_query = user_message.replace("?", "").strip()
                observation = tool_func(search_query)
            elif tool_name == "calculator":
                import re
                calc_pattern = r'[\d+\-*/().\s]+'
                matches = re.findall(calc_pattern, user_message)
                expression = matches[0].strip() if matches else "2+2"
                observation = tool_func(expression)
            elif tool_name == "weather":
                location = "New York"  # default
                observation = tool_func(location)
            
            observations.append({
                "tool": tool_name,
                "result": observation
            })
            
            action_steps.append({
                "type": "action_result",
                "content": f"{tool_name} tool returned: {observation}"
            })
    
    # 4. MEMORY: Store and recall information from past interactions
    # In this simple implementation, we just maintain conversation history
    memory_step = {
        "type": "memory",
        "content": f"Storing interaction in memory. Current history length: {len(history)}"
    }
    
    # 5. RESPOND: Generate final response
    reasoning_steps.extend(action_steps)
    reasoning_steps.append(memory_step)
    
    # Generate final response based on observations
    if not observations:
        final_response = f"I received your message: '{user_message}'. I'm a simple agent that can help with searches, calculations, and weather inquiries. Could you clarify what you'd like me to help you with?"
    else:
        response_parts = []
        for obs in observations:
            if obs["tool"] == "search":
                response_parts.append(f"Based on my search: {obs['result']}")
            elif obs["tool"] == "calculator":
                response_parts.append(f"The calculation result is: {obs['result']}")
            elif obs["tool"] == "weather":
                response_parts.append(f"The weather information is: {obs['result']}")
        
        final_response = " ".join(response_parts)
        
        # Add a conversational touch
        if len(observations) == 1:
            final_response += " Is there anything else I can help you with?"
        else:
            final_response += " Let me know if you need more details on any of this."
    
    # Update history
    updated_history = history.copy()
    updated_history.append({"role": "user", "content": user_message})
    updated_history.append({"role": "assistant", "content": final_response})
    
    return {
        "response": final_response,
        "history": updated_history
    }

@app.get("/")
async def root():
    return {"message": "Simple Agent API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    try:
        result = simple_agent_response(
            user_message=chat_message.message,
            history=chat_message.history or []
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Handler for Netlify Functions
handler = Mangum(app)