
import streamlit as st
import requests
import pandas as pd

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="📰 News Intelligence Dashboard",
    page_icon="📰",
    layout="wide"
)

# =====================================
# API CONFIG
# =====================================

API_KEY = st.secrets["NEWSDATA_API_KEY"]

BASE_URL = "https://newsdata.io/api/1/latest"

# =====================================
# FILTERS
# =====================================

countries = {
    "India":"in",
    "United States":"us",
    "United Kingdom":"gb",
    "Australia":"au",
    "Canada":"ca",
    "Singapore":"sg",
    "Germany":"de",
    "France":"fr",
    "Japan":"jp"
}

categories = [
    "top",
    "business",
    "technology",
    "sports",
    "health",
    "science",
    "entertainment",
    "politics",
    "world"
]

st.sidebar.title("News Filters")

country = st.sidebar.selectbox(
    "Country",
    list(countries.keys())
)

category = st.sidebar.selectbox(
    "Category",
    categories
)

keyword = st.sidebar.text_input(
    "Keyword Search"
)

language = st.sidebar.selectbox(
    "Language",
    ["en","hi"]
)

number = st.sidebar.slider(
    "Number of Articles",
    5,
    20,
    10
)

search = st.sidebar.button("Fetch News")

# =====================================
# FETCH FUNCTION
# =====================================

@st.cache_data(ttl=300)

def fetch_news():

    params = {
        "apikey": API_KEY,
        "country": countries[country],
        "language": language,
        "category": category
    }

    if keyword != "":
        params["q"] = keyword

    response = requests.get(
        BASE_URL,
        params=params
    )

    data = response.json()

    return data

# =====================================
# TITLE
# =====================================

st.title("📰 News Intelligence Dashboard")

st.write(
    "Search and explore the latest news articles from around the world."
)

# =====================================
# FETCH NEWS
# =====================================

if search:

    with st.spinner("Fetching news..."):

        data = fetch_news()

    if data["status"] != "success":

        st.error(data)

    else:

        articles = data["results"][:number]

        st.success(f"{len(articles)} articles found")

        st.divider()

        table = []

        for article in articles:

            table.append({
                "Title":article.get("title"),
                "Source":article.get("source_id"),
                "Date":article.get("pubDate")
            })

            c1,c2 = st.columns([1,3])

            with c1:

                if article.get("image_url"):

                    st.image(
                        article["image_url"],
                        use_container_width=True
                    )

            with c2:

                st.subheader(article.get("title"))

                st.write(
                    "**Source:**",
                    article.get("source_id")
                )

                st.write(
                    "**Published:**",
                    article.get("pubDate")
                )

                if article.get("creator"):

                    st.write(
                        "**Author:**",
                        ", ".join(article.get("creator"))
                    )

                st.write(
                    article.get("description")
                )

                with st.expander("Full Content"):

                    st.write(
                        article.get("content")
                    )

                if article.get("link"):

                    st.link_button(
                        "Read Full Article",
                        article.get("link")
                    )

            st.divider()

        st.header("📊 Data Table")

        df = pd.DataFrame(table)

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(index=False).encode()

        st.download_button(
            "Download CSV",
            csv,
            "news.csv",
            "text/csv"
        )

