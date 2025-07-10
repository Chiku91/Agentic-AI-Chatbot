import streamlit as st
import os

from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖✨ " + self.config.get_page_title(), layout="wide")
        st.header("🤖✨ " + self.config.get_page_title())

        # Get options from config
        llm_options = self.config.get_llm_options()
        usecase_options = self.config.get_usecase_options()
        groq_models = self.config.get_groq_model_options()

        with st.sidebar:
           
            if "selected_llm" not in st.session_state:
                st.session_state.selected_llm = llm_options[0]

            st.session_state.selected_llm = st.selectbox(
                "Select LLM", llm_options, index=llm_options.index(st.session_state.selected_llm)
            )
            selected_llm = st.session_state.selected_llm
            self.user_controls["selected_llm"] = selected_llm

            if selected_llm == "Groq":
                self.user_controls["selected_groq_model"] = st.selectbox("Select Groq Model", groq_models)
                groq_key = st.session_state.get("GROQ_API_KEY", "")
                self.user_controls["GROQ_API_KEY"] = st.text_input("GROQ API KEY", value=groq_key, type="password")
                st.session_state["GROQ_API_KEY"] = self.user_controls["GROQ_API_KEY"]

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API Key. Get one at: https://console.groq.com/keys")

           
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecase", usecase_options)

            if self.user_controls["selected_usecase"] == "Chatbot With Web":
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=st.text_input("TAVILY_API_KEY", type="password")

                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY API Key. Get one at: https://app.tavily.com/home")

        return self.user_controls
