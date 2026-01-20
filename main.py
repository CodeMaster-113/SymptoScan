import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import zipfile
# ------------------ Load Data ------------------
zip_path = "Disease-Symptoms.zip"
csv_name = "sorted-symptoms and disease.csv"
with zipfile.ZipFile(zip_path) as z:
    # Read CSV directly into pandas
    with z.open(csv_name) as f:
        df = pd.read_csv(f)
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

# ------------------ Main Window ------------------
root = tk.Tk()
root.title("SymptoScan")
root.geometry("1100x750")
root.minsize(900, 600)
root.configure(bg="#eef2f7")
root.state("zoomed")

# Make root resizable grid
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# ------------------ Styles ------------------
style = ttk.Style()
style.theme_use("default")

style.configure("Header.TLabel",
                font=("Segoe UI", 28, "bold"),
                background="#eef2f7",
                foreground="#1f2937")

style.configure("Card.TFrame",
                background="white",
                relief="solid",
                borderwidth=1)

style.configure("Section.TLabel",
                font=("Segoe UI", 13, "bold"),
                background="white",
                foreground="#374151")

style.configure("TButton",
                font=("Segoe UI", 11),
                padding=8)

style.configure("Primary.TButton",
                background="#2563eb",
                foreground="white")

# ------------------ Header ------------------
header = ttk.Label(root, text="SymptoScan", style="Header.TLabel")
header.grid(row=0, column=0, pady=15)

# ------------------ Main Container ------------------
main_container = ttk.Frame(root, style="Card.TFrame", padding=15)
main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

main_container.grid_rowconfigure(3, weight=1)
main_container.grid_columnconfigure(0, weight=1)

# ------------------ Patient Details ------------------
details_frame = ttk.Frame(main_container, style="Card.TFrame", padding=15)
details_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
details_frame.grid_columnconfigure((0, 1, 2), weight=1)

ttk.Label(details_frame, text="Enter Patient Details", style="Section.TLabel")\
    .grid(row=0, column=0, columnspan=3, pady=(0, 10))

# Gender
ttk.Label(details_frame, text="Gender").grid(row=1, column=0, sticky="w")
gender_var = tk.StringVar()
gender_box = ttk.Combobox(details_frame, textvariable=gender_var,
                          values=["Male", "Female", "Other"], state="readonly")
gender_box.grid(row=2, column=0, sticky="ew", padx=5)
gender_box.current(0)

# Name
ttk.Label(details_frame, text="Name").grid(row=1, column=1, sticky="w")
name_entry = ttk.Entry(details_frame)
name_entry.grid(row=2, column=1, sticky="ew", padx=5)

# Age
ttk.Label(details_frame, text="Age").grid(row=1, column=2, sticky="w")
age_entry = ttk.Entry(details_frame)
age_entry.grid(row=2, column=2, sticky="ew", padx=5)

# ------------------ Symptoms Section ------------------
symptom_frame = ttk.Frame(main_container, style="Card.TFrame", padding=15)
symptom_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
symptom_frame.grid_rowconfigure(1, weight=1)
symptom_frame.grid_columnconfigure(0, weight=1)

ttk.Label(symptom_frame, text="Select Your Symptoms", style="Section.TLabel")\
    .grid(row=0, column=0, pady=(0, 10))

listbox_frame = ttk.Frame(symptom_frame)
listbox_frame.grid(row=1, column=0, sticky="nsew")

listbox_frame.grid_rowconfigure(0, weight=1)
listbox_frame.grid_columnconfigure(0, weight=1)

symptom_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE,
                             font=("Segoe UI", 10),
                             relief="solid", bd=1)
symptom_listbox.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical",
                          command=symptom_listbox.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
symptom_listbox.config(yscrollcommand=scrollbar.set)

for s in symptom_cols:
    symptom_listbox.insert(tk.END, s)

# ------------------ Buttons ------------------
button_frame = ttk.Frame(main_container)
button_frame.grid(row=2, column=0, pady=10)

def predict():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_var.get()

    # ---------- Validation ----------
    if not name:
        messagebox.showerror("Invalid Name", "Please enter your name.")
        return

    if not name.replace(" ", "").isalpha():
        messagebox.showerror("Invalid Name", "Name should contain only letters.")
        return

    if not age:
        messagebox.showerror("Invalid Age", "Please enter your age.")
        return

    if not age.isdigit() or not (1 <= int(age) <= 120):
        messagebox.showerror("Invalid Age", "Age must be a number between 1 and 120.")
        return

    selected = [symptom_listbox.get(i) for i in symptom_listbox.curselection()]
    if not selected:
        messagebox.showwarning("Warning", "Please select at least one symptom.")
        return
    # --------------------------------

    # ---------- Disease Matching ----------
    disease_scores = {}  # dictionary to store max score for each disease

    for _, row in df.iterrows():
        disease = row[disease_col]
        score = sum(row[s] == 1 for s in selected)
        if score > 0:
            # Keep the maximum score for each disease
            if disease in disease_scores:
                disease_scores[disease] = max(disease_scores[disease], score)
            else:
                disease_scores[disease] = score

    if not disease_scores:
        messagebox.showinfo("No Match", "No diseases matched the selected symptoms.")
        return

    # Sort diseases by score descending
    sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)
    results = sorted_diseases[:5]  # top 5 matches

    # ---------- Output ----------
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END,f"Name: {name}\tAge: {age}\tGender: {gender}\n")

    for i, (disease, _) in enumerate(results, 1):
        remedy = df1.loc[df1[condition_col] == disease, remedy_col]
        remedy = remedy.values[0] if not remedy.empty else "Consult the nearest medical facility immediately."
        output_box.insert(tk.END, f"{i}. {disease}\n   {remedy}\n\n")
    
    output_box.insert(tk.END, "If the symptoms persist or worsen by next 2 to 3 days, immediate medical treatment is advised.")

    output_box.config(state=tk.DISABLED)


def clear_all():
    symptom_listbox.selection_clear(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.config(state=tk.DISABLED)

ttk.Button(button_frame, text="Predict Disease", style="Primary.TButton",
           command=predict).grid(row=0, column=0, padx=10)

ttk.Button(button_frame, text="Clear", command=clear_all)\
    .grid(row=0, column=1, padx=10)

# ------------------ Output Section ------------------
output_frame = ttk.Frame(main_container, style="Card.TFrame", padding=12)
output_frame.grid(row=3, column=0, sticky="nsew")
output_frame.grid_rowconfigure(1, weight=1)
output_frame.grid_columnconfigure(0, weight=1)

ttk.Label(output_frame, text="Prediction Output", style="Section.TLabel")\
    .grid(row=0, column=0, sticky="w", pady=(0, 6))

output_box = tk.Text(output_frame,
                     font=("Consolas", 11),
                     wrap=tk.WORD,
                     relief="solid", bd=1,
                     state=tk.DISABLED)
output_box.grid(row=1, column=0, sticky="nsew")

output_scroll = ttk.Scrollbar(output_frame, orient="vertical",
                              command=output_box.yview)
output_scroll.grid(row=1, column=1, sticky="ns")
output_box.config(yscrollcommand=output_scroll.set)

# ------------------ Run ------------------
root.mainloop()
