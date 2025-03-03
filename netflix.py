import streamlit as st
import datetime
import pandas as pd

#Sfondo
st.set_page_config(page_title='Netflix 2023:popcorn:', page_icon='sfondo.png', layout='wide', initial_sidebar_state='auto')

# Title
st.title("Netflix 2023:popcorn:")

# Dataframe loading and caching
filename = "C:/Users/traet/Desktop/ProgettoISBI/dataset_netflix_2023.csv"
def _lower(string):
    return str.lower(string)

@st.cache_data
def load_data(nrows):
    df = pd.read_csv(filename, nrows=nrows)
    df.rename(_lower, axis="columns", inplace=True)
    return df

with st.spinner("Loading dataframe..."):
    df = load_data(10000)

# Filters
st.sidebar.header("Filters")
lower_rating, higher_rating = st.sidebar.slider(
    "Ratings", min_value=85, max_value=100, step=1, value=(85, 100)
)

# Filtering df
#filtered_df = df[
#    (df["rating"] >= lower_rating) & (df["rating"] <= higher_rating)
#]
# Expander
#with st.expander("Show raw data"):
   # st.dataframe(filtered_df)

genre=st.sidebar.multiselect(
    "Genre",
    options=df["genre"].unique(),
    default=df["genre"].unique(),
)

# Converte la colonna "Release Date" in formato datetime
df["release date"] = pd.to_datetime(df["release date"], errors="coerce")

# Calcola i limiti dell'intervallo per la colonna "Release Date"
min_date = df["release date"].min()
max_date = df["release date"].max()

# Imposta un valore predefinito come la data di mezzo tra il minimo e il massimo
default_date = min_date + (max_date - min_date) // 2

# Converte la data selezionata in formato datetime64[ns]
start_date = pd.to_datetime(st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, value=default_date))

# Filtra il DataFrame in base alla data
filtered_df = df[
    (df["rating"] >= lower_rating) & (df["rating"] <= higher_rating)
    & (df["genre"].isin(genre))
    & (df["release date"] >= start_date)
    ]

# Expander
st.dataframe(filtered_df)

# Grafico basato su "Ratings"
left_column, right_column = st.columns(2)
left_column.header("Best Ratings per Genre")
left_column.line_chart(
    filtered_df.reset_index(),
    x="rating",
    y="number of ratings",
    color="genre",
)

# Istogramma basato sul "Numero Totale di Valutazioni"
right_column.header("Most Rated Movies/TV Series")
right_column.bar_chart(
    filtered_df.reset_index(),
    x="title",
    y="number of ratings",
    color="genre"
)

# Istogramma basato sulle "Ore Visualizzate"
left_column.header("Most Viewed Movies/ TV Series")
left_column.bar_chart(
    filtered_df.reset_index(),
    x="title",
    y="hours viewed",
    color="genre"
)

# import streamlit as st
# import pandas as pd

# # Caricamento dati
# filename = "C:/Users/traet/Desktop/ProgettoISBI/dataset_netflix_2023.csv"
# df = pd.read_csv(filename)

# # Converte la colonna "Release Date" in formato datetime
# df["release date"] = pd.to_datetime(df["release date"], errors="coerce")

# # Estrae il mese dalla colonna "Release Date"
# df["month"] = df["release date"].dt.month

# # Filtra il DataFrame in base ai parametri desiderati
# filtered_df = df[
#     (df["rating"] >= lower_rating) & (df["rating"] <= higher_rating)
#     & (df["genre"].isin(genre))
#     & (df["release date"] >= start_date)
# ]

# # Calcola il conteggio delle serie per ciascun mese
# monthly_counts = filtered_df["month"].value_counts().sort_index()

# # Crea un grafico a barre diviso per i mesi di rilascio delle serie
# st.bar_chart(monthly_counts)

import random
import pandas as pd
import streamlit as st

# Filtra il DataFrame per visualizzare solo alcune colonne
selected_columns = ["title", "rating", "number of ratings", "hours viewed"]
df_subset = df[selected_columns]

# Aggiungi una colonna fittizia per simulare la cronologia delle visualizzazioni
df_subset["views_history"] = [[random.randint(0, 5000) for _ in range(30)] for _ in range(len(df_subset))]

# Configurazione della visualizzazione della colonna
column_config = {
    "title": "Movie Title",
    "rating": st.column_config.NumberColumn("Average Rating", format="%0.2f⭐"),
    "number of ratings": st.column_config.NumberColumn("Total Ratings", format="%d"),
    "hours viewed": st.column_config.NumberColumn("Total Hours Viewed", format="%d hours"),
    "views_history": st.column_config.LineChartColumn("Views (past 30 days)", y_min=0, y_max=5000),
}

# Visualizza il DataFrame e la configurazione delle colonne
st.dataframe(df_subset, column_config=column_config, hide_index=True)

