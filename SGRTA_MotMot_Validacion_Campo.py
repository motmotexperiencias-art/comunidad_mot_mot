import pandas as pd
import xlsxwriter
from io import BytesIO
import urllib.request
import urllib.error

def generar_xlsform_sig():
    # 1. Pestaña 'survey' (Estructura ISO 21101 + Trazabilidad KML/GPX)
    survey = [
        {'type': 'select_one evaluador', 'name': 'evaluador', 'label': 'Nombre del evaluador', 'required': 'yes', 'appearance': 'minimal'},
        {'type': 'select_one servicio', 'name': 'servicio', 'label': 'Servicio operativo a evaluar', 'required': 'yes'},
        {'type': 'select_one tipo_punto', 'name': 'tipo_punto', 'label': 'Tipo de punto evaluado', 'required': 'yes'},
        {'type': 'geopoint', 'name': 'ubicacion_gps', 'label': 'Capturar ubicación GPS exacta (Registra Altitud/Desnivel automáticamente)', 'required': 'yes'},
        
        # Identificación y Evaluación del Riesgo (ISO 21101 - A.3)
        {'type': 'begin_group', 'name': 'grupo_riesgo', 'label': 'Evaluación de Riesgo', 'relevant': "${tipo_punto} = 'zona_riesgo'"},
        {'type': 'select_one peligro_cat', 'name': 'peligro_cat', 'label': 'Categoría del peligro', 'required': 'yes'},
        {'type': 'text', 'name': 'peligro_otro', 'label': 'Especifique otro tipo de peligro', 'relevant': "selected(${peligro_cat}, 'otro')", 'required': 'yes'},
        {'type': 'text', 'name': 'peligro_desc', 'label': 'Descripción específica del peligro en el entorno', 'required': 'yes'},
        {'type': 'select_one posibilidad', 'name': 'posibilidad', 'label': 'Posibilidad de ocurrencia', 'required': 'yes'},
        {'type': 'select_one severidad', 'name': 'severidad', 'label': 'Severidad de la consecuencia', 'required': 'yes'},
        {'type': 'text', 'name': 'control_situ', 'label': 'Medida de control propuesta in situ (Evitar/Mitigar)', 'required': 'yes'},
        {'type': 'image', 'name': 'foto_peligro', 'label': 'Evidencia fotográfica obligatoria in situ', 'required': 'yes', 'appearance': 'new'},
        {'type': 'end_group', 'name': 'grupo_riesgo'},
        
        # Respuesta ante Emergencias (ISO 21101 - 8.2)
        {'type': 'begin_group', 'name': 'grupo_emergencia', 'label': 'Logística de Evacuación y Apoyo', 'relevant': "${tipo_punto} = 'punto_evac'"},
        {'type': 'select_multiple acceso', 'name': 'acceso_evac', 'label': 'Viabilidad de acceso para rescate', 'required': 'yes'},
        {'type': 'text', 'name': 'acceso_otro', 'label': 'Especifique otro método de acceso', 'relevant': "selected(${acceso_evac}, 'otro')", 'required': 'yes'},
        {'type': 'select_one senal', 'name': 'cobertura_senal', 'label': 'Cobertura de telecomunicaciones celular', 'required': 'yes'},
        {'type': 'text', 'name': 'senal_otra', 'label': 'Especifique la red celular (Ej: WOM, Avantel)', 'relevant': "selected(${cobertura_senal}, 'otro')", 'required': 'yes'},
        {'type': 'select_one tiempo_ext', 'name': 'tiempo_evacuacion', 'label': 'Tiempo estimado de evacuación a centro médico o punto de rescate seguro', 'required': 'yes'},
        {'type': 'text', 'name': 'tiempo_evac_otro', 'label': 'Especifique el tiempo exacto estimado', 'relevant': "selected(${tiempo_evacuacion}, 'otro')", 'required': 'yes'},
        {'type': 'text', 'name': 'red_apoyo', 'label': 'Punto de refugio, finca o contacto local adicional (Opcional)', 'required': 'no'},
        {'type': 'text', 'name': 'tel_emergencia', 'label': 'Teléfono del refugio o contacto local (Opcional)', 'required': 'no', 'appearance': 'numbers'},
        {'type': 'image', 'name': 'foto_evac', 'label': 'Evidencia fotográfica in situ del punto de extracción', 'required': 'yes', 'appearance': 'new'},
        {'type': 'end_group', 'name': 'grupo_emergencia'},
        
        # Puntos de Interés / Confort del Caminante
        {'type': 'begin_group', 'name': 'grupo_interes', 'label': 'Interpretación y Confort Logístico', 'relevant': "${tipo_punto} = 'punto_interes'"},
        {'type': 'select_multiple punto_int', 'name': 'cat_interes', 'label': 'Categoría del punto', 'required': 'yes'},
        {'type': 'text', 'name': 'interes_otro', 'label': 'Especifique otro punto de interés', 'relevant': "selected(${cat_interes}, 'otro')", 'required': 'yes'},
        {'type': 'text', 'name': 'guion_guia', 'label': 'Guion interpretativo / Información de valor a transmitir por el guía en este punto', 'required': 'no'},
        {'type': 'text', 'name': 'obs_logistica', 'label': 'Observaciones logísticas (Ej: Estado de la sombra, calidad del agua)', 'required': 'no'},
        {'type': 'end_group', 'name': 'grupo_interes'},
        
        # Trazabilidad de Ruta (Solo visible al finalizar)
        {'type': 'file', 'name': 'archivo_track', 'label': 'Adjuntar archivo GPX/KML del track de la ruta (Opcional para mapeo topográfico)', 'relevant': "${tipo_punto} = 'fin'", 'required': 'no'}
    ]

    # 2. Pestaña 'choices' 
    choices = [
        # Integración de perfiles competentes para cumplimiento ISO 21101
        {'list_name': 'evaluador', 'name': 'liliana', 'label': 'Liliana Paola Rozo Martínez - Gerente General / Auditora'},
        {'list_name': 'evaluador', 'name': 'antonio', 'label': 'Antonio José Becerra Velásquez - Guía Turístico Profesional'},
        {'list_name': 'evaluador', 'name': 'alexander', 'label': 'Alexander Jimenez - Guía Turístico Profesional'},
        
        # Servicios Operativos
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
        
        # Categorías de Puntos
        {'list_name': 'tipo_punto', 'name': 'inicio', 'label': 'Inicio de ruta'},
        {'list_name': 'tipo_punto', 'name': 'fin', 'label': 'Fin de ruta'},
        {'list_name': 'tipo_punto', 'name': 'bifurcacion', 'label': 'Bifurcación / Desvío direccional'},
        {'list_name': 'tipo_punto', 'name': 'zona_riesgo', 'label': 'Zona de Riesgo (Norma A.3)'},
        {'list_name': 'tipo_punto', 'name': 'punto_evac', 'label': 'Punto de Evacuación (Norma 8.2)'},
        {'list_name': 'tipo_punto', 'name': 'punto_interes', 'label': 'Punto de Confort / Sostenibilidad'},
        
        # Riesgos Detallados
        {'list_name': 'peligro_cat', 'name': 'topografico', 'label': 'Topográfico (Terreno suelto, abismos, caídas)'},
        {'list_name': 'peligro_cat', 'name': 'biologico_fauna', 'label': 'Biológico Fauna (Garrapatas, serpientes, abejas)'},
        {'list_name': 'peligro_cat', 'name': 'biologico_flora', 'label': 'Biológico Flora (Vegetación espinosa, plantas tóxicas)'},
        {'list_name': 'peligro_cat', 'name': 'climatico', 'label': 'Climático (Exposición solar extrema, crecientes)'},
        {'list_name': 'peligro_cat', 'name': 'antropico', 'label': 'Antrópico (Tránsito vehicular, zonas de caza)'},
        {'list_name': 'peligro_cat', 'name': 'otro', 'label': 'Otro (Especificar)'},
        
        # Matriz de Riesgo ISO
        {'list_name': 'posibilidad', 'name': 'improbable', 'label': 'Improbable'},
        {'list_name': 'posibilidad', 'name': 'posible', 'label': 'Posible'},
        {'list_name': 'posibilidad', 'name': 'probable', 'label': 'Probable'},
        {'list_name': 'posibilidad', 'name': 'casi_seguro', 'label': 'Casi seguro'},
        
        {'list_name': 'severidad', 'name': 'insignificante', 'label': 'Insignificante (Sin lesiones)'},
        {'list_name': 'severidad', 'name': 'menor', 'label': 'Menor (Primeros auxilios básicos)'},
        {'list_name': 'severidad', 'name': 'moderada', 'label': 'Moderada (Requiere atención médica)'},
        {'list_name': 'severidad', 'name': 'mayor', 'label': 'Mayor (Evacuación inmediata)'},
        {'list_name': 'severidad', 'name': 'catastrofica', 'label': 'Catastrófica'},
        
        # Accesos y Evacuación
        {'list_name': 'acceso', 'name': 'peatonal', 'label': 'Peatonal (Extracción en camilla SKED)'},
        {'list_name': 'acceso', 'name': 'traccion', 'label': 'Tracción animal (Mulas/Caballos)'},
        {'list_name': 'acceso', 'name': '4x4', 'label': 'Vehicular 4x4'},
        {'list_name': 'acceso', 'name': 'remoto', 'label': 'Acceso remoto crítico (Helitransportado)'},
        {'list_name': 'acceso', 'name': 'otro', 'label': 'Otro (Especificar)'},
        
        {'list_name': 'senal', 'name': 'ciega', 'label': 'Sin cobertura celular (Zona ciega)'},
        {'list_name': 'senal', 'name': 'claro', 'label': 'Señal estable (Claro)'},
        {'list_name': 'senal', 'name': 'movistar', 'label': 'Señal estable (Movistar)'},
        {'list_name': 'senal', 'name': 'tigo', 'label': 'Señal estable (Tigo)'},
        {'list_name': 'senal', 'name': 'otro', 'label': 'Otra red (Especificar)'},
        
        {'list_name': 'tiempo_ext', 'name': 't30', 'label': '< 30 minutos'},
        {'list_name': 'tiempo_ext', 'name': 't60', 'label': '1 hora'},
        {'list_name': 'tiempo_ext', 'name': 't120', 'label': '2 a 3 horas'},
        {'list_name': 'tiempo_ext', 'name': 't_medio', 'label': 'Medio día'},
        {'list_name': 'tiempo_ext', 'name': 't_dia', 'label': 'Un día o más'},
        {'list_name': 'tiempo_ext', 'name': 'otro', 'label': 'Otro (Especificar)'},
        
        # Confort y Sostenibilidad
        {'list_name': 'punto_int', 'name': 'descanso', 'label': 'Zona de sombra natural / Descanso'},
        {'list_name': 'punto_int', 'name': 'relajacion', 'label': 'Zona de relajación / Contemplación'},
        {'list_name': 'punto_int', 'name': 'dormir', 'label': 'Zona para dormir / Acampar / Refugio'},
        {'list_name': 'punto_int', 'name': 'hidratacion', 'label': 'Punto hídrico (Reabastecimiento/Filtro)'},
        {'list_name': 'punto_int', 'name': 'banos', 'label': 'Servicios sanitarios / Baños / Letrinas'},
        {'list_name': 'punto_int', 'name': 'alimentacion', 'label': 'Zona de alimentación / Picnic / Restaurante local'},
        {'list_name': 'punto_int', 'name': 'mirador', 'label': 'Mirador panorámico / Punto fotográfico'},
        {'list_name': 'punto_int', 'name': 'comunidad', 'label': 'Interacción comunitaria / Taller artesanal local'},
        {'list_name': 'punto_int', 'name': 'avifauna', 'label': 'Observación de avifauna / Fauna (Bosque seco)'},
        {'list_name': 'punto_int', 'name': 'patrimonio', 'label': 'Patrimonio arquitectónico / Camino ancestral'},
        {'list_name': 'punto_int', 'name': 'otro', 'label': 'Otro (Especificar)'}
    ]

    # 3. Pestaña 'settings'
    settings = [{
        'form_title': 'Validación SIG ISO 21101 - Mot Mot Experiencias',
        'form_id': 'sig_motmot_v5',
        'default_language': 'Español',
        'style': 'theme-grid',
        'logo': 'logo_motmot.png'
    }]

    # Generación y Formato Premium
    nombre_archivo = 'SIG_MotMot_Validacion_Campo.xlsx'
    writer = pd.ExcelWriter(nombre_archivo, engine='xlsxwriter')
    
    pd.DataFrame(survey).to_excel(writer, sheet_name='survey', index=False)
    pd.DataFrame(choices).to_excel(writer, sheet_name='choices', index=False)
    pd.DataFrame(settings).to_excel(writer, sheet_name='settings', index=False)
    
    workbook = writer.book
    
    formato_header = workbook.add_format({
        'bold': True, 'text_wrap': True, 'valign': 'vcenter', 'align': 'center',
        'fg_color': '#DE4A25', 'font_color': 'white', 'border': 1,
        'font_name': 'Arial', 'font_size': 11
    })
    
    formato_celdas = workbook.add_format({
        'valign': 'vcenter', 'text_wrap': True,
        'border': 1, 'border_color': '#8BBFBB',
        'font_name': 'Arial', 'font_size': 10
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
            
    for r in range(len(df_survey)): writer.sheets['survey'].set_row(r+1, 20)
    for r in range(len(df_choices)): writer.sheets['choices'].set_row(r+1, 20)
    for r in range(len(df_settings)): writer.sheets['settings'].set_row(r+1, 100)

    try:
        url_logo = "https://inmobiliariabarichara.wordpress.com/wp-content/uploads/2026/05/cropped-logo-foto-de-perfil-instagram-1.png"
        req = urllib.request.Request(url_logo, headers={'User-Agent': 'Mozilla/5.0'})
        image_data = BytesIO(urllib.request.urlopen(req).read())
        writer.sheets['settings'].insert_image('E2', url_logo, {'image_data': image_data, 'x_scale': 0.15, 'y_scale': 0.15, 'object_position': 1})
    except Exception:
        pass

    writer.close()
    print(f"¡Éxito total! Archivo {nombre_archivo} generado exitosamente. Listo para actualización.")

# Ejecutar
generar_xlsform_sig()