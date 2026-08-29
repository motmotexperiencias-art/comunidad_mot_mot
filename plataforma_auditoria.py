import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="COMMAND CENTER - ISO 21101", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Avanzado
st.markdown("""
    <style>
    .stApp { background-color: #FAFAFA; color: #1F2937; }
    .block-container { padding-top: 2rem !important; padding-bottom: 4rem !important; padding-left: 1.5rem !important; padding-right: 1.5rem !important; max-width: 800px !important; }
    h1, h2, h3, h4 { color: #111827; font-family: 'Segoe UI', Roboto, sans-serif; font-weight: 800; letter-spacing: -0.5px; }
    p, div, span { font-family: 'Segoe UI', Roboto, sans-serif; color: #4B5563; }
    
    .validador-wrapper { display: flex; justify-content: center; margin-top: 10vh; margin-bottom: 30px;}
    .validador-card { background: #ffffff; border-radius: 32px; padding: 40px 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.05); text-align: center; max-width: 320px; width: 100%; border: 1px solid #F3F4F6; }
    .validador-logo { width: 70px; margin-bottom: 15px; border-radius: 50%; }
    .validador-title { font-size: 1.2rem; font-weight: 800; color: #111827; letter-spacing: 1px; margin-bottom: 5px; }
    .validador-status { font-size: 0.75rem; font-weight: 700; color: #10B981; letter-spacing: 2px; margin-bottom: 25px; display: flex; align-items: center; justify-content: center; gap: 6px; }
    .validador-dot { width: 8px; height: 8px; background-color: #10B981; border-radius: 50%; animation: pulse 2s infinite; }
    
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); } 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); } }
    
    div[data-baseweb="input"] { border-radius: 16px !important; background-color: #F3F4F6 !important; border: none !important; }
    
    div[data-testid="stButton"] button, div[data-testid="stLinkButton"] a { background: #DE4A25 !important; color: white !important; font-weight: 700 !important; border-radius: 50px !important; border: none !important; box-shadow: 0 4px 15px rgba(222, 74, 37, 0.25) !important; transition: transform 0.2s ease, box-shadow 0.2s ease !important; padding: 12px 24px !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; width: auto !important; min-width: 200px; text-decoration: none !important; }
    div[data-testid="stButton"] button:hover, div[data-testid="stLinkButton"] a:hover { background: #C43B1D !important; box-shadow: 0 8px 25px rgba(222, 74, 37, 0.35) !important; transform: translateY(-2px) !important; }
    div[data-testid="stButton"] button p, div[data-testid="stLinkButton"] a p { margin: 0 !important; color: white !important; font-size: 1.05rem; }
    
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; gap: 20px; justify-content: center; border-bottom: 2px solid #E5E7EB; padding-bottom: 0px !important; margin-bottom: 25px; }
    .stTabs [data-baseweb="tab"] { background: transparent !important; border: none !important; padding: 10px 5px !important; border-bottom: 3px solid transparent !important; border-radius: 0 !important; color: #9CA3AF !important; transition: color 0.2s ease; }
    .stTabs [data-baseweb="tab"] p { font-weight: 700 !important; font-size: 0.95rem !important; margin: 0; color: inherit !important; }
    .stTabs [aria-selected="true"] { border-bottom: 3px solid #DE4A25 !important; color: #DE4A25 !important; }
    
    div[data-testid="stMetric"] { background: #FFFFFF; border: none; padding: 20px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); transition: transform 0.2s ease; }
    div[data-testid="stMetric"]:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.06); }
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #111827; font-weight: 900; }
    div[data-testid="stMetricLabel"] p { font-size: 0.85rem !important; color: #6B7280 !important; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;}
    
    .tarjeta-expediente { background: #FFFFFF; border: none; border-radius: 20px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border-left: 6px solid #DE4A25; }
    .tarjeta-expediente h4 { color: #DE4A25; margin-top: 0; font-weight: 800; font-size: 1.1rem; }
    .tarjeta-verde { border-left: 6px solid #10B981; }
    .tarjeta-verde h4 { color: #10B981; }
    
    .stDataFrame { filter: none !important; border-radius: 12px; overflow: hidden; border: 1px solid #E5E7EB; }
    </style>
    """, unsafe_allow_html=True)

# 3. Bóveda de Seguridad
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('''
        <div class="validador-wrapper">
            <div class="validador-card">
                <img class="validador-logo" src="https://inmobiliariabarichara.wordpress.com/wp-content/uploads/2026/05/cropped-logo-foto-de-perfil-instagram-1.png">
                <div class="validador-title">ISO 21101</div>
                <div class="validador-status"><div class="validador-dot"></div> TERMINAL ACTIVA</div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        pwd = st.text_input("PIN", type="password", label_visibility="collapsed", placeholder="Ingresar PIN...")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("VALIDAR", use_container_width=True):
            if pwd == "Nomina2026.":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("⚠️ PIN Inválido")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()

# --- 4. MOTOR DE DATOS (Adaptado para leer grupos de repetición de Kobo) ---
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
            
            for envio in datos:
                # Datos fijos para todo el envío
                servicio = envio.get('servicio')
                evaluador = envio.get('evaluador', 'N/A')
                adjuntos = envio.get('_attachments', [])
                
                # Buscar dentro del grupo de repetición "puntos_ruta"
                puntos_ruta = envio.get('puntos_ruta', [])
                for punto in puntos_ruta:
                    tipo_punto = punto.get('puntos_ruta/tipo_punto')
                    gps = punto.get('puntos_ruta/ubicacion_gps')
                    
                    foto_nombre = punto.get('puntos_ruta/foto_punto')
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
                                'instruccion': punto.get('puntos_ruta/instruccion_bifurcacion', 'N/A'),
                                'peligro_cat': punto.get('puntos_ruta/grupo_riesgo/peligro_cat', 'N/A'),
                                'peligro_desc': punto.get('puntos_ruta/grupo_riesgo/peligro_desc', 'N/A'),
                                'control_situ': punto.get('puntos_ruta/grupo_riesgo/control_situ', 'N/A'),
                                'evaluador': evaluador,
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
        estado, nivel = "🔴 PENDIENTE", 0
    else:
        puntos = datos_ruta['tipo_punto'].values
        if 'inicio' in puntos and 'fin' in puntos:
            estado, nivel = "🟢 VALIDADO", 100
            rutas_certificadas += 1
        else:
            estado, nivel = "🟡 EN PROCESO", 50
    estado_rutas.append({'Código': cod, 'Servicio Operativo': nombre, 'Estado': estado, 'Progreso': nivel})

df_auditoria = pd.DataFrame(estado_rutas)
porcentaje_total = (rutas_certificadas / len(catalogo_servicios)) * 100

# --- 5. INTERFAZ TÁCTICA MULTIPESTAÑA ---
st.markdown("<h2 style='text-align: center; font-size: 1.8rem; margin-bottom: 20px;'>Centro Operativo</h2>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Registro", "Dashboard", "Expedientes"])

with tab1:
    st.markdown("<br><h4 style='text-align: center;'>Auditoría en Terreno</h4>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #6B7280; font-size: 0.95rem; margin-bottom: 30px;'>Inicie la validación marcando el Inicio y Fin de ruta.</div>", unsafe_allow_html=True)
    col_izq, col_centro, col_der = st.columns([1, 4, 1])
    with col_centro: st.link_button("ABRIR VALIDACIÓN SATELITAL", "https://ee.kobotoolbox.org/x/ibbsQweo", use_container_width=True)

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CATÁLOGO", f"{len(catalogo_servicios)}")
    col2.metric("VALIDADAS", f"{len(df_auditoria[df_auditoria['Progreso'] == 100])}")
    col3.metric("EN TRÁNSITO", f"{len(df_auditoria[df_auditoria['Progreso'] == 50])}")
    col4.metric("PENDIENTES", f"{len(df_auditoria[df_auditoria['Progreso'] == 0])}")

    st.markdown("<br>", unsafe_allow_html=True)
    colA, colB = st.columns([1.2, 2])

    with colA:
        st.markdown("<h4 style='text-align: center; font-size: 1.1rem;'>CERTIFICACIÓN</h4>", unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", value = porcentaje_total, number = {'suffix': "%", 'font': {'color': '#111827', 'size': 40}}, domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {'axis': {'range': [None, 100], 'tickwidth': 0, 'tickcolor': "white"}, 'bar': {'color': "#10B981"}, 'bgcolor': "#F3F4F6", 'borderwidth': 0,
                     'steps': [{'range': [0, 33], 'color': "#FEE2E2"}, {'range': [33, 66], 'color': "#FEF3C7"}, {'range': [66, 100], 'color': "#D1FAE5"}]}
        ))
        fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "#111827"}, margin=dict(t=10, b=10, l=10, r=10), height=250)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with colB:
        st.markdown("<h4 style='font-size: 1.1rem;'>MATRIZ DE OPERACIONES</h4>", unsafe_allow_html=True)
        st.dataframe(
            df_auditoria.style.map(
                lambda x: 'background-color: #FEE2E2; color: #991B1B' if '🔴' in str(x) else ('background-color: #FEF3C7; color: #92400E' if '🟡' in str(x) else 'background-color: #D1FAE5; color: #065F46'), 
                subset=['Estado']
            ), use_container_width=True, height=280
        )

    if not df_kobo.empty:
        st.markdown("<h4 style='margin-top: 30px; font-size: 1.1rem;'>RADAR TOPOGRÁFICO</h4>", unsafe_allow_html=True)
        fig_map = px.scatter_map(df_kobo, lat="latitud", lon="longitud", color="tipo_punto",
                                    color_discrete_map={'inicio':'#10B981', 'fin':'#DE4A25', 'bifurcacion': '#0EA5E9', 'zona_riesgo':'#F59E0B', 'punto_evac':'#3B82F6', 'punto_interes':'#8B5CF6'},
                                    zoom=9, map_style="carto-positron", size_max=15, hover_name="servicio")
        fig_map.update_traces(marker=dict(size=14, opacity=0.9, line=dict(width=2, color='white')))
        fig_map.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_map, use_container_width=True)

with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    if df_kobo.empty:
        st.info("No hay registros topográficos almacenados.")
    else:
        rutas_activas = df_kobo['servicio'].unique()
        nombres_rutas = {cod: catalogo_servicios.get(cod, cod) for cod in rutas_activas}
        
        ruta_seleccionada = st.selectbox("Expediente de ruta:", options=list(nombres_rutas.keys()), format_func=lambda x: nombres_rutas[x])
        datos_ruta_activa = df_kobo[df_kobo['servicio'] == ruta_seleccionada]
        st.markdown("<br>", unsafe_allow_html=True)
        
        for index, row in datos_ruta_activa.iterrows():
            tipo = row['tipo_punto']
            clase_css = "tarjeta-verde" if tipo in ['inicio', 'fin', 'punto_interes', 'bifurcacion'] else ""
            
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
                elif tipo == 'bifurcacion' and pd.notna(row['instruccion']) and row['instruccion'] != 'N/A':
                    st.write(f"**🧭 Instrucción:** {row['instruccion']}")
            
            with col_img:
                if pd.notna(row.get('foto_url')) and row['foto_url']:
                    imagen = obtener_imagen_kobo(row['foto_url'])
                    if imagen:
                        st.image(imagen, use_container_width=True, caption="Evidencia in situ")
                    else:
                        st.warning("Imagen encriptada o no disponible.")
                else:
                    st.write("*(Sin fotografía)*")
            
            st.markdown('</div>', unsafe_allow_html=True)