import tkinter as tk
from tkinter import messagebox, ttk

# Global list to store student data in memory
students_list = []

# --- Core App Functions ---


def add_student():
    roll_id = int(entry_id.get().strip())
    name = str(entry_name.get().strip())
    age = int(entry_age.get().strip())
    grade = str(entry_grade.get().strip())

    # Validation: Ensure no fields are empty
    if not (roll_id and name and age and grade):
        messagebox.showerror("Error", "All fields are required!")
        return

    # Validation: age must be a whole number
    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a number!")
        return

    # Check for duplicate Roll IDs
    for student in students_list:
        if student["roll_id"] == roll_id:
            messagebox.showerror("Error", f"Roll ID {roll_id} already exists!")
            return

    # Add to our local list
    student = {"roll_id": roll_id, "name": name, "age": age, "grade": grade}
    students_list.append(student)

    # Update the visual table display
    refresh_table()

    # Clear input boxes
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_grade.delete(0, tk.END)

    messagebox.showinfo("Success", f"{name} added successfully!")


def delete_student():
    # Get the selected row from the table
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning(
            "Warning", "Please select a student from the list to delete.")
        return

    # Get the Roll ID of the selected row
    item_details = tree.item(selected_item)
    roll_id_to_delete = item_details['values'][0]

    # Remove from our data list
    global students_list
    students_list = [s for s in students_list if s['roll_id']
                     != str(roll_id_to_delete)]

    refresh_table()
    messagebox.showinfo("Success", "Record deleted successfully!")


def refresh_table():
    # Clear all current visual rows in the table
    for row in tree.get_children():
        tree.delete(row)

    # Re-insert everyone from the updated list
    for student in students_list:
        tree.insert("", tk.END, values=(
            student["roll_id"], student["name"], student["age"], student["grade"]))

# --- GUI Layout Setup ---


# Create window
root = tk.Tk()
root.title("School Record System")
root.geometry("600x450")
root.resizable(False, False)

# Form Section (Labels and Entry Boxes)
# NOTE: tk.LabelFrame doesn't support "padding" (that's a ttk-only option) — use padx/pady instead
frame_form = tk.LabelFrame(root, text=" Student Details ", padx=10, pady=10)
frame_form.pack(fill="x", padx=15, pady=10)

tk.Label(frame_form, text="Roll ID:").grid(
    row=0, column=0, sticky="w", padx=5, pady=2)
entry_id = tk.Entry(frame_form, width=15)
entry_id.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_form, text="Name:").grid(
    row=0, column=2, sticky="w", padx=5, pady=2)
entry_name = tk.Entry(frame_form, width=25)
entry_name.grid(row=0, column=3, padx=5, pady=2)

tk.Label(frame_form, text="Age:").grid(
    row=1, column=0, sticky="w", padx=5, pady=2)
entry_age = tk.Entry(frame_form, width=15)
entry_age.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_form, text="Grade:").grid(
    row=1, column=2, sticky="w", padx=5, pady=2)
entry_grade = tk.Entry(frame_form, width=25)
entry_grade.grid(row=1, column=3, padx=5, pady=2)

# Action Buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(fill="x", padx=15, pady=5)

# NOTE: Tkinter Button has no "px" option — it's "padx"
btn_add = tk.Button(frame_buttons, text="Add Student",
                    command=add_student, bg="#4CAF50", fg="white", padx=10)
btn_add.pack(side="left", padx=5)

btn_delete = tk.Button(frame_buttons, text="Delete Selected",
                       command=delete_student, bg="#f44336", fg="white", padx=10)
btn_delete.pack(side="left", padx=5)

# Visual Table Section (Treeview)
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=15, pady=10)

columns = ("roll_id", "name", "age", "grade")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

# Define table headings
tree.heading("roll_id", text="Roll ID")
tree.heading("name", text="Name")
tree.heading("age", text="Age")
tree.heading("grade", text="Grade")

# Adjust column widths
tree.column("roll_id", width=80, anchor="center")
tree.column("name", width=200, anchor="w")
tree.column("age", width=60, anchor="center")
tree.column("grade", width=120, anchor="center")

tree.pack(fill="both", expand=True)

# Run the app window loop
root.mainloop()
