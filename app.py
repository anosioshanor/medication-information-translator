import streamlit as st
from services.fda_client import FDAClient
from services.recall_checker import RecallChecker
from services.ai_translator import AITranslator
from services.search_history import save_search, load_history
from datetime import datetime
import json



st.set_page_config(
    page_title="Medication Information Translator",
    page_icon="💊",
    layout="wide"
)

# Initialize Services
translator = AITranslator()
fda_client = FDAClient()
recall_checker = RecallChecker()


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
st.write("Enter a medication name to get medical information, recall status and an AI-generated simple explanation.")
st.divider()
with st.sidebar:
    st.header("📋 Search History")
    
    # Load history
    history = load_history()
    
    if history:
        # Show the 10 most recent searches (newest first)
        recent_searches = list(reversed(history[-10:]))
        
        st.write(f"Showing {len(recent_searches)} of {len(history)} searches")
        st.divider()
        
        for entry in recent_searches:
            medication = entry.get("medication", "Unknown")
            timestamp = entry.get("timestamp", "")
            
            # Format timestamp for display
            if timestamp:
                try:
                    # Parse ISO format timestamp
                    dt = datetime.fromisoformat(timestamp)
                    formatted_time = dt.strftime("%b %d, %Y %I:%M %p")
                except:
                    formatted_time = timestamp
            else:
                formatted_time = "Recently"
            
            # Create a clickable button for each history item
            col1, col2 = st.columns([4, 1])
            
            with col1:
                if st.button(
                    f"💊 {medication}",
                    key=f"history_{medication}_{timestamp}"
                ):
                    # Set session state and rerun
                    st.session_state.medication_name = medication
                    st.rerun()
                
                st.caption(f"🕐 {formatted_time}")
            
            with col2:
                # Delete individual entry
                if st.button(
                    "✕",
                    key=f"del_{medication}_{timestamp}"
                ):
                    history = [
                        h for h in history
                        if h.get("timestamp") != timestamp
                    ]

                    from services.search_history import HISTORY_FILE

                    with open(
                        HISTORY_FILE,
                        "w",
                        encoding="utf-8"
                    ) as f:
                        json.dump(
                            history,
                            f,
                            indent=2
                        )

                    st.rerun()

            st.divider()
        
        # Clear all history button
        if st.button(
            "🗑️ Clear All History",
            use_container_width=True
        ):
            from services.search_history import HISTORY_FILE

            try:
                with open(
                    HISTORY_FILE,
                    "w",
                    encoding="utf-8"
                ) as f:
                    json.dump(
                        [],
                        f
                    )

                st.success(
                    "✅ History cleared!"
                )

                st.rerun()

            except Exception as e:
                st.error(
                    f"Could not clear history: {e}"
                )

    else:
        st.info(
            "📭 No searches yet.\n\nStart searching for medications!"
        )


# Search Section
st.subheader("🔍 Search Medication")

default_value = st.session_state.get(
    "medication_name",
    ""
)

medicine_name = st.text_input(
    "Medication Name",
    placeholder="Example: Paracetamol",
    value=default_value
)


if "medication_name" in st.session_state:
    del st.session_state.medication_name


search_button = st.button(
    "🔍 Search",
    use_container_width=True
)
if search_button:
    if not medicine_name or medicine_name.strip() == "":
        st.warning("⚠️ Please enter a medication name.")

    else:
        cleaned_name = medicine_name.strip()

        with st.spinner("🔄 Processing medication information..."):

            try:

                result = fda_client.fetch_drug_info(cleaned_name)
                fda_data = result["extracted"]

                # Check medication recall status
                recall_result = recall_checker.check_recall(cleaned_name)


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


                explanation = translator.translate(medical_text)


                save_search(cleaned_name)

                st.success("✅ Information generated successfully!")
                st.divider()


                st.subheader(
                    f"💊 {cleaned_name.title()}"
                )


                # Recall Alert Display
                if recall_result["recalled"]:

                    st.error(
                        f"""
🚨 RECALL ALERT

Product:
{recall_result["product"]}

Reason:
{recall_result["reason"]}

Company:
{recall_result["company"]}

Date:
{recall_result["date"]}
"""
                    )

                else:

                    st.success(
                        f"✅ {recall_result['message']}"
                    )
                    

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


                # Second row for Side Effects and Dosage
                col3, col4 = st.columns(2)

                with col3:
                    st.container(border=True).markdown(
                        f"""
### ⚠️ Side Effects

{fda_data.get("side_effects", "No side effects available.")}
"""
                    )

                with col4:
                    st.container(border=True).markdown(
                        f"""
### 💊 Dosage Instructions

{fda_data.get("instructions", "No dosage information available.")}
"""
                    )


                st.subheader(
                    "🤖 AI Simplified Explanation"
                )

                st.container(border=True).write(
                    explanation
                )


            except Exception as e:

                st.error(
                    f"❌ An error occurred: {str(e)}"
                )

                st.info(
                    "💡 Please try again later."
                )


# Footer

st.divider()

st.caption(
    "Built with Python, Streamlit & Meta-llama | "
    "By NCAIR COHORT 36 GROUP 1 PYTHON ADVANCED. "
    "Always consult a healthcare professional for medical advice."
)