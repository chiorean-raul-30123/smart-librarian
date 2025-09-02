import os
import sys
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Import local tool

from chatbot import get_summary_by_title

# UI CONFIG
st.set_page_config(page_title="Smart Librarian", layout="wide")
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', sans-serif;
    }
    .stTextInput > div > input {
        border: 1px solid #ccc;
        padding: 0.5rem;
    }
    .recommendation {
        padding: 1rem;
        border-radius: 8px;
        background-color: #ffffff;
        box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
    }
    .header {
        font-size: 2rem;
        font-weight: 700;
        color: #3f3f3f;
    }
    .subheader {
        color: #6c757d;
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# HEADER
st.markdown("<div class='header'>📚 Smart Librarian</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Recomandări inteligente de cărți, alimentate de GPT + RAG</div>", unsafe_allow_html=True)
st.markdown("---")

# TWO COLUMN LAYOUT
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Caută o carte după temă")
    user_input = st.text_input("Ex: dragoste, război, aventură...")

with col2:
    if user_input:
        messages = [
            {"role": "system", "content": "Ești un bibliotecar AI care recomandă cărți pe baza intereselor utilizatorului."},
            {"role": "user", "content": f"Vreau o carte despre: {user_input}"}
        ]

        tools = [{
            "type": "function",
            "function": {
                "name": "get_summary_by_title",
                "description": "Returnează rezumatul complet pentru o carte",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Titlul exact al cărții"
                        }
                    },
                    "required": ["title"]
                }
            }
        }]

        with st.spinner("📖 Caut cea mai bună recomandare..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    tools=tools,
                    tool_choice="auto"
                )

                choice = response.choices[0]

                if choice.finish_reason == "tool_calls":
                    tool_call = choice.message.tool_calls[0]
                    arguments = json.loads(tool_call.function.arguments)
                    title = arguments["title"]

                    summary = get_summary_by_title(title)

                    messages.append(choice.message)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": "get_summary_by_title",
                        "content": summary
                    })

                    final = client.chat.completions.create(
                        model="gpt-4",
                        messages=messages
                    )

                    st.markdown("### Recomandare completă")
                    st.markdown(f"<div class='recommendation'>{final.choices[0].message.content}</div>", unsafe_allow_html=True)

                else:
                    st.markdown("### Recomandare simplă")
                    st.markdown(f"<div class='recommendation'>{choice.message.content}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Eroare: {e}")
