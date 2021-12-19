import streamlit as st
from streamlit import cli as stcli
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from PIL import Image

def main():
    pd.set_option('display.max_colwidth', None)
    df = pd.read_csv(r"https://raw.githubusercontent.com/tobiarnold/Sachsenheim-Klimaneutral/main/output_file.txt",delimiter=";")
    df = df[df.STATIONS_ID != "STATIONS_ID"]
    df_station = pd.read_csv(r"https://raw.githubusercontent.com/tobiarnold/Sachsenheim-Klimaneutral/main/KL_Jahreswerte_Beschreibung_Stationen.txt",encoding='latin-1', delimiter=";")
    df_station.columns = df_station.columns.str.strip()
    df_station = df_station.rename(columns={"Stations_ID": "STATIONS_ID"})
    df_station["STATIONS_ID"] = df_station["STATIONS_ID"].astype(int)
    df["STATIONS_ID"] = df["STATIONS_ID"].astype(int)
    df=pd.merge(df, df_station, on="STATIONS_ID", how="left")
    df = df.drop(["MESS_DATUM_BEGINN", "QN_4", "QN_6", "eor"], axis=1)
    df = df.rename(columns={"STATIONS_ID": "Stations_Id",
                            "MESS_DATUM_ENDE": "Jahr", "JA_N": "Bedeckungsgrad",
                            "JA_TT": "Jahresmittel Lufttemperatur",
                            "JA_TX": "Jahresmittel Max. Lufttemperatur",
                            "JA_TN": "Jahresmittel Min. Lufttemperatur",
                            "JA_FK": "Windstärke", "JA_SD_S": "Sonnenscheindauer",
                            "JA_MX_FX": "abs. Max. Windmaxspitze",
                            "JA_MX_TX": "abs. Max. Lufttemperatur",
                            "JA_MX_TN": "abs. Min. Lufttemperatur",
                            "JA_RR": "Jahressumme Niederschlagshöhe",
                            "JA_MX_RS": "Max. Niederschlagshoehe Jahr"})
    df["Jahr"] = df["Jahr"].astype(str)
    df["Jahr"] = df["Jahr"].str[:4]
    df["Jahr"] = df["Jahr"].astype(int)
    df.set_index("Jahr")
    first_col = df.pop("Stationsname")
    df.insert(0, "Stationsname", first_col)
    df=df.sort_values(["Stationsname","Jahr"])
    df[["Bedeckungsgrad", "Jahresmittel Lufttemperatur", "Jahresmittel Max. Lufttemperatur", "Jahresmittel Min. Lufttemperatur",
        "Sonnenscheindauer", "abs. Max. Windmaxspitze", "abs. Max. Lufttemperatur", "abs. Min. Lufttemperatur", "Jahressumme Niederschlagshöhe",
        "Max. Niederschlagshoehe Jahr"]] = \
        df[["Bedeckungsgrad", "Jahresmittel Lufttemperatur", "Jahresmittel Max. Lufttemperatur", "Jahresmittel Min. Lufttemperatur",
        "Sonnenscheindauer", "abs. Max. Windmaxspitze", "abs. Max. Lufttemperatur", "abs. Min. Lufttemperatur", "Jahressumme Niederschlagshöhe",
        "Max. Niederschlagshoehe Jahr"]].apply(pd.to_numeric, axis=1)
    df=df.replace("-999", np.nan)
    df = df.replace(-999.0000, np.nan)
    df = df.replace(-999, np.nan)
    df=df.round(2)
    df = df[["Stationsname", "Stations_Id", "Jahr", "Jahresmittel Lufttemperatur", "abs. Max. Lufttemperatur", "abs. Min. Lufttemperatur",
             "Jahressumme Niederschlagshöhe", "Max. Niederschlagshoehe Jahr","Jahresmittel Max. Lufttemperatur",
             "Jahresmittel Min. Lufttemperatur" , "Sonnenscheindauer", "Windstärke", "abs. Max. Windmaxspitze", "Bedeckungsgrad"]]
    #print(df.head())
    st.set_page_config(page_title="Wetterdaten des Deutschen Wetterdienstes", page_icon=":green_heart:", layout="wide")
    st.title("Wetterdaten des Deutschen Wetterdienstes")
    st.markdown("***")
    image = Image.open("https://raw.githubusercontent.com/tobiarnold/Sachsenheim-Klimaneutral/main/Sachsenheim-S6.jpg", width=200)
    st.image(image)
    st.write("""Hallo👋 Wir sind **sachsenheim.klimaneutral**!
             Eine überparteiliche Initiative, die erreichen möchte, dass Sachsenheim bis 2035 klimaneutral wird. 
             Wir haben diese Initiative im April 2021 ins Leben gerufen, weil wir davon überzeugt sind, dass große Veränderungen klein und lokal beginnen: 
             Nur gemeinsam können wir der Politik signalisieren, dass das Jahrhundertproblem Klimawandel mutiger angegangen werden kann und muss.""")
    st.markdown("##")
    st.write("""Auf dieser von uns erstellten Seite könnt Ihr euch die verschiedenen (historischen) Daten der Wetterstationen des Deutschen Wetterdienstes in 
             Deutschland anzeigen lassen, wählt dazu  **links einen Filter aus oder gebt direkt die Stadt nach der Ihr sucht ein. Achtung bei Zugriff mit mobilen Geräte ist der 
             Filter standardmäßig ausgeblendet. Der Filter lässt sich mit dem Pfeil oben links einblenden.**
             Insgesamt stehen mehr als 1.100 Stationen zur Verfügung. Viel Spass 😀""")
    st.markdown("##")
   # st.dataframe(df_station)
   # st.dataframe(df)
   # print(df.dtypes)
    st.sidebar.header("Hier filtern oder Suchwort eingeben")
    wetterstation = st.sidebar.selectbox("Wetterstation auswählen", options=df["Stationsname"].unique(), index =847)
    df_selection = df.query("Stationsname == @wetterstation")
    st.dataframe(df_selection.style.format({"Jahresmittel Lufttemperatur": "{:.2f}", "abs. Max. Lufttemperatur": "{:.2f}",
                                            "abs. Min. Lufttemperatur": "{:.2f}", "Jahressumme Niederschlagshöhe": "{:.1f}",
                                            "Max. Niederschlagshoehe Jahr": "{:.1f}", "Jahresmittel Max. Lufttemperatur": "{:.2f}",
                                            "Jahresmittel Min. Lufttemperatur": "{:.2f}", "Sonnenscheindauer": "{:.1f}",
                                            "abs. Max. Windmaxspitze": "{:.2f}", "Bedeckungsgrad": "{:.2f}"}))
    #st.dataframe(df_selection)
    #Diagramme
    st.title(":bar_chart: Daten der Wetterstation")
    st.markdown("##")
    st.write("Die folgenden Diagramme zeigen jeweils die Veränderungen der Temperaturen für die verschiedenen Jahre sowie die Veränderung der Niederschläge.")
    st.write("Die Punkte bei den Diagrammen stellen jeweils die Messwerte in den verschieden Jahren dar, die rote Linie zeigt den Trend auf.")

    #col1, col2 = st.columns(2)
    #with col1:
    fig = px.scatter(df_selection, x="Jahr", y="Jahresmittel Lufttemperatur", trendline="ols", color="Jahresmittel Lufttemperatur", title="<b>durchschnittliche Lufttemperatur je Jahr in Grad Celsius</b>")
    fig.update_traces(marker_size=8)
    st.plotly_chart(fig)
    #with col2:
    fig = px.scatter(df_selection, x="Jahr", y="abs. Max. Lufttemperatur", trendline="ols",
                           color="abs. Max. Lufttemperatur", color_continuous_scale=px.colors.sequential.Hot_r, title="<b>maximal gemessene Lufttemperatur je Jahr in Grad Celsius</b>")
    fig.update_traces(marker_size=8)
    st.plotly_chart(fig)

    #col3, col4 = st.columns(2)
    #with col3:
    fig = px.scatter(df_selection, x="Jahr", y="abs. Min. Lufttemperatur", trendline="ols",
                           color="abs. Min. Lufttemperatur", color_continuous_scale=px.colors.sequential.Viridis, title="<b>minimal gemessene Lufttemperatur je Jahr in Grad Celsius</b>")
    fig.update_traces(marker_size=8)
    st.plotly_chart(fig)
    #with col4:
    fig = px.scatter(df_selection, x="Jahr", y="Jahressumme Niederschlagshöhe", trendline="ols",
                              color="Jahressumme Niederschlagshöhe", color_continuous_scale=px.colors.sequential.Blues,
                              title="<b>Jahressumme Niederschlagshöhe in mm</b>")
    fig.update_traces(marker_size=8)
    st.plotly_chart(fig)
        
    link1 = "[Sachsenheim Klimaneutral](https://sachsenheim-klimaneutral.de/)"
    st.markdown(link1, unsafe_allow_html=True)
    link2="[Instagram sachsenheim.klimaneutral](https://www.instagram.com/sachsenheim.klimaneutral/)"
    st.markdown(link2, unsafe_allow_html=True)
    st.write("Wir würden uns freuen, wenn Ihr unserem Insta Profil folgt und ein Like dalasst.  \n💚💚💚")
    st.markdown("***")
    #heatmap
    df_neu = df_selection.pivot("Jahr", "Stations_Id", "Jahresmittel Lufttemperatur")
    df_neu = df_neu.transpose()
    f, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 3))
    ax = sns.heatmap(df_neu, cmap="coolwarm")
    st.title("Warming Stripes")
    st.write("Die Warming Stripes zeigen die Veränderungen der Durchschnittstemperaturen für die verschiedenen Jahre auf,  \n"
        "wobei blau für eher kalte und rot für eher warme Jahre steht.")
    st.markdown("##")
    st.write(f)
    st.markdown("***")
    st.text("created with Python by Tobias Arnold, Quelle: Deutscher Wetterdienst")
        
if __name__ == "__main__":
  main()
