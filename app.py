import streamlit as st
st.title("Medication Information Translator")
st.write(
    "Search for a medication to view its uses, warnings, side effects, recall status, and a simplified AI explanation"
)

medication_name = st.text_input("Enter a medication name")

search = st.button("Search")
