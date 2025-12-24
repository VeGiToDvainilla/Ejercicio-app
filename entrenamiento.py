import streamlit as st
import time

# --- 1. CONFIGURACIÓN Y BASE DE DATOS ---
st.set_page_config(page_title="Entrenador Pro Final", page_icon="💪")

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

# Rutina de Calentamiento (Estándar)
RUTINA_CALENTAMIENTO = [
    ("Movilidad Articular", 45),
    ("Gato-Vaca (Columna)", 45),
    ("Jumping Jacks", 60)
]

# --- 2. BARRA LATERAL (CONFIGURACIÓN) ---
with st.sidebar:
    st.header("🎛️ Panel de Control")
    
    # Tiempos
    st.subheader("Configuración de Tiempos")
    t_trabajo = st.slider("Tiempo Trabajo (seg)", 20, 90, 45, step=5)
    t_descanso = st.slider("Tiempo Descanso (seg)", 10, 120, 90, step=10)
    vueltas = st.number_input("Número de Vueltas", 1, 10, 3)
    
    st.markdown("---")
    
    # Modo
    modo = st.radio("Modo de Rutina", ["⚡ Rutina Rápida", "🛠️ Personalizada"])

# --- 3. SELECCIÓN DE EJERCICIOS ---
rutina_final = []

st.title("🔥 Sistema de Entrenamiento")

if modo == "⚡ Rutina Rápida":
    st.info("Rutina Full Body estándar activada.")
    rutina_final = ["Sentadillas", "Lagartijas Clásicas", "Zancadas Atrás", "Superman", "Plancha Frontal"]
    
    st.write("📋 **Circuito de hoy:**")
    for i, ej in enumerate(rutina_final, 1):
        st.text(f"{i}. {ej}")

else: # Personalizada
    st.success("Crea tu propia rutina:")
    
    # Aplanar lista para el selector
    todos = []
    for cat, lista in DB_EJERCICIOS.items():
        todos.extend(lista)
        
    seleccion = st.multiselect(
        "Elige tus ejercicios:",
        options=todos,
        default=["Sentadillas", "Lagartijas Clásicas"]
    )
    rutina_final = seleccion
    
    if not rutina_final:
        st.warning("⚠️ Selecciona al menos un ejercicio.")

# --- 4. CALCULADORA DE TIEMPOS ---
st.markdown("---")

if rutina_final:
    # Cálculos
    t_calentamiento = sum([t for n, t in RUTINA_CALENTAMIENTO])
    t_enfriamiento = 120
    
    n_ejercicios = len(rutina_final)
    t_ciclo = n_ejercicios * (t_trabajo + t_descanso)
    t_total = t_calentamiento + (t_ciclo * vueltas) + t_enfriamiento
    
    # Función formato
    def fmt(s): return f"{s // 60} min {s % 60} s"

    c1, c2, c3 = st.columns(3)
    c1.metric("Duración Vuelta", fmt(t_ciclo))
    c2.metric("Tiempo Total", fmt(t_total))
    c3.metric("Series Totales", f"{n_ejercicios * vueltas}")

st.markdown("---")

# --- 5. MOTOR DE EJECUCIÓN (EL ENTRENAMIENTO) ---

if 'entrenando' not in st.session_state:
    st.session_state.entrenando = False

def iniciar():
    st.session_state.entrenando = True

if st.button("▶️ INICIAR SISTEMA", on_click=iniciar, type="primary"):
    if not rutina_final:
        st.error("Faltan ejercicios.")
        st.stop()

if st.session_state.entrenando:
    
    # === DEFINICIÓN DE ZONAS DINÁMICAS (Para evitar NameError) ===
    zona_titulo = st.empty()
    zona_reloj = st.empty()
    zona_barra = st.progress(0)
    zona_mensaje = st.empty()
    
    # A. CALENTAMIENTO
    zona_titulo.markdown("### 🌡️ FASE 1: CALENTAMIENTO")
    zona_mensaje.info("Prepárate. Iniciamos en 5 segundos...")
    
    for i in range(5, 0, -1):
        zona_reloj.markdown(f"<h1 style='text-align: center; color: gray;'>{i}</h1>", unsafe_allow_html=True)
        time.sleep(1)

    for nombre, duracion in RUTINA_CALENTAMIENTO:
        zona_titulo.markdown(f"### 🌡️ Calentamiento: {nombre}")
        
        for t in range(duracion, 0, -1):
            mins, secs = divmod(t, 60)
            zona_reloj.markdown(
                f"<h1 style='text-align: center; font-size: 80px; color: #FF9800;'>{mins:02d}:{secs:02d}</h1>", 
                unsafe_allow_html=True
            )
            zona_barra.progress((duracion - t) / duracion)
            time.sleep(1)
            
    zona_titulo.markdown("### ✅ Fin del Calentamiento")
    zona_mensaje.success("¡Empezamos el circuito en 5 segundos!")
    time.sleep(5)

    # B. CIRCUITO PRINCIPAL
    total_items = len(rutina_final) * vueltas
    contador = 0
    
    for v in range(1, vueltas + 1):
        for ejercicio in rutina_final:
            contador += 1
            
            # --- TRABAJO (EJERCICIO) ---
            zona_titulo.markdown(f"### ⚔️ Vuelta {v}/{vueltas}: {ejercicio}")
            zona_mensaje.warning("¡Dale duro! Controla la bajada.")
            
            for t in range(t_trabajo, 0, -1):
                mins, secs = divmod(t, 60)
                zona_reloj.markdown(
                    f"<h1 style='text-align: center; font-size: 80px; color: #FF4B4B;'>{mins:02d}:{secs:02d}</h1>", 
                    unsafe_allow_html=True
                )
                zona_barra.progress((t_trabajo - t) / t_trabajo)
                time.sleep(1)
            
            # --- DESCANSO ---
            # Solo descansamos si NO es el último ejercicio absoluto
            if contador < total_items:
                zona_titulo.markdown(f"### 💧 DESCANSO")
                zona_mensaje.success("Recupérate. Respira profundo.")
                
                for t in range(t_descanso, 0, -1):
                    mins, secs = divmod(t, 60)
                    zona_reloj.markdown(
                        f"<h1 style='text-align: center; font-size: 80px; color: #4CAF50;'>{mins:02d}:{secs:02d}</h1>", 
                        unsafe_allow_html=True
                    )
                    zona_barra.progress((t_descanso - t) / t_descanso)
                    time.sleep(1)

    # C. FINAL
    zona_titulo.empty()
    zona_reloj.markdown("<h1 style='text-align: center;'>🏆 ¡TERMINADO!</h1>", unsafe_allow_html=True)
    zona_mensaje.info("Buen trabajo. No olvides registrar tu progreso.")
    zona_barra.progress(100)
    st.balloons()
    
    # Detener estado
    st.session_state.entrenando = False
