import streamlit as st
import requests

def main():
    st.title("Intelligent Neighborhood Construction Planner")
    
    # File upload
    uploaded_file = st.file_uploader("Upload location image", type=["jpg", "png"])
    
    # Project requirements
    st.subheader("Project Requirements")
    requirements = {
        "budget": st.number_input("Budget (in millions)", min_value=0.0),
        "area": st.number_input("Area (in square meters)", min_value=0.0),
        "sustainability_goals": st.multiselect(
            "Sustainability Goals",
            ["Carbon Neutral", "Zero Waste", "Water Conservation"]
        )
    }
    
    if st.button("Process Project"):
        if uploaded_file is not None:
            # Send to backend
            response = requests.post(
                "http://localhost:8000/process_project/",
                files={"image": uploaded_file},
                json={"requirements": requirements}
            )
            
            if response.status_code == 200:
                st.success("Project processed successfully!")
                
                # Display visualization
                if st.button("Generate 2D Preview"):
                    viz_response = requests.post(
                        "http://localhost:8000/generate_visualization/"
                    )
                    if viz_response.status_code == 200:
                        st.image(viz_response.json()["visualization_url"])

if __name__ == "__main__":
    main()
