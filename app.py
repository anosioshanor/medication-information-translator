import streamlit as st
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
                
                # TEMPORARY PLACEHOLDER - ??? WILL REPLACE THIS
                medical_text = f"""
                Information about {cleaned_name}.
                This medication is used for treatment of various conditions.
                Follow dosage instructions carefully.
                May cause side effects in some patients.
                Consult your healthcare provider for more information.
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
                
                # TEMPORARY PLACEHOLDER DISPLAY - YOU WILL REPLACE THIS
                col1, col2 = st.columns(2)
                with col1:
                    st.container(border=True).markdown(
                        """
                        ### ✅ Uses
                        
                        • Treatment of pain and inflammation
                        • Fever reduction
                        • Relief of symptoms
                        
                        *Please consult your healthcare provider for specific uses.*
                        """
                    )
                with col2:
                    st.container(border=True).markdown(
                        """
                        ### ⚠️ Warnings
                        
                        • Do not exceed recommended dosage
                        • May cause allergic reactions
                        • Consult doctor if pregnant or nursing
                        
                        *Always read the label carefully.*
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
