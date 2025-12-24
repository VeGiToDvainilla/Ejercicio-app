import streamlit as st
import time

# --- 1. CONFIGURACIÓN Y BASE DE DATOS ---
st.set_page_config(page_title="Entrenador Pro 3.1", page_icon="🔥")

# Diccionario de ejercicios
DB_EJERCICIOS = {
    "🔥 Tren Inferior (Piernas)": [
        "Sentadillas", "Zancadas Atrás", "Sentadilla Búlgara", 
        "Puente de Glúteos", "Sentadilla Isométrica (Pared)"
    ],
    "💪 Tren Superior (Empuje)": [
        "Lagartijas Clásicas", "Lagartijas Diamante", 
        "Fondos (Dips) en silla", "Pike Pushups (Hombro)"
    ],
    "🧗 Tren Superior (Tracción/Espalda)": [
        "Superman (Lumbares)", "Remo en mesa", "Toalla en puerta", 
        "Ángel de nieve inverso"
    ],
    "🍫 Core (Abdomen)": [
        "Plancha Frontal", "Plancha Lateral", "Mountain Climbers", 
        "Leg Raises (Elevación piernas)", "Russian Twist"
    ],
    "🫀 Cardio / Metabólico": [
        "Jumping Jacks", "Burpees", "Rodillas al Pecho", "Salto de Cuerda Fantasma"
    ]
}

# Rutina de Calentamiento (Estándar para todos)
RUTINA_CALENTAMIENTO = [
    ("Movilidad Articular (Cuello/Hombros)", 45),
    ("Gato-Vaca (Columna)", 45),
    ("Jumping Jacks (Activación)", 60)
]

# --- 2. BARRA LATERAL (PANEL DE CONTROL) ---
with st.sidebar:
    st.header("🎛️ Panel de Ingeniero")
    
    # Configuración de Tiempos
    st.subheader("Tiempos")
    t_trabajo = st.slider("Tiempo Trabajo (seg)", 20, 90, 45, step=5)
    t_descanso = st.slider("Tiempo Descanso (seg)", 10, 120, 90, step=10)
    vueltas = st.number_input("Número de Vueltas", 1, 10, 3)
    
    st.markdown("---")
    
    # Selección de Modo
    modo = st.radio("Modo de Rutina", ["⚡ Rutina Rápida (Full Body)", "🛠️ Armar Rutina Personalizada"])

# --- 3. LÓGICA DE SELECCIÓN DE EJERCICIOS ---
rutina_final = []

st.title("🔥 Sistema de Entrenamiento")

if modo == "⚡ Rutina Rápida (Full Body)":
    st.info("Rutina equilibrada pre-diseñada para cuerpo completo.")
    rutina_final = ["Sentadillas", "Lagartijas Clásicas", "Zancadas Atrás", "Superman", "Plancha Frontal"]
    
    st.write("Tu circuito de hoy:")
    for i, ej in enumerate(rutina_final, 1):
        st.text(f"{i}. {ej}")

else: # Modo Personalizado
    st.success("Modo Constructor: Selecciona tus ejercicios del menú.")
    
    todos_los_ejercicios = []
    for categoria, lista in DB_EJERCICIOS.items():
        todos_los_ejercicios.extend(lista)
        
    seleccion = st.multiselect(
        "Selecciona los ejercicios en orden:",
        options=todos_los_ejercicios,
        default=["Sentadillas", "Lagartijas Clásicas"]
    )
    rutina_final = seleccion
    
    if len(rutina_final) == 0:
        st.warning("⚠️ Por favor selecciona al menos 1 ejercicio.")

# --- 4. CALCULADORA DE TIEMPOS ---
st.markdown("---")
st.subheader("⏱️ Estimación de Tiempos")

if len(rutina_final) > 0:
    # Calcular tiempo de calentamiento (suma de la lista fija)
    tiempo_calentamiento = sum([t for n, t in RUTINA_CALENTAMIENTO])
    tiempo_enfriamiento = 120 # 2 min estiramiento
    
    num_ejercicios = len(rutina_final)
    tiempo_por_ciclo = num_ejercicios * (t_trabajo + t_descanso)
    tiempo_total = tiempo_calentamiento + (tiempo_por_ciclo * vueltas) + tiempo_enfriamiento
    
    def fmt(seg): return f"{seg // 60} min {seg % 60} s"

    col1, col2, col3 = st.columns(3)
    col1.metric("Fase Calentamiento", fmt(tiempo_calentamiento))
    col2.metric("Tiempo Total", fmt(tiempo_total), f"{vueltas} vueltas")
    col3.metric("Fase Fuerza", fmt(tiempo_por_ciclo * vueltas))

st.markdown("---")

# --- 5. MOTOR DE ENTRENAMIENTO ---

if 'entrenando' not in st.session_state:
    st.session_state.entrenando = False

def iniciar():
    st.session_state.entrenando = True

if st.button("▶️ INICIAR SISTEMA", on_click=iniciar, type="primary"):
    if len(rutina_final) == 0:
        st.error("Selecciona ejercicios primero.")
        st.stop()

if st.session_state.entrenando:
    
    # Placeholders
    header_ph = st.empty()
    timer_ph = st.empty()
    bar_ph = st.progress(0)
    info_ph = st.empty()
    
    # --- FASE 1: CALENTAMIENTO GUIADO ---
    header_ph.markdown("### 🌡️ FASE 1: CALENTAMIENTO")
    info_ph.info("Preparamos el sistema. Movimientos suaves.")
    
    # Conteo regresivo inicial
    for i in range(5, 0, -1):
        timer_ph.markdown(f"<h1 style='text-align: center; color: gray;'>Inicio en: {i}</h1>", unsafe_allow_html=True)
        time.sleep(1)

    # Bucle de Ejercicios de Calentamiento
    for nombre, duracion in RUTINA_CALENTAMIENTO:
        header_ph.markdown(f"### 🌡️ Calentamiento: {nombre}")
        
        # AQUÍ ESTABA EL ERROR: Asegúrate de copiar toda esta línea
        for t in range(duracion, 0, -1):
            mins, secs = divmod(t, 60)
            timer_ph.markdown(
                f"<h1 style='text-align: center; font-size: 80px; color: #FF9800;'>{mins:02d}:{secs:02d}</h1>", 
                unsafe_allow_html=True
            )
            bar
