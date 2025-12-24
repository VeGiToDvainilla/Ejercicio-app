import streamlit as st
import time

# --- 1. CONFIGURACIÓN Y BASE DE DATOS ---
st.set_page_config(page_title="Entrenador Pro 2.0", page_icon="🏋️")

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

# --- 2. BARRA LATERAL (PANEL DE CONTROL) ---
with st.sidebar:
    st.header("🎛️ Panel de Ingeniero")
    
    # Configuración de Tiempos
    st.subheader("Tiempos")
    t_trabajo = st.slider("Tiempo Trabajo (seg)", 30, 90, 45, step=5)
    t_descanso = st.slider("Tiempo Descanso (seg)", 10, 120, 90, step=10)
    vueltas = st.number_input("Número de Vueltas", 1, 10, 3)
    
    st.markdown("---")
    
    # Selección de Modo
    modo = st.radio("Modo de Rutina", ["⚡ Rutina Rápida (Full Body)", "🛠️ Armar Rutina Personalizada"])

# --- 3. LÓGICA DE SELECCIÓN DE EJERCICIOS ---
rutina_final = []

st.title("🏋️ Arquitecto de Entrenamiento")

if modo == "⚡ Rutina Rápida (Full Body)":
    st.info("Rutina equilibrada pre-diseñada para cuerpo completo.")
    rutina_final = ["Sentadillas", "Lagartijas Clásicas", "Zancadas Atrás", "Superman", "Plancha Frontal"]
    
    # Mostrar la lista
    st.write("Tu circuito de hoy:")
    for i, ej in enumerate(rutina_final, 1):
        st.text(f"{i}. {ej}")

else: # Modo Personalizado
    st.success("Modo Constructor: Selecciona tus ejercicios del menú.")
    
    # Aplanar la lista de categorías para el selector
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

# --- 4. CALCULADORA DE TIEMPOS (PREDICCIÓN) ---
st.markdown("---")
st.subheader("⏱️ Estimación de Tiempos")

if len(rutina_final) > 0:
    # Variables constantes (estimadas)
    tiempo_calentamiento = 5 * 60  # 5 minutos
    tiempo_enfriamiento = 2 * 60   # 2 minutos
    
    # Cálculos matemáticos
    num_ejercicios = len(rutina_final)
    tiempo_por_ciclo_seg = num_ejercicios * (t_trabajo + t_descanso)
    tiempo_total_seg = (tiempo_por_ciclo_seg * vueltas) + tiempo_calentamiento + tiempo_enfriamiento
    
    # Función auxiliar para formato
    def seg_a_min(segundos):
        mins = segundos // 60
        return f"{mins} min"

    # Mostrar métricas
    col1, col2, col3 = st.columns(3)
    col1.metric("Tiempo por Vuelta", seg_a_min(tiempo_por_ciclo_seg))
    col2.metric("Tiempo Total Estimado", seg_a_min(tiempo_total_seg), f"{vueltas} vueltas")
    col3.metric("Series Totales", f"{num_ejercicios * vueltas}")

st.markdown("---")

# --- 5. MOTOR DE ENTRENAMIENTO (EJECUCIÓN) ---

# Control de estado (Session State)
if 'entrenando' not in st.session_state:
    st.session_state.entrenando = False

def iniciar_entrenamiento():
    st.session_state.entrenando = True

# Botón de Inicio
if st.button("▶️ INICIAR SISTEMA", on_click=iniciar_entrenamiento, type="primary"):
    if len(rutina_final) == 0:
        st.error("No hay ejercicios seleccionados.")
        st.stop()

# Lógica del cronómetro (Solo corre si el estado es True)
if st.session_state.entrenando:
    
    # Contenedores vacíos para la UI dinámica
    header_placeholder = st.empty()
    timer_placeholder = st.empty()
    bar_placeholder = st.progress(0)
    info_placeholder = st.empty()
    
    # A. CALENTAMIENTO
    header_placeholder.markdown("### 🔥 CALENTAMIENTO")
    info_placeholder.info("Prepara articulaciones: Cuello, Hombros, Cadera.")
    for i in range(5, 0, -1):
        timer_placeholder.markdown(f"<h1 style='text-align: center;'>Prepárate: {i}</h1>", unsafe_allow_html=True)
        time.sleep(1)

    # B. BUCLE PRINCIPAL
    total_ejercicios = len(rutina_final) * vueltas
    contador_global = 0
    
    for v in range(1, vueltas + 1):
        for ejercicio in rutina_final:
            contador_global += 1
            
            # --- FASE DE TRABAJO ---
            header_placeholder.markdown(f"### ⚔️ Vuelta {v}/{vueltas}: {ejercicio}")
            info_placeholder.warning(f"¡Dale duro! Mantén la técnica.")
            
            for t in range(t_trabajo, 0, -1):
                mins, secs = divmod(t, 60)
                # Formato HTML para números grandes
                timer_placeholder.markdown(
                    f"<h1 style='text-align: center; font-size: 80px; color: #FF4B4B;'>{mins:02d}:{secs:02d}</h1>", 
                    unsafe_allow_html=True
                )
                bar_placeholder.progress((t_trabajo - t) / t_trabajo)
                time.sleep(1)
            
            # --- FASE DE DESCANSO ---
            # Si NO es el último ejercicio absoluto, descansamos
            if contador_global < total_ejercicios:
                header_placeholder.markdown(f"### 💧 DESCANSO")
                info_placeholder.success(f"Recupérate.")
                
                for t in range(t_descanso, 0, -1):
                    mins, secs = divmod(t, 60)
                    timer_placeholder.markdown(
                        f"<h1 style='text-align: center; font-size: 80px; color: #4CAF50;'>{mins:02d}:{secs:02d}</h1>", 
                        unsafe_allow_html=True
                    )
                    bar_placeholder.progress((t_descanso - t) / t_descanso)
                    time.sleep(1)

    # C. FINALIZACIÓN
    header_placeholder.empty()
    timer_placeholder.markdown("<h1 style='text-align: center;'>🏆 ¡MISIÓN CUMPLIDA!</h1>", unsafe_allow_html=True)
    info_placeholder.info("No olvides estirar y comer tu proteína.")
    st.balloons()
    
    # Reset del estado para poder volver a empezar si se quiere
    st.session_state.entrenando = False
