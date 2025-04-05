import streamlit as st
import plotly.express as px
import pandas as pd
from db import get_city_demographics

st.set_page_config(layout="wide")

st.title("Городская статистика: доходы, бедность, образование и этнический состав")

# Получаем данные
city_df = get_city_demographics()

# Обновляем типы данных (мягко)
city_df = city_df.astype({
    "poverty_rate": "float",
    "median_income": "Int64",
    "percent_completed_hs": "float",
    "share_white": "float",
    "share_black": "float",
    "share_hispanic": "float",
    "share_asian": "float"
})

if city_df.empty:
    st.warning("Данные не загружены.")
    st.stop()

# --- Боковая панель ---
st.sidebar.header("Фильтры")

# Фильтр по доходу
min_income, max_income = int(city_df["median_income"].min()), int(city_df["median_income"].max())
income_range = st.sidebar.slider("Медианный доход", min_income, max_income, (min_income, max_income), step=1000)

# Фильтр по бедности
min_pov, max_pov = float(city_df["poverty_rate"].min()), float(city_df["poverty_rate"].max())
poverty_range = st.sidebar.slider("Уровень бедности", float(min_pov), float(max_pov), (float(min_pov), float(max_pov)))

# Фильтр по доле белого населения
min_white, max_white = float(city_df["share_white"].min()), float(city_df["share_white"].max())
white_range = st.sidebar.slider("Доля белого населения", float(min_white), float(max_white), (float(min_white), float(max_white)))

# Применение фильтров
filtered_df = city_df[
    (city_df["median_income"] >= income_range[0]) &
    (city_df["median_income"] <= income_range[1]) &
    (city_df["poverty_rate"] >= poverty_range[0]) &
    (city_df["poverty_rate"] <= poverty_range[1]) &
    (city_df["share_white"] >= white_range[0]) &
    (city_df["share_white"] <= white_range[1])
]

# --- Графики ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Уровень бедности по городам")
    fig1 = px.histogram(filtered_df, x="poverty_rate", nbins=30, title="Распределение бедности", color_discrete_sequence=["#1f77b4"])
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("Этот график показывает, как распределён уровень бедности по выбранным городам. Он помогает быстро увидеть, где уровень бедности выше.")

with col2:
    st.subheader("Образование против бедности")
    fig2 = px.scatter(
        filtered_df,
        x="percent_completed_hs",
        y="poverty_rate",
        title="Зависимость бедности от уровня образования",
        trendline="ols",
        color_discrete_sequence=["#1f77b4"]
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Этот график показывает связь между долей людей с законченным средним образованием и уровнем бедности. Трендовая линия показывает общее направление связи.")

st.subheader("Доход и уровень образования")
fig3 = px.scatter(
    filtered_df,
    x="median_income",
    y="percent_completed_hs",
    title="Доход и образование",
    color_discrete_sequence=["#1f77b4"]
)
st.plotly_chart(fig3, use_container_width=True)
st.caption("Показывает, есть ли зависимость между доходами и образованием: чем выше доход, тем выше доля образованных.")

st.subheader("Расовый состав городов")
fig4 = px.box(
    filtered_df.melt(value_vars=["share_white", "share_black", "share_hispanic", "share_asian"],
                     var_name="Этническая группа", value_name="Доля"),
    x="Этническая группа", y="Доля",
    color="Этническая группа",
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="Сравнение долей разных расовых групп"
)
st.plotly_chart(fig4, use_container_width=True)
st.caption("Боксплот сравнивает, как варьируются доли разных этнических групп по городам.")

st.subheader("Доходы и расовый состав")
fig5 = px.scatter(
    filtered_df,
    x="median_income",
    y="share_hispanic",
    size="poverty_rate",
    color="share_white",
    title="Доход, доля латиноамериканцев и белых",
    color_continuous_scale="Blues",
)
st.plotly_chart(fig5, use_container_width=True)
st.caption("На этом графике можно увидеть, как уровень доходов связан с долей латиноамериканцев и белых, а также размер точки — это уровень бедности.")