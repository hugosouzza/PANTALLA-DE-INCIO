import streamlit as st

def main():
    st.markdown(
        """
        <style>
        .card {
            background-color: #F8F9FA;
            padding: 20px;
            margin: 10px 0;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .card:hover {
            background-color: #E9ECEF;
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
        """,
        unsafe_allow_html=True
    )
    
    st.title("TRAID")
    st.subheader("Bienvenido a la plataforma de asesoramiento financiero")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Iniciar sesión")
    if st.button("Iniciar sesión", key="login", help="Funcionalidad próximamente disponible"):
        st.warning("Funcionalidad aún no implementada")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Registrarse")
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    email = st.text_input("Correo Electrónico")
    contrasena = st.text_input("Contraseña", type="password")
    confirmar_contrasena = st.text_input("Confirmar Contraseña", type="password")
    
    if st.button("Registrarse", key="register"):
        if contrasena == confirmar_contrasena:
            st.success("Registro completado correctamente (sin integración aún)")
        else:
            st.error("Las contraseñas no coinciden. Inténtalo de nuevo.")
    st.markdown('</div>', unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()
