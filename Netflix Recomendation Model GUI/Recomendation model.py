from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

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