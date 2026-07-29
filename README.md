# 💊 Medication Information Translator

A Streamlit based web application that retrieves official medication information from the FDA and uses AI to translate complex medical terminology into simple, easy-to-understand language for everyday users.

---

##  Overview

Understanding medication information can be challenging because drug labels often contain technical medical terms. This project bridges that gap by combining official FDA drug information with AI-powered translation to provide users with clear and simplified explanations.

Users can search for a medication and instantly receive information about:

- Uses
- Warnings
- Side Effects
- Dosage Instructions

The application presents this information through a clean and user-friendly interface while gracefully handling invalid medication names and unavailable data.

---

##  Features

-  Search medications by name
-  Retrieve official FDA medication information
-  AI-powered translation of medical terminology into plain English
-  Display medication warnings
-  Show dosage instructions
-  Display possible side effects
-  Friendly error handling for invalid medication names
-  Simple and responsive Streamlit interface

---

##  Tech Stack

- Python
- Streamlit
- OpenRouter API
- FDA Drug API (openFDA)
- Requests
- python-dotenv

---

##  Project Structure

```
medication-information-translator/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
│
└── services/
    ├── ai_translator.py
    ├── fda_client.py
    ├── recall_checker.py
    ├── search_history.py
    └── utils.py
```

---

##  Installation

### Clone the repository

```bash
git clone https://github.com/anosioshanor/medication-information-translator.git
```

### Navigate into the project

```bash
cd medication-information-translator
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Run the application

```bash
streamlit run app.py
```

---

##  How to Use

1. Launch the application.
2. Enter the name of a medication.
3. Click **Search**.
4. View the retrieved FDA information.
5. Read the AI-generated simplified explanation.

---

##  Example Searches

Try searching for medications such as:

- Paracetamol
- Ibuprofen
- Amoxicillin
- Aspirin
- Metformin

Invalid medication names are handled gracefully with a user-friendly error message.

---

##  Error Handling

The application handles:

- Invalid medication names
- Missing FDA records
- API request failures
- Network-related errors
- Missing API keys

---

## 👥 Team Members & Contributions

| Team Member | Contribution |
|-------------|--------------|
| **Anosi Oshanor** | **Project Lead**, Main Application (`app.py`) development, Streamlit user interface development, FDA API integration, AI translator integration, module integration, debugging, testing, Git/GitHub integration, application refinement, quality assurance, final documentation and project deployment |
| **Muhammad Omeiza** | Medication Model (`medication.py`) development and data modelling |
| **Tremendous Dansale** | Medication Information & Safety Terms module (FDA data retrieval and processing) |
| **Blessing Afaha** | AI Medical Translator module (OpenRouter API integration and translation logic) |
| **Joey Fidelis** | Search History module (search history storage and retrieval) |
| **Khalil Bashir** | User guide preparation and documentation support |

---

##  Future Improvements

- Multi language translation
- Medication comparison
- Drug recall notifications
- Voice assisted interaction
- Search suggestions for misspelled medication names


---

##  Disclaimer

This application was developed for educational purposes only. The information provided should not replace professional medical advice, diagnosis or treatment. Always consult a qualified healthcare professional regarding medications and medical decisions.

---

##  License

This project was developed as part of an academic software development project.
