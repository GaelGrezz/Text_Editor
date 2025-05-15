import streamlit as st
from docx import Document
from io import BytesIO


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
    try:
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
            content = content.split()

        except:
            st.warning("Suba algún archivo para comenzar")

        if "text_body_" not in st.session_state:
            try:
                st.session_state["text_body_"] = content
                save_Value("text_body")
                st.warning("Se ha guardado con éxito los datos")
            except:
                return 0
        elif "text_body_" in st.session_state and content:
            st.session_state["text_body_"] = content
            save_Value("text_body")
            st.warning("Los datos han sido cambiados")
        

        if "text_body_global" in st.session_state and st.session_state["text_body_global"] == []:
            st.session_state["text_body_global"] = "Sin datos"
            message = st.session_state["text_body_global"]
            message
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

        if "text_body_" in st.session_state:
            if st.session_state["text_body_global"] != content:
                st.session_state["text_body_"] = "Este archivo no tiene contenido"
    except:
        st.session_state["text_body_"] = "Este archivo no tiene contenido"
        st.write("He accedido")
        return 0

def TextEditor():

    valid_formt = ["csv", "txt"]
    word_format = ["docx"]

    st.title("TexDitor")
    if "valor_global" not in st.session_state:
        st.warning("Ingrese algún archivo desde la pestaña Home")
        st.page_link(
            page=Home,
            icon=":material/home:",
            label="Ir a Home",
            help="Ve y agrega el archivo que deseas!",
        )
        return 0

    archivo = st.form("Datos de entrada")

    data = load_Value(st.session_state["valor_global"])

    title = archivo.text_input("Ingrese el nuevo nombre del archivo", key="title_")

    text = archivo.text_area("Ingrese el contenido que desee en el archivo", key="body")

    formt = archivo.selectbox(
        "Ingrese el formato que desee", ["csv", "txt", "docx"]
    ).lower()

    submit = archivo.form_submit_button("Aplicar cambios")

    if submit and formt in valid_formt:
        st.warning("Datos aplicados y listos para descargar")

        st.download_button(
            "Descargar archivo",
            data=text,
            file_name=f"{title}.{formt}",
            icon=":material/download:",
        )

    elif submit and formt in word_format:
        st.warning("Ha elegido word")

        doc = Document()

        doc.add_paragraph(text)

        buffer = BytesIO()

        doc.save(buffer)

        buffer.seek(0)

        st.download_button(
            label="Descargar archivo",
            data=buffer,
            file_name=f"{title}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            icon=":material/download:",
        )


Home = st.Page(page=Home, title="Home", icon=":material/house:", url_path="Home")

TextEditor = st.Page(
    page=TextEditor, title="Text Editor", icon=":material/edit:", url_path="Text Editor"
)

pg = st.navigation(pages=[Home, TextEditor])

pg.run()
