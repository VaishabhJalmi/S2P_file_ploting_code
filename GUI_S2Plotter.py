import tkinter as tk
from tkinter import filedialog, messagebox
import skrf as rf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class S2PPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("S2P Plotter")
        self.root.geometry("800x600")

        self.files = []
        self.labels = []
        self.param_options = ["S11", "S21", "S12", "S22"]

        self.create_widgets()

    def create_widgets(self):
        # File selection frame
        self.file_frame = tk.Frame(self.root)
        self.file_frame.pack(pady=10)

        self.add_file_btn = tk.Button(self.file_frame, text="Add S2P File", command=self.add_file)
        self.add_file_btn.pack(side=tk.LEFT, padx=5)

        self.file_listbox = tk.Listbox(self.file_frame, width=50)
        self.file_listbox.pack(side=tk.LEFT, padx=5)

        self.label_entry = tk.Entry(self.file_frame, width=20)
        self.label_entry.pack(side=tk.LEFT, padx=5)

        self.add_label_btn = tk.Button(self.file_frame, text="Add Label", command=self.add_label)
        self.add_label_btn.pack(side=tk.LEFT, padx=5)

        # Parameter selection frame
        self.param_frame = tk.Frame(self.root)
        self.param_frame.pack(pady=10)

        self.param_label = tk.Label(self.param_frame, text="Select Parameter to Plot:")
        self.param_label.pack(side=tk.LEFT, padx=5)

        self.param_var = tk.StringVar(value=self.param_options)
        self.param_menu = tk.OptionMenu(self.param_frame, self.param_var, *self.param_options)
        self.param_menu.pack(side=tk.LEFT, padx=5)

        # Title and axis labels frame
        self.title_frame = tk.Frame(self.root)
        self.title_frame.pack(pady=10)

        self.title_label = tk.Label(self.title_frame, text="Plot Title:")
        self.title_label.pack(side=tk.LEFT, padx=5)
        self.title_entry = tk.Entry(self.title_frame, width=20)
        self.title_entry.pack(side=tk.LEFT, padx=5)

        self.xlabel_label = tk.Label(self.title_frame, text="X Axis Label:")
        self.xlabel_label.pack(side=tk.LEFT, padx=5)
        self.xlabel_entry = tk.Entry(self.title_frame, width=20)
        self.xlabel_entry.pack(side=tk.LEFT, padx=5)

        self.ylabel_label = tk.Label(self.title_frame, text="Y Axis Label:")
        self.ylabel_label.pack(side=tk.LEFT, padx=5)
        self.ylabel_entry = tk.Entry(self.title_frame, width=20)
        self.ylabel_entry.pack(side=tk.LEFT, padx=5)

        # Plot and export buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.plot_btn = tk.Button(self.button_frame, text="Plot", command=self.plot)
        self.plot_btn.pack(side=tk.LEFT, padx=5)

        self.export_btn = tk.Button(self.button_frame, text="Export to Excel", command=self.export_to_excel)
        self.export_btn.pack(side=tk.LEFT, padx=5)

        # Canvas for plot
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def add_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("S2P files", "*.s2p")])
        if file_path:
            self.files.append(file_path)
            self.file_listbox.insert(tk.END, file_path.split("/")[-1])

    def add_label(self):
        label = self.label_entry.get()
        if label:
            self.labels.append(label)
            self.file_listbox.insert(tk.END, f"Label: {label}")
            self.label_entry.delete(0, tk.END)

    def plot(self):
        self.ax.clear()

        all_data = pd.DataFrame()
        param = self.param_var.get().lower()
        param_index = {"s11": (0, 0), "s21": (1, 0), "s12": (0, 1), "s22": (1, 1)}[param]

        for file, label in zip(self.files, self.labels):
            network = rf.Network(file)
            param_db = network.s_db[:, param_index[0], param_index[1]]
            frequency = network.f

            data = pd.DataFrame({'Frequency (Hz)': frequency, f'{param.upper()} (dB) - {label}': param_db})

            if all_data.empty:
                all_data = data
            else:
                all_data = pd.merge(all_data, data, on='Frequency (Hz)', how='outer')

            self.ax.plot(frequency, param_db, label=label)

        self.ax.set_title(self.title_entry.get())
        self.ax.set_xlabel(self.xlabel_entry.get())
        self.ax.set_ylabel(self.ylabel_entry.get())
        self.ax.legend()
        self.canvas.draw()

    def export_to_excel(self):
        if not self.files:
            messagebox.showerror("Error", "No files to export.")
            return

        all_data = pd.DataFrame()
        param = self.param_var.get().lower()
        param_index = {"s11": (0, 0), "s21": (1, 0), "s12": (0, 1), "s22": (1, 1)}[param]

        for file, label in zip(self.files, self.labels):
            network = rf.Network(file)
            param_db = network.s_db[:, param_index[0], param_index[1]]
            frequency = network.f

            data = pd.DataFrame({'Frequency (Hz)': frequency, f'{param.upper()} (dB) - {label}': param_db})

            if all_data.empty:
                all_data = data
            else:
                all_data = pd.merge(all_data, data, on='Frequency (Hz)', how='outer')

        all_data.to_excel('s2p_parameters.xlsx', index=False)
        messagebox.showinfo("Success", "Data exported to s2p_parameters.xlsx")

if __name__ == "__main__":
    root = tk.Tk()
    app = S2PPlotterApp(root)
    root.mainloop()
