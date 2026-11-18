from groq import Groq
import streamlit as st

def chatbot(respuesta):
    client = Groq(api_key = st.secrets["API_KEY"])
    

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role":"user",
                "content": respuesta,
            }
        ],
        model=st.secrets["MODELO"],
    )

    return chat_completion.choices[0].message.content




