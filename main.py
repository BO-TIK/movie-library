import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("700x500")
        
        self.movies = self.load_movies()
        
        # Поля ввода
        tk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.genre_entry = tk.Entry(root, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(root, text="Год:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.year_entry = tk.Entry(root, width=30)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(root, text="Рейтинг (0-10):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.rating_entry = tk.Entry(root, width=30)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Кнопки
        tk.Button(root, text="Добавить фильм", command=self.add_movie).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Фильтры
        filter_frame = tk.LabelFrame(root, text="Фильтрация", padx=5, pady=5)
        filter_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew", padx=10)
        
        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=2)
        self.filter_genre = tk.Entry(filter_frame, width=15)
        self.filter_genre.grid(row=0, column=1, padx=2)
        
        tk.Label(filter_frame, text="Год:").grid(row=0, column=2, padx=2)
        self.filter_year = tk.Entry(filter_frame, width=6)
        self.filter_year.grid(row=0, column=3, padx=2)
        
        tk.Button(filter_frame, text="Фильтровать", command=self.filter_movies).grid(row=0, column=4, padx=5)
        tk.Button(filter_frame, text="Сбросить", command=self.reset_filter).grid(row=0, column=5, padx=5)
        
        # Таблица
        self.tree = ttk.Treeview(root, columns=("Название", "Жанр", "Год", "Рейтинг"), show="headings")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        self.tree.column("Название", width=200)
        self.tree.column("Жанр", width=150)
        self.tree.column("Год", width=80)
        self.tree.column("Рейтинг", width=80)
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Удаление
        tk.Button(root, text="Удалить выбранный", command=self.delete_movie).grid(row=7, column=0, columnspan=2, pady=5)
        
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
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()
        
        if not title or not genre or not year or not rating:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        try:
            year = int(year)
            rating = float(rating)
            if rating < 0 or rating > 10:
                raise ValueError
        except:
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

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
