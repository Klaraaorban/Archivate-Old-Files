import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from tkcalendar import DateEntry

#existing func
from test import archivate_files
from move_files_back import restore_files

app = tk.Tk()
app.title("File Archiver")

mode_var = tk.StringVar(value="archive")

# Mode selection
tk.Label(app, text="Select Mode:").grid(row=0, column=0, sticky=tk.W, padx=6, pady=6)
tk.Radiobutton(app, text="Archive Files", variable=mode_var, value="archive").grid(row=0, column=1, sticky=tk.W)
tk.Radiobutton(app, text="Restore Files", variable=mode_var, value="restore").grid(row=0, column=2, sticky=tk.W)

# Source folder
tk.Label(app, text="Source Folder:").grid(row=1, column=0, sticky=tk.W, padx=6)
source_folder_var = tk.StringVar()
source_entry = tk.Entry(app, textvariable=source_folder_var, width=50)
source_entry.grid(row=1, column=1, columnspan=2, sticky="w")
source_browse_btn = tk.Button(app, text="Browse", command=lambda: source_folder_var.set(filedialog.askdirectory()))
source_browse_btn.grid(row=1, column=3, padx=6)

# Destination folder
tk.Label(app, text="Destination Folder:").grid(row=2, column=0, sticky=tk.W, padx=6)
destination_folder_var = tk.StringVar()
destination_entry = tk.Entry(app, textvariable=destination_folder_var, width=50)
destination_entry.grid(row=2, column=1, columnspan=2, sticky=tk.W)
destination_browse_btn = tk.Button(app, text="Browse", command=lambda: destination_folder_var.set(filedialog.askdirectory()))
destination_browse_btn.grid(row=2, column=3, padx=6)

# # Age
# tk.Label(app, text="Age in Years:").grid(row=3, column=0, sticky=tk.W, padx=6)
# age_years_var = tk.StringVar(value="1")
# age_entry = tk.Entry(app, textvariable=age_years_var, width=10)
# age_entry.grid(row=3, column=1, sticky=tk.W)


# Concrete date
tk.Label(app, text="Date:").grid(row=3, column=0, sticky=tk.W, padx=6)
data_entry = DateEntry(app, width=40, background='blue', foreground='white', borderwidth=2, date_pattern='yyyy.MM.dd')
data_entry.grid(row=3, column=1, columnspan=2, sticky="ew")

# CSV name (for archive)
tk.Label(app, text="CSV Name:").grid(row=4, column=0, sticky=tk.W, padx=6)
csv_name_var = tk.StringVar()
csv_entry = tk.Entry(app, textvariable=csv_name_var, width=50)
csv_entry.grid(row=4, column=1, columnspan=2, sticky=tk.W)
csv_browse_btn = tk.Button(app, text="Browse", command=lambda: csv_name_var.set(filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])))
csv_browse_btn.grid(row=4, column=3, padx=6)

# CSV path for restore
tk.Label(app, text="CSV for restore:").grid(row=5, column=0, sticky=tk.W, padx=6)
log_path_var = tk.StringVar()
log_entry = tk.Entry(app, textvariable=log_path_var, width=50)
log_entry.grid(row=5, column=1, columnspan=2, sticky="w")
log_browse_btn = tk.Button(app, text="Browse", command=lambda: log_path_var.set(filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])))
log_browse_btn.grid(row=5, column=3, padx=6)

app.grid_columnconfigure(1, weight=1, uniform="buttons")
app.grid_columnconfigure(2, weight=1, uniform="buttons")

run_btn = tk.Button(app, text="Run", width=15)
run_btn.grid(row=6, column=1, padx=5,pady=10)

close_btn = tk.Button(app, text="Finish", width=15)
close_btn.grid(row=6, column=2, padx=5, pady=10)


# ---------- Actions ----------
def run_action():
    mode = mode_var.get()
    try:
        if mode == "archive":
            source = source_folder_var.get().strip()
            destination = destination_folder_var.get().strip()
            # age = age_years_var.get().strip()
            selected_date = data_entry.get_date()
            csv_name = csv_name_var.get().strip()

            if not source or not destination or not selected_date or not csv_name:
                messagebox.showerror("Error", "Please fill all archive fields.")
                return
            # if not age.isdigit() or int(age) < 0:
            #     messagebox.showerror("Error", "Age must be a non-negative integer.")
            #     return

            selected_date_str = selected_date.strftime("%Y.%m.%d")


            if not messagebox.askyesno("Confirm", f"Archive files older than {selected_date} years\nfrom:\n{source}\ninto:\n{destination}\nLog: {csv_name}.csv\n\nContinue?"):
                return

            archivate_files(source, destination, selected_date, csv_name)
            messagebox.showinfo("Success", "Archiving finished.")

        elif mode == "restore":
            log_path = log_path_var.get().strip()
            if not log_path:
                messagebox.showerror("Error", "Please select a log CSV file for restore.")
                return

            if not Path(log_path).exists():
                messagebox.showerror("Error", "Selected log file does not exist.")
                return

            if not messagebox.askyesno("Confirm", f"Restore files listed in:\n{log_path}\n\nContinue?"):
                return

            restore_files(log_path)
            messagebox.showinfo("Success", "Restore finished.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")


run_btn.config(command=run_action)
close_btn.config(command=app.destroy)


def toggle_inputs(*args):
    if mode_var.get() == "archive":
        for w in (source_entry, source_browse_btn, destination_entry, destination_browse_btn, data_entry, csv_entry):
            w.config(state=tk.NORMAL)
        for w in (log_entry, log_browse_btn):
            w.config(state=tk.DISABLED)
    else:
        for w in (source_entry, source_browse_btn, destination_entry, destination_browse_btn, data_entry, csv_entry):
            w.config(state=tk.DISABLED)
        for w in (log_entry, log_browse_btn):
            w.config(state=tk.NORMAL)

mode_var.trace_add("write", toggle_inputs)
toggle_inputs()

app.mainloop()
