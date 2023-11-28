import tkinter as tk 
from tkinter import ttk
import pandas as pd

coordinates =[]


def add_coordinates():
    x = x_entry.get()
    y = y_entry.get()
    coordinates.append((x,y))

    x_entry.delete(0,tk.END)
    y_entry.delete(0,tk.END)
    status_label.config(text=f"Coordinates added: {len(coordinates)}")

    if len(coordinates) >= 10:
        add_button.config(state=tk.DISABLED)


def save_to_excel():
    df = pd.DataFrame(coordinates,columns=['X Coordinates', 'Y Coordinates'])
    df.to_excel('coordinates.xlsx', index = False)

    coordinates.clear()
    status_label.config(text="Coordinates saved to excel")
    add_button.config(state=tk.NORMAL)




#Main window 
root = tk.Tk()
root.title("IoT Project")

#Label 
label = ttk.Label(root,text="Hello?")
label.pack()

#Text entry field
entry = ttk.Entry(root)
entry.pack()

#Buton either predetermined coordiantes or manually 
button = ttk.Button(root, text="Click Me!")
button.pack()

#X coordinates entry 
ttk.Label(root,text="X Coordinates:").pack()
x_entry=ttk.Entry(root)
x_entry.pack()

#Y coordinates
ttk.Label(root, text="Y Coordiantes:").pack()
y_entry = ttk.Entry(root)
y_entry.pack()

#Save button
save_button = ttk.Button(root, text="Save as an Excel", command=save_to_excel)
save_button.pack()

#start main 
root.mainloop()