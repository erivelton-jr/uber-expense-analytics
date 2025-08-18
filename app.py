import streamlit as st
import data_pipeline
import charts

st.set_page_config(
    page_title="Uber Expense Analytics",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded")

st.title("📊 Análise de Despesas com Uber")
uber_csv = st.file_uploader("Envie o arquivo exportado da Uber (.csv)", type="csv")

col1, col2 = st.columns([1, 3])

if uber_csv:
    df_completed = data_pipeline.uber_csv(uber_csv)
    with st.sidebar:
        st.header("📊 Filtros do Dashboard")
        st.markdown("Use os filtros abaixo para personalizar a visualização dos dados.")
        year = sorted(df_completed['request_time'].dt.year.unique().tolist())
        year = st.sidebar.multiselect("Ano", options=year, default=year)
        st.sidebar.markdown("---")
        product_type = sorted(df_completed['product_type'].dropna().astype(str).unique().tolist())
        trip_type = st.sidebar.multiselect("Tipo de corrida", options=product_type, default=product_type)
    with col1:
        # Métricas principais
        df_filtered = df_completed[(df_completed['request_time'].dt.year.isin(year)) &
                                   (df_completed['product_type'].isin(trip_type))]

        st.metric("💰 Total Gasto", f"R$ {df_filtered['fare_amount'].sum():,.2f}")
        st.metric("🚗 Total Corridas", df_filtered.shape[0])
        st.metric("📍 Total Km", f"{df_filtered['distance'].sum():,.2f} km")
        st.metric("🚗 Corrida mais cara", f"R$ {df_filtered['fare_amount'].max():,.2f}")
    with col2:
        # Gastos por mes
        df_filtered['month'] = df_filtered['request_time'].dt.to_period('M')
        monthly_expenses = df_filtered.groupby('month')['fare_amount'].sum().reset_index()
        monthly_expenses['month'] = monthly_expenses['month'].dt.to_timestamp()
        charts.bar_chart(monthly_expenses)

    def heatmap(df):
        df = df.groupby(['dropoff_lat', 'dropoff_lng'])['status'].count().reset_index()
        return df
    map = heatmap(df_filtered)
    charts.map_chart(map)

    st.markdown("---")

    # Exibir tabela filtrada
    st.subheader("📊 Tabela de Corridas Filtradas")
    st.dataframe(df_completed)
    st.markdown("---")
