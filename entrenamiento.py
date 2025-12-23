import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Ingeniería Corporal", layout="centered")

st.title("🏗️ Cronograma de Entrenamiento")
st.markdown("### Planificación Estructural del Cuerpo")

# --- BARRA LATERAL (CONTROLES) ---
st.sidebar.header("Parámetros de Diseño")

# Selector de hora de inicio
hora_inicio_input = st.sidebar.time_input("Hora de Inicio", datetime.now())

# Sliders para ajustar tiempos
descanso_segundos = st.sidebar.slider("Tiempo de Descanso (seg)", 30, 180, 90, step=15)
num_vueltas = st.sidebar.slider("Número de Vueltas (Circuitos)", 1, 5, 3)

# Botón para mostrar guía visual
mostrar_guia = st.sidebar.checkbox("Ver Guía de Ejercicios", value=True)

# --- LÓGICA DEL CRONOGRAMA ---
def generar_datos():
    # Convertir el input de hora a un objeto datetime completo para poder sumar
    now = datetime.now()
    tiempo_actual = datetime.combine(now.date(), hora_inicio_input)
    
    cronograma = []
    
    # Duraciones estimadas (en segundos)
    duracion_ejercicio = 45
    transicion = 60
    
    # 1. CALENTAMIENTO
    actividades_calentamiento = [
        ("Movilidad Articular", 120),
        ("Gato-Vaca (Columna)", 60),
        ("Jumping Jacks (Tijeras)", 60),
        ("Rotaciones (Cadera/Muñeca)", 60)
    ]
    
    for nombre, duracion in actividades_calentamiento:
        cronograma.append({
            "Fase": "Calentamiento",
            "Hora": tiempo_actual.strftime("%H:%M:%S"),
            "Actividad": nombre,
            "Duración": f"{duracion//60} min" if duracion >= 60 else f"{duracion} seg"
        })
        tiempo_actual += timedelta(seconds=duracion)

    # Transición
    tiempo_actual += timedelta(seconds=transicion)

    # 2. CIRCUITO DE FUERZA
    ejercicios_fuerza = [
        ("Sentadillas", "12-15 reps"),
        ("Lagartijas", "8-12 reps"),
        ("Zancadas", "10-12/pierna"),
        ("Superman", "15 reps"),
        ("Plancha", "45 seg")
    ]
    
    for vuelta in range(1, num_vueltas + 1):
        for nombre, detalle in ejercicios_fuerza:
            # Ejercicio
            cronograma.append({
                "Fase": f"Circuito {vuelta}",
                "Hora": tiempo_actual.strftime("%H:%M:%S"),
                "Actividad": f"💪 {nombre}",
                "Duración": detalle
            })
            tiempo_actual += timedelta(seconds=duracion_ejercicio)
            
            # Descanso
            cronograma.append({
                "Fase": f"Circuito {vuelta}",
                "Hora": tiempo_actual.strftime("%H:%M:%S"),
                "Actividad": "💤 Descanso (Recarga)",
                "Duración": f"{descanso_segundos} seg"
            })
            tiempo_actual += timedelta(seconds=descanso_segundos)

    # 3. ENFRIAMIENTO
    tiempo_actual += timedelta(seconds=transicion)
    cronograma.append({
        "Fase": "Enfriamiento",
        "Hora": tiempo_actual.strftime("%H:%M:%S"),
        "Actividad": "🧘 Estiramientos",
        "Duración": "5 min"
    })
    
    # Calcular fin
    tiempo_final = tiempo_actual + timedelta(minutes=5)
    
    return cronograma, tiempo_final

# Generar datos
data, hora_fin = generar_datos()
df = pd.DataFrame(data)

# --- MOSTRAR RESULTADOS ---

# 1. Métricas Clave
col1, col2, col3 = st.columns(3)
col1.metric("Inicio", hora_inicio_input.strftime("%H:%M"))
col2.metric("Fin Estimado", hora_fin.strftime("%H:%M"))
col3.metric("Proteína Post-Entreno", "25-30g")

# 2. Tabla del Cronograma
st.subheader("📅 Tu Ruta Crítica de Hoy")
# Usamos un estilo para resaltar los descansos
def color_rows(row):
    if "Descanso" in row["Actividad"]:
        return ['background-color: #e0f7fa; color: black'] * len(row)
    elif "Circuito" in row["Fase"]:
        return ['background-color: #fff3e0; color: black'] * len(row)
    return [''] * len(row)

st.dataframe(df.style.apply(color_rows, axis=1), use_container_width=True)

# --- SECCIÓN VISUAL (GUÍA) ---
if mostrar_guia:
    st.markdown("---")
    st.subheader("📘 Guía Técnica de Ejercicios")
    
    tab1, tab2 = st.tabs(["Gato-Vaca", "Tijeras (Jumping Jacks)"])
    
    with tab1:
        st.markdown("**Objetivo:** Movilidad de columna.")
        st.info("Inhala al arquear (mirada arriba), exhala al encorvar (mirada al ombligo).")
        # Aquí podrías poner st.image("url_imagen") si la tienes
        
    with tab2:
        st.markdown("**Objetivo:** Elevar ritmo cardíaco.")
        st.info("Coordina: Abre piernas y brazos arriba al mismo tiempo. Cae sobre puntas de pies.")

# Nota final
st.caption("Generado con Python para optimización metabólica.")