from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    RemoveMessage,
)
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from database.db_queries import ChatAppDatabase
from langchain_groq import ChatGroq  # Assuming you're using this wrapper
from enums import messageTypeEnum
from utils import register_user
import os
from utils import string_to_md5
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ChatWorkflow:
    def __init__(self, model_name: str, api_key: str, password, thread_id: str = None, temperature: float = 0.7, name_of_user:str='user'):
        self.model = ChatGroq(
            model_name=model_name,
            temperature=temperature,
            api_key=api_key,
        )
        self.password = password
        self.workflow = StateGraph(state_schema=MessagesState)
        self.memory = MemorySaver()
        self.name_of_user = name_of_user
        self.db = ChatAppDatabase()
        self.user_name = name_of_user
        self.user_id = self.db.get_user_id(username=self.user_name,password=self.password)
        self._build_graph()
        if thread_id is None:
            self.thread_id = self.user_name + str(datetime.now().timestamp())
        else:
            self.thread_id = thread_id


    def _call_model(self, state: MessagesState) -> dict:
        """Invokes the model and returns the updated messages list."""
        system_prompt = (
            "You are a helpful assistant and relationship counselor "
            f"Answer all questions to the best of your ability politely and in a relationship-saving manner. The user you are conversing with has a name {self.name_of_user}. "
            "The provided chat history includes a summary of the earlier conversation."
        )
        system_message = SystemMessage(content=system_prompt)
        print(system_message)

        message_history = state["messages"][:-1]
        last_message = state["messages"][-1]
        message_updates = []

        if len(message_history) >= 4:
            # Summarization logic
            summary_prompt = "Distill the above chat messages into a single summary message. Include as many specific details as you can."
            summary_message = self.model.invoke(
                message_history + [HumanMessage(content=summary_prompt)]
            )

            delete_messages = [RemoveMessage(id=m.id) for m in state["messages"]]
            human_message = HumanMessage(content=last_message.content)
            response = self.model.invoke([system_message, summary_message, human_message])

            message_updates = [summary_message, human_message, response] + delete_messages
            
            # Replace the old messages with new summarized history
            state["messages"] = [summary_message, human_message, response]

        else:
            # Normal path
            response = self.model.invoke([system_message] + state["messages"])
            # ➡️ Include both the human message and the AI response
            message_updates = [last_message, response]
            
            # Add the AI response to state
            state["messages"].append(response)

        # Logging
        print("Updated Message State:", [system_message] + state["messages"])
        print("\nMessage Updates:", message_updates)

        for msg in message_updates:
            if isinstance(msg, (HumanMessage, AIMessage)):
                self._log_to_database(msg)

        return {"messages": message_updates}

    def _build_graph(self):
        """Defines the graph structure."""
        self.workflow.add_node("model", self._call_model)
        self.workflow.add_edge(START, "model")
        self.app = self.workflow.compile(checkpointer=self.memory)

    def run(self, messages: list, thread_id: str = "default"):
        """
        Invoke the workflow with a given message list and thread ID.
        The thread ID lets LangGraph distinguish separate conversations.
        """
        return self.app.invoke(
            {"messages": messages},
            config={"configurable": {"thread_id": thread_id}},
        )

    def _log_to_database(self, message):
        # print(message)
        if isinstance(message, RemoveMessage):
            return  # Ignore deletes

        print("[DB LOG] Saving chat message:")
        message_type = (
            messageTypeEnum.user.value if isinstance(message, HumanMessage) else messageTypeEnum.llm.value
        )
        print("\n"*3)
        print("Thread ID:", self.thread_id)
        print("\n"*3) 
        self.db.add_message(
            user_id=self.user_id,
            message_id=str(message.id),
            message_text=message.content,
            message_type=message_type,
            user_password=self.password, 
            thread_id=self.thread_id
        )


if __name__ == "__main__":
    chat = ChatWorkflow(
        model_name="llama-3.1-8b-instant",
        api_key=os.environ.get("GROQ_API_KEY"),
        temperature=0.7,
        password="abhas123",
        name_of_user="abhas"
    )

    demo_chat = [
        HumanMessage(content="Hey there! How are you?"),
        # AIMessage(content="Hello!"),
        # HumanMessage(content="How are you today? I'm feeling good tell me about you"),
        # AIMessage(content="Fine thanks!"),
        # HumanMessage(content="Now tell me what is my name?")
        # HumanMessage(content="hello there!")
    ]

    result = chat.run(messages=demo_chat)
    print("Result:", result)

    # chat = ChatWorkflow()
    # register_user(user_name="Aditi", user_password="aditi123")
    