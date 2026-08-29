import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="COMMAND CENTER - ISO 21101", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Avanzado - DISEÑO "NATURALEZA / WIKILOC" (Clean UI)
st.markdown("""
    <style>
    /* Fondo principal súper limpio y claro */
    .stApp { background-color: #F7F9FC; color: #1F2937; }
    h1, h2, h3, h4 { color: #111827; font-family: 'Segoe UI', Roboto, sans-serif; font-weight: 800; letter-spacing: -0.5px; }
    p, div, span { font-family: 'Segoe UI', Roboto, sans-serif; color: #374151; }
    
    /* Bóveda y Logo */
    .login-container { display: flex; flex-direction: column; align-items: center; text-align: center; background: #FFFFFF; padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #E5E7EB; }
    .logo-container { display: flex; justify-content: center; margin-bottom: 20px; }
    
    /* Métricas con diseño limpio tipo App Deportiva */
    div[data-testid="stMetric"] { background: #FFFFFF; border: 1px solid #E5E7EB; padding: 15px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: transform 0.2s ease; }
    div[data-testid="stMetric"]:hover { transform: translateY(-3px); box-shadow: 0 10px 15px rgba(0,0,0,0.05); border-color: #DE4A25; }
    div[data-testid="stMetricValue"] { font-size: 2rem !important; color: #111827; font-weight: 900; }
    div[data-testid="stMetricLabel"] p { font-size: 0.95rem !important; color: #6B7280 !important; font-weight: 600; white-space: normal !important; overflow: visible !important; }
    
    /* Pestañas (Tabs) rediseñadas: Limpias, sutiles y modernas (Estilo iOS) */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: #E5E7EB !important; 
        border-radius: 12px !important;
        padding: 5px !important;
        gap: 5px; 
        display: flex; 
        flex-wrap: wrap; 
        justify-content: center;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] { 
        background: transparent !important; 
        border-radius: 8px !important; 
        border: none !important; 
        padding: 10px 15px !important; 
        flex: 1;
        min-width: 140px;
        text-align: center;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"] p { 
        color: #6B7280 !important; 
        font-weight: 700 !important; 
        font-size: 1.05rem !important; 
        margin: 0; 
    }
    .stTabs [aria-selected="true"] { 
        background: #FFFFFF !important; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.08) !important; 
    }
    .stTabs [aria-selected="true"] p { color: #DE4A25 !important; font-weight: 900 !important;}
    
    /* Botones de acción principales (Naranja Marca) */
    div[data-testid="stButton"] button, div[data-testid="stLinkButton"] a { 
        background: #DE4A25 !important; 
        color: white !important; 
        font-weight: 800 !important; 
        border-radius: 10px !important; 
        border: none !important; 
        box-shadow: 0 4px 6px rgba(222, 74, 37, 0.2) !important; 
        transition: all 0.2s ease !important; 
        padding: 15px 15px !important; 
        white-space: normal !important;
        height: auto !important;
        min-height: 55px !important; 
        display: inline-flex !important; 
        align-items: center !important; 
        justify-content: center !important; 
        text-align: center !important;
        width: 100% !important; 
        text-decoration: none !important;
    }
    div[data-testid="stButton"] button:hover, div[data-testid="stLinkButton"] a:hover { 
        background: #C43B1D !important; 
        box-shadow: 0 6px 12px rgba(222, 74, 37, 0.3) !important; 
        transform: translateY(-2px) !important; 
    }
    div[data-testid="stButton"] button p, div[data-testid="stLinkButton"] a p { margin: 0 !important; color: white !important; font-size: 1.1rem; }
    
    /* Tarjetas de Expediente (Blancas y limpias) */
    .tarjeta-expediente { background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); border-left: 6px solid #DE4A25; }
    .tarjeta-expediente h4 { color: #DE4A25; margin-top: 0; font-weight: 800; }
    .tarjeta-verde { border-color: #E5E7EB; border-left: 6px solid #16A34A; }
    .tarjeta-verde h4 { color: #16A34A; }
    
    /* Quitamos el filtro invertido de las tablas para que sean blancas normales */
    .stDataFrame { filter: none !important; border-radius: 8px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. Bóveda de Seguridad
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="logo-container"><img src="https://inmobiliariabarichara.wordpress.com/wp-content/uploads/2026/05/cropped-logo-foto-de-perfil-instagram-1.png" width="120"></div>', unsafe_allow_html=True)
        st.markdown("<h2 style='color: #111827;'>PORTAL DE AUDITORÍA</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #6B7280;'>Sistema de Gestión de Riesgos ISO 21101</p>", unsafe_allow_html=True)
        pwd = st.text_input("Llave de acceso:", type="password", placeholder="Ingrese su clave...")
        if st.button("DESBLOQUEAR SISTEMA", use_container_width=True):
            if pwd == "Nomina2026.":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("⚠️ Clave incorrecta. Intente nuevamente.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 4. MOTOR DE DATOS REALES Y EXTRACCIÓN DE IMÁGENES ---
catalogo_servicios = {
    'w_barichara': 'Servicio 1: Walking Tour Barichara', 'w_bucaramanga': 'Servicio 2: Walking Tour Bucaramanga', 'w_zapatoca': 'Servicio 3: Walking Tour Zapatoca',
    'h1_zap_fue': 'Servicio 4: Hiking E1 (Zapatoca - La Fuente)', 'h1_fue_zap': 'Servicio 4: Hiking E1 (La Fuente - Zapatoca)',
    'h2_fue_gua': 'Servicio 5: Hiking E2 (La Fuente - Guane)', 'h2_gua_fue': 'Servicio 5: Hiking E2 (Guane - La Fuente)',
    'h3_bar_gua_cr': 'Servicio 6: Hiking E3 (Barichara - Guane Camino Real)', 'h3_gua_bar_cr': 'Servicio 6: Hiking E3 (Guane - Barichara Camino Real)',
    'h3_gua_bar_ca': 'Servicio 6: Hiking E3 (Guane - Barichara Camino Ancestral)', 'h3_bar_gua_ca': 'Servicio 6: Hiking E3 (Barichara - Guane Camino Ancestral)',
    'h4_bar_vil': 'Servicio 7: Hiking E4 (Barichara - Villanueva)', 'h4_vil_bar': 'Servicio 7: Hiking E4 (Villanueva - Barichara)',
    'h5_vil_jor': 'Servicio 8: Hiking E5 (Villanueva - Jordán)', 'h5_jor_vil': 'Servicio 8: Hiking E5 (Jordán - Villanueva)',
    'h6_jor_san': 'Servicio 9: Hiking E6 (Jordán - Los Santos)', 'h6_san_jor': 'Servicio 9: Hiking E6 (Los Santos - Jordán)',
    'hc_bar_cab_tem': 'Servicio 10: Hiking (Barichara - Cabrera Los Templados)', 'hc_cab_bar_tem': 'Servicio 10: Hiking (Cabrera - Barichara Los Templados)',
    'hc_bar_cab_pen': 'Servicio 10: Hiking (Barichara - Cabrera La Peña)', 'hc_cab_bar_pen': 'Servicio 10: Hiking (Cabrera - Barichara La Peña)',
    'hl_zap_gua': 'Servicio 11: Ruta de Lenguerke (Zapatoca - Guane)', 'hl_gua_zap': 'Servicio 11: Ruta de Lenguerke (Guane - Zapatoca)',
    't_f1_op1': 'Servicio 12: Trekking Fase 1 (Zapatoca a Los Santos)', 't_f1_op2': 'Servicio 12: Trekking Fase 1 (Los Santos a Zapatoca)'
}

TOKEN_KOBO = "Token a019671c4722dc26abfa19036e6f2771c588dd79"

@st.cache_data(ttl=60)
def cargar_datos_kobo():
    url = "https://kf.kobotoolbox.org/api/v2/assets/adcsu3Ks2EEq4Gq7VQ5mW2/data/?format=json"
    headers = {"Authorization": TOKEN_KOBO}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            datos = response.json().get('results', [])
            procesados = []
            for row in datos:
                servicio = row.get('servicio')
                tipo_punto = row.get('tipo_punto')
                gps = row.get('ubicacion_gps')
                
                foto_nombre = row.get('grupo_riesgo/foto_peligro') or row.get('grupo_emergencia/foto_evac')
                adjuntos = row.get('_attachments', [])
                foto_url = None
                if foto_nombre and adjuntos:
                    for adj in adjuntos:
                        if adj.get('filename', '').endswith(foto_nombre):
                            foto_url = adj.get('download_url')
                            break

                if servicio and tipo_punto and gps:
                    partes_gps = str(gps).split()
                    if len(partes_gps) >= 2:
                        procesados.append({
                            'servicio': servicio, 'tipo_punto': tipo_punto, 
                            'latitud': float(partes_gps[0]), 'longitud': float(partes_gps[1]),
                            'peligro_cat': row.get('grupo_riesgo/peligro_cat', 'N/A'),
                            'peligro_desc': row.get('grupo_riesgo/peligro_desc', 'N/A'),
                            'control_situ': row.get('grupo_riesgo/control_situ', 'N/A'),
                            'evaluador': row.get('evaluador', 'N/A'),
                            'foto_url': foto_url
                        })
            return pd.DataFrame(procesados) if procesados else pd.DataFrame()
    except:
        pass
    return pd.DataFrame()

@st.cache_data(show_spinner=False)
def obtener_imagen_kobo(url):
    try:
        res = requests.get(url, headers={"Authorization": TOKEN_KOBO})
        if res.status_code == 200: return BytesIO(res.content)
    except: pass
    return None

df_kobo = cargar_datos_kobo()
estado_rutas = []
rutas_certificadas = 0

for cod, nombre in catalogo_servicios.items():
    datos_ruta = df_kobo[df_kobo['servicio'] == cod] if not df_kobo.empty else pd.DataFrame()
    if len(datos_ruta) == 0:
        estado, nivel = "🔴 PENDIENTE (0%)", 0
    else:
        puntos = datos_ruta['tipo_punto'].values
        if 'inicio' in puntos and 'fin' in puntos:
            estado, nivel = "🟢 VALIDADO (100%)", 100
            rutas_certificadas += 1
        else:
            estado, nivel = "🟡 EN PROCESO (Falta Trazabilidad)", 50
    estado_rutas.append({'Código Operativo': cod, 'Servicio Operativo': nombre, 'Estado ISO 21101': estado, 'Progreso': nivel})

df_auditoria = pd.DataFrame(estado_rutas)
porcentaje_total = (rutas_certificadas / len(catalogo_servicios)) * 100

# --- 5. INTERFAZ TÁCTICA MULTIPESTAÑA ---
st.markdown("<h1 style='color: #111827; font-size: 2.2rem; text-align: center;'>SISTEMA DE GESTIÓN ISO 21101</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280; font-size: 1.1rem; margin-bottom: 30px;'>Mot Mot Experiencias - Panel de Control Operativo</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🛰️ REGISTRO", "📊 DASHBOARD", "📂 EXPEDIENTES"])

# PESTAÑA 1: INGRESO DE DATOS
with tab1:
    col_izq, col_der = st.columns([1, 1])
    with col_izq:
        st.markdown("<h3 style='color: #111827;'>Auditoría en Terreno</h3>", unsafe_allow_html=True)
        st.markdown("""
        **Instrucciones Operativas:**
        1. Toda ruta requiere registrar el **Inicio** y el **Fin** para validarse al 100%.
        2. Registre las zonas de riesgo topográfico o biológico con evidencia visual in situ.
        3. El formulario funciona sin conexión usando la app KoboCollect.
        """)
    with col_der:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.link_button("📡 ABRIR FORMULARIO SATELITAL (EVALUADOR)", "https://ee.kobotoolbox.org/x/ibbsQweo", use_container_width=True)

# PESTAÑA 2: DASHBOARD GLOBAL
with tab2:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CATÁLOGO TOTAL", f"{len(catalogo_servicios)}")
    col2.metric("RUTAS VALIDADAS 🟢", f"{len(df_auditoria[df_auditoria['Progreso'] == 100])}")
    col3.metric("EN TRÁNSITO 🟡", f"{len(df_auditoria[df_auditoria['Progreso'] == 50])}")
    col4.metric("PENDIENTES 🔴", f"{len(df_auditoria[df_auditoria['Progreso'] == 0])}")

    st.markdown("<br>", unsafe_allow_html=True)
    colA, colB = st.columns([1.2, 2])

    with colA:
        st.markdown("<h4 style='color: #111827; text-align: center;'>PROGRESO DE CERTIFICACIÓN</h4>", unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", value = porcentaje_total, number = {'suffix': "%", 'font': {'color': '#111827', 'size': 40}}, domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#374151"}, 'bar': {'color': "#16A34A"}, 'bgcolor': "#F3F4F6", 'borderwidth': 0,
                     'steps': [{'range': [0, 33], 'color': "#FEE2E2"}, {'range': [33, 66], 'color': "#FEF3C7"}, {'range': [66, 100], 'color': "#D1FAE5"}]}
        ))
        fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "#111827"}, margin=dict(t=20, b=20, l=20, r=20), height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with colB:
        st.markdown("<h4 style='color: #111827;'>MATRIZ DE OPERACIONES (EN VIVO)</h4>", unsafe_allow_html=True)
        # Colores suaves para la tabla
        st.dataframe(
            df_auditoria.style.map(
                lambda x: 'background-color: #FEE2E2; color: #991B1B' if '🔴' in str(x) else ('background-color: #FEF3C7; color: #92400E' if '🟡' in str(x) else 'background-color: #D1FAE5; color: #065F46'), 
                subset=['Estado ISO 21101']
            ), use_container_width=True, height=320
        )

    if not df_kobo.empty:
        st.markdown("<h4 style='color: #111827; margin-top: 20px;'>RADAR DE RUTAS (TOPOGRÁFICO)</h4>", unsafe_allow_html=True)
        # Cambio a mapa claro diurno (carto-positron)
        fig_map = px.scatter_map(df_kobo, lat="latitud", lon="longitud", color="tipo_punto",
                                    color_discrete_map={'inicio':'#16A34A', 'fin':'#DE4A25', 'zona_riesgo':'#F59E0B', 'punto_evac':'#3B82F6', 'punto_interes':'#8B5CF6'},
                                    zoom=9, map_style="carto-positron", size_max=15, hover_name="servicio")
        fig_map.update_traces(marker=dict(size=14, opacity=0.9, line=dict(width=1, color='white')))
        fig_map.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_map, use_container_width=True)

# PESTAÑA 3: EXPEDIENTES Y FOTOGRAFÍAS
with tab3:
    if df_kobo.empty:
        st.info("No hay registros topográficos almacenados en la base de datos.")
    else:
        rutas_activas = df_kobo['servicio'].unique()
        nombres_rutas = {cod: catalogo_servicios.get(cod, cod) for cod in rutas_activas}
        
        ruta_seleccionada = st.selectbox("Seleccione un expediente de ruta para auditar:", options=list(nombres_rutas.keys()), format_func=lambda x: nombres_rutas[x])
        datos_ruta_activa = df_kobo[df_kobo['servicio'] == ruta_seleccionada]
        
        for index, row in datos_ruta_activa.iterrows():
            tipo = row['tipo_punto']
            clase_css = "tarjeta-verde" if tipo in ['inicio', 'fin', 'punto_interes'] else ""
            
            st.markdown(f'<div class="tarjeta-expediente {clase_css}">', unsafe_allow_html=True)
            col_info, col_img = st.columns([1.5, 1])
            
            with col_info:
                st.markdown(f"#### Punto: {tipo.replace('_', ' ').upper()}")
                st.write(f"**📍 Coordenadas:** {row['latitud']}, {row['longitud']}")
                st.write(f"**👤 Auditor:** {str(row['evaluador']).title().replace('_', ' ')}")
                
                if tipo == 'zona_riesgo':
                    st.write(f"**⚠️ Peligro:** {str(row['peligro_cat']).title()}")
                    st.write(f"**📄 Descripción:** {row['peligro_desc']}")
                    st.write(f"**🛡️ Mitigación:** {row['control_situ']}")
            
            with col_img:
                if row['foto_url']:
                    imagen = obtener_imagen_kobo(row['foto_url'])
                    if imagen:
                        st.image(imagen, use_container_width=True, caption="Evidencia fotográfica")
                    else:
                        st.warning("Imagen no disponible o encriptada.")
                else:
                    st.write("*(Sin fotografía adjunta)*")
            
            st.markdown('</div>', unsafe_allow_html=True)