import streamlit as st
import requests
from typing import Dict, List

# Define API URL for the Urban Bloom city builder
HOST = ""  # Cloud Run URL

st.title("Urban Bloom")

# Initialize session state for conversation and city plan data
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! How can I assist you in building your city?", "sources": []}
    ]

if "city_data" not in st.session_state:
    st.session_state["city_data"] = {}

# Function to display messages in a chat format
def display_messages():
    for n, message in enumerate(st.session_state["messages"]):
        avatar = "🤖" if message["role"] == "assistant" else "🧑‍💻"
        st.chat_message(message["role"], avatar=avatar).write(message["content"])

        # Show sources if the message has them
        if "sources" in message and message["sources"]:
            for i, source in enumerate(message["sources"]):
                with st.expander(f"Source {i+1} - relevance: {(source['metadata']['score']) * 100:.2f}%"):
                    st.write("Metadata:")
                    st.write(source["metadata"])
                    st.write("Content:")
                    st.write(source["page_content"])

# Display initial chat messages
display_messages()

# When the user submits their city plan, send the data to the backend API
if question := st.chat_input("Describe the city you'd like to build"):
    st.session_state["messages"].append({"role": "user", "content": question})

    # Store only the user input as city_data
    st.session_state["city_data"] = {"description": question}

    # Send city data to the backend for processing
    response = requests.post(
        f"{HOST}/generate_city_plan",
        json=st.session_state["city_data"],
        timeout=30,
    )

    if response.status_code == 200:
        result = response.json()
        answer = result.get("text", "No detailed plan returned")

        # Display the system's response (city plan details)
        st.session_state["messages"].append({"role": "assistant", "content": answer, "sources": []})

        # Display the response message in the chat
        st.chat_message("assistant", avatar="🤖").write(answer)

        # Display the image and SVG if available in the response
        image_url = result.get("image_url", None)
        svg_content = result.get("svg", None)

        if image_url:
            st.write("**City Layout Image from URL**:")
            st.image(image_url, caption="Generated City Layout", use_column_width=True)

        if svg_content:
            st.write("**City Layout SVG**:")
            st.markdown(
                f'<img src="data:image/svg+xml;base64,{svg_content}" />',
                unsafe_allow_html=True,
            )

    else:
        st.write(f"Error: Unable to generate city plan. Status Code: {response.status_code}")
    
    # Display updated chat messages
    display_messages()