import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def load_csv(collector_label, collector_files):
    filenames = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if filenames:
        collector_files.extend(filenames)
        collector_label.config(text=f"Selected: {len(collector_files)} files")

def compare_collections():
    try:
        if not collector1_files or not collector2_files:
            messagebox.showerror("Error", "Please select CSV files for both collectors.")
            return
        
        df1 = load_data(collector1_files)
        df2 = load_data(collector2_files)

        merged = df1.merge(df2, on=['set_id', 'card_id', 'card_name'], suffixes=('_p1', '_p2'), how='outer').fillna(0)
        
        trade_p1 = merged[(merged['quantity_p1'] <= 1) & (merged['quantity_p2'] >= 3)]
        trade_p2 = merged[(merged['quantity_p2'] <= 1) & (merged['quantity_p1'] >= 3)]
        
        result_text_p1.set("\n".join(
            f"{row['card_name']} (Set: {row['set_id']}, ID: {row['card_id']}, x{int(row['quantity_p2'])})"
            for _, row in trade_p1.iterrows()
        ) if not trade_p1.empty else "No possible trades.")
        
        result_text_p2.set("\n".join(
            f"{row['card_name']} (Set: {row['set_id']}, ID: {row['card_id']}, x{int(row['quantity_p1'])})"
            for _, row in trade_p2.iterrows()
        ) if not trade_p2.empty else "No possible trades.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def load_data(file_list):
    """ Load and merge multiple CSV files into a single DataFrame. """
    dataframes = [pd.read_csv(file) for file in file_list]
    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

root = tk.Tk()
root.title("Pokémon TCGP Trading Assistant")

collector1_files = []
collector2_files = []
result_text_p1 = tk.StringVar()
result_text_p2 = tk.StringVar()

# Layout Setup
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=10)

# Collector 1 CSV Selection
tk.Label(frame_top, text="Collector #1 CSVs:").grid(row=0, column=0, padx=10, pady=5)
collector1_label = tk.Label(frame_top, text="No files selected")
collector1_label.grid(row=0, column=1, padx=10, pady=5)
tk.Button(frame_top, text="Select Files", command=lambda: load_csv(collector1_label, collector1_files)).grid(row=0, column=2, padx=10, pady=5)

# Collector 2 CSV Selection
tk.Label(frame_top, text="Collector #2 CSVs:").grid(row=1, column=0, padx=10, pady=5)
collector2_label = tk.Label(frame_top, text="No files selected")
collector2_label.grid(row=1, column=1, padx=10, pady=5)
tk.Button(frame_top, text="Select Files", command=lambda: load_csv(collector2_label, collector2_files)).grid(row=1, column=2, padx=10, pady=5)

# Submit Button
tk.Button(frame_top, text="Show trades!", command=compare_collections).grid(row=2, column=1, pady=10)

# Side-by-Side Results
tk.Label(frame_bottom, text="Collector #1 can request:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Label(frame_bottom, text="Collector #2 can request:").grid(row=0, column=1, padx=10, pady=5, sticky="w")

result_label_p1 = tk.Label(frame_bottom, textvariable=result_text_p1, wraplength=300, justify="left")
result_label_p1.grid(row=1, column=0, padx=10, pady=5, sticky="w")

result_label_p2 = tk.Label(frame_bottom, textvariable=result_text_p2, wraplength=300, justify="left")
result_label_p2.grid(row=1, column=1, padx=10, pady=5, sticky="w")

root.mainloop()