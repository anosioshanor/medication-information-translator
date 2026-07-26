import streamlit as st
from services.fda_client import FDAClient
from services.ai_translator import AITranslator

# ============================================================
# MY TASK: Streamlit UI Components
# ============================================================

st.set_page_config(
    page_title="Medication Information Translator",
    page_icon="💊",
    layout="wide"
)

# Initialize AI Translator
translator = AITranslator()
fda_client = FDAClient()

# Custom Styling
st.markdown("""
<style>
.stButton button {
    background-color: #009688;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
}
.stButton button:hover {
    background-color: #00796B;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("💊 Medication Information Translator")
st.write("Enter a medication name to get medical information and an AI-generated simple explanation.")
st.divider()

# ============================================================
# 👇 TEAMMATE: SEARCH HISTORY (Will be added by ???)
# ============================================================
# with st.sidebar:
#     st.header("📋 Search History")
#     # ... ??? will implement this
# ============================================================

# Search Section
st.subheader("🔍 Search Medication")

medicine_name = st.text_input(
    "Medication Name",
    placeholder="Example: Paracetamol"
)

search_button = st.button("🔍 Search", use_container_width=True)

# ============================================================
# MY TASK: AI Error Handling (Display errors to user)
# ============================================================

if search_button:
    if not medicine_name or medicine_name.strip() == "":
        st.warning("⚠️ Please enter a medication name.")
    else:
        cleaned_name = medicine_name.strip()
        
        with st.spinner("🔄 Processing medication information..."):
            try:
                # ============================================================
                # 👇 ???: FDA DATA (Will be provided by ???)
                # ============================================================
                # medical_text = fda_client.get_medication_info(cleaned_name)
                # ============================================================
                
                result = fda_client.fetch_drug_info(cleaned_name)
                fda_data = result["extracted"]

                medical_text = f"""
                Medication: {cleaned_name}

                Uses:
                {fda_data.get("usage", "No usage information available.")}

                Warnings:
                {fda_data.get("warnings", "No warnings available.")}

                Side Effects:
                {fda_data.get("side_effects", "No side effects available.")}

                Dosage:
                {fda_data.get("instructions", "No dosage information available.")}
                """
                
                # ============================================================
                # MY TASK: AI Translation (Calls my ai_translator.py)
                # ============================================================
                explanation = translator.translate(medical_text)
                
                # ============================================================
                # 👇 ???: SEARCH HISTORY (Will be saved by ???)
                # ============================================================
                # history.save_search(cleaned_name)
                # ============================================================
                
                # ============================================================
                # MY TASK: UI Results Display
                # ============================================================
                st.success("✅ Information generated successfully!")
                st.divider()
                
                st.subheader(f"💊 {cleaned_name.title()}")
                
                # ============================================================
                # 👇 ???: FDA DATA DISPLAY (Will be added by ???)
                # ============================================================
                # col1, col2 = st.columns(2)
                # with col1:
                #     st.container(border=True).markdown(f"### ✅ Uses\n\n{fda_data['uses']}")
                # with col2:
                #     st.container(border=True).markdown(f"### ⚠️ Warnings\n\n{fda_data['warnings']}")
                # ============================================================
                
                col1, col2 = st.columns(2)

                with col1:
                    st.container(border=True).markdown(
                        f"""
### ✅ Uses

{fda_data.get("usage", "No usage information available.")}
"""
                    )

                with col2:
                    st.container(border=True).markdown(
                        f"""
### ⚠️ Warnings

{fda_data.get("warnings", "No warnings available.")}
"""
                    ) 
                
                # ============================================================
                # MY TASK: Display AI Simplified Explanation
                # ============================================================
                st.subheader("🤖 AI Simplified Explanation")
                st.container(border=True).write(explanation)
                
            except Exception as e:
                # ============================================================
                # MY TASK: AI Exception Handling (User-friendly errors)
                # ============================================================
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Please try again later.")

# Footer
st.divider()
st.caption(
    "Built with Python, Streamlit & Meta-llama | "
    "By NCAIR COHORT 36 GROUP 1 PYTHON ADVANCED. "
    "Always consult a healthcare professional for medical advice."
)
