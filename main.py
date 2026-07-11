import tkinter as tk
from tkinter import ttk, messagebox
import json


class MovieLibrary:
    THEMES = [
        {
            "name": "Светлая",
            "bg": "#f5f7fb",
            "panel": "#ffffff",
            "panel_alt": "#eef3ff",
            "fg": "#1f2937",
            "muted": "#5f6c81",
            "entry_bg": "#ffffff",
            "border": "#cbd5e1",
            "accent": "#2563eb",
            "accent_soft": "#dbeafe",
            "button_fg": "#ffffff",
            "button_active": "#1d4ed8",
            "tree_bg": "#ffffff",
            "tree_fg": "#111827",
            "tree_heading": "#e5edff",
            "tree_heading_fg": "#1f2937",
            "tree_selected": "#93c5fd",
            "tree_selected_fg": "#0f172a",
        },
        {
            "name": "Тёмная",
            "bg": "#0f172a",
            "panel": "#111827",
            "panel_alt": "#172033",
            "fg": "#f8fafc",
            "muted": "#94a3b8",
            "entry_bg": "#111827",
            "border": "#334155",
            "accent": "#60a5fa",
            "accent_soft": "#1d4ed8",
            "button_fg": "#f8fafc",
            "button_active": "#3b82f6",
            "tree_bg": "#0f172a",
            "tree_fg": "#e2e8f0",
            "tree_heading": "#1e293b",
            "tree_heading_fg": "#f8fafc",
            "tree_selected": "#1d4ed8",
            "tree_selected_fg": "#f8fafc",
        },
        {
            "name": "Неоновая",
            "bg": "#050816",
            "panel": "#0b1120",
            "panel_alt": "#111a34",
            "fg": "#e2f6ff",
            "muted": "#7dd3fc",
            "entry_bg": "#08101f",
            "border": "#22d3ee",
            "accent": "#e879f9",
            "accent_soft": "#312e81",
            "button_fg": "#050816",
            "button_active": "#a855f7",
            "tree_bg": "#07111f",
            "tree_fg": "#d6f8ff",
            "tree_heading": "#0b1831",
            "tree_heading_fg": "#7dd3fc",
            "tree_selected": "#e879f9",
            "tree_selected_fg": "#050816",
        },
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("840x620")
        self.root.minsize(760, 560)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.current_theme = 0
        self.movies = self.load_movies()

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.main_frame = tk.Frame(root, padx=16, pady=16)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)

        self.header_frame = tk.Frame(self.main_frame, padx=18, pady=16)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = tk.Label(self.header_frame, text="Movie Library", font=("Segoe UI", 20, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.theme_label = tk.Label(self.header_frame, text="Тема: Светлая", font=("Segoe UI", 10, "bold"))
        self.theme_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.theme_button = tk.Button(self.header_frame, text="Сменить тему", command=self.cycle_theme)
        self.theme_button.grid(row=0, column=1, rowspan=2, sticky="e")

        self.form_frame = tk.LabelFrame(self.main_frame, text="Добавить фильм", padx=12, pady=12)
        self.form_frame.grid(row=1, column=0, sticky="ew", pady=(12, 10))
        self.form_frame.grid_columnconfigure(1, weight=1)

        self.field_labels = []
        self.entries = []

        field_definitions = [
            ("Название:", 0),
            ("Жанр:", 1),
            ("Год:", 2),
            ("Рейтинг (0-10):", 3),
        ]

        for text, row in field_definitions:
            label = tk.Label(self.form_frame, text=text, font=("Segoe UI", 10))
            label.grid(row=row, column=0, padx=(0, 10), pady=6, sticky="e")

            entry = tk.Entry(self.form_frame, width=34)
            entry.grid(row=row, column=1, padx=0, pady=6, sticky="ew")

            self.field_labels.append(label)
            self.entries.append(entry)

        self.title_entry, self.genre_entry, self.year_entry, self.rating_entry = self.entries

        self.add_button = tk.Button(self.form_frame, text="Добавить фильм", command=self.add_movie)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=(10, 2), sticky="ew")

        self.filter_frame = tk.LabelFrame(self.main_frame, text="Фильтрация", padx=12, pady=10)
        self.filter_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.filter_frame.grid_columnconfigure(1, weight=1)

        tk.Label(self.filter_frame, text="Жанр:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=(0, 6), pady=4)
        self.filter_genre = tk.Entry(self.filter_frame, width=20)
        self.filter_genre.grid(row=0, column=1, padx=(0, 10), pady=4, sticky="ew")

        tk.Label(self.filter_frame, text="Год:", font=("Segoe UI", 10)).grid(row=0, column=2, padx=(0, 6), pady=4)
        self.filter_year = tk.Entry(self.filter_frame, width=8)
        self.filter_year.grid(row=0, column=3, padx=(0, 10), pady=4)

        self.filter_button = tk.Button(self.filter_frame, text="Фильтровать", command=self.filter_movies)
        self.filter_button.grid(row=0, column=4, padx=(0, 6), pady=4)

        self.reset_button = tk.Button(self.filter_frame, text="Сбросить", command=self.reset_filter)
        self.reset_button.grid(row=0, column=5, pady=4)

        self.tree_container = tk.Frame(self.main_frame)
        self.tree_container.grid(row=3, column=0, sticky="nsew")
        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            self.tree_container,
            columns=("Название", "Жанр", "Год", "Рейтинг"),
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        self.tree.column("Название", width=250, anchor="w")
        self.tree.column("Жанр", width=170, anchor="w")
        self.tree.column("Год", width=100, anchor="center")
        self.tree.column("Рейтинг", width=100, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.delete_button = tk.Button(self.main_frame, text="Удалить выбранный", command=self.delete_movie)
        self.delete_button.grid(row=4, column=0, pady=(10, 0), sticky="ew")

        self.theme_buttons = [self.add_button, self.filter_button, self.reset_button, self.delete_button]

        self.apply_theme()
        self.update_table()

    def load_movies(self):
        try:
            with open("movies.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_movies(self):
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_text = self.year_entry.get().strip()
        rating_text = self.rating_entry.get().strip()

        if not title or not genre or not year_text or not rating_text:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        try:
            year = int(year_text)
            rating = float(rating_text)
            if rating < 0 or rating > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом, рейтинг от 0 до 10")
            return

        self.movies.append({"title": title, "genre": genre, "year": year, "rating": rating})
        self.save_movies()
        self.update_table()
        self.clear_entries()

    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления")
            return

        for item in selected:
            values = self.tree.item(item, "values")
            for i, movie in enumerate(self.movies):
                if movie["title"] == values[0] and movie["year"] == int(values[2]):
                    self.movies.pop(i)
                    break

        self.save_movies()
        self.update_table()

    def filter_movies(self):
        genre_filter = self.filter_genre.get().strip().lower()
        year_filter = self.filter_year.get().strip()
        self.tree.delete(*self.tree.get_children())
        for movie in self.movies:
            if genre_filter and genre_filter not in movie["genre"].lower():
                continue
            if year_filter and str(movie["year"]) != year_filter:
                continue
            self.tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def reset_filter(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.update_table()

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        for movie in self.movies:
            self.tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def cycle_theme(self):
        self.current_theme = (self.current_theme + 1) % len(self.THEMES)
        self.apply_theme()

    def apply_theme(self):
        theme = self.THEMES[self.current_theme]

        self.root.configure(bg=theme["bg"])
        self.main_frame.configure(bg=theme["bg"])
        self.header_frame.configure(bg=theme["panel"])
        self.form_frame.configure(bg=theme["panel"], fg=theme["fg"])
        self.filter_frame.configure(bg=theme["panel"], fg=theme["fg"])
        self.tree_container.configure(bg=theme["panel"])

        self.title_label.configure(bg=theme["panel"], fg=theme["fg"])
        self.theme_label.configure(bg=theme["panel"], fg=theme["muted"], text=f"Тема: {theme['name']}")

        for label in self.field_labels:
            label.configure(bg=theme["panel"], fg=theme["fg"])

        for entry in self.entries:
            entry.configure(
                bg=theme["entry_bg"],
                fg=theme["fg"],
                insertbackground=theme["fg"],
                highlightbackground=theme["border"],
                highlightcolor=theme["accent"],
                highlightthickness=1,
            )

        self.filter_genre.configure(
            bg=theme["entry_bg"],
            fg=theme["fg"],
            insertbackground=theme["fg"],
            highlightbackground=theme["border"],
            highlightcolor=theme["accent"],
            highlightthickness=1,
        )
        self.filter_year.configure(
            bg=theme["entry_bg"],
            fg=theme["fg"],
            insertbackground=theme["fg"],
            highlightbackground=theme["border"],
            highlightcolor=theme["accent"],
            highlightthickness=1,
        )

        for button in self.theme_buttons:
            button.configure(
                bg=theme["accent"],
                fg=theme["button_fg"],
                activebackground=theme["button_active"],
                activeforeground=theme["button_fg"],
                relief="flat",
                bd=0,
                padx=12,
                pady=6,
                highlightthickness=0,
            )

        self.theme_button.configure(
            bg=theme["panel_alt"],
            fg=theme["fg"],
            activebackground=theme["accent_soft"],
            activeforeground=theme["fg"],
            relief="flat",
            bd=0,
            padx=10,
            pady=6,
            highlightthickness=0,
        )

        self.style.configure("Treeview", background=theme["tree_bg"], fieldbackground=theme["tree_bg"], foreground=theme["tree_fg"], rowheight=28)
        self.style.map("Treeview", background=[("selected", theme["tree_selected"])], foreground=[("selected", theme["tree_selected_fg"])])
        self.style.configure("Treeview.Heading", background=theme["tree_heading"], foreground=theme["tree_heading_fg"], relief="flat")
        self.style.map("Treeview.Heading", background=[("active", theme["accent_soft"])])

        self.tree.configure(style="Treeview")


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
