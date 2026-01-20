# SymptoScan: AI-Powered Symptom Checker 🩺
SymptoScan is a Python-based desktop application designed to provide immediate health information. By leveraging data-driven symptom mapping, the tool suggests possible conditions and provides home-care remedies for mild ailments.

Disclaimer: This tool is for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a physician for any medical condition.

🚀 Features
Multi-Symptom Selection: Users can select multiple symptoms from a comprehensive list.

Intelligent Ranking: Uses a weighted matching algorithm to prioritize common illnesses (like the flu or common cold) while still identifying rarer conditions.

Remedy Mapping: Connects identified conditions to specific home-care remedies stored in a secondary database.

Safety First: Includes automated warnings for critical symptoms and advice on when to seek professional medical help.

🛠️ Tech Stack
Language: Python 3.x

GUI Framework: Tkinter

Data Manipulation: Pandas

Data Source: CSV-based symptom-disease mapping and remedy datasets.

📂 Project Structure
main.py: The core logic and Tkinter GUI implementation.

sorted-symptoms and disease.csv: Dataset containing binary mapping (0/1) of symptoms to various diseases.

disease_remedy_lower.csv: Database containing descriptions and home remedies for each condition.

⚙️ How It Works
Vectorization: The app converts the user's selected symptoms into a binary vector.

Dot Product Calculation: It performs a dot product between the user vector and the disease dataset to calculate a "match score."

Heuristic Filtering: The results are sorted. Common diseases are given priority in the results display to prevent "medical student syndrome" (assuming a rare disease for a common symptom).

Remedy Retrieval: The app cross-references the top 5 predicted diseases with the remedy CSV to provide actionable advice.
