// firebase-config.js - VERSIÓN FINAL FERIA BOGOTÁ (FULL TRADUCCIÓN + BANDERAS + BOTÓN)

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged, GoogleAuthProvider, signInWithPopup, updateProfile } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";
import { getFirestore, doc, setDoc, getDoc, addDoc, collection, query, where, getDocs, orderBy, serverTimestamp, onSnapshot } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-firestore.js";
import { getStorage, ref, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-storage.js";

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

export { app, auth, db, storage, provider, doc, setDoc, getDoc, addDoc, collection, query, where, getDocs, orderBy, serverTimestamp, onSnapshot, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged, signInWithPopup, updateProfile, ref, uploadBytes, getDownloadURL };

// ==========================================
// 4. DICCIONARIO MAESTRO (TODO EL CONTENIDO)
// ==========================================
const traducciones = {
    es: { 
        flag: "🇪🇸", btn_volver: "← Ir a Mot Mot Experiencias", titulo_bitacora: "MI BITÁCORA", subtitulo: "Conecta con aventureros reales.", btn_editar: "Editar mi Perfil", btn_salir: "Salir", alerta_ubi: "📍 Ubicación no definida.", configurar_ya: "CONFIGURAR AHORA", buscar_place: "¿A dónde quieres ir?", btn_buscar: "🔍 Buscar", rol_label: "Filtrar por Rol:", f_todos: "🌍 Todos", f_anfitrion: "🏠 Anfitriones", f_guia: "🚩 Guías", f_viajero: "🎒 Viajeros", interes_label: "Por Interés:", opt_todos: "Todos los intereses", exploradores: "Exploradores encontrados", vacio: "Usa el buscador para ver quién está.", seguidores: "Seguidores", siguiendo: "Siguiendo", habla: "Habla:", aprende: "Aprende:", bio_label: "Sobre mí", perfil_privado: "Perfil Privado", seguir: "➕ Seguir", publicar_resena: "Publicar Reseña", identidad_titulo: "Identidad del Creador", siguiente: "Siguiente ➔", atras: "⬅ Atrás", enviar: "✅ ENVIAR A CURADURÍA",
        // LOGIN
        log_img_tit: "Bienvenido de nuevo.", log_img_sub: "La montaña te espera.", log_volver: "← Volver al inicio", log_tit: "Hola viajero", log_sub: "Ingresa tus datos para continuar.", log_email: "Correo Electrónico", log_pass: "Contraseña", log_btn: "ENTRAR", log_o: "O ingresa con", log_google: "Continuar con Google", log_no_cuenta: "¿No tienes cuenta?", log_registro: "Regístrate gratis",
        // REGISTRO
        reg_img_tit: "Tu próxima aventura comienza aquí.", reg_img_sub: "Únete a la comunidad de viajeros y anfitriones MOT.", reg_tit: "Crear Cuenta", reg_sub: "Regístrate para conectar, viajar y compartir.", reg_nombre: "Nombre Completo", reg_place_nom: "Ej. Antonio Mot Mot", reg_btn: "REGISTRARME", reg_o: "O regístrate con", reg_ya_cuenta: "¿Ya tienes cuenta?", reg_inicia: "Inicia Sesión"
    },
    en: { 
        flag: "🇬🇧", btn_volver: "← Back to Mot Mot Experiences", titulo_bitacora: "MY LOGBOOK", subtitulo: "Connect with real adventurers.", btn_editar: "Edit my Profile", btn_salir: "Logout", alerta_ubi: "📍 Location not defined.", configurar_ya: "SETUP NOW", buscar_place: "Where to go?", btn_buscar: "🔍 Search", rol_label: "Filter by Role:", f_todos: "🌍 All", f_anfitrion: "🏠 Hosts", f_guia: "🚩 Guides", f_viajero: "🎒 Travelers", interes_label: "By Interest:", opt_todos: "All interests", exploradores: "Explorers found", vacio: "Use the search to see who is here.", seguidores: "Followers", siguiendo: "Following", habla: "Speaks:", aprende: "Learning:", bio_label: "About me", perfil_privado: "Private Profile", seguir: "➕ Follow", publicar_resena: "Post Review", identidad_titulo: "Creator Identity", siguiente: "Next ➔", atras: "⬅ Back", enviar: "✅ SUBMIT TO CURATION",
        // LOGIN
        log_img_tit: "Welcome back.", log_img_sub: "The mountain awaits.", log_volver: "← Back to home", log_tit: "Hello traveler", log_sub: "Enter your details to continue.", log_email: "Email", log_pass: "Password", log_btn: "LOGIN", log_o: "Or sign in with", log_google: "Continue with Google", log_no_cuenta: "Don't have an account?", log_registro: "Sign up for free",
        // REGISTRO
        reg_img_tit: "Your next adventure starts here.", reg_img_sub: "Join the MOT traveler and host community.", reg_tit: "Create Account", reg_sub: "Sign up to connect, travel and share.", reg_nombre: "Full Name", reg_place_nom: "E.g. Antonio Mot Mot", reg_btn: "SIGN UP", reg_o: "Or sign up with", reg_ya_cuenta: "Already have an account?", reg_inicia: "Login"
    },
    de: { 
        flag: "🇩🇪", btn_volver: "← Zurück zu Mot Mot", titulo_bitacora: "MEIN LOGBUCH", subtitulo: "Mit Abenteurern verbinden.", btn_editar: "Profil bearbeiten", btn_salir: "Abmelden", alerta_ubi: "📍 Ort nicht definiert.", configurar_ya: "JETZT KONFIGURIEREN", buscar_place: "Wohin gehen?", btn_buscar: "🔍 Suchen", rol_label: "Nach Rolle filtern:", f_todos: "🌍 Alle", f_anfitrion: "🏠 Gastgeber", f_guia: "🚩 Führer", f_viajero: "🎒 Reisende", interes_label: "Nach Interesse:", opt_todos: "Alle Interessen", exploradores: "Gefundene Entdecker", vacio: "Suche nutzen.", seguidores: "Follower", siguiendo: "Folgt", habla: "Spricht:", aprende: "Lernt:", bio_label: "Über mich", perfil_privado: "Privates Profil", seguir: "➕ Folgen", publicar_resena: "Bewertung posten", identidad_titulo: "Identität", siguiente: "Weiter ➔", atras: "⬅ Zurück", enviar: "✅ EINREICHEN",
        // LOGIN
        log_img_tit: "Willkommen zurück.", log_img_sub: "Die Berge warten.", log_volver: "← Zurück zur Startseite", log_tit: "Hallo Reisender", log_sub: "Geben Sie Ihre Daten ein.", log_email: "E-Mail", log_pass: "Passwort", log_btn: "ANMELDEN", log_o: "Oder anmelden mit", log_google: "Weiter mit Google", log_no_cuenta: "Noch kein Konto?", log_registro: "Kostenlos registrieren",
        // REGISTRO
        reg_img_tit: "Dein nächstes Abenteuer beginnt hier.", reg_img_sub: "Tritt der MOT-Community bei.", reg_tit: "Konto erstellen", reg_sub: "Registrieren, um sich zu verbinden.", reg_nombre: "Vollständiger Name", reg_place_nom: "Z.B. Antonio Mot Mot", reg_btn: "REGISTRIEREN", reg_o: "Oder registrieren mit", reg_ya_cuenta: "Hast du schon ein Konto?", reg_inicia: "Anmelden"
    },
    fr: { 
        flag: "🇫🇷", btn_volver: "← Retour à Mot Mot", titulo_bitacora: "MON JOURNAL", subtitulo: "Connectez avec des aventuriers.", btn_editar: "Modifier le profil", btn_salir: "Quitter", alerta_ubi: "📍 Lieu non défini.", configurar_ya: "CONFIGURER", buscar_place: "Où allez-vous?", btn_buscar: "🔍 Chercher", rol_label: "Filtrer par rôle:", f_todos: "🌍 Tous", f_anfitrion: "🏠 Hôtes", f_guia: "🚩 Guides", f_viajero: "🎒 Voyageurs", interes_label: "Par intérêt:", opt_todos: "Tous les intérêts", exploradores: "Explorateurs trouvés", vacio: "Utilisez la recherche.", seguidores: "Abonnés", siguiendo: "Abonnements", habla: "Parle:", aprende: "Apprend:", bio_label: "À propos", perfil_privado: "Profil Privé", seguir: "➕ Suivre", publicar_resena: "Publier un avis", identidad_titulo: "Identité", siguiente: "Suivant ➔", atras: "⬅ Retour", enviar: "✅ ENVOYER",
        // LOGIN
        log_img_tit: "Bon retour.", log_img_sub: "La montagne vous attend.", log_volver: "← Retour à l'accueil", log_tit: "Bonjour voyageur", log_sub: "Entrez vos coordonnées.", log_email: "E-mail", log_pass: "Mot de passe", log_btn: "CONNEXION", log_o: "Ou se connecter avec", log_google: "Continuer avec Google", log_no_cuenta: "Pas de compte ?", log_registro: "S'inscrire gratuitement",
        // REGISTRO
        reg_img_tit: "Votre prochaine aventure commence ici.", reg_img_sub: "Rejoignez la communauté MOT.", reg_tit: "Créer un compte", reg_sub: "Inscrivez-vous pour voyager.", reg_nombre: "Nom complet", reg_place_nom: "Ex. Antonio Mot Mot", reg_btn: "S'INSCRIRE", reg_o: "Ou s'inscrire avec", reg_ya_cuenta: "Vous avez déjà un compte ?", reg_inicia: "Se connecter"
    },
    it: { 
        flag: "🇮🇹", btn_volver: "← Vai a Mot Mot", titulo_bitacora: "IL MIO DIARIO", subtitulo: "Connettiti con avventurieri.", btn_editar: "Modifica profilo", btn_salir: "Esci", alerta_ubi: "📍 Luogo non definito.", configurar_ya: "CONFIGURA", buscar_place: "Dove andare?", btn_buscar: "🔍 Cerca", rol_label: "Filtra per ruolo:", f_todos: "🌍 Tutti", f_anfitrion: "🏠 Ospiti", f_guia: "🚩 Guide", f_viajero: "🎒 Viaggiatori", interes_label: "Per interesse:", opt_todos: "Tutti gli interessi", exploradores: "Esploratori trovati", vacio: "Usa la ricerca.", seguidores: "Follower", siguiendo: "Seguiti", habla: "Parla:", aprende: "Impara:", bio_label: "Su di me", perfil_privado: "Profilo Privato", seguir: "➕ Segui", publicar_resena: "Recensisci", identidad_titulo: "Identità", seguente: "Avanti ➔", atras: "⬅ Indietro", enviar: "✅ INVIA",
        // LOGIN
        log_img_tit: "Bentornato.", log_img_sub: "La montagna ti aspetta.", log_volver: "← Torna alla home", log_tit: "Ciao viaggiatore", log_sub: "Inserisci i tuoi dati.", log_email: "Email", log_pass: "Password", log_btn: "ACCEDI", log_o: "Oppure accedi con", log_google: "Continua con Google", log_no_cuenta: "Non hai un account?", log_registro: "Iscriviti gratis",
        // REGISTRO
        reg_img_tit: "La tua prossima avventura inizia qui.", reg_img_sub: "Unisciti alla comunità MOT.", reg_tit: "Crea Account", reg_sub: "Iscriviti per connetterti.", reg_nombre: "Nome e Cognome", reg_place_nom: "Es. Antonio Mot Mot", reg_btn: "ISCRIVITI", reg_o: "O iscriviti con", reg_ya_cuenta: "Hai già un account?", reg_inicia: "Accedi"
    },
    pt: { 
        flag: "🇧🇷", btn_volver: "← Ir para Mot Mot", titulo_bitacora: "MEU DIÁRIO", subtitulo: "Conecte-se com aventureiros.", btn_editar: "Editar perfil", btn_salir: "Sair", alerta_ubi: "📍 Local não definido.", configurar_ya: "CONFIGURAR", buscar_place: "Para onde quer ir?", btn_buscar: "🔍 Buscar", rol_label: "Filtrar por cargo:", f_todos: "🌍 Todos", f_anfitrion: "🏠 Anfitriões", f_guia: "🚩 Guias", f_viajero: "🎒 Viajeros", interes_label: "Por interesse:", opt_todos: "Todos interesses", exploradores: "Exploradores encontrados", vacio: "Use a busca.", seguidores: "Seguidores", siguiendo: "Seguindo", habla: "Fala:", aprende: "Aprende:", bio_label: "Sobre mim", perfil_privado: "Perfil Privado", seguir: "➕ Seguir", publicar_resena: "Publicar Resenha", identidad_titulo: "Identidade", siguiente: "Próximo ➔", atras: "⬅ Voltar", enviar: "✅ ENVIAR",
        // LOGIN
        log_img_tit: "Bem-vindo de volta.", log_img_sub: "A montanha te espera.", log_volver: "← Voltar ao início", log_tit: "Olá viajante", log_sub: "Insira seus dados.", log_email: "E-mail", log_pass: "Senha", log_btn: "ENTRAR", log_o: "Ou entrar com", log_google: "Continuar com o Google", log_no_cuenta: "Não tem uma conta?", log_registro: "Cadastre-se grátis",
        // REGISTRO
        reg_img_tit: "Sua próxima aventura começa aqui.", reg_img_sub: "Junte-se à comunidade MOT.", reg_tit: "Criar Conta", reg_sub: "Cadastre-se para viajar.", reg_nombre: "Nome Completo", reg_place_nom: "Ex. Antonio Mot Mot", reg_btn: "CADASTRAR", reg_o: "Ou cadastre-se com", reg_ya_cuenta: "Já tem uma conta?", reg_inicia: "Entrar"
    }
};

// ==========================================
// 5. LÓGICA DE INTERFAZ (UI)
// ==========================================
window.cambiarIdiomaManual = (lang) => {
    localStorage.setItem('motmot_lang', lang);
    location.reload(); // Recarga para aplicar a todo el DOM de forma limpia
};

function aplicarTraduccionCompleta(lang) {
    const d = traducciones[lang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (d[key]) {
            if (el.tagName === 'INPUT') el.placeholder = d[key];
            else el.innerText = d[key];
        }
    });
}

function cargarUI() {
    const ruta = window.location.pathname;
    
    // NOTA: Quité 'login.html' y 'registro.html' de aquí para que SÍ aparezcan las banderas
    if (['/index.html', '/'].some(p => ruta.endsWith(p))) return;

    const lang = localStorage.getItem('motmot_lang') || (navigator.language.startsWith('es') ? 'es' : 'en');
    
    const css = `
        <style>
            .btn-flotante-motmot { position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%); background: #F05F3E; color: white !important; padding: 12px 25px; border-radius: 50px; text-decoration: none; font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 14px; box-shadow: 0 4px 15px rgba(230,81,39,0.4); z-index: 10000; transition: 0.3s; white-space: nowrap; }
            .btn-flotante-motmot:hover { transform: translateX(-50%) scale(1.05); background: #d84b2d; }
            
            .lang-wrapper { position: fixed; top: 15px; left: 15px; z-index: 10001; font-family: sans-serif; }
            .lang-trigger { background: white; padding: 8px; border-radius: 50%; box-shadow: 0 2px 10px rgba(0,0,0,0.1); cursor: pointer; font-size: 20px; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border: 2px solid #eee; }
            .lang-menu { display: none; position: absolute; top: 50px; left: 0; background: white; border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.15); padding: 5px; flex-direction: column; gap: 5px; }
            .lang-wrapper:hover .lang-menu { display: flex; }
            .lang-option { padding: 8px 15px; cursor: pointer; border-radius: 8px; font-size: 18px; display: flex; gap: 10px; align-items: center; transition: 0.2s; }
            .lang-option:hover { background: #f4f6f8; }
        </style>
    `;

    // LÓGICA PARA OCULTAR EL BOTÓN NARANJA SOLO EN LOGIN Y REGISTRO
    let botonHTML = "";
    if (!ruta.endsWith('/login.html') && !ruta.endsWith('/registro.html')) {
        botonHTML = `<a href="https://motmotexperiencias.com" class="btn-flotante-motmot">${traducciones[lang].btn_volver}</a>`;
    }

    const html = `
        ${css}
        <div class="lang-wrapper">
            <div class="lang-trigger">${traducciones[lang].flag}</div>
            <div class="lang-menu">
                <div class="lang-option" onclick="cambiarIdiomaManual('es')">🇪🇸 <span style="font-size:12px; font-weight:bold;">ES</span></div>
                <div class="lang-option" onclick="cambiarIdiomaManual('en')">🇬🇧 <span style="font-size:12px; font-weight:bold;">EN</span></div>
                <div class="lang-option" onclick="cambiarIdiomaManual('de')">🇩🇪 <span style="font-size:12px; font-weight:bold;">DE</span></div>
                <div class="lang-option" onclick="cambiarIdiomaManual('fr')">🇫🇷 <span style="font-size:12px; font-weight:bold;">FR</span></div>
                <div class="lang-option" onclick="cambiarIdiomaManual('it')">🇮🇹 <span style="font-size:12px; font-weight:bold;">IT</span></div>
                <div class="lang-option" onclick="cambiarIdiomaManual('pt')">🇧🇷 <span style="font-size:12px; font-weight:bold;">PT</span></div>
            </div>
        </div>
        ${botonHTML}
    `;

    document.body.insertAdjacentHTML('afterbegin', html);
    aplicarTraduccionCompleta(lang);
}

if (typeof document !== 'undefined') {
    document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", cargarUI) : cargarUI();
}