from src.langgraphagenticai.state.state import State
from langchain_core.messages import ToolMessage, AIMessage
import json

class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """
    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response with tool integration.
        """
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role": "user", "content": user_input}])

        # Simulate tool output (for demo, you'd return actual JSON search result from Tavily)
        tools_output = [
            {
                "title": "Bharati Vidyapeeth College of Engineering - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Bharati_Vidyapeeth_College_of_Engineering",
                "content": "Bharati Vidyapeeth College of Engineering (BVCoE)... established in 1990... affiliated to University Of Mumbai..."
            },
            {
                "title": "Bharati Vidyapeeth's College of Engineering – New Delhi",
                "url": "https://bvcoend.ac.in/",
                "content": "Bharati Vidyapeeth's College of Engineering, New Delhi since its establishment in 1999..."
            }
        ]

        tool_message = ToolMessage(content=json.dumps(tools_output), tool_name="search")

        return {"messages": [tool_message, AIMessage(content="Here are some results I found for you:")]}

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function with tools bound.
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            return {"messages": [llm_with_tools.invoke(state["messages"])]}

        return chatbot_node
