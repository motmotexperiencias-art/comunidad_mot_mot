import pandas as pd
import xlsxwriter
from io import BytesIO
import urllib.request
import urllib.error
import ssl

def generar_xlsform_sig():
    # Evitar problemas de certificado SSL al descargar el logo
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # 1. Pestaña 'survey'
    survey = [
        # --- METADATOS (El guía puede configurar la app para que recuerde estas 2 respuestas) ---
        {'type': 'select_one evaluador', 'name': 'evaluador', 'label': '1. Nombre del evaluador', 'required': 'yes', 'appearance': 'minimal'},
        {'type': 'select_one servicio', 'name': 'servicio', 'label': '2. Ruta a evaluar', 'required': 'yes'},
        
        # --- EL PUNTO A REPORTAR ---
        {'type': 'select_one tipo_punto', 'name': 'tipo_punto', 'label': '3. ¿Qué vas a reportar aquí?', 'required': 'yes'},
        {'type': 'geopoint', 'name': 'ubicacion_gps', 'label': '4. Capturar ubicación GPS exacta', 'required': 'yes'},
        
        # --- BIFURCACIONES (Instrucciones) ---
        {'type': 'text', 'name': 'instruccion_bifurcacion', 'label': 'Instrucciones: ¿Qué camino tomar en esta bifurcación?', 'relevant': "${tipo_punto} = 'bifurcacion'", 'required': 'yes'},

        # --- Identificación y Evaluación del Riesgo (ISO 21101 - A.3) ---
        {'type': 'begin_group', 'name': 'grupo_riesgo', 'label': 'Evaluación de Riesgo', 'relevant': "${tipo_punto} = 'zona_riesgo'"},
        {'type': 'select_one peligro_cat', 'name': 'peligro_cat', 'label': 'Categoría del peligro', 'required': 'yes'},
        {'type': 'text', 'name': 'peligro_otro', 'label': 'Especifique otro tipo de peligro', 'relevant': "selected(${peligro_cat}, 'otro')", 'required': 'yes'},
        {'type': 'text', 'name': 'peligro_desc', 'label': 'Descripción específica del peligro', 'required': 'yes'},
        {'type': 'select_one posibilidad', 'name': 'posibilidad', 'label': 'Posibilidad de ocurrencia', 'required': 'yes'},
        {'type': 'select_one severidad', 'name': 'severidad', 'label': 'Severidad', 'required': 'yes'},
        {'type': 'text', 'name': 'control_situ', 'label': 'Medida de control in situ (Evitar/Mitigar)', 'required': 'yes'},
        {'type': 'end_group', 'name': 'grupo_riesgo'},
        
        # --- Respuesta ante Emergencias (ISO 21101 - 8.2) ---
        {'type': 'begin_group', 'name': 'grupo_emergencia', 'label': 'Punto de Evacuación / Rescate', 'relevant': "${tipo_punto} = 'punto_evac'"},
        {'type': 'select_multiple acceso', 'name': 'acceso_evac', 'label': 'Viabilidad de acceso para rescate', 'required': 'yes'},
        {'type': 'text', 'name': 'acceso_otro', 'label': 'Especifique otro método', 'relevant': "selected(${acceso_evac}, 'otro')", 'required': 'yes'},
        {'type': 'select_one senal', 'name': 'cobertura_senal', 'label': 'Cobertura celular', 'required': 'yes'},
        {'type': 'text', 'name': 'senal_otra', 'label': 'Especifique red celular', 'relevant': "selected(${cobertura_senal}, 'otro')", 'required': 'yes'},
        {'type': 'select_one tiempo_ext', 'name': 'tiempo_evacuacion', 'label': 'Tiempo estimado de evacuación', 'required': 'yes'},
        {'type': 'text', 'name': 'tiempo_evac_otro', 'label': 'Especifique el tiempo exacto', 'relevant': "selected(${tiempo_evacuacion}, 'otro')", 'required': 'yes'},
        {'type': 'text', 'name': 'red_apoyo', 'label': 'Finca o contacto local (Opcional)', 'required': 'no'},
        {'type': 'text', 'name': 'tel_emergencia', 'label': 'Teléfono del contacto (Opcional)', 'required': 'no', 'appearance': 'numbers'},
        {'type': 'end_group', 'name': 'grupo_emergencia'},
        
        # --- Puntos de Interés / Confort ---
        {'type': 'begin_group', 'name': 'grupo_interes', 'label': 'Punto de Confort / Interés', 'relevant': "${tipo_punto} = 'punto_interes'"},
        {'type': 'select_multiple punto_int', 'name': 'cat_interes', 'label': 'Categoría del punto', 'required': 'yes'},
        {'type': 'text', 'name': 'interes_otro', 'label': 'Especifique otro', 'relevant': "selected(${cat_interes}, 'otro')", 'required': 'yes'},
        {'type': 'text', 'name': 'guion_guia', 'label': 'Guion interpretativo (Opcional)', 'required': 'no'},
        {'type': 'text', 'name': 'obs_logistica', 'label': 'Observaciones logísticas', 'required': 'no'},
        {'type': 'end_group', 'name': 'grupo_interes'},
        
        # --- FOTOGRAFÍA UNIVERSAL (Para cualquier punto, obligatoria solo para Riesgos/Evac) ---
        {'type': 'image', 'name': 'foto_punto', 'label': '📸 Evidencia fotográfica del lugar', 'required': 'no', 'appearance': 'new'},
        
        # --- TRACK DE RUTA (Solo al terminar) ---
        {'type': 'file', 'name': 'archivo_track', 'label': '🗺️ Adjuntar archivo GPX/KML del track (Solo al llegar al final)', 'relevant': "${tipo_punto} = 'fin'", 'required': 'no'}
    ]

    # 2. Pestaña 'choices'
    choices = [
        {'list_name': 'evaluador', 'name': 'liliana', 'label': 'Liliana Paola Rozo Martínez - Gerente General / Auditora'},
        {'list_name': 'evaluador', 'name': 'antonio', 'label': 'Antonio José Becerra Velásquez - Guía Turístico Profesional'},
        {'list_name': 'evaluador', 'name': 'alexander', 'label': 'Alexander Jimenez - Guía Turístico Profesional'},
        
        {'list_name': 'servicio', 'name': 'w_barichara', 'label': 'Servicio 1: Walking Tour Barichara'},
        {'list_name': 'servicio', 'name': 'w_bucaramanga', 'label': 'Servicio 2: Walking Tour Bucaramanga'},
        {'list_name': 'servicio', 'name': 'w_zapatoca', 'label': 'Servicio 3: Walking Tour Zapatoca'},
        {'list_name': 'servicio', 'name': 'h1_zap_fue', 'label': 'Servicio 4: Hiking Etapa 1 (Zapatoca - La Fuente)'},
        {'list_name': 'servicio', 'name': 'h1_fue_zap', 'label': 'Servicio 4: Hiking Etapa 1 (La Fuente - Zapatoca)'},
        {'list_name': 'servicio', 'name': 'h2_fue_gua', 'label': 'Servicio 5: Hiking Etapa 2 (La Fuente - Guane)'},
        {'list_name': 'servicio', 'name': 'h2_gua_fue', 'label': 'Servicio 5: Hiking Etapa 2 (Guane - La Fuente)'},
        {'list_name': 'servicio', 'name': 'h3_bar_gua_cr', 'label': 'Servicio 6: Hiking Etapa 3 (Barichara - Guane Camino Real)'},
        {'list_name': 'servicio', 'name': 'h3_gua_bar_cr', 'label': 'Servicio 6: Hiking Etapa 3 (Guane - Barichara Camino Real)'},
        {'list_name': 'servicio', 'name': 'h3_gua_bar_ca', 'label': 'Servicio 6: Hiking Etapa 3 (Guane - Barichara Camino Ancestral)'},
        {'list_name': 'servicio', 'name': 'h3_bar_gua_ca', 'label': 'Servicio 6: Hiking Etapa 3 (Barichara - Guane Camino Ancestral)'},
        {'list_name': 'servicio', 'name': 'h4_bar_vil', 'label': 'Servicio 7: Hiking Etapa 4 (Barichara - Villanueva)'},
        {'list_name': 'servicio', 'name': 'h4_vil_bar', 'label': 'Servicio 7: Hiking Etapa 4 (Villanueva - Barichara)'},
        {'list_name': 'servicio', 'name': 'h5_vil_jor', 'label': 'Servicio 8: Hiking Etapa 5 (Villanueva - Jordán)'},
        {'list_name': 'servicio', 'name': 'h5_jor_vil', 'label': 'Servicio 8: Hiking Etapa 5 (Jordán - Villanueva)'},
        {'list_name': 'servicio', 'name': 'h6_jor_san', 'label': 'Servicio 9: Hiking Etapa 6 (Jordán - Los Santos)'},
        {'list_name': 'servicio', 'name': 'h6_san_jor', 'label': 'Servicio 9: Hiking Etapa 6 (Los Santos - Jordán)'},
        {'list_name': 'servicio', 'name': 'hc_bar_cab_tem', 'label': 'Servicio 10: Hiking (Barichara - Cabrera Los Templados)'},
        {'list_name': 'servicio', 'name': 'hc_cab_bar_tem', 'label': 'Servicio 10: Hiking (Cabrera - Barichara Los Templados)'},
        {'list_name': 'servicio', 'name': 'hc_bar_cab_pen', 'label': 'Servicio 10: Hiking (Barichara - Cabrera La Peña)'},
        {'list_name': 'servicio', 'name': 'hc_cab_bar_pen', 'label': 'Servicio 10: Hiking (Cabrera - Barichara La Peña)'},
        {'list_name': 'servicio', 'name': 'hl_zap_gua', 'label': 'Servicio 11: Ruta de Lenguerke (Zapatoca - Guane)'},
        {'list_name': 'servicio', 'name': 'hl_gua_zap', 'label': 'Servicio 11: Ruta de Lenguerke (Guane - Zapatoca)'},
        {'list_name': 'servicio', 'name': 't_f1_op1', 'label': 'Servicio 12: Trekking Fase 1 (Zapatoca a Los Santos)'},
        {'list_name': 'servicio', 'name': 't_f1_op2', 'label': 'Servicio 12: Trekking Fase 1 (Los Santos a Zapatoca)'},
        
        {'list_name': 'tipo_punto', 'name': 'inicio', 'label': 'Inicio de ruta'},
        {'list_name': 'tipo_punto', 'name': 'fin', 'label': 'Fin de ruta'},
        {'list_name': 'tipo_punto', 'name': 'bifurcacion', 'label': 'Bifurcación / Desvío direccional'},
        {'list_name': 'tipo_punto', 'name': 'zona_riesgo', 'label': 'Zona de Riesgo (Norma A.3)'},
        {'list_name': 'tipo_punto', 'name': 'punto_evac', 'label': 'Punto de Evacuación (Norma 8.2)'},
        {'list_name': 'tipo_punto', 'name': 'punto_interes', 'label': 'Punto de Confort / Sostenibilidad'},
        
        {'list_name': 'peligro_cat', 'name': 'topografico', 'label': 'Topográfico (Terreno suelto, abismos)'},
        {'list_name': 'peligro_cat', 'name': 'biologico_fauna', 'label': 'Biológico Fauna (Serpientes, abejas)'},
        {'list_name': 'peligro_cat', 'name': 'biologico_flora', 'label': 'Biológico Flora (Vegetación espinosa)'},
        {'list_name': 'peligro_cat', 'name': 'climatico', 'label': 'Climático (Exposición solar, crecientes)'},
        {'list_name': 'peligro_cat', 'name': 'antropico', 'label': 'Antrópico (Tránsito, zonas de caza)'},
        {'list_name': 'peligro_cat', 'name': 'otro', 'label': 'Otro (Especificar)'},
        
        {'list_name': 'posibilidad', 'name': 'improbable', 'label': 'Improbable'},
        {'list_name': 'posibilidad', 'name': 'posible', 'label': 'Posible'},
        {'list_name': 'posibilidad', 'name': 'probable', 'label': 'Probable'},
        {'list_name': 'posibilidad', 'name': 'casi_seguro', 'label': 'Casi seguro'},
        
        {'list_name': 'severidad', 'name': 'insignificante', 'label': 'Insignificante'},
        {'list_name': 'severidad', 'name': 'menor', 'label': 'Menor'},
        {'list_name': 'severidad', 'name': 'moderada', 'label': 'Moderada'},
        {'list_name': 'severidad', 'name': 'mayor', 'label': 'Mayor'},
        {'list_name': 'severidad', 'name': 'catastrofica', 'label': 'Catastrófica'},
        
        {'list_name': 'acceso', 'name': 'peatonal', 'label': 'Peatonal'},
        {'list_name': 'acceso', 'name': 'traccion', 'label': 'Tracción animal'},
        {'list_name': 'acceso', 'name': '4x4', 'label': 'Vehicular 4x4'},
        {'list_name': 'acceso', 'name': 'remoto', 'label': 'Helitransportado'},
        {'list_name': 'acceso', 'name': 'otro', 'label': 'Otro'},
        
        {'list_name': 'senal', 'name': 'ciega', 'label': 'Sin cobertura celular'},
        {'list_name': 'senal', 'name': 'claro', 'label': 'Señal estable (Claro)'},
        {'list_name': 'senal', 'name': 'movistar', 'label': 'Señal estable (Movistar)'},
        {'list_name': 'senal', 'name': 'tigo', 'label': 'Señal estable (Tigo)'},
        {'list_name': 'senal', 'name': 'otro', 'label': 'Otra red'},
        
        {'list_name': 'tiempo_ext', 'name': 't30', 'label': '< 30 minutos'},
        {'list_name': 'tiempo_ext', 'name': 't60', 'label': '1 hora'},
        {'list_name': 'tiempo_ext', 'name': 't120', 'label': '2 a 3 horas'},
        {'list_name': 'tiempo_ext', 'name': 't_medio', 'label': 'Medio día'},
        {'list_name': 'tiempo_ext', 'name': 't_dia', 'label': 'Un día o más'},
        {'list_name': 'tiempo_ext', 'name': 'otro', 'label': 'Otro'},
        
        {'list_name': 'punto_int', 'name': 'descanso', 'label': 'Descanso / Sombra'},
        {'list_name': 'punto_int', 'name': 'relajacion', 'label': 'Relajación'},
        {'list_name': 'punto_int', 'name': 'dormir', 'label': 'Acampar / Refugio'},
        {'list_name': 'punto_int', 'name': 'hidratacion', 'label': 'Punto hídrico'},
        {'list_name': 'punto_int', 'name': 'banos', 'label': 'Baños'},
        {'list_name': 'punto_int', 'name': 'alimentacion', 'label': 'Alimentación'},
        {'list_name': 'punto_int', 'name': 'mirador', 'label': 'Mirador'},
        {'list_name': 'punto_int', 'name': 'comunidad', 'label': 'Comunidad / Artesanos'},
        {'list_name': 'punto_int', 'name': 'avifauna', 'label': 'Avifauna'},
        {'list_name': 'punto_int', 'name': 'patrimonio', 'label': 'Patrimonio'},
        {'list_name': 'punto_int', 'name': 'otro', 'label': 'Otro'}
    ]

    # 3. Pestaña 'settings'
    settings = [{
        'form_title': 'Validación ISO 21101 - Mot Mot Experiencias',
        'form_id': 'sig_motmot_v8_final',
        'default_language': 'Español',
        'style': 'theme-grid',
        'logo': 'logo_motmot.png'
    }]

    nombre_archivo = 'SIG_MotMot_Validacion_Campo.xlsx'
    writer = pd.ExcelWriter(nombre_archivo, engine='xlsxwriter')
    
    pd.DataFrame(survey).to_excel(writer, sheet_name='survey', index=False)
    pd.DataFrame(choices).to_excel(writer, sheet_name='choices', index=False)
    pd.DataFrame(settings).to_excel(writer, sheet_name='settings', index=False)
    
    workbook = writer.book
    
    formato_header = workbook.add_format({
        'bold': True, 'text_wrap': True, 'valign': 'vcenter', 'align': 'center',
        'fg_color': '#DE4A25', 'font_color': 'white', 'border': 1, 'font_name': 'Arial', 'font_size': 11
    })
    
    formato_celdas = workbook.add_format({
        'valign': 'vcenter', 'text_wrap': True, 'border': 1, 'border_color': '#8BBFBB', 'font_name': 'Arial', 'font_size': 10
    })
    
    df_survey = pd.DataFrame(survey)
    df_choices = pd.DataFrame(choices)
    df_settings = pd.DataFrame(settings)

    for sheet_name in ['survey', 'choices', 'settings']:
        worksheet = writer.sheets[sheet_name]
        worksheet.set_row(0, 30)
        worksheet.set_column('A:F', 28, formato_celdas)
        for col_num, value in enumerate(df_survey.columns if sheet_name == 'survey' else (df_choices.columns if sheet_name == 'choices' else df_settings.columns)):
            worksheet.write(0, col_num, value, formato_header)
            
    try:
        url_logo = "https://inmobiliariabarichara.wordpress.com/wp-content/uploads/2026/05/cropped-logo-foto-de-perfil-instagram-1.png"
        req = urllib.request.Request(url_logo, headers={'User-Agent': 'Mozilla/5.0'})
        image_data = BytesIO(urllib.request.urlopen(req, context=ctx).read())
        writer.sheets['settings'].insert_image('E2', url_logo, {'image_data': image_data, 'x_scale': 0.15, 'y_scale': 0.15, 'object_position': 1})
    except Exception:
        pass

    writer.close()
    print(f"¡Éxito total! Archivo {nombre_archivo} generado exitosamente. Súbelo a Kobo.")

generar_xlsform_sig()