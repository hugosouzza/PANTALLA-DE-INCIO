import streamlit as st
import sqlite3
import hashlib

def crear_base_datos():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT,
                 apellido TEXT,
                 email TEXT UNIQUE,
                 contrasena TEXT,
                 kyc_completed INTEGER,
                 risk_profile_completed INTEGER)''')
    conn.commit()
    conn.close()

def encriptar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

def registrar_usuario(nombre, apellido, email, contrasena):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios (nombre, apellido, email, contrasena, kyc_completed, risk_profile_completed) VALUES (?, ?, ?, ?, 0, 0)",
                  (nombre, apellido, email, encriptar_contrasena(contrasena)))
        conn.commit()
        st.success("User registered successfully. Now complete the KYC.")
        st.session_state.step = "KYC"
        st.session_state.email = email
    except sqlite3.IntegrityError:
        st.error("The email is already registered.")
    conn.close()

def complete_kyc():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("UPDATE usuarios SET kyc_completed = 1 WHERE email = ?", (st.session_state.email,))
    conn.commit()
    conn.close()
    st.session_state.step = "Risk Profile"

def complete_risk_profile():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("UPDATE usuarios SET risk_profile_completed = 1 WHERE email = ?", (st.session_state.email,))
    conn.commit()
    conn.close()
    st.session_state.step = "Registration"

def mostrar_dashboard():
    st.sidebar.title("Menu")
    menu = ["Summary", "User Information", "Documents", "Analysis", "Portfolios", "Operations", "Proposals", "Alerts"]
    opcion = st.sidebar.radio("Select an option", menu)
    
    st.title(opcion)
    st.write("Content under development...")

def main():
    crear_base_datos()
    
    if "usuario_autenticado" not in st.session_state:
        st.session_state.usuario_autenticado = False
    if "step" not in st.session_state:
        st.session_state.step = "Start"
    
    if st.session_state.usuario_autenticado:
        mostrar_dashboard()
    else:
        if st.session_state.step == "Start":
            st.title("TRAID")
            opcion = st.radio("", ["Login", "Register"], index=0, horizontal=True)
            
            if opcion == "Login":
                st.subheader("Login")
                email = st.text_input("Email")
                contrasena = st.text_input("Password", type="password")
                if st.button("LOG IN"):
                    usuario = verificar_usuario(email, contrasena)
                    if usuario:
                        st.session_state.usuario_autenticado = True
                        st.experimental_rerun()
                    else:
                        st.error("Incorrect credentials.")
            
            elif opcion == "Register":
                st.subheader("Register")
                nombre = st.text_input("First Name")
                apellido = st.text_input("Last Name")
                email = st.text_input("Email")
                contrasena = st.text_input("Password", type="password")
                confirmar_contrasena = st.text_input("Confirm Password", type="password")
                
                if st.button("CREATE ACCOUNT"):
                    if contrasena == confirmar_contrasena:
                        registrar_usuario(nombre, apellido, email, contrasena)
                    else:
                        st.error("Passwords do not match. Try again.")
        
        elif st.session_state.step == "KYC":
            st.subheader("KYC Process")
            st.write("Complete the KYC process before proceeding.")
            if st.button("Complete KYC"):
                complete_kyc()
                st.experimental_rerun()
        
        elif st.session_state.step == "Risk Profile":
            st.subheader("Risk Profile Test")
            st.write("Complete the risk profile assessment before registering.")
            if st.button("Complete Risk Profile"):
                complete_risk_profile()
                st.experimental_rerun()
        
if __name__ == "__main__":
    main()
