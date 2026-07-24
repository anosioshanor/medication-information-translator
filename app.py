import streamlit as st
import re
from services.ai_translator import AITranslator
from services.search_history import SearchHistory
from models.medication import Medication
from services.fda_client import FDAClient  # ✅ Your FDA client side is needed

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Medication Information Translator",
    page_icon="💊",
    layout="wide"
)

# -----------------------------
# Initialize Services
# -----------------------------

translator = AITranslator()
history = SearchHistory()
fda_client = FDAClient()  # ✅ Initialize FDA client

# -----------------------------
# Custom Styling
# -----------------------------

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
.error-message {
    color: #d32f2f;
    padding: 10px;
    border-radius: 5px;
    background-color: #ffebee;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------

st.title("💊 Medication Information Translator")
st.write(
    "Enter a medication name to get medical information "
    "and an AI-generated simple explanation."
)
st.divider()

# -----------------------------
# Sidebar - History
# -----------------------------

with st.sidebar:
    st.header("📋 Search History")
    
    previous_searches = history.get_history()
    
    if previous_searches:
        for i, item in enumerate(previous_searches, 1):
            st.write(f"{i}. {item}")
        
        if st.button("🗑️ Clear History"):
            history.clear_history()
            st.rerun()
    else:
        st.info("No searches yet.")

# -----------------------------
# Search Section
# -----------------------------

st.subheader("🔍 Search Medication")

def validate_medication_name(name):
    """Validate medication name using regular expression"""
    pattern = r"^[A-Za-z\s\-']{2,50}$"
    return re.match(pattern, name.strip()) is not None

medicine_name = st.text_input(
    "Medication Name",
    placeholder="Example: Paracetamol",
    help="Enter a valid medication name (letters, spaces, hyphens, and apostrophes only)"
)

col1, col2 = st.columns([1, 5])
with col1:
    search_button = st.button("🔍 Search", use_container_width=True)

# -----------------------------
# Processing
# -----------------------------

if search_button:
    # Exception handling for empty field
    if not medicine_name or medicine_name.strip() == "":
        st.warning("⚠️ Please enter a medication name.")
    
    # Validate medication name using regex
    elif not validate_medication_name(medicine_name):
        st.error(
            "❌ Invalid medication name. "
            "Please use only letters, spaces, hyphens, and apostrophes."
        )
    
    else:
        cleaned_name = medicine_name.strip()
        
        with st.spinner("🔄 Fetching FDA data and translating..."):
            try:
                # ============================================================
                # 1️⃣ FETCH REAL DATA FROM FDA API
                # ============================================================
                
                fda_data = fda_client.search_medication(cleaned_name)
                
                # Handle case where no data is found
                if not fda_data or fda_data.get("error"):
                    st.warning(f"⚠️ No FDA data found for '{cleaned_name}'. Please check the name and try again.")
                    st.stop()
                
                # ============================================================
                # 2️⃣ CREATE MEDICATION OBJECT WITH REAL FDA DATA
                # ============================================================
                
                medication = Medication(
                    name=cleaned_name,
                    uses=fda_data.get("uses", "No use information available."),
                    warnings=fda_data.get("warnings", "No warning information available."),
                    side_effects=fda_data.get("side_effects", "No side effect information available.")
                )
                
                # ============================================================
                # 3️⃣ BUILD MEDICAL TEXT FOR AI TRANSLATION
                # ============================================================
                
                medical_text = f"""
Medication: {medication.display_name()}

Uses:
{fda_data.get('uses', 'Not specified')}

Warnings:
{fda_data.get('warnings', 'None reported')}

Side Effects:
{fda_data.get('side_effects', 'None reported')}

Additional Information:
{fda_data.get('additional_info', 'No additional information available.')}
"""
                
                # ============================================================
                # 4️⃣ AI TRANSLATION (YOUR CODE)
                # ============================================================
                
                explanation = translator.translate(medical_text)
                
                # ============================================================
                # 5️⃣ SAVE SEARCH HISTORY
                # ============================================================
                
                history.save_search(cleaned_name)
                
                # ============================================================
                # 6️⃣ DISPLAY RESULTS (ALL FROM FDA, NO PLACEHOLDERS)
                # ============================================================
                
                st.success("✅ Information generated successfully!")
                st.divider()
                
                st.subheader(f"💊 {medication.display_name()}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.container(border=True).markdown(
                        f"""
                        ### ✅ Uses
                        
                        {medication.get_uses()}
                        """
                    )
                    
                    # Also show side effects in same column
                    st.container(border=True).markdown(
                        f"""
                        ### 🔬 Side Effects
                        
                        {medication.get_side_effects()}
                        """
                    )
                
                with col2:
                    st.container(border=True).markdown(
                        f"""
                        ### ⚠️ Warnings
                        
                        {medication.get_warnings()}
                        """
                    )
                    
                    # Show additional info if available
                    if fda_data.get("additional_info"):
                        st.container(border=True).markdown(
                            f"""
                            ### 📋 Additional Information
                            
                            {fda_data.get('additional_info')}
                            """
                        )
                
                # AI Simplified Explanation
                st.subheader("🤖 AI Simplified Explanation")
                st.container(border=True).write(explanation)
                
                # Extract and show warning keywords using regex
                from utils.helpers import find_warning_words
                warnings_found = find_warning_words(explanation)
                if warnings_found:
                    st.info(f"⚠️ Warning keywords detected in the explanation: {', '.join(warnings_found)}")
            
            except ConnectionError as e:
                st.error(f"❌ Network error: Could not reach FDA API. Please check your internet connection.")
                st.info("💡 Tip: Try again in a few moments.")
            
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")
                st.info("💡 Please try again later or contact support.")

# -----------------------------
# Footer
# -----------------------------

st.divider()
st.caption(
    "Built with Python, Streamlit & Meta-llama | "
    "Always consult a healthcare professional for medical advice."
)
