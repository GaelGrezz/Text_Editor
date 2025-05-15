import streamlit as st


def save_Value(key):
    st.session_state[key + "_global"] = st.session_state[key + "_"]

def load_Value(value, section=False):

    if section:
        section = st.expander("Ver archivo", expanded=False, icon=":material/add:")

        with section:
            st.write("Archivo: ")
            value

    return value


def Home():
    st.title("Home")
    file = st.file_uploader(
        "Selecciona un archivo",
        key="valor_",
        on_change=lambda: save_Value("valor"),
        type=["csv", "txt", "xlsx"],
    )

    try:
        title = load_Value(st.session_state["valor_global"].name)
        type = load_Value(st.session_state["valor_global"].type)
        content = load_Value(st.session_state["valor_global"].read())

    except:
        st.warning("No se ha subido ningún archivo")

    if "text_body_" not in st.session_state:
        try:
            st.session_state["text_body_"] = content
            save_Value("text_body")
            st.warning("Se ha guardado con éxito los datos")
        except:
            return 0

    try:
        st.write("### Archivo seleccionado: ")
        st.write(f"<b>Título del archivo</b>: {title}", unsafe_allow_html=True)
        st.write(f"<b>Tipo de archivo</b>: {type}", unsafe_allow_html=True)
        st.write(
            f"<b>Contenido en el archivo</b>: {str(st.session_state["text_body_"])}",
            unsafe_allow_html=True,
        )
        load_Value(st.session_state["valor_global"], True)
    except:
        st.warning("Una vez subas el archivo, aquí se mostrarán sus datos")


def TextEditor():
    st.title("TexDitor")
    if "valor_global" not in st.session_state:
        st.warning("Ingrese algún dato en Home")
        st.page_link(
            page=Home,
            icon=":material/home:",
            label="Home",
            help="Ve y agrega el archivo que deseas!",
        )
        return 0

    archivo = st.form("Datos de entrada")

    data = load_Value(st.session_state["valor_global"])

    title = archivo.text_input("Ingrese un título", key="title_")

    text = archivo.text_area("Ingrese texto", key="body")

    submit = archivo.form_submit_button("Aplicar cambios")

    if submit:
        st.warning("Datos aplicados")

    st.download_button(
        "Descargar archivo",
        data=text,
        file_name=f"{title}.txt",
        icon=":material/download:",
    )


Home = st.Page(page=Home, title="Home", icon=":material/house:", url_path="Home")

TextEditor = st.Page(
    page=TextEditor, title="Text Editor", icon=":material/edit:", url_path="Text Editor"
)

pg = st.navigation(pages=[Home, TextEditor])

pg.run()
