// firebase-config.js - VERSIÓN MAESTRA FINAL (Soporta Todo + Red Social)

// 1. Importamos TODAS las herramientas necesarias
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";

import { 
    getAuth, 
    createUserWithEmailAndPassword, 
    signInWithEmailAndPassword, 
    signOut, 
    onAuthStateChanged, 
    GoogleAuthProvider, 
    signInWithPopup, 
    updateProfile 
} from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";

import { 
    getFirestore, 
    doc, 
    setDoc, 
    getDoc, 
    addDoc, 
    collection, 
    query, 
    where, 
    getDocs, 
    orderBy,          
    serverTimestamp,
    onSnapshot       // <--- ESTE FALTABA Y ERA EL QUE ROMPÍA TODA LA PÁGINA
} from "https://www.gstatic.com/firebasejs/10.11.0/firebase-firestore.js";

import { 
    getStorage, 
    ref, 
    uploadBytes, 
    getDownloadURL 
} from "https://www.gstatic.com/firebasejs/10.11.0/firebase-storage.js";

// 2. TUS LLAVES (PROYECTO MOT-MOT-V5 OFICIAL)
const firebaseConfig = {
  apiKey: "AIzaSyD8X77jva96u1AXBGi0Qn6OpeYDHVRIm9M",
  authDomain: "mot-mot-v5.firebaseapp.com",
  projectId: "mot-mot-v5",
  storageBucket: "mot-mot-v5.firebasestorage.app",
  messagingSenderId: "725633195616",
  appId: "1:725633195616:web:9d1741c664dd84d1246d05"
};

// 3. Inicializar Firebase (El Corazón de la App)
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);
const provider = new GoogleAuthProvider();

// 4. EXPORTAR TODO
export { 
    app, auth, db, storage, provider,
    doc, setDoc, getDoc, addDoc, collection, query, where, getDocs, orderBy, serverTimestamp, onSnapshot, // <-- Exportado aquí
    createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged, signInWithPopup, updateProfile,
    ref, uploadBytes, getDownloadURL 
};