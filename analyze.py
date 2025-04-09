import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GameDataAnalysis:
    def __init__(self, csv_path="history.csv"):
        self.master = tk.Toplevel()
        self.csv_path = csv_path

        try:
            self.df = pd.read_csv(self.csv_path)
            self.df['total_tower_placed'] = self.df['Tower1'] + self.df['Tower2'] + self.df['Tower3']
            self.setup_ui()
        except Exception as e:
            print("Error loading or plotting data:", e)

    def setup_ui(self):
        self.master.title("📊 Game Data Analysis")
        self.master.geometry("1000x750")
        self.master.configure(bg="#2e2e2e")

        style = ttk.Style(self.master)
        style.theme_use("clam")
        style.configure("Treeview", background="#3a3a3a", foreground="white", fieldbackground="#3a3a3a", font=("Arial", 12))
        style.configure("Treeview.Heading", background="#555", foreground="white", font=("Arial", 13, "bold"))
        style.configure("TNotebook", background="#2e2e2e")
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"))

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.create_summary_stats_tab()
        self.create_monsters_killed_tab()
        self.create_damage_chart_tab()
        self.create_tower_usage_tab()

    def create_summary_stats_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Summary Stats")

        header = ttk.Label(frame, text="Game Summary Statistics", font=("Arial", 16, "bold"))
        header.pack(pady=10)

        summary = {
            'Time': self.df['Time'].describe(),
            'Tower Placed': self.df['total_tower_placed'].describe(),
            'Score': self.df['Score'].describe()
        }

        columns = ["Stat"] + list(summary.keys())
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=6)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        stat_labels = {
            'mean': 'Mean',
            'min': 'Min',
            'max': 'Max',
            'std': 'Std Dev'
        }

        for stat_key in ['mean', 'min', 'max', 'std']:
            label = stat_labels[stat_key]
            row = [label] + [round(summary[col][stat_key], 2) for col in summary.keys()]
            tree.insert('', 'end', values=row)

        tree.pack(pady=10)

    def create_monsters_killed_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Monsters Killed")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(range(len(self.df)), self.df['Monsters Killed'], color="#ff6f61")
        ax.set_title("Monsters Killed per Game")
        ax.set_xlabel("Game Session")
        ax.set_ylabel("Monsters Killed")
        ax.grid(True, linestyle='--', alpha=0.5)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

    def create_damage_chart_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Damage Over Time")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(self.df['Damage'], marker='o', linestyle='-', color="#00c3ff")
        ax.set_title("Total Damage per Game")
        ax.set_xlabel("Game Session")
        ax.set_ylabel("Damage")
        ax.grid(True, linestyle='--', alpha=0.5)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

    def create_tower_usage_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Tower Usage")

        tower_sums = self.df[['Tower1', 'Tower2', 'Tower3']].sum()
        fig, ax = plt.subplots()
        ax.pie(
            tower_sums,
            labels=['Tower 1', 'Tower 2', 'Tower 3'],
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 12}
        )
        ax.set_title("Tower Type Usage", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
