# Contenido para: src/visualizacion.py

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns
import pandas as pd

def visualizar_datos(df):
    """
    Genera y MUESTRA un conjunto de visualizaciones avanzadas una por una.
    """
    print("\nMostrando visualizaciones... Cierra cada ventana para ver la siguiente.")
    
    # Estilo
    sns.set_theme(style="whitegrid", palette="muted")

    # Gráfico 1: Distribución de Edad de los Pacientes 
    sns.histplot(df['age'], kde=True, bins=30, color='skyblue')
    plt.title('Distribución de Edades de los Pacientes', fontsize=16)
    plt.xlabel('Edad', fontsize=12)
    plt.ylabel('Cantidad de Pacientes', fontsize=12)
    plt.tight_layout()
    plt.show() 

    #Gráfico 2: Conteo de Pacientes por Categoría de IMC 
    plt.figure(figsize=(10, 6))
    sns.countplot(y='Categoria_BMI', data=df, order=df['Categoria_BMI'].value_counts().index, palette='pastel')
    plt.title('Número de Pacientes por Categoría de IMC', fontsize=16)
    plt.xlabel('Cantidad de Pacientes', fontsize=12)
    plt.ylabel('Categoría de IMC', fontsize=12)
    plt.tight_layout()
    plt.show() 

    # Gráfico 3  Proporción de Pacientes con Diabetes
  
    plt.figure(figsize=(8, 8))
    counts = df['diabetes'].value_counts()
    labels = {1: 'Con Diabetes', 0: 'Sin Diabetes'}
    plt.pie(counts, labels=[labels[i] for i in counts.index], autopct='%1.1f%%', startangle=90, colors=["#86ed86","#f96060"])
    plt.title('Proporción de Pacientes con Diagnóstico de Diabetes', fontsize=16)
    plt.ylabel('')
    plt.show()

    


  
  



    print("\nFin de las visualizaciones.")



def grafico_riesgo_combinado(df):
    print("\nGráfico de riesgo combinado (Diabetes e Hipertensión)...")

    # --- Preparación de Datos específica para este gráfico ---
    def clasificar_riesgo(row):
        es_diabetico = row['diabetes'] == 1
        es_hipertenso = row['hypertension'] == 1
        
        if es_diabetico and es_hipertenso:
            return 'Diabetes + Hipertensión'
        elif es_hipertenso:
            return 'Solo Hipertensión'
        elif es_diabetico:
            return 'Solo Diabetes'
        else:
            return 'Ninguna de las dos'

    df_temp = df.copy()
    df_temp['Grupo_Riesgo_Combinado'] = df_temp.apply(clasificar_riesgo, axis=1)
    conteo_riesgo = df_temp['Grupo_Riesgo_Combinado'].value_counts()

    orden_grafico = ['Diabetes + Hipertensión', 'Solo Hipertensión', 'Solo Diabetes', 'Ninguna de las dos']
    datos_ordenados = conteo_riesgo.reindex(orden_grafico)
    colores = ["#FA2209", "#F89900", '#F1C40F', "#00B91F"] 
    explode = (0.1, 0, 0, 0) 

    plt.figure(figsize=(12, 8))
    plt.pie(
        datos_ordenados, 
        labels=datos_ordenados.index, 
        colors=colores,
        autopct='%1.1f%%',
        startangle=140,
        explode=explode,
        pctdistance=0.85,
        textprops={'fontsize': 12, 'color': 'white', 'weight': 'bold'}
    )

    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.title('Pacientes por riesgo combinado\n(Diabetes e Hipertensión)', fontsize=18, weight='bold')
    plt.axis('equal')  
    plt.legend(title="Grupos de riesgo", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.tight_layout()
    plt.show()

def analizar_poblacion_diabetica(df):
    # Filtrar solo pacientes con diabetes
    df_diabetes = df[df['diabetes'] == 1].copy()


    """Diabetes por Sexo y Tipo de Sangre"""

    # Configuración del gráfico
    plt.figure(figsize=(12, 7))
    sns.set_style("whitegrid")
    # Valores color

    sex_palette = {'Male': 'skyblue', 'Female': 'lightpink', 'Other': 'lightgreen'}
    # Orden explícito de los tipos de sangre
    blood_order = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

    ax1 = sns.countplot(
        data=df_diabetes,
        x='Blood Type',
        hue='sex',
        palette=sex_palette,
        order=blood_order
    )

    for p in ax1.patches:
        height = p.get_height()
        if height > 0:
            ax1.annotate(
                str(int(height)),
                (p.get_x() + p.get_width() / 2., height),
                ha='center',
                va='bottom',
                fontsize=9
            )

    plt.title("Pacientes con diabetes por sexo y tipo de sangre", fontsize=16, weight='bold')
    plt.xlabel("Tipo de sangre", fontsize=12)
    plt.ylabel("Cantidad de pacientes", fontsize=12)
    plt.legend(title="Sexo", labels=["Hombre", "Mujer", "Otro"], loc='upper right')
    plt.tight_layout()
    plt.show()

    print("Gráfico: Diabetes por grupo etario y sexo...")

    # Clasificar por grupo etario
    bins_edad = [0, 17, 39, 64, 100]
    labels_edad = ["Niño/Adolescente (0-17)", "Adulto joven (18-39)", "Adulto (40-64)", "Adulto mayor (65+)"]
    df_diabetes['Grupo_Etario'] = pd.cut(df_diabetes['age'], bins=bins_edad, labels=labels_edad, right=True)

    plt.figure(figsize=(10, 7))
    sns.set_style("whitegrid")

    ax2 = sns.countplot(
        data=df_diabetes,
        x='Grupo_Etario',
        hue='sex',
        palette={'Male': 'skyblue', 'Female': 'lightpink', 'Other': 'lightgreen'}
    )

    for p in ax2.patches:
        height = p.get_height()
        if height > 0:
            ax2.annotate(
                str(int(height)), 
                (p.get_x() + p.get_width() / 2., height), 
                ha='center', va='bottom', fontsize=9
            )

    plt.title("Pacientes con diabetes por grupo etario y sexo", fontsize=16, weight='bold')
    plt.xlabel("Grupo etario", fontsize=12)
    plt.ylabel("Cantidad de pacientes", fontsize=12)
    plt.legend(title="Sexo", labels=["Hombre", "Mujer", "Otro"], loc='upper right')
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.show()
    
    print("Análisis de población diabética finalizado.")

def mapa_hipertension (df):

    """ Genera un mapa de calor clínico de presión arterial, 
    permite visualizar de forma grafica que nivel de Hipertension
    se encuentran la mayoria de pacientes atendidos """
   
    sistolica = np.arange(90, 221, 1)
    diastolica = np.arange(40, 141, 1)
    sist, diast = np.meshgrid(sistolica, diastolica)
    categoria = np.zeros_like(sist, dtype=int)

    crisis_hipertensiva = (sist > 180) |(diast > 180) 
    categoria[crisis_hipertensiva] = 4

    hipertension_2 = ((sist >= 140) | (diast >= 90)) & (~crisis_hipertensiva)
    categoria[hipertension_2] = 3

    hipertension_1 = (((sist >= 130) & (sist <= 139)) | ((diast >= 80) & (diast <= 89))) & (~crisis_hipertensiva) & (~hipertension_2)
    categoria[hipertension_1] = 2

    presion_elev = ((sist >= 120) & (sist <= 129) & (diast < 80)) & (~crisis_hipertensiva) & (~hipertension_2) & (~hipertension_1)
    categoria[presion_elev] = 1

    fig, ax = plt.subplots(figsize=(8,6))

    grafica= ax.imshow(categoria, origin='lower',extent=(sistolica.min(), sistolica.max(), diastolica.min(), diastolica.max()),interpolation='nearest', aspect='auto')

    ax.set_xlabel('Sistólica (mmHg)')
    ax.set_ylabel('Diastólica (mmHg)')
    ax.set_title('Mapa de calor de presión arterial con pacientes')

    cbar = plt.colorbar(grafica, ax=ax, ticks=[0,1,2,3,4])
    cbar.ax.set_yticklabels(['Normal', 'Elevada', 'Hipertensión G1', 'Hipertensión G2', 'Crisis'])
    muestra = df.sample(1000, random_state=42)
    plt.scatter(muestra['systolic_bp'], muestra['diastolic_bp'],color='red', alpha=0.5, s=10, label='Pacientes')
    
    plt.legend()

    # Ajustar el diseño y mostrar
    plt.tight_layout()
    plt.show()


def grafica(df):
    informacion = []

    for _, fila in df.iterrows():
        edad = fila["age"]
        valor_colesterol = fila["cholesterol"]
        valor_presion = fila["hypertension"]
        valor_systolic = fila["systolic_bp"]
        valor_diabetes = fila["diabetes"]

        factor = 0

        if edad > 55:
            factor += 1
        if valor_colesterol > 200:
            factor += 1
        if valor_presion == 1 or valor_systolic >= 130:
            factor += 1
        if valor_diabetes == 1:
            factor += 1

        informacion.append({"Edad": edad, "Factores_Riesgo": factor})

    df_datos = pd.DataFrame(informacion)

    plt.figure(figsize=(8,5))
    plt.scatter(df_datos["Edad"], df_datos["Factores_Riesgo"], color="royalblue")
    plt.title("Relación entre Edad y Factores de Riesgo Coronario")
    plt.xlabel("Edad")
    plt.ylabel("Factores de Riesgo")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

  






