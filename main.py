import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from db import get_city_demographics

st.set_page_config(layout="wide")

st.title("📊 Городская статистика: доходы, бедность, образование и этнический состав")

# Получаем данные
city_df = get_city_demographics()

# Обновляем типы данных
city_df = city_df.astype({
    "poverty_rate": "float",
    "median_income": "Int64",
    "percent_completed_hs": "float",
    "share_white": "float",
    "share_black": "float",
    "share_hispanic": "float",
    "share_asian": "float",
    "share_native_american": "float"
})

if city_df.empty:
    st.warning("Данные не загружены.")
    st.stop()

# --- Боковая панель ---
st.sidebar.header("🔧 Фильтры")

# Фильтр по штату
states = sorted(city_df["state"].unique())
selected_states = st.sidebar.multiselect("Выберите штат(ы)", states, default=states[:5])

# Фильтр по уровню бедности
poverty_range = st.sidebar.slider("📉 Уровень бедности (%)", 0.0, 100.0, (0.0, 100.0))

# Фильтр по образованию
education_threshold = st.sidebar.slider("📘 Минимальный % окончивших среднюю школу", 0, 100, 60)

# Применение фильтров
filtered_df = city_df[
    (city_df["state"].isin(selected_states)) &
    (city_df["poverty_rate"] >= poverty_range[0]) &
    (city_df["poverty_rate"] <= poverty_range[1]) &
    (city_df["percent_completed_hs"] >= education_threshold)
]

# --- 📘 Образование ---
st.header("📘 Образование")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Связь образования и бедности")
    fig1 = px.scatter(
        filtered_df,
        x="percent_completed_hs",
        y="poverty_rate",
        trendline="ols",
        title="Образование и уровень бедности"
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("Чем выше процент окончивших школу, тем ниже уровень бедности — прослеживается отрицательная корреляция.")

with col2:
    st.subheader("Образование и доход")
    fig2 = px.scatter(
        filtered_df,
        x="percent_completed_hs",
        y="median_income",
        trendline="ols",
        title="Образование и доход"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Города с высоким уровнем образования обычно имеют более высокий медианный доход.")

# --- 💰 Доход ---
st.header("💰 Доход")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Доход и бедность")
    fig3 = px.scatter(
        filtered_df,
        x="median_income",
        y="poverty_rate",
        trendline="ols",
        title="Медианный доход и бедность"
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Более высокий доход в городе связан с более низким уровнем бедности.")

with col4:
    st.subheader("Доход и доля белого населения")
    fig4 = px.scatter(
        filtered_df,
        x="share_white",
        y="median_income",
        trendline="ols",
        title="Доля белого населения и доход"
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("Города с большей долей белого населения чаще имеют более высокий доход — требуется дополнительный анализ на причинность.")

# --- 🌍 Расовый состав ---
st.header("🌍 Расовый состав")

fig5 = px.box(
    filtered_df.melt(value_vars=["share_white", "share_black", "share_hispanic", "share_asian", "share_native_american"],
                     var_name="Этническая группа", value_name="Доля"),
    x="Этническая группа",
    y="Доля",
    color="Этническая группа",
    title="Сравнение долей этнических групп по городам",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig5, use_container_width=True)
st.caption("Боксплот показывает, как варьируются доли разных этнических групп среди городов.")

# --- 📉 Уровень бедности ---
st.header("📉 Уровень бедности")

fig6 = px.histogram(
    filtered_df,
    x="poverty_rate",
    nbins=30,
    title="Распределение уровня бедности по городам",
    color_discrete_sequence=["#EF553B"]
)
st.plotly_chart(fig6, use_container_width=True)
st.caption("Позволяет увидеть общее распределение бедности — большинство городов находится в нижней половине шкалы.")