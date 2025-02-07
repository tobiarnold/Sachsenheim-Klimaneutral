import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import statsmodels.api as sm
import urllib.request
from PIL import Image

def main():
    df = pd.read_csv(r"https://raw.githubusercontent.com/tobiarnold/Sachsenheim-Klimaneutral/main/df.csv",sep="|")
    st.set_page_config(page_title="Wetterdaten DWD", page_icon=":green_heart:", layout="centered")
    hide_streamlit_style = """
                 <style>
                  div.block-container{padding-top:2rem;}
                   div[data-testid="stToolbar"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                 </style>
                 """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.title("Wetterdaten des Deutschen Wetterdienstes")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/tobiarnold/Sachsenheim-Klimaneutral/main/Sachsenheim-S6.jpg","logo.jpg")
    image = Image.open("logo.jpg")
    st.image(image, width=100)
    st.write("""Hallo👋 Wir sind **sachsenheim.klimaneutral**!
             Eine überparteiliche Initiative, die erreichen möchte, dass Sachsenheim bis 2035 klimaneutral wird. 
             Wir haben diese Initiative im April 2021 ins Leben gerufen, weil wir davon überzeugt sind, dass große Veränderungen klein und lokal beginnen: 
             Nur gemeinsam können wir der Politik signalisieren, dass das Jahrhundertproblem Klimawandel mutiger angegangen werden kann und muss.""")
    st.write("""Auf dieser von uns erstellten Seite könnt Ihr euch die verschiedenen **historischen Daten der Wetterstationen des Deutschen Wetterdienstes** in 
             Deutschland anzeigen lassen. Wählt oder gebt dazu direkt die Stadt nach der ihr sucht ein.""")
    st.write("Insgesamt stehen mehr als 1.000 Stationen zur Verfügung. Die Daten reichen je nach Wetterstation von 1781 bis 2023. Viel Spass 😀")
    st.markdown("##### Hier filtern oder Suchwort eingeben:")
    wetterstation = st.selectbox("Wetterstation auswählen", options=df["Stationsname"].unique(), index =815)
    df_selection = df.query("Stationsname == @wetterstation")
    st.markdown("##### Hier Datentabelle ein- oder ausblenden:")
    tabelle = st.radio(
        "Datentabelle ein- oder ausblenden",
        ("Ausblenden","Einblenden"))
    if tabelle == "Ausblenden":
        st.write("Datentabelle ist ausgeblendet.")
    else:
        st.dataframe(df_selection.style.format({"Jahresmittel Lufttemperatur": "{:.2f}", "abs. Max. Lufttemperatur": "{:.2f}",
                                            "abs. Min. Lufttemperatur": "{:.2f}", "Jahressumme Niederschlagshöhe": "{:.1f}",
                                            "Max. Niederschlagshoehe Jahr": "{:.1f}", "Jahresmittel Max. Lufttemperatur": "{:.2f}",
                                            "Jahresmittel Min. Lufttemperatur": "{:.2f}", "Sonnenscheindauer": "{:.1f}",
                                            "abs. Max. Windmaxspitze": "{:.2f}", "Bedeckungsgrad": "{:.2f}"}))
    st.title(":bar_chart: Daten der Wetterstation")
    st.markdown("##")
    st.write("Die folgenden Diagramme zeigen jeweils die Veränderungen der Temperaturen für die verschiedenen Jahre sowie die Veränderung der Niederschläge.")
    st.write("Die Punkte bei den Diagrammen stellen jeweils die Messwerte in den verschieden Jahren dar, die rote bzw. blaue Linie zeigt den Trend auf.")
    fig = px.scatter(df_selection, x="Jahr", y="Jahresmittel Lufttemperatur", trendline="ols",
                     color="Jahresmittel Lufttemperatur",color_continuous_scale=px.colors.sequential.Agsunset,
                     title="<b>durchschnittliche Temperatur in Grad Celsius</b>", trendline_color_override="red")
    config = {"displayModeBar": False}
    fig.update_traces(marker_size=8)
    fig.update_layout(coloraxis_colorbar_x=0.95, coloraxis_colorbar=dict(title="Temperatur"),
                      margin=dict(l=0, r=0, t=60, b=50), width=600, height=450)
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    st.plotly_chart(fig, use_container_width=True, config=config)
    fig = px.scatter(df_selection, x="Jahr", y="abs. Max. Lufttemperatur", trendline="ols",
                     color="abs. Max. Lufttemperatur", color_continuous_scale=px.colors.sequential.Hot_r,
                     title="<b>maximale Temperatur in Grad Celsius</b>",trendline_color_override="red")
    config = {"displayModeBar": False}
    fig.update_traces(marker_size=8)
    fig.update_layout(coloraxis_colorbar_x=0.95, coloraxis_colorbar=dict(title="Temperatur"),
                      margin=dict(l=0, r=0, t=60, b=50), width=600, height=450)
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    st.plotly_chart(fig, use_container_width=True, config=config)
    fig = px.scatter(df_selection, x="Jahr", y="abs. Min. Lufttemperatur", trendline="ols", trendline_color_override="blue",
                     color="abs. Min. Lufttemperatur", color_continuous_scale=px.colors.sequential.Viridis,
                     title="<b>minimale Temperatur in Grad Celsius</b>")
    config = {"displayModeBar": False}
    fig.update_traces(marker_size=8)
    fig.update_layout(coloraxis_colorbar_x=0.95, coloraxis_colorbar=dict(title="Temperatur"),
                      margin=dict(l=0, r=0, t=60, b=50), width=600, height=450)
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    st.plotly_chart(fig, use_container_width=True, config=config)
    fig = px.scatter(df_selection, x="Jahr", y="Jahressumme Niederschlagshöhe", trendline="ols", trendline_color_override="blue",
                     color="Jahressumme Niederschlagshöhe", color_continuous_scale=px.colors.sequential.Blues,
                     title="<b>Jahressumme Niederschlagshöhe in mm</b>")
    config = {"displayModeBar": False}
    fig.update_traces(marker_size=8)
    fig.update_layout(coloraxis_colorbar_x=0.95, coloraxis_colorbar=dict(title="Niederschlagshöhe"),
                      margin=dict(l=0, r=0, t=60, b=50), width=600, height=450)
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    st.plotly_chart(fig, use_container_width=True, config=config)
    link1 = "[Sachsenheim Klimaneutral](https://sachsenheim-klimaneutral.de/)"
    st.markdown(link1, unsafe_allow_html=True)
    link2 = "[Instagram sachsenheim.klimaneutral](https://www.instagram.com/sachsenheim.klimaneutral/)"
    st.markdown(link2, unsafe_allow_html=True)
    st.write("Wir würden uns freuen, wenn Ihr unserem Insta Profil folgt und ein Like dalasst.  \n💚💚💚")
    st.markdown("***")
    try:
        df_neu = df_selection.pivot(index="Jahr",columns= "Stations_Id", values="Jahresmittel Lufttemperatur")
        df_neu = df_neu.transpose()
        f, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 3))
        ax = sns.heatmap(df_neu, cmap="coolwarm")
        st.title("Warming Stripes")
        st.write(
            "Die Warming Stripes zeigen die Veränderungen der Durchschnittstemperaturen für die verschiedenen Jahre auf, wobei blau für eher kalte und rot für eher warme Jahre steht.")
        st.markdown("##")
        st.write(f)
    except:
        st.write("Daten können nicht angezeigt werden")
    st.markdown("***")
    st.text("created with Python by Tobias Arnold, Quelle: Deutscher Wetterdienst")
    link3 = "[Historische Wetterdaten](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/annual/kl/historical/)"
    st.markdown(link3, unsafe_allow_html=True)
        
if __name__ == "__main__":
  main()
