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
                 contrasena TEXT)''')
    conn.commit()
    conn.close()

def encriptar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

def registrar_usuario(nombre, apellido, email, contrasena):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios (nombre, apellido, email, contrasena) VALUES (?, ?, ?, ?)",
                  (nombre, apellido, email, encriptar_contrasena(contrasena)))
        conn.commit()
        st.success("Registro completado correctamente.")
    except sqlite3.IntegrityError:
        st.error("El correo electrónico ya está registrado.")
    conn.close()

def verificar_usuario(email, contrasena):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE email = ? AND contrasena = ?", (email, encriptar_contrasena(contrasena)))
    usuario = c.fetchone()
    conn.close()
    return usuario

def main():
    st.markdown("""
        <style>
        .card {
            background-color: #F8F9FA;
            padding: 20px;
            margin: 10px 0;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .button {
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            border: none;
            background-color: #0D6EFD;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #0B5ED7;
        }
        </style>
        """, unsafe_allow_html=True)
    
    crear_base_datos()
    st.title("TRAID")
    st.subheader("Bienvenido a la plataforma de asesoramiento financiero")
    
    opcion = st.radio("Selecciona una opción", ["Iniciar sesión", "Registrarse"], index=1)
    
    if opcion == "Iniciar sesión":
        st.subheader("Iniciar sesión")
        email = st.text_input("Correo Electrónico")
        contrasena = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            usuario = verificar_usuario(email, contrasena)
            if usuario:
                st.success(f"Bienvenido, {usuario[1]} {usuario[2]}!")
            else:
                st.error("Credenciales incorrectas.")
    
    elif opcion == "Registrarse":
        st.subheader("Registro de Usuario")
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        email = st.text_input("Correo Electrónico")
        contrasena = st.text_input("Contraseña", type="password")
        confirmar_contrasena = st.text_input("Confirmar Contraseña", type="password")
        
        if st.button("Registrarse"):
            if contrasena == confirmar_contrasena:
                registrar_usuario(nombre, apellido, email, contrasena)
            else:
                st.error("Las contraseñas no coinciden. Inténtalo de nuevo.")
    
if __name__ == "__main__":
    main()
