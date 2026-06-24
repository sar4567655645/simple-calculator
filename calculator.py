import customtkinter as ctk
import math

# Configure appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class AdvancedCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Pro Calculator")
        self.geometry("380x640")
        self.resizable(False, False)
        
        # Variables
        self.expression = ""
        
        # Font settings
        self.display_font = ctk.CTkFont(family="Segoe UI", size=48, weight="bold")
        self.btn_font = ctk.CTkFont(family="Segoe UI", size=26, weight="bold")
        
        # Increased font size for top buttons to make them clearer
        self.adv_btn_font = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        
        # Display Screen
        self.display_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.display_frame.pack(pady=(20, 10), padx=20, fill="x")
        
        self.display_label = ctk.CTkLabel(
            self.display_frame, 
            text="0", 
            font=self.display_font, 
            anchor="e",
            text_color="white",
            justify="right"
        )
        self.display_label.pack(fill="x")
        
        # Keyboard bindings
        self.bind('<Key>', self.on_key_press)
        
        # Buttons Frame
        self.btns_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btns_frame.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Grid layout config
        for i in range(4):
            self.btns_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.btns_frame.grid_rowconfigure(i, weight=1)
            
        self.create_ui()

    def create_ui(self):
        # Colors matching a very premium dark theme
        op_color = "#FF9F0A"  # Orange
        op_hover = "#FFB340"
        
        num_color = "#333333" # Dark Gray
        num_hover = "#4C4C4C"
        
        func_color = "#A5A5A5" # Light Gray
        func_hover = "#D4D4D2"
        func_text = "#000000"
        
        # Lighter Gray for advanced buttons to make them much clearer
        adv_color = "#4D4D4D" 
        adv_hover = "#666666"

        # Helper to create buttons
        def btn(text, r, c, command, color, hover, text_col="white", font=None, colspan=1):
            f = font if font else self.btn_font
            b = ctk.CTkButton(
                self.btns_frame, 
                text=text, 
                font=f, 
                fg_color=color, 
                hover_color=hover, 
                text_color=text_col,
                command=command,
                corner_radius=25,  # Slightly less rounded for a clean modern look
                height=65
            )
            b.grid(row=r, column=c, columnspan=colspan, padx=5, pady=5, sticky="nsew")
            return b

        # Row 0 (Advanced functions)
        btn("sin", 0, 0, lambda: self.add_to_expr("sin("), adv_color, adv_hover, font=self.adv_btn_font)
        btn("cos", 0, 1, lambda: self.add_to_expr("cos("), adv_color, adv_hover, font=self.adv_btn_font)
        btn("tan", 0, 2, lambda: self.add_to_expr("tan("), adv_color, adv_hover, font=self.adv_btn_font)
        btn("log", 0, 3, lambda: self.add_to_expr("log("), adv_color, adv_hover, font=self.adv_btn_font)

        # Row 1
        btn("√", 1, 0, lambda: self.add_to_expr("sqrt("), adv_color, adv_hover, font=self.btn_font)
        btn("(", 1, 1, lambda: self.add_to_expr("("), adv_color, adv_hover, font=self.adv_btn_font)
        btn(")", 1, 2, lambda: self.add_to_expr(")"), adv_color, adv_hover, font=self.adv_btn_font)
        btn("^", 1, 3, lambda: self.add_to_expr("^"), adv_color, adv_hover, font=self.adv_btn_font)

        # Row 2 (Standard Top row)
        btn("AC", 2, 0, self.clear_expr, func_color, func_hover, text_col=func_text)
        btn("⌫", 2, 1, self.backspace_expr, func_color, func_hover, text_col=func_text)
        btn("π", 2, 2, lambda: self.add_to_expr("π"), func_color, func_hover, text_col=func_text)
        btn("÷", 2, 3, lambda: self.add_to_expr("/"), op_color, op_hover)

        # Row 3
        btn("7", 3, 0, lambda: self.add_to_expr("7"), num_color, num_hover)
        btn("8", 3, 1, lambda: self.add_to_expr("8"), num_color, num_hover)
        btn("9", 3, 2, lambda: self.add_to_expr("9"), num_color, num_hover)
        btn("×", 3, 3, lambda: self.add_to_expr("*"), op_color, op_hover)

        # Row 4
        btn("4", 4, 0, lambda: self.add_to_expr("4"), num_color, num_hover)
        btn("5", 4, 1, lambda: self.add_to_expr("5"), num_color, num_hover)
        btn("6", 4, 2, lambda: self.add_to_expr("6"), num_color, num_hover)
        btn("-", 4, 3, lambda: self.add_to_expr("-"), op_color, op_hover)

        # Row 5
        btn("1", 5, 0, lambda: self.add_to_expr("1"), num_color, num_hover)
        btn("2", 5, 1, lambda: self.add_to_expr("2"), num_color, num_hover)
        btn("3", 5, 2, lambda: self.add_to_expr("3"), num_color, num_hover)
        btn("+", 5, 3, lambda: self.add_to_expr("+"), op_color, op_hover)

        # Row 6
        btn("0", 6, 0, lambda: self.add_to_expr("0"), num_color, num_hover, colspan=2)
        btn(".", 6, 2, lambda: self.add_to_expr("."), num_color, num_hover)
        btn("=", 6, 3, self.evaluate_expr, op_color, op_hover)

    def update_display(self, text):
        # Truncate if too long to fit nicely
        display_text = text if text else "0"
        if len(display_text) > 12:
            self.display_label.configure(font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"))
        else:
            self.display_label.configure(font=self.display_font)
            
        self.display_label.configure(text=display_text)

    def add_to_expr(self, val):
        if self.expression == "Error":
            self.expression = ""
        self.expression += str(val)
        self.update_display(self.expression)

    def clear_expr(self):
        self.expression = ""
        self.update_display("0")

    def backspace_expr(self):
        if self.expression == "Error":
            self.expression = ""
        self.expression = self.expression[:-1]
        self.update_display(self.expression)

    def evaluate_expr(self):
        try:
            if not self.expression:
                return
            
            calc_expr = self.expression.replace('^', '**').replace('π', str(math.pi)).replace('e', str(math.e))
            allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
            
            result = str(eval(calc_expr, {"__builtins__": None}, allowed_names))
            
            # Format nicely
            if '.' in result:
                result = str(round(float(result), 8)).rstrip('0').rstrip('.')
            
            self.expression = result
            self.update_display(self.expression)
        except Exception:
            self.expression = "Error"
            self.update_display("Error")

    def on_key_press(self, event):
        key = event.char
        if key in '0123456789+-*/.()':
            self.add_to_expr(key)
        elif key == '\r' or event.keysym == 'Return':
            self.evaluate_expr()
        elif event.keysym == 'BackSpace':
            self.backspace_expr()
        elif event.keysym == 'Escape':
            self.clear_expr()


if __name__ == "__main__":
    app = AdvancedCalculator()
    app.mainloop()
