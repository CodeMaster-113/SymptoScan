import tkinter as tk
from tkinter import messagebox
import pandas as pd

df = pd.read_csv("sorted-symptoms and disease.csv")
df1 = pd.read_csv("disease_remedy_lower.csv")

disease_col = "diseases"
symptom_cols = df.columns.drop(disease_col)

condition_col = "Condition"
remedy_col = "Remedy"


common_diseases = {
    "Common Cold", "Flu", "Fever", "Headache", "Migraine",
    "Food Poisoning", "Stomach Ache", "Diarrhea", "Indigestion",
    "Sore Throat", "Cough", "Allergy"
}

def predict():
    selected = [symptom_listbox.get(i) for i in symptom_listbox.curselection()]

    if not selected:
        messagebox.showwarning("No Symptoms", "Please select at least one symptom.")
        return

    user_vector = pd.Series(0, index=symptom_cols)

    for s in selected:
        if s in user_vector.index:
            user_vector[s] = 1

    df["match_score"] = df[symptom_cols].dot(user_vector)

    result = (
        df.groupby(disease_col)["match_score"]
        .mean()
        .sort_values(ascending=False)
    )

    common = [d for d in result.index if d in common_diseases]
    others = [d for d in result.index if d not in common_diseases]
    ordered = common + others


    output_box.config(state=tk.NORMAL)
    output_box.delete(1.0, tk.END)

    output_box.insert(tk.END, "🩺 Possible Conditions (Most Likely First)\n\n")
    output_box.insert(
        tk.END,
        "This tool gives suggestions based on symptoms.\n"
        "Most conditions are mild and improve with rest and care.\n\n"
    )

    for i, disease in enumerate(ordered[:5], start=1):

        match = df1[df1[condition_col] == disease]

        if not match.empty:
            remedy = match.iloc[0][remedy_col]
        else:
            remedy = "Immediate Medical help advised."

        output_box.insert(
            tk.END,
            f"{i}. {disease}\n   Home Care: {remedy}\n\n"
        )

    output_box.insert(
        tk.END,
        "⚠ If symptoms worsen or last more than 2–3 days, please consult a medical professional.\n"
    )

    # ---- Lock output box again ----
    output_box.config(state=tk.DISABLED)


root = tk.Tk()
root.title("")
root.state("zoomed")

tk.Label(root, text="SymptoScan", font=("lucida console", 35, "bold")).pack(pady=10)
tk.Label(
    root,
    text="*This system suggests possible conditions based on symptoms and is not a medical diagnosis*",
    font=("Arial", 10, "underline")
).pack(pady=5)

tk.Label(
    root,
    text="Most symptoms are mild and improve with home care. Please consult the nearesty medical facility in case of emergency or critical condition.",
    font=("Arial", 10, "underline")
).pack(pady=5)

tk.Label(root, text="Select Your Symptoms", font=("Arial", 16, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

symptom_listbox = tk.Listbox(frame, width=50, height=20, selectmode=tk.MULTIPLE)
symptom_listbox.pack(side=tk.LEFT, padx=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

symptom_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=symptom_listbox.yview)

for s in symptom_cols:
    symptom_listbox.insert(tk.END, s)

tk.Button(root, text="Predict Disease", font=("Arial", 12, "bold"), command=predict).pack(pady=15)


output_frame = tk.Frame(root)
output_frame.pack(pady=10, fill=tk.BOTH, expand=True)

output_box = tk.Text(
    output_frame,
    height=20,
    width=40,
    font=("Consolas", 11),
    wrap=tk.WORD,
    state=tk.DISABLED 
)
output_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar1 = tk.Scrollbar(output_frame, command=output_box.yview)
scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

output_box.config(yscrollcommand=scrollbar1.set)

root.mainloop()
