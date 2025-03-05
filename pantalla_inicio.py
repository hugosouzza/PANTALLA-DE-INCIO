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
        st.success("Registro completado correctamente. Ahora puedes iniciar sesión.")
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

def mostrar_dashboard():
    st.sidebar.title("Menú")
    menu = ["Resumen", "Información del Usuario", "Documentos", "Análisis", "Carteras", "Operaciones", "Propuestas", "Alertas"]
    opcion = st.sidebar.radio("Selecciona una opción", menu)
    
    st.title(opcion)
    st.write("Contenido en desarrollo...")

def main():
    crear_base_datos()
    
    if "usuario_autenticado" not in st.session_state:
        st.session_state.usuario_autenticado = False
    
    if st.session_state.usuario_autenticado:
        mostrar_dashboard()
    else:
        st.markdown("""
            <style>
            .centered {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 90vh;
                text-align: center;
            }
            .button {
                width: 300px;
                padding: 10px;
                margin: 10px;
                border-radius: 5px;
                border: none;
                font-size: 16px;
                cursor: pointer;
            }
            .login-btn {
                background-color: black;
                color: white;
            }
            .register-btn {
                background-color: white;
                color: black;
                border: 1px solid black;
            }
            </style>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="centered">', unsafe_allow_html=True)
        st.title("TRAID")
        st.subheader("Bienvenido a la plataforma de asesoramiento financiero")
        
        opcion = st.radio("", ["Iniciar sesión", "Registrarse"], index=0, horizontal=True)
        
        if opcion == "Iniciar sesión":
            st.subheader("Iniciar sesión")
            email = st.text_input("Correo Electrónico")
            contrasena = st.text_input("Contraseña", type="password")
            if st.button("LOG IN", key="login", help="Iniciar sesión", use_container_width=True):
                usuario = verificar_usuario(email, contrasena)
                if usuario:
                    st.session_state.usuario_autenticado = True
                    st.experimental_rerun()
                else:
                    st.error("Credenciales incorrectas.")
        
        elif opcion == "Registrarse":
            st.subheader("Registro de Usuario")
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            email = st.text_input("Correo Electrónico")
            contrasena = st.text_input("Contraseña", type="password")
            confirmar_contrasena = st.text_input("Confirmar Contraseña", type="password")
            
            if st.button("CREATE ACCOUNT", key="register", use_container_width=True):
                if contrasena == confirmar_contrasena:
                    registrar_usuario(nombre, apellido, email, contrasena)
                else:
                    st.error("Las contraseñas no coinciden. Inténtalo de nuevo.")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
