# app.py
import streamlit as st
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

from chat_function import ChatWorkflow
from database.db_queries import ChatAppDatabase
from utils import register_user, string_to_md5


class AuthManager:
    def __init__(self):
        self.db = ChatAppDatabase()

    def login(self, username, password):
        if self.db.user_exists(username, string_to_md5(password)):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.password = string_to_md5(password)
            return True
        return False

    def register(self, username, password):
        return register_user(user_name=username, user_password=password)

    def is_logged_in(self):
        return st.session_state.get("logged_in", False)


class ChatApp:
    def __init__(self, db, auth):
        self.db = db
        self.auth = auth

    def initialize_chat_model(self):
        @st.cache_resource
        def load_model():
            return ChatWorkflow(
                model_name="llama-3.1-8b-instant",
                api_key=os.getenv("GROQ_API_KEY"),
                temperature=0.7,
                password=st.session_state.password,
                name_of_user=st.session_state.username,
                thread_id=st.session_state.thread_id
            )
        return load_model()

    def display_threads(self, threads):
        st.sidebar.title("Your Threads")
        for thread in threads:
            latest_message = self.db.get_latest_message_by_thread(thread)
            preview = (latest_message[:30] + "...") if latest_message and len(latest_message) > 10 else latest_message

            cols = st.sidebar.columns([8, 2])

            with cols[0]:
                if st.button(f"📄 {preview}", key=f"thread_{thread}"):
                    if thread != st.session_state.thread_id:
                        st.session_state.thread_id = thread
                        st.session_state.messages = []
                        self.load_thread_messages(thread)

            with cols[1]:
                if st.button("🗑️", key=f"delete_{thread}"):
                    self.db.delete_thread_by_id(thread)
                    st.success(f"Deleted thread {thread}")
                    st.session_state.thread_id = None
                    st.session_state.messages = []
                    st.rerun()

    def load_thread_messages(self, thread_id):
        messages = self.db.get_messages_by_thread_id(thread_id)
        st.session_state.messages = []
        for msg in messages:
            if not msg.message_text:
                continue
            role = "user" if msg.message_type.name == "user" else "assistant"
            st.session_state.messages.append({"role": role, "content": msg.message_text})

    def render_chat(self):
        st.title("💬 Relationship Chat Assistant")

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if user_input := st.chat_input("Say something to your counselor..."):
            self.handle_user_message(user_input)

        if st.session_state.messages:
            if st.button("🆕 Start New Session"):
                self.start_new_session()

    def handle_user_message(self, user_input):
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        formatted = [HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
                     for m in st.session_state.messages]
        formatted.append(HumanMessage(content=user_input))

        model = self.initialize_chat_model()
        response_state = model.run(formatted, thread_id=st.session_state.thread_id)
        ai_messages = [msg for msg in response_state["messages"] if isinstance(msg, AIMessage)]

        if ai_messages:
            latest = ai_messages[-1]
            with st.chat_message("assistant"):
                self.stream_response(latest.content)
            st.session_state.messages.append({"role": "assistant", "content": latest.content})

    def stream_response(self, message):
        for word in message.split():
            yield word + " "
            time.sleep(0.05)

    def start_new_session(self):
        st.session_state.thread_id = st.session_state.username + str(datetime.now())
        st.session_state.messages = []

        self.db.add_message(
            user_id=self.db.get_user_id(st.session_state.username, st.session_state.password),
            thread_id=st.session_state.thread_id,
            message_text="",
            message_type="user",
            user_password=st.session_state.password
        )
        st.rerun()

    def run(self):
        if "thread_id" not in st.session_state:
            st.session_state.thread_id = st.session_state.username + str(datetime.now())
        if "messages" not in st.session_state:
            st.session_state.messages = []

        threads = self.db.get_threads_by_user(self.db.get_user_id(st.session_state.username, st.session_state.password))
        if not st.session_state.thread_id or st.session_state.thread_id not in threads:
            st.session_state.thread_id = threads[0] if threads else st.session_state.username + str(datetime.now())

        self.display_threads(threads)
        self.render_chat()


class MainApp:
    def __init__(self):
        load_dotenv("C:\\Users\\ABHAS\\Downloads\\trying to code\\keys_and_tokens.env")
        self.auth = AuthManager()
        self.db = ChatAppDatabase()

    def registration_ui(self):
        st.title("Register")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            if self.auth.register(username, password):
                st.success("You have registered successfully! Please log in.")
            else:
                st.error("Username or Email already exists.")

    def login_ui(self):
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if self.auth.login(username, password):
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials.")

    def run(self):
        if self.auth.is_logged_in():
            ChatApp(self.db, self.auth).run()
        else:
            page = st.sidebar.selectbox("Choose a page", ["Login", "Register"])
            if page == "Login":
                self.login_ui()
            else:
                self.registration_ui()


if __name__ == "__main__":
    MainApp().run()
