from turtledemo.penrose import start
import streamlit as st
from data_extraction import extract_data_from_pdf
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(
    page_title="Uber Expense Analytics",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded")

st.title("📊 Análise de Despesas com Uber")

uploaded_file = st.file_uploader("Envie o arquivo exportado da Uber (.csv)", type="csv")

if uploaded_file:
    try:
        #transformação dos dados
        df = pd.read_csv(uploaded_file)
        df['request_time'] = pd.to_datetime(df['request_time'])
        df['fare_amount'] = pd.to_numeric(df['fare_amount'], errors='coerce')
        df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
        df['product_type'] = df['product_type'].str.title()

        # extrair somente corridas concluídas
        df_completed = df[df['status'] == 'completed']
        st.success("✅ Dados carregados com sucesso!")


        # Filtros
        with st.sidebar:
            st.header("📊 Filtros do Dashboard")
            st.markdown("Use os filtros abaixo para personalizar a visualização dos dados.")
            year = sorted(df_completed['request_time'].dt.year.unique().tolist())
            year = st.sidebar.multiselect("Ano", options=year, default=year)
            st.sidebar.markdown("---")
            product_type = sorted(df_completed['product_type'].dropna().astype(str).unique().tolist())
            trip_type = st.sidebar.multiselect("Tipo de corrida", options=product_type, default=product_type)


        # Métricas principais
        df_filtered = df_completed[(df_completed['request_time'].dt.year.isin(year)) &
                                    (df_completed['product_type'].isin(trip_type))]

        st.metric("💰 Total Gasto", f"R$ {df_filtered['fare_amount'].sum():,.2f}")
        st.metric("🚗 Total Corridas", df_filtered.shape[0])
        st.metric("📍 Total Km", f"{df_filtered['distance'].sum():,.2f} km")
        st.metric("🚗 Corrida mais cara", f"R$ {df_filtered['fare_amount'].max():,.2f}")

        # Gastos por mes
        df_filtered['month'] = df_filtered['request_time'].dt.to_period('M')
        monthly_expenses = df_filtered.groupby('month')['fare_amount'].sum().reset_index()
        monthly_expenses['month'] = monthly_expenses['month'].dt.to_timestamp()
        st.subheader("📈 Gastos Mensais")
        st.bar_chart(monthly_expenses.set_index('month'))

        st.markdown("---")

        # Exibir tabela filtrada
        st.subheader("📊 Tabela de Corridas Filtradas")
        st.dataframe(df_completed)


    except Exception as e:
        st.error(f"❌ Erro ao carregar o arquivo: {e}")