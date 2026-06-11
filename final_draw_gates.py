#-----------------------------------------------------------------------------#
# Code Author          : Ahmed El.badawi
# Contact me           : Email: tech.wizardegypt@gmail.com
# Created On           : Monday - November 11, 2024 / 16:55:22 UTC+2
# Operating System     : Windows 11, Ubuntu Linux
# Programming Language : Python (Version 3.12.4)
# File Name            : final_draw_gates.py
# Version              : v2.0.0
# Code Title           : LogicFlow - Modern Logic Circuit Generator
#-----------------------------------------------------------------------------#

import os
import tempfile
import re
import customtkinter as ctk
from tkinter import messagebox, filedialog, Menu
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Select non-interactive backend
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="schemdraw")
from schemdraw.parsing import logicparse

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class OnboardingScreen(ctk.CTkToplevel):
    def __init__(self, master, on_close_callback):
        super().__init__(master)
        
        self.title("LogicFlow - Onboarding")
        
        window_width = 550
        window_height = 450
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.configure(fg_color="#F3F4F6")
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.on_close_callback = on_close_callback
        
        self.card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=16, border_width=1, border_color="#E5E7EB")
        self.card.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.title_label = ctk.CTkLabel(
            self.card, 
            text="⚡ Welcome to LogicFlow", 
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#111827"
        )
        self.title_label.pack(pady=(30, 10))
        
        instructions = (
            "How to use:\n\n"
            "• Enter your logic expression in the text box.\n"
            "• Use the keypad or your keyboard to type.\n\n"
            "⚠️ IMPORTANT ⚠️\n"
            "You must enclose your functions in parentheses!\n"
            "Even if you are writing a simple expression like 'a and b',\n"
            "you MUST add parentheses, otherwise the circuit won't appear!\n\n"
            "Example: (A and B) or C"
        )
        
        self.inst_label = ctk.CTkLabel(
            self.card,
            text=instructions,
            font=ctk.CTkFont(family="Segoe UI", size=16),
            text_color="#374151",
            justify="center"
        )
        self.inst_label.pack(pady=20, padx=20)
        
        self.start_btn = ctk.CTkButton(
            self.card,
            text="Got it!",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            command=self.on_close,
            height=45,
            width=200,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8"
        )
        self.start_btn.pack(pady=(10, 30))
        
        self.grab_set()

    def on_close(self):
        self.grab_release()
        self.destroy()
        self.on_close_callback()

class LogicFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LogicFlow")
        
        window_width = 800
        window_height = 650
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.configure(fg_color="#F3F4F6") # Light clean background

        self.temp_image_path = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # MAIN CARD
        self.main_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=16, border_width=1, border_color="#E5E7EB")
        self.main_card.grid(row=0, column=0, padx=40, pady=20, sticky="nsew")
        self.main_card.grid_columnconfigure(0, weight=1)
        self.main_card.grid_rowconfigure(3, weight=1) # preview expands

        # HEADER
        self.header_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=30, pady=(30, 20), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="⚡ LogicFlow", 
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color="#111827"
        )
        self.title_label.pack(side="left")

        # INPUT ROW
        self.input_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=30, pady=0, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1) # Entry expands
        
        self.entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Enter logic expression (e.g., A and B or C)", 
            font=ctk.CTkFont(family="Segoe UI", size=14), 
            height=42,
            corner_radius=8,
            border_width=1,
            border_color="#D1D5DB",
            fg_color="#F9FAFB"
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 15))
        self.entry.bind("<Return>", lambda event: self.generate_preview())
        self.entry.bind("<KeyRelease>", lambda event: self.generate_preview(silent=True))

        # Context menu for copy/paste
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Cut", command=lambda: self.entry.event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Copy", command=lambda: self.entry.event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Paste", command=self.custom_paste)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=lambda: self.entry.select_range(0, 'end'))

        self.entry.bind("<Button-3>", self.show_context_menu)
        self.entry.bind("<Control-v>", self.custom_paste)

        self.btn_generate = ctk.CTkButton(
            self.input_frame, 
            text="Generate", 
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), 
            height=42, 
            corner_radius=8,
            width=120,
            command=self.generate_preview,
            fg_color="#2563EB",
            hover_color="#1D4ED8"
        )
        self.btn_generate.grid(row=0, column=1)

        # KEYPAD AREA
        self.keypad_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.keypad_frame.grid(row=2, column=0, padx=30, pady=(15, 0), sticky="ew")
        
        for i in range(5):
            self.keypad_frame.grid_columnconfigure(i, weight=1)
            
        buttons = [
            ('A', 'var'), ('B', 'var'), ('C', 'var'), ('(', 'sym'), (')', 'sym'),
            ('D', 'var'), ('E', 'var'), ('F', 'var'), ('NOT', 'op'), ('XOR', 'op'),
            ('AND', 'op'), ('OR', 'op'), ('NAND', 'op'), ('NOR', 'op'), ('XNOR', 'op')
        ]
        
        row_idx = 0
        col_idx = 0
        for btn_text, btn_type in buttons:
            btn_color = "#F3F4F6" if btn_type == 'var' else ("#E0E7FF" if btn_type == 'op' else "#FDE68A")
            text_color = "#111827"
            hover_color = "#E5E7EB" if btn_type == 'var' else ("#C7D2FE" if btn_type == 'op' else "#FCD34D")
            
            btn = ctk.CTkButton(
                self.keypad_frame, text=btn_text,
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                fg_color=btn_color, text_color=text_color, hover_color=hover_color,
                height=35, corner_radius=6,
                command=lambda t=btn_text, ty=btn_type: self.insert_text(t, ty)
            )
            btn.grid(row=row_idx, column=col_idx, padx=4, pady=4, sticky="ew")
            
            col_idx += 1
            if col_idx > 4:
                col_idx = 0
                row_idx += 1
                
        # Action Buttons row
        action_frame = ctk.CTkFrame(self.keypad_frame, fg_color="transparent")
        action_frame.grid(row=row_idx, column=0, columnspan=5, sticky="ew", pady=(4,0))
        action_frame.grid_columnconfigure((0, 1), weight=1)
        
        btn_backspace = ctk.CTkButton(
            action_frame, text="⌫ Backspace", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color="#FEE2E2", text_color="#991B1B", hover_color="#FECACA", height=35, corner_radius=6,
            command=self.backspace_text
        )
        btn_backspace.grid(row=0, column=0, padx=(4, 2), sticky="ew")
        
        btn_clear = ctk.CTkButton(
            action_frame, text="C Clear", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color="#FEF2F2", text_color="#B91C1C", hover_color="#FEE2E2", height=35, corner_radius=6,
            command=self.clear_text
        )
        btn_clear.grid(row=0, column=1, padx=(2, 4), sticky="ew")

        # PREVIEW AREA
        self.preview_frame = ctk.CTkFrame(self.main_card, fg_color="#F9FAFB", corner_radius=12, border_width=1, border_color="#E5E7EB")
        self.preview_frame.grid(row=3, column=0, padx=30, pady=(20, 20), sticky="nsew")
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(0, weight=1)

        self.img_label = ctk.CTkLabel(
            self.preview_frame, 
            text="Your circuit preview will appear here.", 
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#9CA3AF"
        )
        self.img_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # FOOTER (SAVE BUTTON)
        self.footer_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.footer_frame.grid(row=4, column=0, padx=30, pady=(0, 30), sticky="ew")
        
        self.btn_save = ctk.CTkButton(
            self.footer_frame,
            text="Export PNG",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=40,
            width=120,
            corner_radius=8,
            command=self.save_image,
            state="disabled",
            fg_color="#10B981",
            hover_color="#059669"
        )
        self.btn_save.pack(side="right")

        self.credit_label = ctk.CTkLabel(
            self.footer_frame,
            text="Programming & Design by Sima for Digital Solutions - Ahmed Elbadawi | v2.0",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#6B7280"
        )
        self.credit_label.pack(side="left", padx=10)

        # Show onboarding screen
        self.withdraw()
        self.onboarding = OnboardingScreen(self, self.show_main_window)

    def show_main_window(self):
        self.deiconify()

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def custom_paste(self, event=None):
        try:
            text = self.clipboard_get()
            if '\n' in text or '\r' in text:
                text = text.replace('\n', ' ').replace('\r', '')
                self.clipboard_clear()
                self.clipboard_append(text)
            
            if event is None:
                self.entry.event_generate("<<Paste>>")
            
            self.after(50, lambda: self.generate_preview(silent=True))
        except Exception:
            pass

    def insert_text(self, text, btn_type):
        current_pos = self.entry.index("insert")
        if btn_type == 'op':
            insert_str = f" {text} "
        else:
            insert_str = text
            
        self.entry.insert(current_pos, insert_str)
        self.generate_preview(silent=True)
        
    def backspace_text(self):
        current_pos = self.entry.index("insert")
        if current_pos > 0:
            self.entry.delete(current_pos - 1, current_pos)
            self.generate_preview(silent=True)
            
    def clear_text(self):
        self.entry.delete(0, 'end')
        self.img_label.configure(image=None, text="Your circuit preview will appear here.")
        self.img_label.image = None
        self.btn_save.configure(state="disabled")

    def generate_preview(self, silent=False):
        expression = self.entry.get().strip()
        if not expression:
            if not silent:
                messagebox.showwarning("Warning", "Please enter a logic expression.")
            else:
                self.img_label.configure(image="", text="Your circuit preview will appear here.")
                self.img_label.image = None
                self.btn_save.configure(state="disabled")
            return

        # schemdraw logicparse requires lowercase logic operators
        for op in ['AND', 'OR', 'NOT', 'XOR', 'NAND', 'NOR', 'XNOR']:
            expression = re.sub(rf'\b{op}\b', op.lower(), expression)

        self.btn_save.configure(state="disabled")
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        self.temp_image_path = temp_file.name
        temp_file.close()

        try:
            with logicparse(expression, outlabel='$X$') as d:
                d.save(self.temp_image_path)
        except Exception as e:
            if not silent:
                messagebox.showerror("Error", f"Error parsing expression: {e}")
            self.temp_image_path = None
            return
        
        if not os.path.exists(self.temp_image_path):
            if not silent:
                messagebox.showerror("Error", "Failed to generate the circuit diagram.")
            self.temp_image_path = None
            return
        
        try:
            img = Image.open(self.temp_image_path)
            # max size bounded by card size
            max_size = (680, 400)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                bg.paste(img, (0,0), img.convert('RGBA'))
            else:
                bg.paste(img, (0,0))

            ctk_img = ctk.CTkImage(light_image=bg, dark_image=bg, size=bg.size)
            self.img_label.configure(image=ctk_img, text="")
            self.img_label.image = ctk_img
            self.btn_save.configure(state="normal")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying image: {e}")

    def save_image(self):
        if not self.temp_image_path or not os.path.exists(self.temp_image_path):
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
            title="Save Circuit Image"
        )

        if file_path:
            try:
                import shutil
                shutil.copy2(self.temp_image_path, file_path)
                messagebox.showinfo("Success", f"Diagram saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

if __name__ == "__main__":
    app = LogicFlowApp()
    app.mainloop()
