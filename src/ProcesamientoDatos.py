import pandas as pd


def cargar_y_preparar_datos(ruta):
    try:
        df = pd.read_csv(ruta)
    except FileNotFoundError:
        print(f"No se encontró el archivo en la ruta: {ruta}")
        return None

    # Validar que las columnas necesarias existan
    columnas_necesarias = ["age", "bmi", "patient_id", "Name", "systolic_bp", "diastolic_bp", 
                          "cholesterol", "hypertension", "diabetes", "glucose", "creatinine"]
    for col in columnas_necesarias:
        if col not in df.columns:
            print(f"Error: la columna '{col}' no está en el dataset.")
            return None

    # Clasificación por edad
    Grupo_etario_lista = []
    Categoria_bmi_lista = []

    for i, row in df.iterrows():
        edad = row["age"]
        if edad < 18:
            Grupo_etario_lista.append("Niño/Adolescente")
        elif 18 <= edad < 40:
            Grupo_etario_lista.append("Adulto Joven")
        elif 40 <= edad < 65:
            Grupo_etario_lista.append("Adulto")
        else:
            Grupo_etario_lista.append("Adulto Mayor")

        bmi = row['bmi']
        if bmi < 18.5:
            Categoria_bmi_lista.append("Bajo Peso")
        elif 18.5 <= bmi < 25:
            Categoria_bmi_lista.append("Normal")
        elif 25 <= bmi < 30:
            Categoria_bmi_lista.append("Sobrepeso")
        else:
            Categoria_bmi_lista.append("Obesidad")

    df["Grupo_Etario"] = Grupo_etario_lista
    df["Categoria_BMI"] = Categoria_bmi_lista

    return df


def buscar_paciente(df, patient_id=None, nombre_completo=None):
    """
    Busca un paciente por su ID o por su nombre completo en la columna 'name'.
    La búsqueda por nombre no es sensible a mayúsculas.
    """
    if df is None:
        print("Error: el DataFrame está vacío o no se cargó correctamente.")
        return None

    if patient_id is not None:
        paciente = df[df['patient_id'] == patient_id]
        if not paciente.empty:
            print(f"\nPaciente encontrado por ID: {patient_id}")
            return paciente.iloc[0]
        else:
            print(f"\nNo se encontró paciente con ID: {patient_id}")

    if nombre_completo is not None:
        paciente = df[df['Name'].str.lower() == nombre_completo.lower()]
        if not paciente.empty:
            print(f"\nPaciente encontrado por nombre: '{nombre_completo}'")
            return paciente.iloc[0]
        else:
            print(f"\nNo se encontró paciente con nombre: '{nombre_completo}'")

    return None



#Riesgos Cardiovasculares y de Circulación-----------------------------------------------------------
print("="*60)
print("Riesgos Cardiovasculares y de Circulación")
print("="*60)

def evaluar_hipertension(paciente):
    """1. Evalúa la presión arterial y la clasifica por etapas."""
    sistolica, diastolica = paciente['systolic_bp'], paciente['diastolic_bp']
    
    if sistolica > 180 or diastolica > 120:
        return "Crisis Hipertensiva", "Atención Médica de Emergencia"
    elif sistolica >= 140 or diastolica >= 90:
        return "Hipertensión Grado 2", "Cardiólogo"
    elif 130 <= sistolica <= 139 or 80 <= diastolica <= 89:
        return "Hipertensión Grado 1", "Cardiólogo"
    elif 120 <= sistolica <= 129 and diastolica < 80:
        return "Presión Arterial Elevada", "Monitoreo y cambios en estilo de vida"
    else:
        return "Presión Arterial Normal", None


print("Riesgo de Enfermedad Coronaria (Aterosclerosis)")

""""Evalúa el riesgo de enfermedad coronaria (aterosclerosis) contando factores de riesgo clave.
    Lógica basada en tu propuesta."""

def evaluar_riesgo_coronario(paciente):
    factores = 0
    factores_encontrados = []

    # Análisis Edad
    if paciente["age"] > 55:
        factores += 1
        factores_encontrados.append("Edad > 55")
    # Análisis colesterol
    if paciente["cholesterol"] > 200:
        factores += 1
        factores_encontrados.append("Colesterol mayor a 200")
    # Análisis de Presión
    if paciente["hypertension"] == 1 or paciente["systolic_bp"] >= 130:
        factores += 1
        factores_encontrados.append("Presión alta")
    # Diabetes
    if paciente["diabetes"] == 1:
        factores += 1
        factores_encontrados.append("Diabetes")
    
    # Nivel de riesgo
    
    if factores >= 3:
        riesgo = "Alto"
    elif factores == 2:
        riesgo = "Moderado"
    else:
        riesgo = "Bajo"

    descripcion = f"Riesgo de Enfermedad Coronaria: {riesgo} ({factores}/4 factores: {', '.join(factores_encontrados)})"

    # Agrega una recomendación acorde
    if riesgo == "Alto":
        recomendacion = "Cardiólogo"
    elif riesgo == "Moderado":
        recomendacion = "Revisión médica general"
    else:
        recomendacion = None

    return descripcion, recomendacion




#Trastornos Metabólicos------------------------------------------------------------------------------
print("="*60)
print("Trastornos Metabólicos")
print("="*60)

def evaluar_glucosa(paciente):
    """3. Evalúa el estado de la glucosa para detectar Prediabetes o Diabetes."""
    glucosa = paciente['glucose']
    
    if paciente['diabetes'] == 1:
        return "Diagnóstico Previo de Diabetes", "Endocrinólogo"
    elif glucosa >= 126:
        return "Posible Diabetes (Glucosa en ayunas alta)", "Endocrinólogo"
    elif 100 <= glucosa < 126:
        return "Posible Prediabetes", "Médico Internista / Nutricionista"
    else:
        return "Glucosa Normal", None
    
"""def clasificar_glucosa(df):
    normales = []
    prediabetes = []
    nuevo_diabetes = []
    con_diabetes = []

    for _, fila in df.iterrows():
        id_paciente = fila ["patient_id"]
        valor_glucosa = fila ["glucose"]
        diag_diabetes = fila ["diabetes"]

        if valor_glucosa < 140 and diag_diabetes == 0:
            normales.append((id_paciente, valor_glucosa))
        elif 140 <= valor_glucosa < 200 and diag_diabetes == 0:
            prediabetes.append((id_paciente, valor_glucosa))
        elif 200 <= valor_glucosa and diag_diabetes == 0:
            nuevo_diabetes.append((id_paciente, valor_glucosa))
        else:
            con_diabetes.append((id_paciente, valor_glucosa))
        
    df_normales = pd.DataFrame(normales, columns=["patient_id", "glucose"])
    df_prediabetes = pd.DataFrame(prediabetes, columns=["patient_id", "glucose"])
    df_nuevo_diabetes = pd.DataFrame(nuevo_diabetes, columns=["patient_id", "glucose"])
    df_con_diabetes = pd.DataFrame(con_diabetes, columns=["patient_id", "glucose"])

    return df_normales, df_prediabetes, df_nuevo_diabetes, df_con_diabetes  

df_normales, df_prediabetes, df_nuevo_diabetes, df_con_diabetes = clasificar_glucosa(df)
print("="*60)
print("PACIENTES CLASIFICADOS MEDICIÓN DE GLUCOSA")
print("="*60)

print("Cantidad de pacientes normales:", len(df_normales))
print("Normales:")
print(df_normales.head(20), "\n")

print("Cantidad de pacientes con prediabetes:", len(df_prediabetes))
print("Prediabetes:")
print(df_prediabetes.head(), "\n")

print("Cantidad de pacientes con nuevo diagnóstico de diabetes:", len(df_nuevo_diabetes))
print("Recien diagnosticados con Diabetes:")
print(df_nuevo_diabetes.head(), "\n")

print("Cantidad de pacientes con diabetes diagnosticada:", len(df_con_diabetes))
print("Prediagnosticados con Diabetes:")
print(df_con_diabetes.head(), "\n")"""

def evaluar_sindrome_metabolico(paciente):
    """Evalúa si el paciente cumple criterios para Síndrome Metabólico."""
    factores = 0
    
    if paciente['Categoria_BMI'] == "Obesidad": factores += 1
    if paciente['systolic_bp'] >= 130 or paciente['diastolic_bp'] >= 85: factores += 1
    if paciente['glucose'] >= 100: factores += 1
    if paciente['cholesterol'] > 200: factores += 1 # Usamos colesterol total como proxy
    
    if factores >= 3:
        return "Alto Riesgo de Síndrome Metabólico", "Endocrinólogo y Cardiólogo"
    return None, None

# Riesgo de Enfermedad Renal-------------------------------------------------------------
print("="*60)
print("Riesgo de Enfermedad Renal")
print("="*60)
def evaluar_riesgo_renal(paciente):
    """5. Evalúa el riesgo de Enfermedad Renal Crónica (ERC)."""
    if paciente['creatinine'] > 1.3:
        if paciente['diabetes'] == 1 or paciente['hypertension'] == 1:
            return "Riesgo Renal Crítico (agravado por comorbilidades)", "Nefrólogo"
        else:
            return "Riesgo Renal (Creatinina elevada)", "Nefrólogo"
    return None, None

cargar_y_preparar_datos("EC03/GESTOR DE EXPEDIENTES CLÍNICOS Y ANALIZADOR DE SALUD/data/dataset_final.csv")


#Informe final------------------------------------------------------------------------------
def generar_informe_paciente(paciente):
    """
    Llama a todas las funciones de evaluación y genera un informe consolidado.
    """
    print(f"\n--- INFORME DE SALUD PARA EL PACIENTE ID: {int(paciente['patient_id'])} ---")
    print("-" * 60)
    
    riesgos = []
    recomendaciones = set() # Usamos un set para evitar especialistas duplicados

    # Ejecutar cada una de las 5 evaluaciones
    evaluaciones = [
        evaluar_riesgo_coronario(paciente),
        evaluar_sindrome_metabolico(paciente),
        evaluar_riesgo_renal(paciente),
        evaluar_glucosa(paciente),
        evaluar_hipertension(paciente)

    ]

    for resultado in evaluaciones:
    # Verificar que resultado sea una tupla o lista de tamaño 2
        if isinstance(resultado, (tuple, list)) and len(resultado) == 2:
            riesgo, recomendacion = resultado
        else:
            print("Error: una función no devolvió una tupla de 2 elementos, se ignora:", resultado)
            continue

    if riesgo:
        riesgos.append(riesgo)
    if recomendacion:
        recomendaciones.add(recomendacion)

            
    print("[ RESULTADOS Y RIESGOS DETECTADOS ]")
    for r in riesgos:
        print(f"- {r}")
        
    print("\n[ RECOMENDACIONES ]")
    if recomendaciones:
        for rec in sorted(list(recomendaciones)):
            print(f"- Se sugiere consulta con: {rec}")
    else:
        print("- Mantener controles de rutina y estilo de vida saludable.")
    print("-" * 60)



