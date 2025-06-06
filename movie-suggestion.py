import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

class MovieSuggestionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Suggestion Machine")
        self.root.geometry("800x600")
        
        # Initialize movie database
        self.movie_database = self.load_movie_database()
        
        # Theme variables
        self.dark_mode = False
        self.theme_colors = {
            "light": {
                "bg": "#f0f0f0",
                "fg": "#333333",
                "button_bg": "#e0e0e0",
                "button_fg": "#000000",
                "highlight": "#4CAF50"
            },
            "dark": {
                "bg": "#2d2d2d",
                "fg": "#ffffff",
                "button_bg": "#3d3d3d",
                "button_fg": "#ffffff",
                "highlight": "#4CAF50"
            }
        }
        
        # Fullscreen state
        self.fullscreen = False
        
        # Create UI
        self.create_widgets()
        self.apply_theme()
        
        # Bind keyboard shortcuts
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
    
    def load_movie_database(self):
        """Load movie database from JSON file or create a sample one if not found"""
        if os.path.exists("movies.json"):
            with open("movies.json", "r") as f:
                return json.load(f)
        else:
            # Sample movie database
            sample_db = {
                "genres": ["Action", "Comedy", "Drama", "Sci-Fi", "Horror", "Romance"],
                "movies": [
                    {
                        "title": "The Shawshank Redemption",
                        "genre": "Drama",
                        "year": 1994,
                        "cast": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"],
                        "director": "Frank Darabont"
                    },
                    {
                        "title": "The Godfather",
                        "genre": "Drama",
                        "year": 1972,
                        "cast": ["Marlon Brando", "Al Pacino", "James Caan"],
                        "director": "Francis Ford Coppola"
                    },
                    {
                        "title": "The Dark Knight",
                        "genre": "Action",
                        "year": 2008,
                        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
                        "director": "Christopher Nolan"
                    },
                    {
                        "title": "Pulp Fiction",
                        "genre": "Crime",
                        "year": 1994,
                        "cast": ["John Travolta", "Uma Thurman", "Samuel L. Jackson"],
                        "director": "Quentin Tarantino"
                    }
                ]
            }
            with open("movies.json", "w") as f:
                json.dump(sample_db, f, indent=4)
            return sample_db
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create frames for each tab
        self.suggest_frame = ttk.Frame(self.notebook)
        self.search_frame = ttk.Frame(self.notebook)
        self.cast_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.suggest_frame, text="Suggest Movies")
        self.notebook.add(self.search_frame, text="Search Movies")
        self.notebook.add(self.cast_frame, text="Cast & Crew")
        
        # Suggest Movies Tab
        self.create_suggest_tab()
        
        # Search Movies Tab
        self.create_search_tab()
        
        # Cast & Crew Tab
        self.create_cast_tab()
        
        # Theme toggle button
        self.theme_button = ttk.Button(
            self.root, 
            text="Toggle Dark Mode", 
            command=self.toggle_theme
        )
        self.theme_button.pack(side=tk.BOTTOM, pady=10)
    
    def create_suggest_tab(self):
        """Create widgets for the Suggest Movies tab"""
        # Genre selection
        ttk.Label(self.suggest_frame, text="Select Genre:").pack(pady=5)
        
        self.genre_var = tk.StringVar()
        self.genre_combobox = ttk.Combobox(
            self.suggest_frame, 
            textvariable=self.genre_var,
            values=self.movie_database["genres"],
            state="readonly"
        )
        self.genre_combobox.pack(pady=5)
        self.genre_combobox.current(0)
        
        # Suggest button
        ttk.Button(
            self.suggest_frame, 
            text="Suggest Movies", 
            command=self.suggest_movies
        ).pack(pady=10)
        
        # Results frame
        self.suggest_results_frame = ttk.Frame(self.suggest_frame)
        self.suggest_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Results text
        self.suggest_results = tk.Text(
            self.suggest_results_frame,
            wrap=tk.WORD,
            height=10,
            state=tk.DISABLED
        )
        self.suggest_results.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.suggest_results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.suggest_results.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.suggest_results.yview)
    
    def create_search_tab(self):
        """Create widgets for the Search Movies tab"""
        # Search entry
        ttk.Label(self.search_frame, text="Search Movie:").pack(pady=5)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            self.search_frame, 
            textvariable=self.search_var
        )
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<Return>", lambda e: self.search_movies())
        
        # Search button
        ttk.Button(
            self.search_frame, 
            text="Search", 
            command=self.search_movies
        ).pack(pady=10)
        
        # Results frame
        self.search_results_frame = ttk.Frame(self.search_frame)
        self.search_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for results
        self.search_results = ttk.Treeview(
            self.search_results_frame,
            columns=("title", "genre", "year"),
            show="headings"
        )
        self.search_results.heading("title", text="Title")
        self.search_results.heading("genre", text="Genre")
        self.search_results.heading("year", text="Year")
        self.search_results.column("title", width=300)
        self.search_results.column("genre", width=150)
        self.search_results.column("year", width=100)
        self.search_results.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.search_results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.search_results.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.search_results.yview)
    
    def create_cast_tab(self):
        """Create widgets for the Cast & Crew tab"""
        # Movie selection
        ttk.Label(self.cast_frame, text="Select Movie:").pack(pady=5)
        
        self.cast_var = tk.StringVar()
        self.cast_combobox = ttk.Combobox(
            self.cast_frame, 
            textvariable=self.cast_var,
            values=[movie["title"] for movie in self.movie_database["movies"]],
            state="readonly"
        )
        self.cast_combobox.pack(pady=5)
        self.cast_combobox.current(0)
        
        # Get info button
        ttk.Button(
            self.cast_frame, 
            text="Get Cast & Crew", 
            command=self.get_cast_info
        ).pack(pady=10)
        
        # Results frame
        self.cast_results_frame = ttk.Frame(self.cast_frame)
        self.cast_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Results text
        self.cast_results = tk.Text(
            self.cast_results_frame,
            wrap=tk.WORD,
            height=10,
            state=tk.DISABLED
        )
        self.cast_results.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.cast_results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cast_results.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.cast_results.yview)
    
    def suggest_movies(self):
        """Suggest movies based on selected genre"""
        genre = self.genre_var.get()
        if not genre:
            messagebox.showerror("Error", "Please select a genre")
            return
        
        movies_in_genre = [
            movie for movie in self.movie_database["movies"] 
            if movie["genre"].lower() == genre.lower()
        ]
        
        if not movies_in_genre:
            self.update_suggest_results(f"No movies found in the {genre} genre.")
            return
        
        # Select 3 random movies
        suggested_movies = random.sample(movies_in_genre, min(3, len(movies_in_genre)))
        
        result_text = f"Suggested {genre} movies:\n\n"
        for i, movie in enumerate(suggested_movies, 1):
            result_text += f"{i}. {movie['title']} ({movie['year']})\n"
        
        self.update_suggest_results(result_text)
    
    def update_suggest_results(self, text):
        """Update the suggest results text widget"""
        self.suggest_results.config(state=tk.NORMAL)
        self.suggest_results.delete(1.0, tk.END)
        self.suggest_results.insert(tk.END, text)
        self.suggest_results.config(state=tk.DISABLED)
    
    def search_movies(self):
        """Search for movies by name"""
        query = self.search_var.get().strip().lower()
        if not query:
            messagebox.showerror("Error", "Please enter a search term")
            return
        
        # Clear previous results
        for item in self.search_results.get_children():
            self.search_results.delete(item)
        
        # Find matching movies
        found_movies = [
            movie for movie in self.movie_database["movies"]
            if query in movie["title"].lower()
        ]
        
        if not found_movies:
            messagebox.showinfo("No Results", "No movies found matching your search.")
            return
        
        # Add results to treeview
        for movie in found_movies:
            self.search_results.insert(
                "", tk.END, 
                values=(movie["title"], movie["genre"], movie["year"])
            )
    
    def get_cast_info(self):
        """Get cast and crew information for selected movie"""
        title = self.cast_var.get()
        if not title:
            messagebox.showerror("Error", "Please select a movie")
            return
        
        movie = next(
            (m for m in self.movie_database["movies"] if m["title"] == title),
            None
        )
        
        if not movie:
            self.update_cast_results(f"Could not find information for {title}")
            return
        
        result_text = f"Movie: {movie['title']} ({movie['year']})\n"
        result_text += f"Genre: {movie['genre']}\n"
        result_text += f"Director: {movie['director']}\n\n"
        result_text += "Cast:\n"
        result_text += "\n".join(f"• {actor}" for actor in movie["cast"])
        
        self.update_cast_results(result_text)
    
    def update_cast_results(self, text):
        """Update the cast results text widget"""
        self.cast_results.config(state=tk.NORMAL)
        self.cast_results.delete(1.0, tk.END)
        self.cast_results.insert(tk.END, text)
        self.cast_results.config(state=tk.DISABLED)
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme colors"""
        theme = "dark" if self.dark_mode else "light"
        colors = self.theme_colors[theme]
        
        # Main window
        self.root.config(bg=colors["bg"])
        
        # Update all widgets
        self.update_widget_colors(self.root, colors)
        
        # Special cases for text widgets
        self.suggest_results.config(
            bg=colors["bg"], 
            fg=colors["fg"],
            insertbackground=colors["fg"]
        )
        self.cast_results.config(
            bg=colors["bg"], 
            fg=colors["fg"],
            insertbackground=colors["fg"]
        )
        
        # Configure Treeview style
        style = ttk.Style()
        style.theme_use("default")  # Changed from "clam" to "default" for better compatibility
        
        # Configure Treeview colors
        style.configure(
            "Treeview",
            background=colors["bg"],
            foreground=colors["fg"],
            fieldbackground=colors["bg"]
        )
        style.configure(
            "Treeview.Heading",
            background=colors["button_bg"],
            foreground=colors["button_fg"]
        )
        style.map(
            "Treeview",
            background=[('selected', colors["highlight"])],
            foreground=[('selected', colors["fg"])]
        )
    
    def update_widget_colors(self, widget, colors):
        """Recursively update widget colors"""
        try:
            widget.config(
                bg=colors["bg"],
                fg=colors["fg"],
                highlightbackground=colors["bg"],
                highlightcolor=colors["highlight"]
            )
        except tk.TclError:
            pass
        
        try:
            widget.config(
                selectbackground=colors["highlight"],
                selectforeground=colors["fg"]
            )
        except tk.TclError:
            pass
        
        for child in widget.winfo_children():
            self.update_widget_colors(child, colors)
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        return "break"
    
    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        if self.fullscreen:
            self.fullscreen = False
            self.root.attributes("-fullscreen", False)
            return "break"

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieSuggestionApp(root)
    root.mainloop()
