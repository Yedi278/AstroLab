import tkinter as tk
from tkinter import messagebox, Listbox, simpledialog
from angles import angleStrToFloat
import numpy as np


def add_item(listbox):
    """Add an item to the list."""
    new_item = simpledialog.askstring("Add Item", "Enter the new item:")
    
    for i in new_item:
        if i.isdigit() or i in ['°', '\'', '\"']:
            continue
        else:
            messagebox.showerror('Error', 'Invalid angle format')
            return
    if new_item:
        listbox.insert(tk.END, new_item)

def remove_item(listbox):
    """Remove the selected item from the list."""
    selected_items = listbox.curselection()
    for index in selected_items[::-1]:  # Reverse to avoid index shifting
        listbox.delete(index)

def edit_item(listbox):
    """Edit the selected item."""
    selected_items = listbox.curselection()
    if selected_items:
        index = selected_items[0]
        current_value = listbox.get(index)
        new_value = simpledialog.askstring("Edit Item", "Modify the item:", initialvalue=current_value)
        if new_value:
            listbox.delete(index)
            listbox.insert(index, new_value)

def save_list(listbox):
    """Save the list to a file."""
    items = listbox.get(0, tk.END)
    with open('tmp/angles.txt', 'w', encoding='UTF-8') as f:
        f.write("#    DONT\'T MODIFY THE COMMENT SECTION \n#   This file contains the angles for the inner circle\n#   modify by putting angles in DD°MM\'SS\" format\n#   put only one angle per row and no commas or other symbol\n#\n")
        for item in items:
            f.write(f"{item}\n")


def anglesManager(class_obj:object, master:tk.Tk):

    window = tk.Toplevel(master=master)
    window.title('Angles Manager')
    window.geometry('400x400')
    # window.bind("quit", lambda:class_obj.refresh())
    angles = []
    try:
        with open('tmp/angles.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:

                if i.strip() == '':
                    continue
                if i.strip()[0] == '#':
                    continue
                angles.append(i.strip())
            
            angles = np.array(angles)
    except Exception as e:
        messagebox.showerror('Error', f'Error loading angles: {e}')
        return
    
    list = Listbox(window, selectmode='multiple', width=50, height=20)
    list.pack(pady=10)

    for i in angles:
        list.insert(tk.END, i)
    
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    add_btn = tk.Button(btn_frame, text="Add Item", command=lambda:add_item(list))
    add_btn.grid(row=0, column=0, padx=5)

    remove_btn = tk.Button(btn_frame, text="Remove Item", command=lambda:remove_item(list))
    remove_btn.grid(row=0, column=1, padx=5)

    edit_btn = tk.Button(btn_frame, text="Edit Item", command=lambda:edit_item(list))
    edit_btn.grid(row=0, column=2, padx=5)

    save_btn = tk.Button(btn_frame, text="Save List", command=lambda:save_list(list))
    save_btn.grid(row=0, column=3, padx=5)


if __name__ == '__main__':

    import os 
    import python.main as main

    os.chdir(os.path.dirname(__file__))
    
    astro = main.AstrGraph()
    astro.run()
    anglesManager(astro, astro._window)