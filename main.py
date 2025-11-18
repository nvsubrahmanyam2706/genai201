import streamlit as st
from langchain_helper import get_few_shot_db_chain

st.title("Global T-Shirts: Database Q&A 👕")

question = st.text_input("Ask your question:")

if st.button("Get Answer"):
    if question.strip() == "":
        st.error("Please enter a question")
    else:
        chain = get_few_shot_db_chain()
        answer = chain(question)
        st.subheader("Answer:")
        st.write(answer)
