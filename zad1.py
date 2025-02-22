import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# Funkcja do obliczania Ng dla danej długości fali
def calculate_Ng(lam):
    lam1 = lam / 1000
    Ng = 287.6155 + 4.8866 / (lam1 ** 2) + 0.0680 / (lam1 ** 4)
    return Ng

# Zakres długości fali od 400 do 1600 nm z krokiem 10 nm
wavelengths = np.arange(400, 1601, 10)

# Obliczanie wartości Ng dla każdej długości fali
ng_values = [calculate_Ng(wavelength) for wavelength in wavelengths]
ng_values_small = [(Ng / (10 ** 6) + 1) for Ng in ng_values]

# Tworzenie wykresów
fig, axs = plt.subplots(2, 1, figsize=(8, 8), sharex=True, gridspec_kw={'hspace': 0.3})

# Wykres Ng
axs[0].plot(wavelengths, ng_values, 'o-', markersize=2, linewidth=1, label='Ng')
axs[0].set_title('Zależność współczynnika Ng od długości fali')
axs[0].set_ylabel('Ng')
axs[0].grid(True)
axs[0].legend()

# Wykres ng
axs[1].plot(wavelengths, ng_values_small,'o-', markersize=2, linewidth=1, label='ng')
axs[1].set_title('Zależność ng od długości fali')
axs[1].set_xlabel('Długość fali (nm)')
axs[1].set_ylabel('ng')
axs[1].grid(True)
axs[1].legend()
axs[1].yaxis.set_major_formatter(ticker.FormatStrFormatter('%.6f'))



def calculate_Ng(lam):
    lam1 = lam / 1000
    Ng = 287.6155 + 4.8866 / (lam1 ** 2) + 0.0680 / (lam1 ** 4)
    return Ng

def ng(wavelength, dry_temperature, pressure, e_value):
    return calculate_Ng(wavelength)* 0.269578 * pressure/(dry_temperature+273.15) - 11.27*e_value/(dry_temperature+273.15)

def Ew(wet_temperature):
    return 6.1078*np.exp((17.269*wet_temperature)/(237.30+wet_temperature))  

def e(Ew, wet_temperature, dry_temperature, pressure):
    return Ew -0.000662*pressure*(dry_temperature-wet_temperature)
def dD(wavelength, dry_temperature, pressure, wet_temperature):
    ewd= Ew(wet_temperature)
    ed= e(ewd, wet_temperature, dry_temperature, pressure)
    ng_dow_war= ng(wavelength, dry_temperature, pressure, ed)
    ng_normalne= ng(wavelength, 15, 1013.25,10.87)
    return ng_normalne-ng_dow_war


def calculate_atmospheric_correction(wavelength, dry_temperature, wet_temperature, pressure, measured_length):
    

    atmospheric_correction_km = dD(wavelength, dry_temperature, pressure, wet_temperature)
    atmospheric_correction_length = (atmospheric_correction_km / 1000) * measured_length # Zamiana na metry
    atmospheric_correction_length/=1000
    corrected_length = measured_length + atmospheric_correction_length
    return atmospheric_correction_km, atmospheric_correction_length, corrected_length

def calculate_button_clicked():
    wavelength = float(entry_wavelength.get())
    dry_temperature = float(entry_dry_temperature.get())
    wet_temperature = float(entry_wet_temperature.get())
    pressure = float(entry_pressure.get())
    measured_length = float(entry_measured_length.get())

    atmospheric_correction_km, atmospheric_correction_length, corrected_length = \
        calculate_atmospheric_correction(wavelength, dry_temperature, wet_temperature, pressure, measured_length)

    label_result.config(text=f"Poprawka na km: {atmospheric_correction_km:.6f} km\n"
                             f"Poprawka do mierzonej długości: {atmospheric_correction_length:.6f} m\n"
                             f"Długość poprawiona: {corrected_length:.6f} m")


# Tworzenie głównego okna Tkinter
root = tk.Tk()
root.title("Wykresy Matplotlib w Tkinter")

# Dodanie zakładki
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky="nsew")

# Zakładka z kodem
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text='Pierwsza zakładka')

# Kod
canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, sticky="nsew")  

# Dorysowanie tabeli z suwakiem
frame = ttk.Frame(frame1)
frame.grid(row=0, column=1, sticky="ns")

tree = ttk.Treeview(frame, columns=(1, 2), show="headings", height="10")
tree.heading(1, text="Długość fali (nm)")
tree.heading(2, text="Ng")

for i in range(len(wavelengths)):
    tree.insert("", "end", values=(wavelengths[i], ng_values[i]))

tree.pack(side=tk.LEFT, fill=tk.Y)

# Dodanie suwaka
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)


# Zakładka 2
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text='Druga zakładka')



# Dodawanie zakładek do okna głównego
notebook.pack(expand=True, fill="both")

# Elementy interfejsu dla zakładki 2
label_wavelength = ttk.Label(frame2, text="Długość fali (nm):")
label_dry_temperature = ttk.Label(frame2, text="Temperatura sucha (°C):")
label_wet_temperature = ttk.Label(frame2, text="Temperatura mokra (°C):")
label_pressure = ttk.Label(frame2, text="Ciśnienie (hPa):")
label_measured_length = ttk.Label(frame2, text="Pomierzona długość (m):")

entry_wavelength = ttk.Entry(frame2)
entry_dry_temperature = ttk.Entry(frame2)
entry_wet_temperature = ttk.Entry(frame2)
entry_pressure = ttk.Entry(frame2)
entry_measured_length = ttk.Entry(frame2)

calculate_button = ttk.Button(frame2, text="Oblicz", command=calculate_button_clicked)

label_result = ttk.Label(frame2, text="Wyniki będą wyświetlane tutaj.")

# Układ elementów interfejsu
label_wavelength.grid(row=0, column=0, padx=10, pady=5, sticky="e")
label_dry_temperature.grid(row=1, column=0, padx=10, pady=5, sticky="e")
label_wet_temperature.grid(row=2, column=0, padx=10, pady=5, sticky="e")
label_pressure.grid(row=3, column=0, padx=10, pady=5, sticky="e")
label_measured_length.grid(row=4, column=0, padx=10, pady=5, sticky="e")

entry_wavelength.grid(row=0, column=1, padx=10, pady=5)
entry_dry_temperature.grid(row=1, column=1, padx=10, pady=5)
entry_wet_temperature.grid(row=2, column=1, padx=10, pady=5)
entry_pressure.grid(row=3, column=1, padx=10, pady=5)
entry_measured_length.grid(row=4, column=1, padx=10, pady=5)

calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

label_result.grid(row=6, column=0, columnspan=2, pady=10)

# ------------------------------------------------------------------------------------------------------------
frame3 = ttk.Frame(notebook)
notebook.add(frame3, text='Trzecia zakładka')

# Set print options for NumPy array
np.set_printoptions(precision=8, suppress=True, linewidth=150)

r_Ziemi = 8 * 6378
r = 8 * r_Ziemi

# Define the range of distances from 1 km to 100 km with a step of 1 km
distances = np.arange(1, 101, 1)

# Initialize an empty list to store the results
differences = []

# Calculate the differences for each distance
for d in distances:
    # Convert distance to kilometers before applying the formula
    del_c = -1 * d**3 / (24 * r_Ziemi**2)
    del_c = del_c * 10**6
    differences.append(del_c)


# Convert the list to a NumPy array for easier handling
differences = np.array(differences)

# Create Matplotlib figure and axes
fig, axs = plt.subplots(1, 1, figsize=(8, 4), gridspec_kw={'hspace': 0.3})

# Plot the results
line, = axs.plot(distances, differences)
axs.set_xlabel('Distance (km)')
axs.set_ylabel('Difference between arc and chord (mm)')
axs.set_title('Difference between Arc and Chord vs. Distance')
axs.grid(True)

# Display the table
table = np.column_stack((distances, differences))
header = "Distance (km) | Difference (mm)"
table_str = f"{header}\n{'-' * len(header)}\n{table}"

# Set up the Tkinter window
#root = tk.Tk()
#root.title("Difference between Arc and Chord")

# Create Matplotlib canvas
canvas = FigureCanvasTkAgg(fig, master=frame3)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Add slider
slider_frame = ttk.Frame(frame3)
slider_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

slider_label = ttk.Label(slider_frame, text="Select Distance:")
slider_label.pack(side=tk.LEFT)

# Create a scale/slider
slider = ttk.Scale(slider_frame, from_=min(distances), to=max(distances), orient=tk.HORIZONTAL, length=200)
slider.pack(side=tk.LEFT)

# Callback function for slider
def update_plot(_):
    selected_distance = int(slider.get())
    selected_index = np.where(distances == selected_distance)[0][0]

    # Update the plot
    line.set_xdata(distances[:selected_index + 1])
    line.set_ydata(differences[:selected_index + 1])

    # Update the table
    tree.delete(*tree.get_children())
    for i in range(selected_index + 1):
        #tree.insert("", "end", values=(distances[i], differences[i]))
        formatted_difference = f'{differences[i]:.8f}'
        tree.insert("", "end", values=(distances[i], formatted_difference), tags=("formatted",))
    fig.canvas.draw_idle()

# Attach the callback function to the slider
slider.configure(command=update_plot)

# Create a frame for the table
frame = ttk.Frame(frame3)
frame.grid(row=0, column=2, rowspan=2, sticky="ns")

# Create a treeview for the table
tree = ttk.Treeview(frame, columns=(1, 2), show="headings", height="10")
tree.heading(1, text="Distance (km)")
tree.heading(2, text="Difference (mm)")


for i in range(len(distances)):
    formatted_difference = f'{differences[i]:.8f}'
    tree.insert("", "end", values=(distances[i], formatted_difference))

tree.pack(side=tk.LEFT, fill=tk.Y)

# Add scrollbar to the table
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)

root.mainloop()

