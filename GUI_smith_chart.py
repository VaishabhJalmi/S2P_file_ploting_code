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
        self.root.geometry("800x700")

        self.files = []
        self.labels = []
        self.param_options = ["S11", "S21", "S12", "S22"]

        self.create_widgets()

    def create_widgets(self):
        # File selection frame
        self.file_frame = tk.Frame(self.root)
        self.file_frame.pack(pady=10)

        self.add_file_btn = tk.Button(self.file_frame, text="Add S2P File", command=self.add_file)
        self.add_file_btn.pack(side=tk.RIGHT, padx=1)

        self.remove_file_btn = tk.Button(self.file_frame, text="Remove S2P File", command=self.remove_file)
        self.remove_file_btn.pack(side=tk.RIGHT, padx=5)

        self.file_listbox = tk.Listbox(self.file_frame, width=50)
        self.file_listbox.pack(side=tk.LEFT, padx=5)

        self.label_entry = tk.Entry(self.file_frame, width=20)
        self.label_entry.pack(side=tk.LEFT, padx=5)

        self.add_label_btn = tk.Button(self.file_frame, text="Add Label", command=self.add_label)
        self.add_label_btn.pack(side=tk.LEFT, padx=10)

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

        # Grid and axis limits frame
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=10)

        self.grid_var = tk.IntVar()
        self.grid_check = tk.Checkbutton(self.grid_frame, text="Show Grid", variable=self.grid_var)
        self.grid_check.pack(side=tk.LEFT, padx=5)

        self.xmin_label = tk.Label(self.grid_frame, text="X Min:")
        self.xmin_label.pack(side=tk.LEFT, padx=5)
        self.xmin_entry = tk.Entry(self.grid_frame, width=10)
        self.xmin_entry.pack(side=tk.LEFT, padx=5)

        self.xmax_label = tk.Label(self.grid_frame, text="X Max:")
        self.xmax_label.pack(side=tk.LEFT, padx=5)
        self.xmax_entry = tk.Entry(self.grid_frame, width=10)
        self.xmax_entry.pack(side=tk.LEFT, padx=5)

        self.ymin_label = tk.Label(self.grid_frame, text="Y Min:")
        self.ymin_label.pack(side=tk.LEFT, padx=5)
        self.ymin_entry = tk.Entry(self.grid_frame, width=10)
        self.ymin_entry.pack(side=tk.LEFT, padx=5)

        self.ymax_label = tk.Label(self.grid_frame, text="Y Max:")
        self.ymax_label.pack(side=tk.LEFT, padx=5)
        self.ymax_entry = tk.Entry(self.grid_frame, width=10)
        self.ymax_entry.pack(side=tk.LEFT, padx=5)

        # Plot and export buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.plot_btn = tk.Button(self.button_frame, text="Plot", command=self.plot)
        self.plot_btn.pack(side=tk.LEFT, padx=5)

        self.plot_smith_btn = tk.Button(self.button_frame, text="Plot Smith Chart", command=self.plot_smith_chart)
        self.plot_smith_btn.pack(side=tk.LEFT, padx=5)

        self.back_btn = tk.Button(self.button_frame, text="Back", command=self.plot)
        self.back_btn.pack(side=tk.LEFT, padx=5)

        self.export_btn = tk.Button(self.button_frame, text="Export to Excel", command=self.export_to_excel)
        self.export_btn.pack(side=tk.LEFT, padx=5)

        self.export_png_btn = tk.Button(self.button_frame, text="Export to PNG", command=self.export_to_png)
        self.export_png_btn.pack(side=tk.LEFT, padx=5)

        # Canvas for plot
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def add_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("S2P files", "*.s2p")])
        if file_path:
            self.files.append(file_path)
            self.file_listbox.insert(tk.END, file_path.split("/")[-1])

    def remove_file(self):
        selected = self.file_listbox.curselection()
        if selected:
            index = selected[0]
            self.file_listbox.delete(index)
            del self.files[index]
            del self.labels[index]

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
        
        try:
            x_min = float(self.xmin_entry.get())
            x_max = float(self.xmax_entry.get())
            self.ax.set_xlim(x_min, x_max)
        except ValueError:
            pass

        try:
            y_min = float(self.ymin_entry.get())
            y_max = float(self.ymax_entry.get())
            self.ax.set_ylim(y_min, y_max)
        except ValueError:
            pass

        if self.grid_var.get():
            self.ax.grid(True)

        self.ax.legend()
        self.canvas.draw()

    def plot_smith_chart(self):
        self.ax.clear()

        for file, label in zip(self.files, self.labels):
            network = rf.Network(file)
            self.ax = network.plot_s_smith(m=0, n=0, label=label, ax=self.ax)

        self.ax.set_title("Smith Chart")
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

    def export_to_png(self):
        if not self.files:
            messagebox.showerror("Error", "No files to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png")],
                                                 title="Save plot as PNG")

        if file_path:
            self.fig.savefig(file_path)
            messagebox.showinfo("Success", f"Plot exported to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = S2PPlotterApp(root)
    root.mainloop()