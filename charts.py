import plotly.express as px
import streamlit as st
from matplotlib.pyplot import margins, title


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


def map_chart(df):
    fig = px.density_map(df, lat='dropoff_lat',
                         lon='dropoff_lng', z="freq", radius=10,
                         center=dict(lat=df['dropoff_lat'].mean(),
                                     lon=df['dropoff_lng'].mean()),
                         zoom=8,
                         color_continuous_scale="RdYlGn_r",
                         map_style="open-street-map")
    #remove color bar
    fig.update_coloraxes(showscale=False)
    # add title
    fig.update_layout(hovermode=False, margin={"r":0,"t":0,"l":0,"b":0})

    st.plotly_chart(fig, use_container_width=True)
