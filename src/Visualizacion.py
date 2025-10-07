# Contenido para: src/visualizacion.py

import matplotlib.pyplot as plt
import seaborn as sns

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
    plt.pie(counts, labels=[labels[i] for i in counts.index], autopct='%1.1f%%', startangle=90, colors=['#ff6666','#99ff99'])
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