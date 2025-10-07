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