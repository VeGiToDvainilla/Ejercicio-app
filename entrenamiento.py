import streamlit as st
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Entrenador en Vivo", page_icon="⏱️")

st.title("⏱️ Modo Entrenador: Tiempo Real")
st.markdown("Presiona **INICIAR** y sigue las instrucciones en pantalla.")

# --- BARRA LATERAL (CONFIGURACIÓN) ---
with st.sidebar:
    st.header("⚙️ Ajustes del Motor")
    tiempo_ejercicio = st.number_input("Duración Ejercicio (seg)", value=45, step=5)
    tiempo_descanso = st.number_input("Duración Descanso (seg)", value=90, step=5)
    num_vueltas = st.slider("Vueltas al Circuito", 1, 5, 3)
    
    st.info("💡 Tip: Sube el volumen de tu música. La pantalla te indicará cuándo cambiar.")

# --- DEFINICIÓN DE LA RUTINA ---
# Lista de tuplas: (Nombre, Tipo, Duración_Override o None)
# Tipo: 'calentamiento', 'fuerza', 'descanso', 'enfriamiento'

def crear_secuencia():
    secuencia = []
    
    # 1. Calentamiento
    calentamiento = [
        ("Movilidad Articular", "calentamiento", 120),
        ("Gato-Vaca", "calentamiento", 60),
        ("Jumping Jacks", "calentamiento", 60)
    ]
    secuencia.extend(calentamiento)
    
    # 2. Circuito Fuerza
    ejercicios = ["Sentadillas", "Lagartijas", "Zancadas", "Superman (Espalda)", "Plancha"]
    
    for vuelta in range(1, num_vueltas + 1):
        for ejercicio in ejercicios:
            # Fase de Esfuerzo
            secuencia.append((f"{ejercicio} (Vuelta {vuelta})", "fuerza", tiempo_ejercicio))
            # Fase de Descanso
            secuencia.append((f"Descanso: Respira", "descanso", tiempo_descanso))
            
    # 3. Enfriamiento
    secuencia.append(("Estiramientos Finales", "enfriamiento", 300))
    
    return secuencia

# --- LÓGICA DEL CRONÓMETRO ---
# Usamos un botón para detonar el loop
if st.button("▶️ INICIAR ENTRENAMIENTO", type="primary"):
    
    rutina = crear_secuencia()
    total_pasos = len(rutina)
    
    # Creamos CONTENEDORES VACÍOS que iremos llenando
    # Esto evita que se dibuje una lista infinita hacia abajo
    status_text = st.empty()
    timer_display = st.empty()
    progress_bar = st.progress(0)
    info_box = st.empty()

    # Bucle principal de la rutina
    for i, (nombre, tipo, duracion) in enumerate(rutina):
        
        # Definir colores e íconos según el tipo
        if tipo == "fuerza":
            icono = "🔥"
            color_msg = "¡DALE DURO!"
            info_msg = "Concéntrate en la técnica. Movimientos controlados."
        elif tipo == "descanso":
            icono = "💧"
            color_msg = "RECUPERACIÓN"
            info_msg = "Camina un poco, toma agua, sacude los músculos."
        elif tipo == "calentamiento":
            icono = "🌡️"
            color_msg = "CALENTAMIENTO"
            info_msg = "Movimientos suaves para lubricar articulaciones."
        else:
            icono = "🧘"
            color_msg = "ENFRIAMIENTO"
            info_msg = "Relaja el cuerpo, baja las pulsaciones."

        # Actualizar el título de la actividad
        status_text.markdown(f"### {icono} {nombre}")
        info_box.info(info_msg)

        # Cuenta Regresiva (El Loop dentro del Loop)
        for segundos_restantes in range(duracion, 0, -1):
            # Formato de minutos:segundos
            mins, secs = divmod(segundos_restantes, 60)
            tiempo_formato = '{:02d}:{:02d}'.format(mins, secs)
            
            # Mostrar el tiempo gigante
            # Usamos HTML simple para hacerlo grande y centrado
            timer_display.markdown(
                f"""
                <div style="text-align: center; font-size: 80px; font-weight: bold; color: #333;">
                    {tiempo_formato}
                </div>
                <div style="text-align: center; font-size: 20px; color: gray;">
                    {color_msg}
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Actualizar barra de progreso del ejercicio actual
            progreso = (duracion - segundos_restantes) / duracion
            progress_bar.progress(progreso)
            
            # Esperar 1 segundo real
            time.sleep(1)
        
        # Pequeña pausa visual al terminar un bloque
        time.sleep(0.5)

    # --- FIN DE LA RUTINA ---
    status_text.empty()
    timer_display.markdown(
        """
        <div style="text-align: center; font-size: 50px; color: green;">
            ✅ ¡ENTRENAMIENTO COMPLETADO!
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.balloons()
