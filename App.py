
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

@app.route("/")
def inicio_sesion():
    return render_template("registro.html")

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    codigo = request.form["codigo"]

    if usuario and codigo:  # validación básica
        return redirect(url_for("pagina_principal"))
    else:
        return redirect(url_for("inicio_sesion"))

@app.route("/principal")
def pagina_principal():
    # Cargar y procesar datos
    data = pd.read_excel("indicador31.xlsx")
    data.columns = data.columns.str.strip()

    # Gráfico 1: Barras por región
    fig1 = px.bar(data, 
                 x="Región(es) en la que se implementa",
                 title="Cantidad de iniciativas por región",
                 labels={"x": "Región", "count": "Cantidad"},
                 color="Región(es) en la que se implementa")

    # Gráfico 2: Pie de estados
    fig2 = px.pie(data, 
                 names="Estado del proceso", 
                 title="Distribución de los estados del proceso")

    # Gráfico 3: Sostenibilidad
    conteo_sostenibilidad = data["¿La iniciativa tiene una forma de hacer seguimiento o estrategia de sostenibilidad?"].value_counts().reset_index()
    conteo_sostenibilidad.columns = ["Tiene_sostenibilidad", "Cantidad"]
    fig3 = px.bar(conteo_sostenibilidad,
                 x="Tiene_sostenibilidad",
                 y="Cantidad",
                 text_auto=True,
                 title="Estrategia de sostenibilidad en iniciativas",
                 labels={"Tiene_sostenibilidad": "¿Tiene sostenibilidad?", "Cantidad": "Cantidad"})

    # Renombrar columnas 
    data.rename(columns={
        "Participantes directos (OSIGD)": "Participantes",
        "Región(es) en la que se implementa": "Region",
        "Periodo de implementación": "Periodo",
        "Población objetivo de la iniciativa": "Estrato"
    }, inplace=True)

    # Gráfico 4: Participantes por región
    region_participantes = data.groupby("Region")["Participantes"].sum().reset_index()
    fig4 = px.bar(region_participantes,
                  x="Participantes",
                  y="Region",
                  text_auto=True,
                  title="Total de Participantes OSIGD por Región",
                  text="Participantes",
                  labels={"Participantes": "N° de Participantes"},
                  template="plotly_white")
    fig4.update_traces(textposition="outside")

    # Gráfico 5: Participantes por región y población
    cruce_region_poblacion = data.groupby(["Region", "Estrato"])["Participantes"].sum().reset_index()
    fig5 = px.bar(cruce_region_poblacion,
                  x="Region",
                  y="Participantes",
                  color="Estrato",
                  text_auto=True,
                  barmode="group",
                  title="Participantes por Región y Población Objetivo",
                  labels={"Participantes": "N° de Participantes"},
                  template="plotly_white")

    # Gráfico 6: grafico de dispersion 3D
    data["Poblacion_objetivo"] = pd.factorize(data["Estrato"])[0]
    fig6 = px.scatter_3d(data,
                        x="Poblacion_objetivo",
                        y="Participantes",
                        z="Periodo",
                        color="Region",
                        hover_name="Estrato",
                        title="Participantes por Población Objetivo",
                        labels={"Participantes": "N° de Participantes"},
                        template="plotly_dark")

    # Gráfico 7: Grafico de Línea 3D
    totalizados = data.groupby(["Region","Estrato"])["Participantes directos (mujeres)"].sum().reset_index()
    top = totalizados.sort_values("Estrato", ascending=False).head(10)
    top["Trazabilidad"] = "Escala"
    fig7 = px.line_3d(top, 
                     x="Region", 
                     y="Participantes directos (mujeres)",
                     z="Estrato",
                     color="Trazabilidad",
                     color_discrete_sequence=["Green"])

    # Convertir gráficos a HTML
    graphs = {
        "graph1": pio.to_html(fig1, full_html=False),
        "graph2": pio.to_html(fig2, full_html=False),
        "graph3": pio.to_html(fig3, full_html=False),
        "graph4": pio.to_html(fig4, full_html=False),
        "graph5": pio.to_html(fig5, full_html=False),
        "graph6": pio.to_html(fig6, full_html=False),
        "graph7": pio.to_html(fig7, full_html=False)
    }
    
    return render_template("principal.html", **graphs)

if __name__ == "__main__":
    app.run(debug=True)



