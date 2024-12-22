import streamlit as st
import requests
from PIL import Image
import io

HOST="http://localhost:8000/analyze"
# Page config
st.set_page_config(page_title="Intelligent Neighborhood", layout="wide")

st.title("🏘️ Intelligent Neighborhood Planner")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        # Display images if present
        if "images" in message:
            if "url_image" in message["images"]:
                try:
                    response = requests.get(message["images"]["url_image"])
                    img = Image.open(io.BytesIO(response.content))
                    st.image(img, caption="Neighborhood Overview")
                except Exception as e:
                    st.error(f"Error loading URL image: {str(e)}")

            if "svg_image" in message["images"]:
                st.markdown(
                    """
                    <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
                        <h4>Preview of the Intelligent Neighborhood</h4>
                        {}
                    </div>
                """.format(
                        message["images"]["svg_image"]
                    ),
                    unsafe_allow_html=True,
                )

# Chat input
if prompt := st.chat_input("What would you like to know about the neighborhood?"):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from backend
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = requests.post(
                HOST , json={"prompt": prompt}
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": data["report"],
                        "images": data["images"],
                    }
                )

                st.write(data["report"])

                # Display images
                if "url_image" in data["images"]:
                    try:
                        response = requests.get(data["images"]["url_image"])
                        img = Image.open(io.BytesIO(response.content))
                        st.image(img, caption="Neighborhood Overview")
                    except Exception as e:
                        st.error(f"Error loading URL image: {str(e)}")

                if "svg_image" in data["images"]:
                    st.markdown(
                        """
                        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
                            <h4>Preview of the Intelligent Neighborhood</h4>
                            {}
                        </div>
                    """.format(
                            data["images"]["svg_image"]
                        ),
                        unsafe_allow_html=True,
                    )