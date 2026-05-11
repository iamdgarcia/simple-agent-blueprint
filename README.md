# Simple Agent Blueprint

A deployable template for a Simple Agent based on the Agentic AI for Beginners course. This template implements the basic agent loop: perception, reasoning, action, and memory.

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/iamdgarcia/simple-agent-blueprint&affiliate=8mntz9z1uxdi-96ld6)

## What is a Simple Agent?

A Simple Agent implements the foundational agent architecture:
1. **Perception** - Receive input from the environment
2. **Reasoning** - Process the input and decide what to do
3. **Action** - Execute actions based on reasoning
4. **Memory** - Store and recall information from past interactions

This pattern is covered in Modules 1.1 and 1.2 of the Agentic AI for Beginners course.

## Features

- 🤖 **Working Simple Agent** - Implementation based on course teachings
- 💬 **Chat Interface** - Interact with the agent through a web UI
- 🧠 **Basic Memory** - Remembers conversation history
- ⚡ **Netlify Functions** - Serverless backend for the agent logic
- 🎨 **Clean Interface** - Responsive design that works on mobile and desktop
- 📚 **Course-Aligned** - Directly implements concepts from Modules 1.1-1.2
- 🚀 **One-Click Deploy** - Ready to deploy to Netlify with affiliate tracking

## How It Works

The Simple Agent follows this loop:
1. **Perceive** - Receive user input
2. **Reason** - Analyze the input and determine intent
3. **Act** - Select and execute appropriate tools/actions
4. **Remember** - Store interaction in memory for future reference
5. **Respond** - Return results to the user

## Included Implementation

- Python-based Simple Agent logic
- Simple REST API endpoint (`/.netlify/functions/simple-agent`)
- HTML/JavaScript frontend for interaction
- Conversation memory storage
- Example tools: search, calculator, and weather (mock implementations)
- Conversation history tracking

## Accessing the API Directly

After deployment, you can access the Simple Agent API directly at:
```
https://YOUR-SITE-NAME.netlify.app/.netlify/functions/simple-agent
```

Replace `YOUR-SITE-NAME` with your actual Netlify subdomain.

### API Endpoint
- **URL**: `https://YOUR-SITE-NAME.netlify.app/.netlify/functions/simple-agent`
- **Method**: `POST`
- **Content-Type**: `application/json`

### Request Format
```json
{
  "message": "Your question or command here",
  "history": [
    {"role": "user", "content": "previous message"},
    {"role": "assistant", "content": "previous response"}
  ]
}
```

## Local Development

To run this blueprint locally:

```bash
# Clone the repository
git clone https://github.com/iamdgarcia/simple-agent-blueprint.git
cd simple-agent-blueprint

# Install dependencies
pip install -r requirements.txt

# Start the server (for local testing)
python server.py

# Visit http://localhost:8000 to test
```

## Deployment Details

This blueprint uses:
- **Netlify Functions** for the agent logic (Python runtime)
- **Static frontend** served from the `public/` directory
- **Build command**: None (static site + functions)
- **Publish directory**: `public/`
- **Functions directory**: `netlify/functions/`

## Customization

After deployment, you can:
1. Modify the agent's reasoning logic in `netlify/functions/simple-agent.py`
2. Add or modify tools in the `tools/` directory
3. Update the frontend in `public/` directory
4. Change the styling in `public/style.css`
5. Add more sophisticated tools (real APIs, etc.)

## Course Connection

This blueprint directly implements the agent architecture taught in:
- **Module 1.1: The Agent Loop (Perception, Reasoning, Action, Memory)**
- **Module 1.2: Agent Reasoning & Prompt Engineering**
- Shows how to build a foundational agent that processes input and responds appropriately
- Provides the basis for more complex agents like ReAct, Planning, and Reflective agents

## Extending This Blueprint

You can extend this to:
- Add real API integrations (weather, search, etc.)
- Implement more sophisticated memory systems (vector databases, etc.)
- Add more advanced reasoning patterns
- Build upon it to create ReAct, Planning, Reflective, or other specialized agents

## Support

For issues or questions:
- Refer to the course materials in tlc_agents_training and tlc_course
- Check Netlify Functions documentation: https://docs.netlify.com/functions/
- Review the original agent implementation concepts

---

*Built with ❤️ for The Learning Curve community. Deploy using your affiliate link to support continued development of free AI education resources.*