import streamlit as st
from chatbot import generate_response

def main():
    st.title("MLOps Chatbot")
    st.write("Ask me anything about MLOps!")
    
    user_query = st.text_input("Enter your question:")
    if st.button("Get Answer"):
        response = generate_response(user_query)
        st.write(response)

if __name__ == "__main__":
    main()