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



if uber_csv:
    df_completed = data_pipeline.uber_csv(uber_csv)
    col1, col2 = st.columns([0.9, 3])
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

        # Exibir métricas principais
        col1.metric("💰 Total Gasto", f"R$ {df_filtered['fare_amount'].sum():,.2f}",
                    delta=f"R$ {df_filtered['fare_amount'].mean():,.2f} por corrida",
                    border=True)

        col1.metric("🚗 Total Corridas", df_filtered.shape[0],
                    delta=f"{df_filtered.shape[0]/len(year):.0f} por ano",
                    border=True)

        col1.metric("📍 Total Km", f"{df_filtered['distance'].sum():,.2f} km",
                    delta=f"{df_filtered['distance'].mean():.2f} km por corrida",
                    border=True)

        col1.metric("🚗 Corrida mais cara", f"R$ {df_filtered['fare_amount'].max():,.2f}",
                    delta=f"R$ {df_filtered['fare_amount'].max() - df_filtered['fare_amount'].min():,.2f} de diferença",
                    border=True)
    with col2:
        st.markdown("##### 📊 Gastos e KM percorridos por mês")
        def monthly_expenses(df=df_filtered):
            df['month'] = df['request_time'].dt.to_period('M').astype(str)
            df_grouped = df.groupby("month").agg({
                "fare_amount": "sum",  # gasto total
                "distance": "sum"  # km total
            }).reset_index()
            charts.bar_chart(df_grouped)

        monthly_expenses()

        st.markdown("##### 🗺️ Mapa de Calor dos Locais de Desembarque")
        def heatmap(df=df_filtered):
            df = df.groupby(['dropoff_lat', 'dropoff_lng']).size().reset_index(name='freq')
            charts.map_chart(df)
        heatmap()
        st.markdown("---")

    # Exibir tabela filtrada
    st.subheader("📊 Tabela de Corridas Filtradas")
    st.dataframe(df_completed)
    st.markdown("---")




