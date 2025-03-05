import streamlit as st

def main():
    st.title("TRAID")
    st.subheader("Bienvenido a la plataforma de asesoramiento financiero")
    
    # Opciones de inicio de sesión y registro
    opcion = st.radio("Selecciona una opción", ["Iniciar sesión", "Registrarse"], index=1)
    
    if opcion == "Iniciar sesión":
        st.info("Funcionalidad próximamente disponible")
    
    elif opcion == "Registrarse":
        st.subheader("Registro de Usuario")
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        email = st.text_input("Correo Electrónico")
        contrasena = st.text_input("Contraseña", type="password")
        confirmar_contrasena = st.text_input("Confirmar Contraseña", type="password")
        
        if st.button("Registrarse"):
            if contrasena == confirmar_contrasena:
                st.success("Registro completado correctamente (sin integración aún)")
            else:
                st.error("Las contraseñas no coinciden. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
