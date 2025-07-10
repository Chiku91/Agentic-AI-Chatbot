import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        # Prepare input
        initial_state = {"messages": [HumanMessage(content=user_message)]}
        st.chat_message("user").write(user_message)

        if usecase == "Basic Chatbot":
            for event in graph.stream(initial_state):
                for value in event.values():
                    for msg in value.get("messages", []):
                        if isinstance(msg, AIMessage):
                            with st.chat_message("assistant"):
                                st.write(msg.content)

        elif usecase == "Chatbot With Web":
            res = graph.invoke(initial_state)
            for message in res.get('messages', []):
                if isinstance(message, ToolMessage):
                    with st.chat_message("ai"):
                        st.markdown("🔧 **Tool Call Start**")
                        try:
                            results = json.loads(message.content)
                            for result in results:
                                st.markdown(f"🔹 **[{result['title']}]({result['url']})**")
                                st.markdown(f"> {result['content'][:300]}...")  # Trim for readability
                        except Exception as e:
                            st.warning("Unable to parse tool output. Showing raw:")
                            st.write(message.content)
                        st.markdown("🔧 **Tool Call End**")

                elif isinstance(message, AIMessage):
                    with st.chat_message("assistant"):
                        st.write(message.content)
