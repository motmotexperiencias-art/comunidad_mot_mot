// firebase-config.js - VERSIÓN MAESTRA FERIA BOGOTÁ (MULTI-IDIOMA + BOTÓN NARANJA + SELECTOR MANUAL)

// 1. Importaciones de Firebase (NO TOCAR)
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { 
    getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, 
    signOut, onAuthStateChanged, GoogleAuthProvider, signInWithPopup, updateProfile 
} from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";
import { 
    getFirestore, doc, setDoc, getDoc, addDoc, collection, query, where, 
    getDocs, orderBy, serverTimestamp, onSnapshot 
} from "https://www.gstatic.com/firebasejs/10.11.0/firebase-firestore.js";
import { 
    getStorage, ref, uploadBytes, getDownloadURL 
} from "https://www.gstatic.com/firebasejs/10.11.0/firebase-storage.js";

// 2. Configuración de Firebase (NO TOCAR)
const firebaseConfig = {
  apiKey: "AIzaSyD8X77jva96u1AXBGi0Qn6OpeYDHVRIm9M",
  authDomain: "mot-mot-v5.firebaseapp.com",
  projectId: "mot-mot-v5",
  storageBucket: "mot-mot-v5.firebasestorage.app",
  messagingSenderId: "725633195616",
  appId: "1:725633195616:web:9d1741c664dd84d1246d05"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);
const provider = new GoogleAuthProvider();

// 3. Exportaciones (NO TOCAR)
export { 
    app, auth, db, storage, provider,
    doc, setDoc, getDoc, addDoc, collection, query, where, getDocs, orderBy, serverTimestamp, onSnapshot,
    createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged, signInWithPopup, updateProfile,
    ref, uploadBytes, getDownloadURL 
};

// ==========================================
// 4. SISTEMA DE TRADUCCIÓN MULTI-IDIOMA
// ==========================================
const traducciones = {
    es: { btn_volver: "← Ir a Mot Mot Experiencias", titulo_bitacora: "MI BITÁCORA", subtitulo: "Conecta con aventureros reales.", btn_publicar: "PUBLICAR EXPERIENCIA" },
    en: { btn_volver: "← Go to Mot Mot Experiences", titulo_bitacora: "MY LOGBOOK", subtitulo: "Connect with real adventurers.", btn_publicar: "POST EXPERIENCE" },
    de: { btn_volver: "← Zurück zu Mot Mot", titulo_bitacora: "MEIN LOGBUCH", subtitulo: "Abenteurern verbinden.", btn_publicar: "ERFAHRUNG POSTEN" },
    fr: { btn_volver: "← Aller à Mot Mot", titulo_bitacora: "MON JOURNAL", subtitulo: "Connectez avec aventuriers.", btn_publicar: "PUBLIER EXPÉRIENCE" },
    it: { btn_volver: "← Vai a Mot Mot", titulo_bitacora: "IL MIO DIARIO", subtitulo: "Connettiti con avventurieri.", btn_publicar: "PUBBLICA ESPERIENZA" },
    pt: { btn_volver: "← Ir para Mot Mot", titulo_bitacora: "MEU DIÁRIO", subtitulo: "Conecte com aventureiros.", btn_publicar: "PUBLICAR EXPERIÊNCIA" }
};

// Función para cambiar idioma manualmente
window.cambiarIdiomaManual = function(lang) {
    localStorage.setItem('motmot_idioma', lang);
    aplicarTraduccionCompleta(lang);
};

function aplicarTraduccionCompleta(lang) {
    // 1. Traducir elementos con data-i18n
    const elementos = document.querySelectorAll('[data-i18n]');
    elementos.forEach(el => {
        const clave = el.getAttribute('data-i18n');
        if (traducciones[lang] && traducciones[lang][clave]) {
            el.innerText = traducciones[lang][clave];
        }
    });

    // 2. Actualizar el texto del botón flotante naranja
    const btnRegresar = document.getElementById('btn-regresar-motmot');
    if (btnRegresar) {
        btnRegresar.innerText = traducciones[lang].btn_volver;
    }
}

function obtenerIdiomaInicial() {
    const guardado = localStorage.getItem('motmot_idioma');
    if (guardado) return guardado;
    const navLang = navigator.language.split('-')[0];
    return traducciones[navLang] ? navLang : 'es';
}

// ==========================================
// 5. INTERFAZ: BOTÓN NARANJA + SELECTOR
// ==========================================
function gestionarInterfazGlobal() {
    const rutaActual = window.location.pathname;
    const paginasExcluidas = ['/index.html', '/', '/registro.html'];
    if (paginasExcluidas.some(p => rutaActual.endsWith(p))) return;

    const idioma = obtenerIdiomaInicial();

    const estiloGlobal = `
        <style>
            /* Botón Naranja Centrado */
            .btn-flotante-motmot {
                position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
                background-color: #F05F3E; color: white !important;
                padding: 14px 24px; border-radius: 50px; text-decoration: none;
                font-family: 'Segoe UI', sans-serif; font-weight: bold; font-size: 15px;
                box-shadow: 0 6px 20px rgba(240, 95, 62, 0.4); z-index: 10000;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                display: flex; align-items: center; gap: 10px; white-space: nowrap;
            }
            .btn-flotante-motmot:hover { background-color: #d84b2d; transform: translateX(-50%) scale(1.05); }

            /* Selector de Idiomas (Arriba Derecha) */
            .selector-idiomas {
                position: fixed; top: 15px; right: 80px; z-index: 10001;
                background: rgba(255,255,255,0.9); padding: 5px 10px;
                border-radius: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                display: flex; gap: 8px; font-family: sans-serif;
            }
            .lang-dot { 
                cursor: pointer; font-size: 12px; font-weight: bold; color: #666; 
                text-transform: uppercase; transition: 0.2s; 
            }
            .lang-dot:hover { color: #F05F3E; }
        </style>
    `;

    const htmlInterfaz = `
        ${estiloGlobal}
        <div class="selector-idiomas">
            <span class="lang-dot" onclick="cambiarIdiomaManual('es')">ES</span>
            <span class="lang-dot" onclick="cambiarIdiomaManual('en')">EN</span>
            <span class="lang-dot" onclick="cambiarIdiomaManual('de')">DE</span>
            <span class="lang-dot" onclick="cambiarIdiomaManual('fr')">FR</span>
            <span class="lang-dot" onclick="cambiarIdiomaManual('pt')">PT</span>
        </div>
        <a href="https://motmotexperiencias.com" id="btn-regresar-motmot" class="btn-flotante-motmot">
            ${traducciones[idioma].btn_volver}
        </a>
    `;

    document.body.insertAdjacentHTML('beforeend', htmlInterfaz);
    aplicarTraduccionCompleta(idioma);
}

// Ejecución segura
if (typeof document !== 'undefined') {
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", gestionarInterfazGlobal);
    } else { gestionarInterfazGlobal(); }
}