#-----------------------------------------------------------------------------#
# Code Author          : Ahmed El.badawi
# Contact me           : Email: tech.wizardegypt@gmail.com
# Created On           : Monday - November 11, 2024 / 16:55:22 UTC+2
# Operating System     : Windows 11, Ubuntu Linux
# Programming Language : Python (Version 3.12.4)
# File Name            : final_draw_gates.py
# Version              : v1.0.0
# Code Title           : ---ENTER CODE TITLE HERE---
#-----------------------------------------------------------------------------#
# Temporary terminal clear command, remove when done.
# pylint: disable=wrong-import-position
from os import system
from sys import platform
if platform == 'win32':
    system('cls')
else:
    system('clear')
# pylint: enable=wrong-import-position
#-----------------------------------------------------------------------------#


import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib
matplotlib.use('Agg')  # Select non-interactive backend
from schemdraw.parsing import logicparse
import os  # Import os to check file existence

def generate_and_display():
    # Get the logic expression from the entry widget
    expression = entry.get()
    
    # Try to parse and generate the logic circuit diagram
    try:
        with logicparse(expression, outlabel=f'$X$') as d:
            d.save("circuit_generated.png")
    except ValueError as e:
        messagebox.showerror("Error", f"Error parsing logic expression: {e}")
        return
    
    # Check if the image was generated successfully
    if not os.path.exists("circuit_generated.png"):
        messagebox.showerror("Error", "Failed to generate the circuit diagram.")
        return
    
    # Display the saved PNG file in the Tkinter window
    img = Image.open('circuit_generated.png')
    img = ImageTk.PhotoImage(img)
    
    img_label.config(image=img)
    img_label.image = img

    # Set the generated image as background
    background_image = Image.open("circuit_generated.png")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label.config(image=background_photo)
    background_label.image = background_photo

def toggle_theme():
    # Switch between light and dark mode
    if root.option_get('theme', 'light') == 'light':
        # Change to dark mode
        root.configure(bg='#333333')
        label_expression.config(fg='white', bg='#333333')
        entry_frame.config(bg='#444444')
        entry.config(bg='#555555', fg='white')
        button_generate.config(bg='#555555', fg='white')
        img_frame.config(bg='#444444')
        background_label.config(bg='#333333')
        root.option_add('*TButton*highlightColor', 'white')
        root.option_add('*TButton*highlightBackground', '#444444')
        root.option_add('theme', 'dark')
    else:
        # Change to light mode
        root.configure(bg='#f0f0f0')
        label_expression.config(fg='#333333', bg='#f0f0f0')
        entry_frame.config(bg='#ffffff')
        entry.config(bg='#f9f9f9', fg='#333333')
        button_generate.config(bg='#4CAF50', fg='white')
        img_frame.config(bg='#ffffff')
        background_label.config(bg='#f0f0f0')
        root.option_add('*TButton*highlightColor', 'black')
        root.option_add('*TButton*highlightBackground', '#f0f0f0')
        root.option_add('theme', 'light')

# Create the main Tkinter window
root = tk.Tk()
root.title("Logic Circuit Generator")

# Set a fixed size for the window
window_width = 700
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set initial theme to light mode
root.option_add('theme', 'light')

# Create and pack the widgets
label_expression = tk.Label(root, text="Enter Logic Expression:", font=("Helvetica", 14, "bold"), fg="#333333", bg="#f0f0f0")
label_expression.pack(pady=20)

entry_frame = tk.Frame(root, bd=2, relief="solid", bg="#ffffff")
entry_frame.pack(pady=10)
entry = tk.Entry(entry_frame, width=50, font=("Helvetica", 14), relief="flat", bg="#f9f9f9")
entry.pack(padx=10, pady=5)

button_generate = tk.Button(root, text="Generate and Display", command=generate_and_display, font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white", relief="flat", cursor="hand2")
button_generate.pack(pady=20)

# Add a button to toggle between dark mode and light mode
toggle_button = tk.Button(root, text="Toggle Theme", command=toggle_theme, font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white", relief="flat", cursor="hand2")
toggle_button.pack(pady=10)

img_frame = tk.Frame(root, relief="solid", bd=2, padx=5, pady=5, bg="#ffffff")
img_frame.pack(pady=20, fill="both", expand=True)
img_label = tk.Label(img_frame, bg="#ffffff")
img_label.pack(expand=True)

# Background label, but no image set initially
background_label = tk.Label(root)
background_label.place(relwidth=1, relheight=1)

# Put the widgets on top of the background
label_expression.lift()
entry_frame.lift()
button_generate.lift()
toggle_button.lift()
img_frame.lift()

# Start the Tkinter main loop
root.mainloop()
