from src.langgraphagenticai.state.state import State
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

class BasicChatbotNode:
    """
    Basic Chatbot logic implementation
    """

    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        latest_user_message = state["messages"][-1]

        if isinstance(latest_user_message, HumanMessage):
            response = self.llm.invoke(latest_user_message.content)

            if isinstance(response, BaseMessage):
                return {"messages": state["messages"] + [response]}
            else:
                return {"messages": state["messages"] + [AIMessage(content=str(response))]}

        return {"messages": state["messages"]}
