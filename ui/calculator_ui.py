import tkinter as tk
from tkinter import ttk

from logic.calculator_logic import CalculatorLogic


class CalculatorUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CALC — Modern Calculator")
        self.root.geometry("900x620")
        self.root.minsize(700, 520)

        self.logic = CalculatorLogic()

        self.display_var = tk.StringVar(value="0")
        self.expression_var = tk.StringVar(value="")
        self.history_visible = False

        self.themes = {
            "Obsidian": {
                "bg": "#111315",
                "panel": "#191c1f",
                "button": "#24282c",
                "button_hover": "#30353a",
                "operator": "#30363b",
                "accent": "#d8a85f",
                "text": "#f5f5f5",
                "secondary": "#858b91",
                "border": "#292e33"
            },
            "Ocean": {
                "bg": "#08151c",
                "panel": "#0e2029",
                "button": "#17313d",
                "button_hover": "#214453",
                "operator": "#194052",
                "accent": "#48c6ef",
                "text": "#eefaff",
                "secondary": "#7da5b4",
                "border": "#1b3a47"
            },
            "Forest": {
                "bg": "#0d1712",
                "panel": "#14231a",
                "button": "#1d3024",
                "button_hover": "#294333",
                "operator": "#24402d",
                "accent": "#7bd88f",
                "text": "#f1fff3",
                "secondary": "#86a68d",
                "border": "#284532"
            },
            "Paper": {
                "bg": "#eee9df",
                "panel": "#f8f5ed",
                "button": "#e2ddd2",
                "button_hover": "#d6d0c3",
                "operator": "#d8d1c4",
                "accent": "#a56b35",
                "text": "#24221f",
                "secondary": "#81796f",
                "border": "#d4cec2"
            },
            "Midnight": {
                "bg": "#110f1b",
                "panel": "#1b1729",
                "button": "#29233c",
                "button_hover": "#382f50",
                "operator": "#342b4b",
                "accent": "#b58cff",
                "text": "#f7f2ff",
                "secondary": "#9b91ad",
                "border": "#332b46"
            }
        }

        self.current_theme = "Obsidian"
        self.apply_theme_colors()

        self.create_styles()
        self.create_main_layout()
        self.create_header()
        self.create_display()
        self.create_buttons()
        self.create_history()
        self.bind_keyboard()

    def apply_theme_colors(self):
        theme = self.themes[self.current_theme]

        self.bg = theme["bg"]
        self.panel = theme["panel"]
        self.button = theme["button"]
        self.button_hover = theme["button_hover"]
        self.operator = theme["operator"]
        self.accent = theme["accent"]
        self.text = theme["text"]
        self.secondary_text = theme["secondary"]
        self.border = theme["border"]

        self.root.configure(bg=self.bg)

    def create_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.update_styles()

    def update_styles(self):
        self.style.configure(
            "Calc.TButton",
            font=("Segoe UI", 15),
            foreground=self.text,
            background=self.button,
            borderwidth=0,
            padding=(10, 16),
            relief="flat"
        )

        self.style.map(
            "Calc.TButton",
            background=[
                ("active", self.button_hover),
                ("pressed", self.button_hover)
            ],
            foreground=[
                ("active", self.text)
            ]
        )

        self.style.configure(
            "Operator.TButton",
            font=("Segoe UI Semibold", 15),
            foreground=self.accent,
            background=self.operator,
            borderwidth=0,
            padding=(10, 16),
            relief="flat"
        )

        self.style.map(
            "Operator.TButton",
            background=[
                ("active", self.button_hover),
                ("pressed", self.button_hover)
            ]
        )

        self.style.configure(
            "Equals.TButton",
            font=("Segoe UI Semibold", 17),
            foreground=self.bg,
            background=self.accent,
            borderwidth=0,
            padding=(10, 16),
            relief="flat"
        )

        self.style.map(
            "Equals.TButton",
            background=[
                ("active", self.accent),
                ("pressed", self.accent)
            ]
        )

    def create_main_layout(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.container = tk.Frame(
            self.root,
            bg=self.bg
        )

        self.container.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=24,
            pady=20
        )

        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=1)

    def create_header(self):
        self.header = tk.Frame(
            self.container,
            bg=self.bg
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        self.header.columnconfigure(1, weight=1)

        self.title_label = tk.Label(
            self.header,
            text="CALC",
            font=("Segoe UI Semibold", 22),
            fg=self.text,
            bg=self.bg
        )

        self.title_label.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.subtitle_label = tk.Label(
            self.header,
            text="PRECISION • SIMPLICITY • CONTROL",
            font=("Segoe UI", 8),
            fg=self.secondary_text,
            bg=self.bg
        )

        self.subtitle_label.grid(
            row=1,
            column=0,
            sticky="w"
        )

        self.theme_var = tk.StringVar(
            value=self.current_theme
        )

        self.theme_menu = ttk.Combobox(
            self.header,
            textvariable=self.theme_var,
            values=list(self.themes.keys()),
            state="readonly",
            width=12
        )

        self.theme_menu.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=(10, 10)
        )

        self.theme_menu.bind(
            "<<ComboboxSelected>>",
            self.change_theme
        )

        self.history_button = tk.Button(
            self.header,
            text="HISTORY",
            command=self.toggle_history,
            font=("Segoe UI Semibold", 9),
            fg=self.secondary_text,
            bg=self.bg,
            activeforeground=self.accent,
            activebackground=self.bg,
            bd=0,
            cursor="hand2"
        )

        self.history_button.grid(
            row=0,
            column=3,
            rowspan=2,
            sticky="e"
        )

    def create_display(self):
        self.display_frame = tk.Frame(
            self.container,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        self.display_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.display_frame.columnconfigure(0, weight=1)
        self.display_frame.rowconfigure(1, weight=1)

        self.expression_label = tk.Label(
            self.display_frame,
            textvariable=self.expression_var,
            font=("Segoe UI", 13),
            fg=self.secondary_text,
            bg=self.panel,
            anchor="e"
        )

        self.expression_label.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(22, 0)
        )

        self.display_label = tk.Label(
            self.display_frame,
            textvariable=self.display_var,
            font=("Segoe UI Light", 48),
            fg=self.text,
            bg=self.panel,
            anchor="e"
        )

        self.display_label.grid(
            row=1,
            column=0,
            sticky="sew",
            padx=25,
            pady=(0, 20)
        )

    def create_buttons(self):
        self.button_frame = tk.Frame(
            self.container,
            bg=self.bg
        )

        self.button_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            pady=(14, 0)
        )

        for column in range(4):
            self.button_frame.columnconfigure(
                column,
                weight=1
            )

        for row in range(5):
            self.button_frame.rowconfigure(
                row,
                weight=1
            )

        buttons = [
            ("AC", 0, 0, self.clear, "Operator.TButton"),
            ("⌫", 0, 1, self.backspace, "Operator.TButton"),
            ("%", 0, 2, self.percentage, "Operator.TButton"),
            ("÷", 0, 3, lambda: self.operator("÷"), "Operator.TButton"),

            ("7", 1, 0, lambda: self.number("7"), "Calc.TButton"),
            ("8", 1, 1, lambda: self.number("8"), "Calc.TButton"),
            ("9", 1, 2, lambda: self.number("9"), "Calc.TButton"),
            ("×", 1, 3, lambda: self.operator("×"), "Operator.TButton"),

            ("4", 2, 0, lambda: self.number("4"), "Calc.TButton"),
            ("5", 2, 1, lambda: self.number("5"), "Calc.TButton"),
            ("6", 2, 2, lambda: self.number("6"), "Calc.TButton"),
            ("−", 2, 3, lambda: self.operator("-"), "Operator.TButton"),

            ("1", 3, 0, lambda: self.number("1"), "Calc.TButton"),
            ("2", 3, 1, lambda: self.number("2"), "Calc.TButton"),
            ("3", 3, 2, lambda: self.number("3"), "Calc.TButton"),
            ("+", 3, 3, lambda: self.operator("+"), "Operator.TButton"),

            ("±", 4, 0, self.toggle_sign, "Calc.TButton"),
            ("0", 4, 1, lambda: self.number("0"), "Calc.TButton"),
            (".", 4, 2, self.decimal, "Calc.TButton"),
            ("=", 4, 3, self.calculate, "Equals.TButton")
        ]

        for text, row, column, command, style in buttons:
            button = ttk.Button(
                self.button_frame,
                text=text,
                command=command,
                style=style
            )

            button.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=4,
                pady=4
            )

    def create_history(self):
        self.history_frame = tk.Frame(
            self.container,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        title = tk.Label(
            self.history_frame,
            text="CALCULATION HISTORY",
            font=("Segoe UI Semibold", 11),
            fg=self.text,
            bg=self.panel
        )

        title.pack(
            anchor="w",
            padx=18,
            pady=(18, 12)
        )

        self.history_list = tk.Listbox(
            self.history_frame,
            bg=self.panel,
            fg=self.secondary_text,
            selectbackground=self.button_hover,
            selectforeground=self.text,
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=0
        )

        self.history_list.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

    def change_theme(self, event=None):
        self.current_theme = self.theme_var.get()

        self.apply_theme_colors()
        self.update_styles()

        self.container.configure(bg=self.bg)
        self.header.configure(bg=self.bg)
        self.button_frame.configure(bg=self.bg)

        self.title_label.configure(
            bg=self.bg,
            fg=self.text
        )

        self.subtitle_label.configure(
            bg=self.bg,
            fg=self.secondary_text
        )

        self.history_button.configure(
            bg=self.bg,
            fg=self.secondary_text,
            activebackground=self.bg,
            activeforeground=self.accent
        )

        self.display_frame.configure(
            bg=self.panel,
            highlightbackground=self.border
        )

        self.expression_label.configure(
            bg=self.panel,
            fg=self.secondary_text
        )

        self.display_label.configure(
            bg=self.panel,
            fg=self.text
        )

        self.history_frame.configure(
            bg=self.panel,
            highlightbackground=self.border
        )

        for widget in self.history_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(
                    bg=self.panel,
                    fg=self.text
                )

        self.history_list.configure(
            bg=self.panel,
            fg=self.secondary_text,
            selectbackground=self.button_hover,
            selectforeground=self.text
        )

    def toggle_history(self):
        self.history_visible = not self.history_visible

        if self.history_visible:
            self.history_button.configure(
                fg=self.accent
            )

            self.history_frame.grid(
                row=1,
                column=1,
                rowspan=2,
                sticky="nsew",
                padx=(14, 0)
            )

            self.container.columnconfigure(
                1,
                weight=0
            )

            self.history_frame.configure(
                width=230
            )

        else:
            self.history_button.configure(
                fg=self.secondary_text
            )

            self.history_frame.grid_remove()

    def number(self, value):
        result = self.logic.input_number(value)
        self.update_display(result)

    def decimal(self):
        result = self.logic.input_decimal()
        self.update_display(result)

    def operator(self, operator):
        result = self.logic.set_operator(operator)

        if result != "Error":
            self.expression_var.set(
                f"{result} {operator}"
            )

        self.update_display(result)

    def calculate(self):
        previous = self.logic.previous
        operator = self.logic.operator
        current = self.logic.current

        result = self.logic.calculate()

        if result != "Error" and previous is not None and operator is not None:
            expression = f"{previous:g} {operator} {current} ="

            self.expression_var.set(expression)

            self.history_list.insert(
                0,
                f"{expression} {result}"
            )

        self.update_display(result)

    def clear(self):
        result = self.logic.clear()
        self.expression_var.set("")
        self.update_display(result)

    def backspace(self):
        result = self.logic.backspace()
        self.update_display(result)

    def toggle_sign(self):
        result = self.logic.toggle_sign()
        self.update_display(result)

    def percentage(self):
        result = self.logic.percentage()
        self.update_display(result)

    def update_display(self, value):
        self.display_var.set(value)

    def bind_keyboard(self):
        self.root.bind("<Key>", self.keyboard_input)
        self.root.bind(
            "<Return>",
            lambda event: self.calculate()
        )
        self.root.bind(
            "<BackSpace>",
            lambda event: self.backspace()
        )
        self.root.bind(
            "<Escape>",
            lambda event: self.clear()
        )

    def keyboard_input(self, event):
        key = event.char

        if key.isdigit():
            self.number(key)
        elif key == ".":
            self.decimal()
        elif key == "+":
            self.operator("+")
        elif key == "-":
            self.operator("-")
        elif key == "*":
            self.operator("×")
        elif key == "/":
            self.operator("÷")
        elif key == "%":
            self.percentage()

    def run(self):
        self.root.mainloop()