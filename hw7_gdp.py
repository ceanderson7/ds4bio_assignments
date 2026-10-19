import requests as rq
import bs4
import pandas as pd
import plotly.express as px
import streamlit as st
from io import StringIO

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
old_url = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_GDP_(nominal)&oldid=1187446467"
headers = {"User-Agent": "MyDataScraperBot/1.0 (https://mywebsite.com; myemail@example.com)"}

@st.cache_data
def load_data():
   
    page = rq.get(url, headers=headers)
    page.raise_for_status()
    bs4page = bs4.BeautifulSoup(page.text, "html.parser")
    first_table = bs4page.find("table", {"class": "wikitable"})
    gdp = pd.read_html(StringIO(str(first_table)))[0]
    gdp.columns = ["Country", "IMF", "WorldBank", "UN"]

    for col in ["IMF", "WorldBank", "UN"]:
        s = gdp[col].astype(str)
        cleaned = (s.str.replace(r"[(]\d\d\d\d[)]", "", regex=True)
                    .str.replace(",", "", regex=False)
                    .str.strip())
        gdp[col] = pd.to_numeric(cleaned, errors="coerce")

    gdp["Country"] = gdp["Country"].str.split("[", regex=False).str[0].str.strip()
    gdp = gdp[gdp["Country"] != "World"].reset_index(drop=True)

    old_page = rq.get(old_url, headers=headers)
    old_page.raise_for_status()
    old_soup = bs4.BeautifulSoup(old_page.text, "html.parser")
    all_tables = old_soup.find_all("table")
    old_gdp = pd.read_html(StringIO(str(all_tables[2])))[0]

    regions = old_gdp.iloc[:, [0, 1]].copy()
    regions.columns = ["Country", "Region"]
    regions["Country"] = regions["Country"].str.split("[", regex=False).str[0].str.strip()
    regions = regions[regions["Country"] != "World"].reset_index(drop=True)

   
    return gdp.merge(regions, on="Country", how="inner")


st.title("GDP by region, stacked by country")

try:
    merged = load_data()
except Exception as err:
    st.error(f"Could not load the Wikipedia data: {err}")
    st.stop()

choice = st.selectbox("Source", ["IMF", "UN", "World Bank"])
column_name = {"IMF": "IMF", "UN": "UN", "World Bank": "WorldBank"}[choice]

plot_df = merged.dropna(subset=[column_name])

fig = px.bar(
    plot_df,
    x="Region",
    y=column_name,
    color="Country",
    title=f"GDP (nominal, million US$) by region, {choice} numbers",
    labels={column_name: "GDP (million US$)"},
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, width="stretch")

st.caption(f"{len(plot_df)} countries plotted; {len(merged) - len(plot_df)} have no {choice} number.")