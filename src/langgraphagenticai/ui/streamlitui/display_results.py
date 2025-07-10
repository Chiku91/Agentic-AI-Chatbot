import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        if usecase == "Basic Chatbot":
            for event in graph.stream({"messages": ("user", user_message)}):
                for value in event.values():
                    for msg in value.get("messages", []):
                        if isinstance(msg, HumanMessage):
                            with st.chat_message("user"):
                                st.write(msg.content)
                        elif isinstance(msg, AIMessage):
                            with st.chat_message("assistant"):
                                st.write(msg.content)

        elif usecase == "Chatbot With Web":
            # Prepare state and invoke the graph
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            res = graph.invoke(initial_state)

            for message in res.get('messages', []):
                if isinstance(message, HumanMessage):
                    with st.chat_message("user"):
                        st.write(message.content)
                elif isinstance(message, ToolMessage):
                    with st.chat_message("ai"):
                        st.write("🔧 Tool Call Start")
                        st.write(message.content)
                        st.write("🔧 Tool Call End")
                elif isinstance(message, AIMessage):
                    with st.chat_message("assistant"):
                        st.write(message.content)
