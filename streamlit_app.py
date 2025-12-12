import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Credit Risk Scoring", page_icon="💳", layout="wide")

# ---------- 1) Estado ----------
if "mode" not in st.session_state:
    st.session_state.mode = None  # "single" o "bulk"
if "bulk_df" not in st.session_state:
    st.session_state.bulk_df = None

# ---------- 2) Pantalla de selección ----------
def choose_mode():
    st.title("Entrada de solicitudes")
    st.write("¿Vas a rellenar datos para **1 persona** o para **varias personas**?")

    option = st.radio("Selecciona una opción:", ["1 persona", "Varias personas"], horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Continuar", use_container_width=True):
            st.session_state.mode = "single" if option == "1 persona" else "bulk"
            st.rerun()

# ---------- 3) Tu formulario (1 persona) ----------
def single_form():
    st.title("Formulario del préstamo (1 persona)")

    # ✅ AQUÍ pegas tu formulario anterior (todo lo de st.text_input, selectbox, etc.)
    # Ejemplo mínimo:
    sk_id = st.text_input("ID del solicitante")
    name = st.text_input("Nombre del solicitante")

    if st.button("Guardar / Predecir"):
        st.success("Aquí iría tu lógica de merge + predicción + guardado")

    st.divider()
    if st.button("⬅️ Volver"):
        st.session_state.mode = None
        st.rerun()

# ---------- 4) Tabla para varias personas ----------
def bulk_table():
    st.title("Carga múltiple (varias personas)")
    st.write("Rellena la tabla y luego pulsa **Procesar**.")

    # Define las columnas mínimas que quieres capturar en modo masivo
    cols = [
        "SK_ID_CURR",
        "NAME",
        "AGE",
        "GENDER",                # "M" / "F"
        "CNT_CHILDREN",
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "NAME_EDUCATION_TYPE",
        "NAME_FAMILY_STATUS",
        "NAME_HOUSING_TYPE",
        "NAME_INCOME_TYPE",
        "YEARS_ACTUAL_WORK",
        "FLAG_OWN_REALTY",
        "FLAG_PHONE",
        "FLAG_DNI",
        "FLAG_PASAPORTE",
        "FLAG_COMPROBANTE_DOM_FISCAL",
        "FLAG_ESTADO_CUENTA_BANC",
        "FLAG_TARJETA_ID_FISCAL",
        "FLAG_CERTIFICADO_LABORAL",
    ]

    # Inicializa una tabla con N filas
    n = st.number_input("Número de solicitantes", min_value=2, max_value=200, value=5, step=1)

    if st.session_state.bulk_df is None or len(st.session_state.bulk_df) != n:
        st.session_state.bulk_df = pd.DataFrame([{c: None for c in cols} for _ in range(int(n))])

    edited = st.data_editor(
        st.session_state.bulk_df,
        num_rows="fixed",
        use_container_width=True
    )
    st.session_state.bulk_df = edited

    colA, colB, colC = st.columns(3)

    with colA:
        if st.button("✅ Validar", use_container_width=True):
            # Ejemplo de validación simple:
            errors = []
            if edited["SK_ID_CURR"].isna().any():
                errors.append("Hay SK_ID_CURR vacíos.")
            if edited["NAME"].isna().any():
                errors.append("Hay NAME vacíos.")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                st.success("Validación básica OK.")

    with colB:
        if st.button("⚙️ Procesar / Predecir", use_container_width=True):
            # AQUÍ: tu lógica para iterar filas -> preparar features -> predecir -> guardar
            st.info("Aquí iría: merge con datos_internos + predicción por fila + guardado (CSV/Supabase).")

    with colC:
        if st.button("⬅️ Volver", use_container_width=True):
            st.session_state.mode = None
            st.session_state.bulk_df = None
            st.rerun()

# ---------- 5) Router ----------
if st.session_state.mode is None:
    choose_mode()
elif st.session_state.mode == "single":
    single_form()
elif st.session_state.mode == "bulk":
    bulk_table()
