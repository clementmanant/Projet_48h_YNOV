import tkinter as tk
from tkinter import ttk

def create_rounded_frame(parent, width, height, radius, bg_color, fg_color, title=""):
    """
    Crée un cadre avec des bords arrondis simulés.
    bg_color : couleur de fond (doit correspondre au fond parent pour que les coins se fondent)
    fg_color : couleur de la zone arrondie
    """
    # Le Canvas hérite de la couleur de fond du parent pour masquer les "coins blancs"
    canvas = tk.Canvas(parent, width=width, height=height, bg=bg_color, highlightthickness=0)
    canvas.grid_propagate(False)

    # Dessiner la zone arrondie
    # Les arcs + les rectangles peignent toute la surface avec fg_color
    canvas.create_arc((0, 0, radius * 2, radius * 2), start=90, extent=90, fill=fg_color, outline="")
    canvas.create_arc((width - radius * 2, 0, width, radius * 2), start=0, extent=90, fill=fg_color, outline="")
    canvas.create_arc((0, height - radius * 2, radius * 2, height), start=180, extent=90, fill=fg_color, outline="")
    canvas.create_arc((width - radius * 2, height - radius * 2, width, height), start=270, extent=90, fill=fg_color, outline="")

    canvas.create_rectangle((radius, 0, width - radius, height), fill=fg_color, outline="")
    canvas.create_rectangle((0, radius, width, height - radius), fill=fg_color, outline="")

    # Ajout du titre en haut à gauche (optionnel)
    if title:
        canvas.create_text(15, 15, anchor="nw", text=title, font=("Arial", 14, "bold"), fill="black")

    return canvas


# --- Création de la fenêtre principale ---
root = tk.Tk()
root.title("BMS Interface")
root.geometry("1200x900")  
# Choisissez une couleur de fond gris clair
root.configure(bg="#ECECEC")

# Cadre principal (même couleur de fond pour uniformiser)
outer_frame = tk.Frame(root, bg="#FFFFFF")
outer_frame.pack(fill="both", expand=True)

# Canvas pour le scrolling, même couleur de fond
canvas = tk.Canvas(outer_frame, bg="#FFFFFF", highlightthickness=0)
scroll_y = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
scroll_x = ttk.Scrollbar(outer_frame, orient="horizontal", command=canvas.xview)

scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")
canvas.pack(side="left", fill="both", expand=True)

canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

# On utilise un Frame "classique" (pas ttk) pour pouvoir récupérer la couleur de fond
main_frame = tk.Frame(canvas, bg="#FFFFFF")
canvas.create_window((0, 0), window=main_frame, anchor="nw")

# --- Organisation des cadres avec bordures arrondies ---
# On passe main_frame['bg'] comme bg_color pour masquer les coins
frame_voltages = create_rounded_frame(
    main_frame, 450, 400, 20, main_frame['bg'], "#CCE5FF", title="Cell voltages"
)
frame_voltages.grid(row=0, column=0, padx=15, pady=15)

frame_temperatures = create_rounded_frame(
    main_frame, 450, 130, 20, main_frame['bg'], "#FFD9B3", title="Temperatures"
)
frame_temperatures.grid(row=1, column=0, padx=15, pady=15)

frame_alerts = create_rounded_frame(
    main_frame, 450, 400, 20, main_frame['bg'], "#FFCCCC", title="Alerts"
)
frame_alerts.grid(row=0, column=1, padx=15, pady=15)

frame_customer = create_rounded_frame(
    main_frame, 450, 130, 20, main_frame['bg'], "#D9F2D9", title="Customer information"
)
frame_customer.grid(row=1, column=1, padx=15, pady=15)

frame_board = create_rounded_frame(
    main_frame, 450, 250, 20, main_frame['bg'], "#E6E6FA", title="Board information"
)
frame_board.grid(row=2, column=0, padx=15, pady=15)

frame_control = create_rounded_frame(
    main_frame, 450, 250, 20, main_frame['bg'], "#D1FFD0", title="Hardware control"
)
frame_control.grid(row=2, column=1, padx=15, pady=15)

frame_global = create_rounded_frame(
    main_frame, 950, 170, 20, main_frame['bg'], "#FFEDCC", title="Global measures"
)
frame_global.grid(row=3, column=0, columnspan=2, padx=15, pady=15)

# --- Ajout des widgets aux cadres ---

# Cell voltages (V1 à V14)
voltages_frame_inner = ttk.Frame(frame_voltages)
# Placement absolu à l'intérieur du Canvas "arrondi"
voltages_frame_inner.place(x=10, y=40, width=430, height=345)

for i in range(1, 14):
    row = (i - 1) // 3
    col = (i - 1) % 3
    ttk.Label(voltages_frame_inner, text=f"V{i}:", font=("Arial", 12)).grid(row=row, column=col * 2, padx=5, pady=5, sticky="w")
    ttk.Entry(voltages_frame_inner, width=9).grid(row=row, column=col * 2 + 1, padx=5, pady=5, sticky="w")

# Temperatures (NTC 1 à 3)
temperatures_frame_inner = ttk.Frame(frame_temperatures)
temperatures_frame_inner.place(x=10, y=40, width=430, height=80)

for i in range(1, 4):
    ttk.Label(temperatures_frame_inner, text=f"NTC {i}:", font=("Arial", 12)).grid(row=0, column=(i - 1) * 2, padx=5, pady=5, sticky="w")
    ttk.Entry(temperatures_frame_inner, width=7).grid(row=0, column=(i - 1) * 2 + 1, padx=5, pady=5, sticky="w")

# Alerts
alerts_frame_inner = ttk.Frame(frame_alerts)
alerts_frame_inner.place(x=10, y=40, width=430, height=345)

alerts = ["Minor 1", "Minor 2", "Major 1", "Major 2", "Major 3", "Major 4"]
for i, alert in enumerate(alerts):
    ttk.Label(alerts_frame_inner, text=alert, font=("Arial", 12)).grid(row=i, column=0, padx=5, pady=5, sticky="w")
    ttk.Entry(alerts_frame_inner, width=15).grid(row=i, column=1, padx=5, pady=4, sticky="w")

ttk.Label(alerts_frame_inner, text="Addr. param. Error:", font=("Arial", 12)).grid(row=6, column=0, padx=5, pady=5, sticky="w")
tk.Text(alerts_frame_inner, height=4, width=30).grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

tk.Button(alerts_frame_inner, text="Reset alerts", font=("Arial", 12)).grid(row=8, column=0, columnspan=2, pady=4)

# Customer Information
customer_frame_inner = ttk.Frame(frame_customer)
customer_frame_inner.place(x=10, y=40, width=430, height=80)

customer_fields = [("Serial number:", 0), ("Part number:", 1)]
for field, row in customer_fields:
    ttk.Label(customer_frame_inner, text=field, font=("Arial", 12)).grid(row=row, column=0, padx=5, pady=5, sticky="w")
    ttk.Entry(customer_frame_inner, width=20).grid(row=row, column=1, padx=5, pady=5, sticky="w")

# Board Information
board_frame_inner = ttk.Frame(frame_board)
board_frame_inner.place(x=10, y=40, width=430, height=200)

board_fields = ["Hardware v.", "Software v.", "Bootloader v.", "Serial number", "Part number"]
for i, field in enumerate(board_fields):
    ttk.Label(board_frame_inner, text=field, font=("Arial", 12)).grid(row=i, column=0, padx=5, pady=5, sticky="w")
    ttk.Entry(board_frame_inner, width=20).grid(row=i, column=1, padx=5, pady=5, sticky="w")

# Hardware Control
control_frame_inner = ttk.Frame(frame_control)
control_frame_inner.place(x=10, y=40, width=430, height=200)

ttk.Label(control_frame_inner, text="Vbatt:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(control_frame_inner, width=15).grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Global Measures
global_frame_inner = ttk.Frame(frame_global)
global_frame_inner.place(x=10, y=40, width=930, height=120)

global_fields = [
    ("Pack (sum):", 0, 0),
    ("V min:", 0, 1),
    ("V max:", 1, 0),
    ("T min:", 1, 1),
    ("T max:", 2, 0),
]
for field, row, col in global_fields:
    ttk.Label(global_frame_inner, text=field, font=("Arial", 12)).grid(row=row, column=col * 2, padx=5, pady=5, sticky="w")
    ttk.Entry(global_frame_inner, width=15).grid(row=row, column=col * 2 + 1, padx=5, pady=5, sticky="w")

# Lancement de la boucle principale
root.mainloop()
