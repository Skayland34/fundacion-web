import pandas as pd
import plotly.express as px

# Carga del archivo Excel
data = pd.read_excel("indicador31.xlsx")

# Eliminar espacios en nombres de columnas
data.columns = data.columns.str.strip()

# Ver columnas para identificar correctamente las que quieres analizar
print(data.columns)



fig = px.bar(data, 
             x='Región(es) en la que se implementa', 
             title='Cantidad de iniciativas por región',
             labels={'x': 'Región', 'count': 'Cantidad'},
             color='Región(es) en la que se implementa')
fig.show()


fig = px.pie(data, 
             names='Estado del proceso', 
             title='Distribución de los estados del proceso')
fig.show()


conteo_sostenibilidad = data['¿La iniciativa tiene una forma de hacer seguimiento o estrategia de sostenibilidad?'].value_counts().reset_index()
conteo_sostenibilidad.columns = ['Tiene_sostenibilidad', 'Cantidad']


fig = px.bar(conteo_sostenibilidad,
             x='Tiene_sostenibilidad',
             y='Cantidad',
             title='Estrategia de sostenibilidad en iniciativas',
             labels={'Tiene_sostenibilidad': '¿Tiene sostenibilidad?', 'Cantidad': 'Cantidad'})
fig.show()


data.rename(columns={
    'Participantes directos (OSIGD)': 'Participantes',
    'Región(es) en la que se implementa': 'Region',
    'Periodo de implementación': 'Periodo',
    'Población objetivo de la iniciativa': 'PoblacionObjetivo'
}, inplace=True)

region_participantes = data.groupby('Region')['Participantes'].sum().reset_index()

fig1 = px.bar(region_participantes,
              x='Region',
              y='Participantes',
              title='Total de Participantes OSIGD por Región',
              text='Participantes',
              labels={'Participantes': 'N° de Participantes'},
              template='plotly_white')
fig1.update_traces(textposition='outside')
fig1.show()


cruce_region_poblacion = data.groupby(['Region', 'PoblacionObjetivo'])['Participantes'].sum().reset_index()

fig3 = px.bar(cruce_region_poblacion,
              x='Region',
              y='Participantes',
              color='PoblacionObjetivo',
              barmode='group',
              title='Participantes por Región y Población Objetivo',
              labels={'Participantes': 'N° de Participantes'},
              template='plotly_white')
fig3.show()

data['Poblacion_objetivo'] = pd.factorize(data['PoblacionObjetivo'])[0]

fig = px.scatter_3d(data,
                    x='Poblacion_objetivo',
                    y='Participantes',
                    z='Periodo',  # o cualquier otra columna numérica o codificada
                    color='Region',
                    hover_name='PoblacionObjetivo',
                    title='Participantes por Población Objetivo',
                    labels={'Participantes': 'N° de Participantes'},
                    template='plotly_dark')
fig.show()

#fig.write_html("grafico3d.html")

totalizados=data.groupby(["Region","PoblacionObjetivo"])["Participantes directos (mujeres)"].sum().reset_index()
top = totalizados.sort_values("PoblacionObjetivo", ascending=False).head(10)
top["Trazabilidad"]="Escala"
top


figu_linea = px.line_3d(top, x="Region", y="Participantes directos (mujeres)",z="PoblacionObjetivo",color="Trazabilidad",color_discrete_sequence=["Green"])

#figu_linea.write_html("Grafico linea 3d.html")
figu_linea.show()