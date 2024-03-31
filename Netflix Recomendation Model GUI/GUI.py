import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity


def open_filtering_system():
    root.withdraw()
    filtering_page.deiconify()


def open_recommendation_model():
    root.withdraw()
    recommendation_page.deiconify()

def filter_data():
    # Retrieve user inputs
    cast = cast_entry.get().split(",") if cast_entry.get() else []
    type_ = type_entry.get().lower()
    release_year = release_year_entry.get()
    age_certification = age_certification_entry.get()
    genre = genre_entry.get().split(",") if genre_entry.get() else []
    imdb_score = imdb_score_entry.get()
    tmdb_score = tmdb_score_entry.get()
    min_seasons = min_seasons_entry.get()
    max_seasons = max_seasons_entry.get()
    production_country = production_country_entry.get()

    filtered_df = df
    if cast:
        filtered_df = filtered_df[filtered_df['cast'].str.lower().str.contains('|'.join(cast), na=False, case=False)]
    if type_:
        filtered_df = filtered_df[filtered_df['type'].str.lower() == type_]
    if release_year:
        filtered_df = filtered_df[filtered_df['release_year'] >= int(release_year)]
    if age_certification:
        filtered_df = filtered_df[filtered_df['age_certification'] == age_certification]
    if genre:
        genre_filters = '|'.join(genre)
        filtered_df = filtered_df[filtered_df['genres'].str.lower().str.contains(genre_filters, na=False)]
    if imdb_score:
        filtered_df = filtered_df[filtered_df['imdb_score'] >= float(imdb_score)]
    if tmdb_score:
        filtered_df = filtered_df[filtered_df['tmdb_score'] >= float(tmdb_score)]
    if min_seasons:
        filtered_df = filtered_df[filtered_df['seasons'] >= int(min_seasons)]
    if max_seasons:
        filtered_df = filtered_df[filtered_df['seasons'] <= int(max_seasons)]
    if production_country:
        filtered_df = filtered_df[filtered_df['production_countries'].str.contains(production_country, na=False)]

    result_text.delete(1.0, tk.END)
    if not filtered_df.empty:
        result_text.insert(tk.END, "\n".join(filtered_df['title']))
    else:
        result_text.insert(tk.END, "No matches found")

def recommend_similar_shows(target_title):
    df = pd.read_csv(r"C:\Users\carlo\Downloads\database.csv")

    df.columns = df.columns.astype(str)

    label_encoder = LabelEncoder()
    df['genre_index'] = label_encoder.fit_transform(df['genres'])

    column_transformer = ColumnTransformer(
        [('encoder', OneHotEncoder(), ['genre_index']),],
        remainder='passthrough'
    )
    df_encoded = pd.DataFrame(column_transformer.fit_transform(df[['genre_index']]).toarray())
    df = pd.concat([df, df_encoded], axis=1)

    features = ['imdb_score', 'runtime', 'tmdb_score', 'seasons'] + list(range(len(label_encoder.classes_)))
    X = df[features]

    numerical_features = ['imdb_score', 'runtime', 'tmdb_score', 'seasons']
    scaler = StandardScaler()
    X[numerical_features] = scaler.fit_transform(X[numerical_features])

    if target_title in df['title'].values:
        target_item = X[df['title'] == target_title].values.reshape(1, -1)
        similarities = cosine_similarity(target_item, X.values)[0]
        df['similarity'] = similarities
        sorted_df = df.sort_values(by="similarity", ascending=False)
        top_similar_items = sorted_df.head(4)
        return top_similar_items[['title', 'similarity']]
    else:
        return None

df = pd.read_csv(r"C:\Users\carlo\Downloads\database.csv")

root = tk.Tk()
root.title("Netflix Filtering and Recommendation System")

window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry(f"{window_width}x{window_height}")

root.configure(bg="#1f1f1f")

style = ttk.Style()
style.configure("Custom.TButton", background="white", foreground="black",font=('Gill Sans MT', 24))  # Set background color to white and text color to black


main_label = ttk.Label(root, text="Netflix Filtering and Recommendation System", font=('Gill Sans MT', 48), foreground="#e50914", background="#1f1f1f")
main_label.pack(pady=window_height//4)

filtering_button = ttk.Button(root, text="Filtering System", command=open_filtering_system, style="Custom.TButton")
filtering_button.pack(pady=20)

recommendation_button = ttk.Button(root, text="Recommendation Model", command=open_recommendation_model, style="Custom.TButton")
recommendation_button.pack(pady=20)

style = ttk.Style()
style.configure("DarkButton.TButton", foreground="#ffffff", background="#1f1f1f", font=("Custom.TButton", 36))

filtering_page = tk.Toplevel()
filtering_page.title("Filtering System")
filtering_page.geometry(f"{window_width}x{window_height}")
filtering_page.configure(bg="#1f1f1f")  # Set background color to dark gray

cast_label = ttk.Label(filtering_page, text="Cast:", foreground="#ffffff", background="#1f1f1f", font=('Custom.TButton', 18))
cast_label.pack(pady=10)

cast_entry = ttk.Entry(filtering_page, font=('Custom.TButton', 20))
cast_entry.pack()

type_label = ttk.Label(filtering_page, text="Type (Movie/Show):", foreground="#ffffff", background="#1f1f1f", font=('Custom.TButton', 18))
type_label.pack(pady=10)

type_entry = ttk.Entry(filtering_page, font=('Custom.TButton', 20))
type_entry.pack()

release_year_label = ttk.Label(filtering_page, text="Minimum Release Year:", foreground="#ffffff", background="#1f1f1f", font=('Custom.TButton', 18))
release_year_label.pack(pady=10)

release_year_entry = ttk.Entry(filtering_page, font=('Custom.TButton', 20))
release_year_entry.pack()

age_certification_label = ttk.Label(filtering_page, text="Age Certification:", foreground="#ffffff", background="#1f1f1f", font=('Custom.TButton', 18))
age_certification_label.pack(pady=10)

age_certification_entry = ttk.Entry(filtering_page, font=('Custom.TButton', 20))
age_certification_entry.pack()

genre_label = ttk.Label(filtering_page, text="Genre:", foreground="#ffffff", background="#1f1f1f", font=('Custom.TButton', 18))
genre_label.pack(pady=10)

genre_entry = ttk.Entry(filtering_page, font=('Custom.TButton', 20))
genre_entry.pack()

imdb_score_label = ttk.Label(filtering_page, text="Minimum IMDb Score:", foreground="#ffffff", background="#1f1f1f", font=('Custom.TButton', 18))
imdb_score_label.pack(pady=10)

imdb_score_entry = ttk.Entry(filtering_page, font=('Custom.TButton', 20))
imdb_score_entry.pack()

tmdb_score_label = ttk.Label(filtering_page, text="Minimum TMDB Score:", foreground="#ffffff", background="#1f1f1f", font=('Custom.TButton', 18))
tmdb_score_label.pack(pady=10)

tmdb_score_entry = ttk.Entry(filtering_page, font=('Custom.TButton', 20))
tmdb_score_entry.pack()

min_seasons_label = ttk.Label(filtering_page, text="Minimum Number of Seasons:", foreground="#ffffff", background="#1f1f1f", font=('Custom.TButton', 18))
min_seasons_label.pack(pady=10)

min_seasons_entry = ttk.Entry(filtering_page, font=('Custom.TButton', 20))
min_seasons_entry.pack()

max_seasons_label = ttk.Label(filtering_page, text="Maximum Number of Seasons:", foreground="#ffffff", background="#1f1f1f", font=('Custom.TButton', 18))
max_seasons_label.pack(pady=10)

max_seasons_entry = ttk.Entry(filtering_page, font=('Custom.TButton', 20))
max_seasons_entry.pack()

production_country_label = ttk.Label(filtering_page, text="Production Country:", foreground="#ffffff", background="#1f1f1f", font=('Custom.TButton', 18))
production_country_label.pack(pady=10)

production_country_entry = ttk.Entry(filtering_page, font=('Custom.TButton', 20))
production_country_entry.pack()

filter_button = ttk.Button(filtering_page, text="Filter", command=filter_data, style="Custom.TButton")
filter_button.pack(pady=20)

result_text = tk.Text(filtering_page, height=10, width=50, bg="#1f1f1f", fg="#ffffff", insertbackground="#ffffff", font=('Custom.TButton', 18))
result_text.pack(pady=20)

back_to_main_button1 = ttk.Button(filtering_page, text="Back to Main Page", command=root.deiconify, style="Custom.TButton")
back_to_main_button1.pack(pady=20)

filtering_page.withdraw()

recommendation_page = tk.Toplevel()
recommendation_page.title("Recommendation Model")
recommendation_page.geometry(f"{window_width}x{window_height}")
recommendation_page.configure(bg="#1f1f1f")  # Set background color to dark gray

recommendation_label = ttk.Label(recommendation_page, text="Recommendation Model", font=('Gill Sans MT', 48), foreground="#e50914", background="#1f1f1f")
recommendation_label.pack(pady=window_height//4)

target_title_entry = ttk.Entry(recommendation_page, font=('Custom.TButton', 20))
target_title_entry.pack()

recommendation_button = ttk.Button(recommendation_page, text="Recommend Similar Shows", command=lambda: recommend_and_display(target_title_entry.get()), style="Custom.TButton")
recommendation_button.pack(pady=20)

back_to_main_button2 = ttk.Button(recommendation_page, text="Back to Main Page", command=root.deiconify, style="Custom.TButton")
back_to_main_button2.pack(pady=20)

def recommend_and_display(target_title):
    if target_title:
        similar_shows = recommend_similar_shows(target_title)
        if similar_shows is not None:
            messagebox.showinfo("Similar Shows", similar_shows.to_string(index=False))
        else:
            messagebox.showinfo("No shows found", "No films found with that title")
    else:
        messagebox.showinfo("No input", "Please enter a movie/show title")

recommendation_page.withdraw()

root.mainloop()
