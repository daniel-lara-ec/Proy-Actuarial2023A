from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import json
from .forms import FormularioSeguro
from pyliferisk import MortalityTable,Actuarial,Ax,Axn,nEx
import numpy as np
import plotly.graph_objects as go
# get 404
from django.shortcuts import get_object_or_404

archivo = '/home/azureuser/myprojectdir/static/files/Mortalidad_Amazonia.xlsx'


def Procesodf(df):
    json_df = df.reset_index().to_json(orient="records")
    df_json_export = json.loads(json_df)
    return df_json_export

def Home(request):
    return render(
        request,
        "index.html"
)

def Indicadores(request):
    return render(
        request,
        "indicadores.html"
)

def Calculadora(request):
    if request.method == 'POST':

        sexo = request.POST.get('sexo')
        edad = request.POST.get('edad')
        cobertura_fallecimiento = request.POST.get('cobertura_fallecimiento')
        cobertura_supervivencia = request.POST.get('cobertura_supervivencia')
        cuantia = request.POST.get('cuantia')
        interes = request.POST.get('interes')

        if sexo == 'M':
            tabla = pd.read_excel(archivo,sheet_name='Mortalidad Hombres')
            tabla = list(tabla['qxH_SA'].values)
            
        else:
            tabla = pd.read_excel(archivo,sheet_name='Mortalidad Mujeres')
            tabla = list(tabla['qxM_SA'].values)

        tabla.insert(0, 0)
        tabla = [x*1000 for x in tabla]

        interes = float(interes)/100
        tariff = Actuarial(nt=tabla,i=interes)

        seguro_entera = np.round(float(cuantia)*Ax(tariff, int(edad)),2)
        seguro_temporal = np.round(float(cuantia)*Axn(tariff, int(edad), n=int(cobertura_fallecimiento)),2)
        seguro_supervivencia = np.round(float(cuantia)*nEx(tariff, int(edad),int(cobertura_supervivencia)),2)

        return render(
            request,
            'seguro.html',
            {'seguro_entera': seguro_entera,
             'seguro_temporal': seguro_temporal,
             'seguro_supervivencia': seguro_supervivencia})
    else:
        return render(
            request,
            'calculadora.html',
            {'form': FormularioSeguro()}
        )

def Tabla(request):
    df_hombres = pd.read_excel(archivo,sheet_name="Mortalidad Hombres")
    df_mujeres = pd.read_excel(archivo,sheet_name="Mortalidad Mujeres")

    return render(
        request,
        'tabla.html',
        {
            'df_hombres': Procesodf(df_hombres),
            'df_mujeres': Procesodf(df_mujeres)
        }
    )

def Descargar(request):

    df_hombres = pd.read_excel(archivo,sheet_name="Mortalidad Hombres")
    df_mujeres = pd.read_excel(archivo,sheet_name="Mortalidad Mujeres")

    response = HttpResponse(content_type="application/xlsx")
    response["Content-Disposition"] = f'attachment; filename="tabla_mortalidad.xlsx"'
    with pd.ExcelWriter(response) as writer:
        df_hombres.to_excel(writer, sheet_name="Mortalidad Hombres", index=False)
        df_mujeres.to_excel(writer, sheet_name="Mortalidad Mujeres", index=False)

    return response

def Grafica(request):

    df_hombres = pd.read_excel(archivo,sheet_name="Mortalidad Hombres")
    df_mujeres = pd.read_excel(archivo,sheet_name="Mortalidad Mujeres")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df_hombres["Edad"], y=df_hombres["qxH_SA"], name="Hombres")
    )
    fig.add_trace(
        go.Scatter(x=df_mujeres["Edad"], y=df_mujeres["qxM_SA"], name="Mujeres")
    )
    
    fig.update_layout(
        title="Probabilidades de fallecimiento por edad",
        xaxis_title="Edad",
        yaxis_title="Probabilidad de fallecimiento",
        legend_title="",
        font=dict(family="Poppins", size=14, color="black"),
    )

    grafica = fig.to_html()

    return render(
        request,
        'graficas.html',
        {
            'grafica': grafica
        }
    )