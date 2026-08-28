import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuración de página (Fuerza y Seguridad)
st.set_page_config(page_title="COMMAND CENTER - ISO 21101", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Avanzado: Estética Tecnológica, Oscura, Táctica y Dinámica
st.markdown("""
    <style>
    /* Fondo oscuro inmersivo */
    .stApp {
        background-color: #050A15;
        background-image: radial-gradient(circle at 50% 0%, #0F1A2C 0%, #050A15 80%);
        color: #E2E8F0;
    }
    /* Textos y títulos */
    h1, h2, h3 { color: #FFFFFF; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 700; letter-spacing: -0.5px; }
    p, div { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    /* Tarjetas de métricas tácticas */
    div[data-testid="stMetric"] {
        background: rgba(15, 26, 44, 0.7);
        border: 1px solid #1E2D4A;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.2);
    }
    div[data-testid="stMetricValue"] { font-size: 2.5rem; color: #38BDF8; font-weight: 900; }
    /* Bóveda de login centrada sin recuadro rojo */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        background: transparent;
        padding: 40px;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    /* Botón de ingreso con resplandor */
    .stButton>button { 
        background: linear-gradient(90deg, #DE4A25, #FF5A33) !important; 
        color: white !important; 
        font-weight: bold; 
        border-radius: 8px; 
        border: none; 
        box-shadow: 0 0 15px rgba(222, 74, 37, 0.5); 
        transition: all 0.3s ease-in-out; 
        padding: 10px 0;
    }
    .stButton>button:hover { 
        background: linear-gradient(90deg, #FF5A33, #DE4A25) !important; 
        box-shadow: 0 0 30px rgba(222, 74, 37, 0.9); 
        transform: scale(1.03); 
    }
    /* Tablas oscuras */
    .stDataFrame { filter: invert(0.9) hue-rotate(180deg); }
    </style>
    """, unsafe_allow_html=True)

# 3. Bóveda de Seguridad Encriptada
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="logo-container"><img src="https://inmobiliariabarichara.wordpress.com/wp-content/uploads/2026/05/cropped-logo-foto-de-perfil-instagram-1.png" width="120"></div>', unsafe_allow_html=True)
        st.markdown("<h2 style='color: #DE4A25;'>NÚCLEO DE AUDITORÍA ISO 21101</h2>", unsafe_allow_html=True)
        st.markdown("🔒 **ACCESO RESTRINGIDO | PROTOCOLO DE SEGURIDAD ACTIVO**")
        pwd = st.text_input("Ingrese llave criptográfica de nómina:", type="password")
        if st.button("DESBLOQUEAR SISTEMA", use_container_width=True):
            if pwd == "Nomina2026.":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("⚠️ BRECHA DETECTADA. CONTRASEÑA INCORRECTA.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 4. MOTOR DE DATOS Y LÓGICA DE CERTIFICACIÓN ---

# Catálogo maestro oficial y desglosado con las 25 variantes direccionales
catalogo_servicios = {
    'w_barichara': 'Servicio 1: Walking Tour Barichara',
    'w_bucaramanga': 'Servicio 2: Walking Tour Bucaramanga',
    'w_zapatoca': 'Servicio 3: Walking Tour Zapatoca',
    'h1_zap_fue': 'Servicio 4: Hiking E1 (Zapatoca - La Fuente)',
    'h1_fue_zap': 'Servicio 4: Hiking E1 (La Fuente - Zapatoca)',
    'h2_fue_gua': 'Servicio 5: Hiking E2 (La Fuente - Guane)',
    'h2_gua_fue': 'Servicio 5: Hiking E2 (Guane - La Fuente)',
    'h3_bar_gua_cr': 'Servicio 6: Hiking E3 (Barichara - Guane Camino Real)',
    'h3_gua_bar_cr': 'Servicio 6: Hiking E3 (Guane - Barichara Camino Real)',
    'h3_gua_bar_ca': 'Servicio 6: Hiking E3 (Guane - Barichara Camino Ancestral)',
    'h3_bar_gua_ca': 'Servicio 6: Hiking E3 (Barichara - Guane Camino Ancestral)',
    'h4_bar_vil': 'Servicio 7: Hiking E4 (Barichara - Villanueva)',
    'h4_vil_bar': 'Servicio 7: Hiking E4 (Villanueva - Barichara)',
    'h5_vil_jor': 'Servicio 8: Hiking E5 (Villanueva - Jordán)',
    'h5_jor_vil': 'Servicio 8: Hiking E5 (Jordán - Villanueva)',
    'h6_jor_san': 'Servicio 9: Hiking E6 (Jordán - Los Santos)',
    'h6_san_jor': 'Servicio 9: Hiking E6 (Los Santos - Jordán)',
    'hc_bar_cab_tem': 'Servicio 10: Hiking (Barichara - Cabrera Los Templados)',
    'hc_cab_bar_tem': 'Servicio 10: Hiking (Cabrera - Barichara Los Templados)',
    'hc_bar_cab_pen': 'Servicio 10: Hiking (Barichara - Cabrera La Peña)',
    'hc_cab_bar_pen': 'Servicio 10: Hiking (Cabrera - Barichara La Peña)',
    'hl_zap_gua': 'Servicio 11: Ruta de Lenguerke (Zapatoca - Guane)',
    'hl_gua_zap': 'Servicio 11: Ruta de Lenguerke (Guane - Zapatoca)',
    't_f1_op1': 'Servicio 12: Trekking Fase 1 (Zapatoca a Los Santos)',
    't_f1_op2': 'Servicio 12: Trekking Fase 1 (Los Santos a Zapatoca)'
}

@st.cache_data
def cargar_datos_kobo():
    # Estructura vacía inicial, esperando conexión real vía API.
    data = {
        'servicio': [],
        'tipo_punto': [],
        'latitud': [],
        'longitud': []
    }
    return pd.DataFrame(data)

df_kobo = cargar_datos_kobo()

# Lógica de validación estricta y REAL
estado_rutas = []
rutas_certificadas = 0

for cod, nombre in catalogo_servicios.items():
    if len(df_kobo) == 0:
        datos_ruta = pd.DataFrame() 
    else:
        datos_ruta = df_kobo[df_kobo['servicio'] == cod]
    
    if len(datos_ruta) == 0:
        estado = "🔴 PENDIENTE (0%)"
        nivel = 0
    else:
        puntos_registrados = datos_ruta['tipo_punto'].values
        tiene_inicio = 'inicio' in puntos_registrados
        tiene_fin = 'fin' in puntos_registrados
        
        if tiene_inicio and tiene_fin:
            estado = "🟢 VALIDADO (100%)"
            nivel = 100
            rutas_certificadas += 1
        else:
            estado = "🟡 EN PROCESO (Falta Trazabilidad)"
            nivel = 50

    estado_rutas.append({'Código Operativo': cod, 'Servicio Operativo': nombre, 'Estado ISO 21101': estado, 'Progreso': nivel})

df_auditoria = pd.DataFrame(estado_rutas)
porcentaje_total = (rutas_certificadas / len(catalogo_servicios)) * 100

# --- 5. INTERFAZ DEL COMMAND CENTER ---

st.markdown("<h1 style='color: #DE4A25; font-size: 3rem;'>SISTEMA DE GESTIÓN DE RIESGOS NTC-ISO 21101</h1>", unsafe_allow_html=True)
st.markdown("Monitor de certificación operativa. Trazabilidad de campo conectada al catálogo maestro de servicios.")
st.markdown("---")

# Indicadores de Fuerza
col1, col2, col3, col4 = st.columns(4)
col1.metric("CATÁLOGO TOTAL", f"{len(catalogo_servicios)} TRAYECTOS")
col2.metric("RUTAS VALIDADAS (🟢)", f"{len(df_auditoria[df_auditoria['Progreso'] == 100])}")
col3.metric("EN TRÁNSITO (🟡)", f"{len(df_auditoria[df_auditoria['Progreso'] == 50])}")
col4.metric("PENDIENTES (🔴)", f"{len(df_auditoria[df_auditoria['Progreso'] == 0])}")

st.markdown("<br>", unsafe_allow_html=True)

colA, colB = st.columns([1.2, 2])

with colA:
    st.markdown("<h3 style='color: #38BDF8;'>PROGRESO DE CERTIFICACIÓN GLOBAL</h3>", unsafe_allow_html=True)
    # Medidor tecnológico
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = porcentaje_total,
        number = {'suffix': "%", 'font': {'color': '#38BDF8'}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#DE4A25"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#1E2D4A",
            'steps': [
                {'range': [0, 33], 'color': "rgba(255, 51, 51, 0.2)"},
                {'range': [33, 66], 'color': "rgba(255, 204, 0, 0.2)"},
                {'range': [66, 100], 'color': "rgba(0, 255, 0, 0.2)"}],
        }
    ))
    fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, margin=dict(t=20, b=20, l=20, r=20), height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

with colB:
    st.markdown("<h3 style='color: #38BDF8;'>MATRIZ DE OPERACIONES (TIEMPO REAL)</h3>", unsafe_allow_html=True)
    st.dataframe(
        df_auditoria.style.map(
            lambda x: 'background-color: rgba(255,51,51,0.2); color: #FF3333' if '🔴' in str(x) 
            else ('background-color: rgba(255,204,0,0.2); color: #FFCC00' if '🟡' in str(x) 
            else 'background-color: rgba(0,255,0,0.2); color: #00FF00'), 
            subset=['Estado ISO 21101']
        ),
        use_container_width=True,
        height=320
    )

st.markdown("---")
st.markdown("<h3 style='color: #38BDF8;'>RADAR TOPOGRÁFICO DE RUTAS ACTIVAS</h3>", unsafe_allow_html=True)

# Manejo de mapa vacío cuando no hay datos
if len(df_kobo) > 0:
    fig_map = px.scatter_map(df_kobo, lat="latitud", lon="longitud", color="tipo_punto",
                                color_discrete_map={'inicio':'#00FF00', 'fin':'#DE4A25', 'zona_riesgo':'#FFCC00', 'punto_evac':'#38BDF8'},
                                zoom=10, map_style="carto-darkmatter", size_max=15,
                                hover_name="servicio")
    fig_map.update_traces(marker=dict(size=12, opacity=0.8))
    fig_map.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("🛰️ A la espera de transmisiones satelitales GPS desde campo. Inicie la evaluación en KoBoToolbox para visualizar el mapa.")