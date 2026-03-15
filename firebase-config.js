// firebase-config.js - VERSIÓN FINAL FERIA BOGOTÁ (FULL TRADUCCIÓN + BANDERAS + TARJETAS DINÁMICAS + LOGIN/REGISTRO + HABEAS DATA)

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
// 🛡️ INYECCIÓN FASE 3: IMPORTAMOS deleteUser
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged, GoogleAuthProvider, signInWithPopup, updateProfile, deleteUser } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";

// ✔️ CORRECCIÓN: Se agregó updateDoc a la siguiente línea de importación
import { getFirestore, doc, setDoc, getDoc, addDoc, collection, query, where, getDocs, orderBy, serverTimestamp, onSnapshot, deleteDoc, updateDoc } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-firestore.js";
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

// 🛡️ INYECCIÓN FASE 3: EXPORTAMOS deleteUser y deleteDoc
// ✔️ CORRECCIÓN: Se agregó updateDoc a la siguiente línea de exportación
export { app, auth, db, storage, provider, doc, setDoc, getDoc, addDoc, collection, query, where, getDocs, orderBy, serverTimestamp, onSnapshot, deleteDoc, updateDoc, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged, signInWithPopup, updateProfile, deleteUser, ref, uploadBytes, getDownloadURL };

// ==========================================
// 4. DICCIONARIO MAESTRO (TODO EL CONTENIDO)
// ==========================================
const traducciones = {
    es: { 
        flag: "🇪🇸", titulo_bitacora: "MI BITÁCORA", subtitulo: "Conecta con aventureros reales.", btn_editar: "Editar mi Perfil", btn_salir: "Salir", alerta_ubi: "📍 Ubicación no definida.", configurar_ya: "CONFIGURAR AHORA", buscar_place: "¿A dónde quieres ir?", btn_buscar: "🔍 Buscar", rol_label: "Filtrar por Rol:", f_todos: "🌍 Todos", f_anfitrion: "🏠 Anfitriones", f_guia: "🚩 Guías", f_viajero: "🎒 Viajeros", interes_label: "Por Interés:", opt_todos: "Todos los intereses", exploradores: "Exploradores encontrados", vacio: "Usa el buscador para ver quién está.", seguidores: "Seguidores", siguiendo: "Siguiendo", habla: "Habla:", aprende: "Aprende:", bio_label: "Sobre mí", perfil_privado: "Perfil Privado", seguir: "➕ Seguir", publicar_resena: "Publicar Reseña", identidad_titulo: "Identidad del Creador", siguiente: "Siguiente ➔", atras: "⬅ Atrás", enviar: "✅ ENVIAR A CURADURÍA",
        // BANNERS DASHBOARD
        p_guia_tit: "Eres un Guía Profesional 🏕️", p_guia_sub: "Publica tus rutas y caminatas para que los viajeros te encuentren.", p_guia_btn: "👑 Crear Ruta", p_anf_tit: "Eres Anfitrión Local 🧑‍🌾", p_anf_sub: "¿Te gustaría enseñar un oficio, dar un taller o vender tu itinerario?", p_anf_btn: "👑 Publicar Experiencia", p_via_tit: "Eres un Viajero 🎒", p_via_sub: "¿Quieres planear tu viaje, crear tu ruta y compartirla con la comunidad?", p_via_btn: "📍 Armar Mi Viaje",
        // TARJETAS DINÁMICAS
        rol_guia: "Guía", rol_anfitrion: "Anfitrión", rol_viajero: "Viajero", sin_etiquetas: "Sin etiquetas", default_user: "Usuario", explorador_nav: "Explorador",
        // LOGIN / REGISTRO
        log_img_tit: "Bienvenido de nuevo.", log_img_sub: "La montaña te espera.", log_volver: "← Volver al inicio", log_tit: "Hola viajero", log_sub: "Ingresa tus datos para continuar.", log_email: "Correo Electrónico", log_pass: "Contraseña", log_btn: "ENTRAR", log_o: "O ingresa con", log_google: "Continuar con Google", log_no_cuenta: "¿No tienes cuenta?", log_registro: "Regístrate gratis", reg_img_tit: "Tu próxima aventura comienza aquí.", reg_img_sub: "Únete a la comunidad de viajeros y anfitriones MOT.", reg_tit: "Crear Cuenta", reg_sub: "Regístrate para conectar, viajar y compartir.", reg_nombre: "Nombre Completo", reg_place_nom: "Ej. Antonio Mot Mot", reg_btn: "REGISTRARME", reg_o: "O regístrate con", reg_ya_cuenta: "¿Ya tienes cuenta?", reg_inicia: "Inicia Sesión"
    },
    en: { 
        flag: "🇬🇧", titulo_bitacora: "MY LOGBOOK", subtitulo: "Connect with real adventurers.", btn_editar: "Edit my Profile", btn_salir: "Logout", alerta_ubi: "📍 Location not defined.", configurar_ya: "SETUP NOW", buscar_place: "Where to go?", btn_buscar: "🔍 Search", rol_label: "Filter by Role:", f_todos: "🌍 All", f_anfitrion: "🏠 Hosts", f_guia: "🚩 Guides", f_viajero: "🎒 Travelers", interes_label: "By Interest:", opt_todos: "All interests", exploradores: "Explorers found", vacio: "Use the search to see who is here.", seguidores: "Followers", siguiendo: "Following", habla: "Speaks:", aprende: "Learning:", bio_label: "About me", perfil_privado: "Private Profile", seguir: "➕ Follow", publicar_resena: "Post Review", identidad_titulo: "Creator Identity", siguiente: "Next ➔", atras: "⬅ Back", enviar: "✅ SUBMIT TO CURATION",
        p_guia_tit: "You are a Professional Guide 🏕️", p_guia_sub: "Publish your routes and hikes so travelers can find you.", p_guia_btn: "👑 Create Route", p_anf_tit: "You are a Local Host 🧑‍🌾", p_anf_sub: "Would you like to teach a craft, give a workshop or sell your itinerary?", p_anf_btn: "👑 Post Experience", p_via_tit: "You are a Traveler 🎒", p_via_sub: "Want to plan your trip, create a route and share it?", p_via_btn: "📍 Plan My Trip",
        rol_guia: "Guide", rol_anfitrion: "Host", rol_viajero: "Traveler", sin_etiquetas: "No tags", default_user: "User", explorador_nav: "Explorer",
        log_img_tit: "Welcome back.", log_img_sub: "The mountain awaits.", log_volver: "← Back to home", log_tit: "Hello traveler", log_sub: "Enter your details to continue.", log_email: "Email", log_pass: "Password", log_btn: "LOGIN", log_o: "Or sign in with", log_google: "Continue with Google", log_no_cuenta: "Don't have an account?", log_registro: "Sign up for free", reg_img_tit: "Your next adventure starts here.", reg_img_sub: "Join the MOT traveler and host community.", reg_tit: "Create Account", reg_sub: "Sign up to connect, travel and share.", reg_nombre: "Full Name", reg_place_nom: "E.g. Antonio Mot Mot", reg_btn: "SIGN UP", reg_o: "Or sign up with", reg_ya_cuenta: "Already have an account?", reg_inicia: "Login"
    },
    de: { 
        flag: "🇩🇪", titulo_bitacora: "MEIN LOGBUCH", subtitulo: "Mit Abenteurern verbinden.", btn_editar: "Profil bearbeiten", btn_salir: "Abmelden", alerta_ubi: "📍 Ort nicht definiert.", configurar_ya: "JETZT KONFIGURIEREN", buscar_place: "Wohin gehen?", btn_buscar: "🔍 Suchen", rol_label: "Nach Rolle filtern:", f_todos: "🌍 Alle", f_anfitrion: "🏠 Gastgeber", f_guia: "🚩 Führer", f_viajero: "🎒 Reisende", interes_label: "Nach Interesse:", opt_todos: "Alle Interessen", exploradores: "Gefundene Entdecker", vacio: "Suche nutzen.", seguidores: "Follower", siguiendo: "Folgt", habla: "Spricht:", aprende: "Lernt:", bio_label: "Über mich", perfil_privado: "Privates Profil", seguir: "➕ Folgen", publicar_resena: "Bewertung posten", identidad_titulo: "Identität", siguiente: "Weiter ➔", atras: "⬅ Zurück", enviar: "✅ EINREICHEN",
        p_guia_tit: "Du bist ein professioneller Führer 🏕️", p_guia_sub: "Veröffentliche deine Routen, damit Reisende dich finden.", p_guia_btn: "👑 Route erstellen", p_anf_tit: "Du bist ein lokaler Gastgeber 🧑‍🌾", p_anf_sub: "Möchtest du ein Handwerk unterrichten oder dein Programm verkaufen?", p_anf_btn: "👑 Erfahrung posten", p_via_tit: "Du bist ein Reisender 🎒", p_via_sub: "Möchtest du deine Reise planen und mit der Community teilen?", p_via_btn: "📍 Meine Reise planen",
        rol_guia: "Führer", rol_anfitrion: "Gastgeber", rol_viajero: "Reisender", sin_etiquetas: "Keine Tags", default_user: "Benutzer", explorador_nav: "Entdecker",
        log_img_tit: "Willkommen zurück.", log_img_sub: "Die Berge warten.", log_volver: "← Zurück zur Startseite", log_tit: "Hallo Reisender", log_sub: "Geben Sie Ihre Daten ein.", log_email: "E-Mail", log_pass: "Passwort", log_btn: "ANMELDEN", log_o: "Oder anmelden mit", log_google: "Weiter mit Google", log_no_cuenta: "Noch kein Konto?", log_registro: "Kostenlos registrieren", reg_img_tit: "Dein nächstes Abenteuer beginnt hier.", reg_img_sub: "Tritt der MOT-Community bei.", reg_tit: "Konto erstellen", reg_sub: "Registrieren, um sich zu verbinden.", reg_nombre: "Vollständiger Name", reg_place_nom: "Z.B. Antonio Mot Mot", reg_btn: "REGISTRIEREN", reg_o: "Oder registrieren mit", reg_ya_cuenta: "Hast du schon ein Konto?", reg_inicia: "Anmelden"
    },
    fr: { 
        flag: "🇫🇷", titulo_bitacora: "MON JOURNAL", subtitulo: "Connectez avec des aventuriers.", btn_editar: "Modifier le profil", btn_salir: "Quitter", alerta_ubi: "📍 Lieu non défini.", configurar_ya: "CONFIGURER", buscar_place: "Où allez-vous?", btn_buscar: "🔍 Chercher", rol_label: "Filtrer par rôle:", f_todos: "🌍 Tous", f_anfitrion: "🏠 Hôtes", f_guia: "🚩 Guides", f_viajero: "🎒 Voyageurs", interes_label: "Par intérêt:", opt_todos: "Tous les intérêts", exploradores: "Explorateurs trouvés", vacio: "Utilisez la recherche.", seguidores: "Abonnés", siguiendo: "Abonnements", habla: "Parle:", aprende: "Apprend:", bio_label: "À propos", perfil_privado: "Profil Privé", seguir: "➕ Suivre", publicar_resena: "Publier un avis", identidad_titulo: "Identité", siguiente: "Suivant ➔", atras: "⬅ Retour", envoyer: "✅ ENVOYER",
        p_guia_tit: "Vous êtes un Guide Professionnel 🏕️", p_guia_sub: "Publiez vos itinéraires pour que les voyageurs vous trouvent.", p_guia_btn: "👑 Créer un itinéraire", p_anf_tit: "Vous êtes un Hôte Local 🧑‍🌾", p_anf_sub: "Aimeriez-vous enseigner un métier ou vendre votre itinéraire ?", p_anf_btn: "👑 Publier une expérience", p_via_tit: "Vous êtes un Voyageur 🎒", p_via_sub: "Voulez-vous planifier votre voyage et le partager ?", p_via_btn: "📍 Planifier mon voyage",
        rol_guia: "Guide", rol_anfitrion: "Hôte", rol_viajero: "Voyageur", sin_etiquetas: "Sans tags", default_user: "Utilisateur", explorador_nav: "Explorateur",
        log_img_tit: "Bon retour.", log_img_sub: "La montagne vous attend.", log_volver: "← Retour à l'accueil", log_tit: "Bonjour voyageur", log_sub: "Entrez vos coordonnées.", log_email: "E-mail", log_pass: "Mot de passe", log_btn: "CONNEXION", log_o: "Ou se connecter avec", log_google: "Continuer avec Google", log_no_cuenta: "Pas de compte ?", log_registro: "S'inscrire gratuitement", reg_img_tit: "Votre prochaine aventure commence ici.", reg_img_sub: "Rejoignez la communauté MOT.", reg_tit: "Créer un compte", reg_sub: "Inscrivez-vous pour voyager.", reg_nombre: "Nom complet", reg_place_nom: "Ex. Antonio Mot Mot", reg_btn: "S'INSCRIRE", reg_o: "Ou s'inscrire avec", reg_ya_cuenta: "Vous avez déjà un compte ?", reg_inicia: "Se connecter"
    },
    it: { 
        flag: "🇮🇹", titulo_bitacora: "IL MIO DIARIO", subtitulo: "Connettiti con avventurieri.", btn_editar: "Modifica profilo", btn_salir: "Esci", alerta_ubi: "📍 Luogo non definito.", configurar_ya: "CONFIGURA", buscar_place: "Dove andare?", btn_buscar: "🔍 Cerca", rol_label: "Filtra per ruolo:", f_todos: "🌍 Tutti", f_anfitrion: "🏠 Ospiti", f_guia: "🚩 Guide", f_viajero: "🎒 Viaggiatori", interes_label: "Per interesse:", opt_todos: "Tutti gli interessi", exploradores: "Esploratori trovati", vacio: "Usa la ricerca.", seguidores: "Follower", siguiendo: "Seguiti", habla: "Parla:", aprende: "Impara:", bio_label: "Su di me", perfil_privado: "Profilo Privato", seguir: "➕ Segui", publicar_resena: "Recensisci", identidad_titulo: "Identità", seguente: "Avanti ➔", atras: "⬅ Indietro", inviare: "✅ INVIA",
        p_guia_tit: "Sei una Guida Professionale 🏕️", p_guia_sub: "Pubblica i tuoi percorsi in modo che i viaggiatori ti trovino.", p_guia_btn: "👑 Crea Percorso", p_anf_tit: "Sei un Ospite Locale 🧑‍🌾", p_anf_sub: "Ti piacerebbe insegnare un mestiere o vendere il tuo itinerario?", p_anf_btn: "👑 Pubblica Esperienza", p_via_tit: "Sei un Viaggiatore 🎒", p_via_sub: "Vuoi pianificare il tuo viaggio e condividerlo?", p_via_btn: "📍 Pianifica il mio viaggio",
        rol_guia: "Guida", rol_anfitrion: "Ospite", rol_viajero: "Viaggiatore", sin_etiquetas: "Senza tag", default_user: "Utente", explorador_nav: "Esploratore",
        log_img_tit: "Bentornato.", log_img_sub: "La montagna ti aspetta.", log_volver: "← Torna alla home", log_tit: "Ciao viaggiatore", log_sub: "Inserisci i tuoi dati.", log_email: "Email", log_pass: "Password", log_btn: "ACCEDI", log_o: "Oppure accedi con", log_google: "Continua con Google", log_no_cuenta: "Non hai un account?", log_registro: "Iscriviti gratis", reg_img_tit: "La tua prossima avventura inizia qui.", reg_img_sub: "Unisciti alla comunità MOT.", reg_tit: "Crea Account", reg_sub: "Iscriviti per connetterti.", reg_nombre: "Nome e Cognome", reg_place_nom: "Es. Antonio Mot Mot", reg_btn: "ISCRIVITI", reg_o: "O iscriviti con", reg_ya_cuenta: "Hai già un account?", reg_inicia: "Accedi"
    },
    pt: { 
        flag: "🇧🇷", titulo_bitacora: "MEU DIÁRIO", subtitulo: "Conecte-se com aventureiros.", btn_editar: "Editar perfil", btn_salir: "Sair", alerta_ubi: "📍 Local não definido.", configurar_ya: "CONFIGURAR", buscar_place: "Para onde quer ir?", btn_buscar: "🔍 Buscar", rol_label: "Filtrar por cargo:", f_todos: "🌍 Todos", f_anfitrion: "🏠 Anfitriões", f_guia: "🚩 Guias", f_viajero: "🎒 Viajeros", interes_label: "Por interesse:", opt_todos: "Todos interesses", exploradores: "Exploradores encontrados", vacio: "Use a busca.", seguidores: "Seguidores", siguiendo: "Seguindo", habla: "Fala:", aprende: "Aprende:", bio_label: "Sobre mim", perfil_privado: "Perfil Privado", seguir: "➕ Seguir", publicar_resena: "Publicar Resenha", identidade_titulo: "Identidade", seguinte: "Próximo ➔", atras: "⬅ Voltar", enviar: "✅ ENVIAR",
        p_guia_tit: "Você é um Guia Profissional 🏕️", p_guia_sub: "Publique suas rotas para que os viajantes o encontrem.", p_guia_btn: "👑 Criar Rota", p_anf_tit: "Você é um Anfitrião Local 🧑‍🌾", p_anf_sub: "Gostaria de ensinar um ofício ou vender seu itinerário?", p_anf_btn: "👑 Publicar Experiência", p_via_tit: "Você é um Viajante 🎒", p_via_sub: "Quer planejar sua viagem e compartilhar com a comunidade?", p_via_btn: "📍 Planejar Minha Viagem",
        rol_guia: "Guia", rol_anfitrion: "Anfitrião", rol_viajero: "Viajante", sin_etiquetas: "Sem tags", default_user: "Usuário", explorador_nav: "Explorador",
        log_img_tit: "Bem-vindo de volta.", log_img_sub: "A montanha te espera.", log_volver: "← Voltar ao início", log_tit: "Olá viajante", log_sub: "Insira seus dados.", log_email: "E-mail", log_pass: "Senha", log_btn: "ENTRAR", log_o: "Ou entrar com", log_google: "Continuar com o Google", log_no_cuenta: "Não tem uma conta?", log_registro: "Cadastre-se grátis", reg_img_tit: "Sua próxima aventura começa aqui.", reg_img_sub: "Junte-se à comunidade MOT.", reg_tit: "Criar Conta", reg_sub: "Cadastre-se para viajar.", reg_nombre: "Nome Completo", reg_place_nom: "Ex. Antonio Mot Mot", reg_btn: "CADASTRAR", reg_o: "Ou cadastre-se com", reg_ya_cuenta: "Já tem uma conta?", reg_inicia: "Entrar"
    }
};

// Guardamos el diccionario globalmente para que las tarjetas de usuario dinámicas puedan leerlo
window.diccionarioGlobal = traducciones;

// ==========================================
// 5. LÓGICA DE INTERFAZ (UI)
// ==========================================
window.cambiarIdiomaManual = (lang) => {
    localStorage.setItem('motmot_lang', lang);
    location.reload(); 
};

function aplicarTraduccionCompleta(lang) {
    const d = traducciones[lang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (d[key]) {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') el.placeholder = d[key];
            else el.innerText = d[key];
        }
    });
}

function cargarUI() {
    const ruta = window.location.pathname;
    
    if (['/index.html', '/'].some(p => ruta.endsWith(p))) return;

    const lang = localStorage.getItem('motmot_lang') || (navigator.language.startsWith('es') ? 'es' : 'en');
    
    // CSS Actualizado y Limpio
    const css = `
        <style>
            .lang-wrapper { z-index: 10001; font-family: 'Montserrat', sans-serif; }
            .lang-wrapper.fixed-mode { position: fixed; top: 15px; left: 15px; } 
            .lang-wrapper.nav-mode { position: relative; display: inline-block; margin-right: auto;}
            
            .lang-trigger { background: white; padding: 8px; border-radius: 50%; box-shadow: 0 2px 10px rgba(0,0,0,0.1); cursor: pointer; font-size: 20px; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border: 2px solid #eee; transition: 0.3s; }
            .lang-trigger:hover { border-color: #80C4C8; }
            
            .lang-menu { display: none; position: absolute; top: 50px; left: 0; background: white; border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.15); padding: 10px; flex-direction: column; gap: 5px; min-width: 140px; border: 1px solid #eee; }
            .lang-wrapper:hover .lang-menu { display: flex; }
            
            .lang-option { padding: 8px 15px; cursor: pointer; border-radius: 8px; font-size: 14px; display: flex; gap: 10px; align-items: center; transition: 0.2s; font-weight: 600; color: #333; }
            .lang-option:hover { background: #f4f6f8; color: #E65127; }
        </style>
    `;

    // Nuevo selector con nombres completos
    const langHTML = `
        <div class="lang-wrapper" id="selector-idiomas">
            <div class="lang-trigger">${traducciones[lang].flag}</div>
            <div class="lang-menu">
                <div class="lang-option" onclick="cambiarIdiomaManual('es')">🇪🇸 Español</div>
                <div class="lang-option" onclick="cambiarIdiomaManual('en')">🇬🇧 English</div>
                <div class="lang-option" onclick="cambiarIdiomaManual('de')">🇩🇪 Deutsch</div>
                <div class="lang-option" onclick="cambiarIdiomaManual('fr')">🇫🇷 Français</div>
                <div class="lang-option" onclick="cambiarIdiomaManual('it')">🇮🇹 Italiano</div>
                <div class="lang-option" onclick="cambiarIdiomaManual('pt')">🇧🇷 Português</div>
            </div>
        </div>
    `;

    document.head.insertAdjacentHTML('beforeend', css);

    // INYECCIÓN INTELIGENTE: Si hay barra de navegación blanca, lo anclamos ahí.
    const navBarLeft = document.querySelector('.dashboard-nav > div:first-child');
    if (navBarLeft) {
        navBarLeft.innerHTML = langHTML;
        document.getElementById('selector-idiomas').classList.add('nav-mode');
        navBarLeft.style.width = 'auto'; // Ajuste visual
    } else {
        // Si no hay barra (como en el login), lo dejamos flotando en la esquina
        document.body.insertAdjacentHTML('afterbegin', langHTML);
        document.getElementById('selector-idiomas').classList.add('fixed-mode');
    }

    aplicarTraduccionCompleta(lang);
}

if (typeof document !== 'undefined') {
    document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", cargarUI) : cargarUI();
}