import csv
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

DATA_FILE = "assignment_data.json"


class AssignmentTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Assignment Tracker")
        self.root.geometry("900x600")
        self.records = self.load_data()
        self.create_widgets()
        self.show_records()

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return []

        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except:
            return []

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.records, file, indent=2)

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="x")

        ttk.Label(frame, text="Enrollment").grid(row=0, column=0)
        self.enrollment = ttk.Entry(frame)
        self.enrollment.grid(row=0, column=1)

        ttk.Label(frame, text="Name").grid(row=0, column=2)
        self.name = ttk.Entry(frame)
        self.name.grid(row=0, column=3)

        ttk.Label(frame, text="Assignment").grid(row=1, column=0)
        self.assignment = ttk.Entry(frame)
        self.assignment.grid(row=1, column=1)

        ttk.Label(frame, text="Status").grid(row=1, column=2)
        self.status = ttk.Combobox(frame, values=["Pending", "Completed"], state="readonly")
        self.status.set("Pending")
        self.status.grid(row=1, column=3)

        ttk.Label(frame, text="Marks").grid(row=2, column=0)
        self.marks = ttk.Entry(frame)
        self.marks.grid(row=2, column=1)

        ttk.Label(frame, text="Remarks").grid(row=2, column=2)
        self.remarks = ttk.Entry(frame)
        self.remarks.grid(row=2, column=3)

        ttk.Button(frame, text="Add Student", command=self.add_record).grid(row=3, column=0)
        ttk.Button(frame, text="Filter", command=self.filter_records).grid(row=3, column=1)
        ttk.Button(frame, text="Show All", command=self.show_records).grid(row=3, column=2)
        ttk.Button(frame, text="Export CSV", command=self.export_csv).grid(row=3, column=3)

        columns = ("enrollment", "name", "assignment", "status", "marks", "remarks")
        self.table = ttk.Treeview(self.root, columns=columns, show="headings")
        for column in columns:
            self.table.heading(column, text=column.title())
            self.table.column(column, width=130)
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

    def add_record(self):
        enrollment = self.enrollment.get().strip()
        name = self.name.get().strip()
        assignment = self.assignment.get().strip()
        marks = self.marks.get().strip()

        if enrollment == "" or name == "" or assignment == "":
            messagebox.showerror("Error", "Please fill all required fields")
            return

        if marks != "":
            try:
                marks = float(marks)
                if marks < 0 or marks > 100:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Marks must be between 0 and 100")
                return

        record = {
            "enrollment": enrollment,
            "name": name,
            "assignment": assignment,
            "status": self.status.get(),
            "marks": marks,
            "remarks": self.remarks.get().strip()
        }

        self.records.append(record)
        self.save_data()
        self.show_records()
        messagebox.showinfo("Success", "Record saved")

    def show_records(self, records=None):
        if records is None:
            records = self.records

        for item in self.table.get_children():
            self.table.delete(item)

        for record in records:
            values = (
                record["enrollment"],
                record["name"],
                record["assignment"],
                record["status"],
                record["marks"],
                record["remarks"]
            )
            self.table.insert("", "end", values=values)

    def filter_records(self):
        status = self.status.get()
        records = []

        for record in self.records:
            if record["status"] == status:
                records.append(record)

        self.show_records(records)

    def export_csv(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if filename == "":
            return

        fields = ["enrollment", "name", "assignment", "status", "marks", "remarks"]

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self.records)

        messagebox.showinfo("Success", "CSV file exported")


def main():
    root = tk.Tk()
    AssignmentTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
