import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import openrouteservice
import pandas as pd
from pandas.core.util.hashing import hash_pandas_object


def bar_chart(df):
    fig = px.bar(
        df,
        x="month",
        y=["fare_amount", "distance"],
        barmode="group",
        color_discrete_sequence=["#636EFA", "#EF553B"],
        labels={
            "month": "Mês",
            "value": "Valor",
            "variable": "Métrica",
            "fare_amount": "Preço",  # Updated label
            "distance": "Distância"
        }
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(xaxis_tickformat="%b/%Y", margin={"r":0,"t":30,"l":0,"b":0})
    fig.for_each_trace(lambda t: t.update(name="Preço") if t.name == "fare_amount" else t.update(name="Distância"))
    st.plotly_chart(fig, use_container_width=True)


def trace_route(df):
    df = df.sort_values(by='fare_amount', ascending=False).head(1)
    start_coord = (df['begintrip_lng'].values[0], df['begintrip_lat'].values[0])
    end_coord = (df['dropoff_lng'].values[0], df['dropoff_lat'].values[0])
    coords = [start_coord, end_coord]

    # call open route service api
    API_KEY = st.secrets["ORS_API_KEY"]
    client = openrouteservice.Client(key=API_KEY)
    route = client.directions(coordinates=coords, profile='driving-car', format='geojson')

    route_coords = route['features'][0]['geometry']['coordinates']
    return route_coords, start_coord, end_coord


def map_chart(df, show_route_option=True):
    df_heat = df.groupby(['dropoff_lat', 'dropoff_lng']).size().reset_index(name='freq')

    # Criar figura vazia
    fig = go.Figure()

    # Adicionar heatmap usando go.Densitymapbox
    fig.add_trace(go.Densitymapbox(
        lat=df_heat['dropoff_lat'],
        lon=df_heat['dropoff_lng'],
        z=df_heat['freq'],
        radius=10,
        colorscale="RdYlGn_r",
        showscale=False,
        hoverinfo='skip',
        visible=True
    ))

    # Configurar layout do mapa
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(
                lat=df_heat['dropoff_lat'].mean(),
                lon=df_heat['dropoff_lng'].mean()
            ),
            zoom=8
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    if show_route_option:
        try:
            route_coords_list, start_coord, end_coord = trace_route(df)
            route_df = pd.DataFrame(route_coords_list, columns=["lon", "lat"])

            idx_max = df['fare_amount'].idxmax()
            start_address = df.loc[idx_max, 'begintrip_address']
            end_address = df.loc[idx_max, 'dropoff_address']

            # Adicionar linha da rota (inicialmente oculta)
            fig.add_trace(go.Scattermapbox(
                lon=route_df["lon"],
                lat=route_df["lat"],
                mode="lines",
                line=dict(width=4, color="royalblue"),
                name="Rota",
                hoverinfo="none",
                visible=False
            ))

            # Adicionar marcador de início
            fig.add_trace(go.Scattermapbox(
                lon=[start_coord[0]],
                lat=[start_coord[1]],
                mode="markers",
                marker=dict(size=12, color="green", symbol="circle"),
                name="Embarque",
                text=[f"Endereço: {start_address}"],
                hovertemplate="<b>Ponto de Embarque</b><br>%{text}<extra></extra>",
                visible=False
            ))

            # Adicionar marcador de fim
            fig.add_trace(go.Scattermapbox(
                lon=[end_coord[0]],
                lat=[end_coord[1]],
                mode="markers",
                marker=dict(size=12, color="red", symbol="circle"),
                name="Desembarque",
                text=[f"Endereço: {end_address}"],
                hovertemplate="<b>Ponto de Chegada</b><br>%{text}<extra></extra>",
                visible=False
            ))

            # Criar menu de seleção
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="left",
                        buttons=[
                            dict(
                                args=[{"visible": [True, False, False, False]}],
                                label="🗺 Mapa de Calor",
                                method="update"
                            ),
                            dict(
                                args=[
                                    {"visible": [False, True, True, True]},
                                    {"mapbox.zoom": 8,
                                     "mapbox.center": {"lat": route_df["lat"].mean(),
                                                       "lon": route_df["lon"].mean()}}
                                ],
                                label="💲 Rota da Corrida Mais Cara",
                                method="update"
                            )
                        ],
                        pad={"r": 10, "t": 10},
                        showactive=True,
                        x=0.01,
                        xanchor="left",
                        y=0.99,
                        yanchor="top",
                        bgcolor="darkgrey",
                        bordercolor="black",
                        borderwidth=1,
                        font=dict(color="black"),
                    )
                ]
            )
        except Exception as e:
            st.warning(f"Não foi possível carregar a rota: {e}")

    st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True})

