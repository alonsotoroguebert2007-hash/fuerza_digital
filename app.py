"""Interfaz educativa. Ejecutar: python -m streamlit run app.py."""
from pathlib import Path
from string import ascii_uppercase, ascii_lowercase, digits, punctuation
import streamlit as st
import altair as alt
import pandas as pd
from calculos import entropia, tiempos, formato_tiempo
from config import VELOCIDADES, LONGITUD_MAXIMA
from evaluador import EvaluadorContrasena, recomendaciones
from chatbot import chatbot


st.set_page_config(page_title="Fortaleza Digital", page_icon="🛡️", layout="wide")
st.html("<style>" + Path(__file__).with_name("styles.css").read_text(encoding="utf-8") + "</style>")
evaluador = EvaluadorContrasena()


def cientifico(n):
    return f"{n:.2e}".replace("e+", " × 10^")


def resultado(texto):
    try:
        return evaluador.evaluar(texto)
    except ValueError as error:
        st.warning(str(error))
        return None


def tarjetas(r):
    cols = st.columns(4)
    for col, label, value, detail in zip(cols,
        ["Longitud (L)", "Alfabeto estimado (S)", "Combinaciones C = S^L", "Entropía ideal log₂(C)"],
        [str(r.longitud), str(r.alfabeto), cientifico(r.combinaciones), f"{r.bits:.2f} bits"],
        ["caracteres", "símbolos posibles", "cadenas teóricas", "supone selección uniforme"]):
        with col:
            st.html(f'<div class="metric"><span>{label}</span><strong>{value}</strong><small>{detail}</small></div>')


with st.sidebar:
    st.html('<div class="brand">🛡️ Fortaleza<br><span>Digital</span></div>')
    st.divider()
    pagina = st.radio("Navegación", ["Evaluador de contraseña", "Comparar ejemplos", "Cómo funciona (C = S^L)", "Tipos de ataque", "Consejos de seguridad", "Chatea con la IA"])
    st.divider()
    velocidad = st.selectbox("Escenario hipotético", VELOCIDADES, index=1, format_func=lambda r: f"{r:,} intentos/s")
    procedimiento = st.toggle("Mostrar procedimiento", value=True)
    st.caption("Proyecto educativo · Matemáticas y concientización")
    st.caption("No se realizan ataques ni se consultan bases de datos.")

st.title("Fortaleza Digital")
st.markdown('<p class="subtitle">Explora la seguridad de contraseñas con funciones exponenciales.</p>', unsafe_allow_html=True)
st.warning("Solo ejemplos ficticios. Los cálculos son hipotéticos y no predicen la seguridad real.")

if pagina == "Evaluador de contraseña":
    with st.form("evaluar"):
        ejemplo = st.text_input("Introduce un ejemplo ficticio", value="DemoFicticia!42", type="password", max_chars=LONGITUD_MAXIMA)
        st.form_submit_button("Evaluar ejemplo", type="primary")
    st.caption("Sin almacenamiento persistente de ejemplos. El navegador envía la entrada al servidor Streamlit; ejecútalo localmente para mantenerla en tu equipo.")
    r = resultado(ejemplo)
    if r:
        indice = {"Débil": 0, "Moderada": 1, "Fuerte": 2}[r.nivel]
        st.markdown(f"**Clasificación didáctica por longitud: {r.nivel.upper()}**")
        st.html('<div class="strength">' + ''.join(f'<div class="level level{i} {"on" if i <= indice else ""}">{label}</div>' for i, label in enumerate(["Débil", "Moderada", "Fuerte"])) + '</div>')
        st.caption("Regla original del proyecto: menos de 8 caracteres = Débil; de 8 a 14 = Moderada; desde 15 = Fuerte. Umbrales didácticos, no estándares oficiales.")
        tarjetas(r)
        st.subheader("Composición del ejemplo")
        grupos = [("Mayúsculas", ascii_uppercase), ("Minúsculas", ascii_lowercase), ("Números", digits), ("Símbolos", punctuation), ("Espacios", " ")]
        st.html('<div class="chips">' + ''.join(f'<span>{"✓" if any(c in g for c in ejemplo) else "—"} {nombre}</span>' for nombre, g in grupos) + '</div>')
        st.caption("S suma los tamaños de los grupos presentes: 26 + 26 + 10 + 32 + 1 (espacio), según corresponda. Es una estimación del alfabeto permitido, no un conteo de caracteres distintos ni una medición de predictibilidad.")
        izquierda, derecha = st.columns([1.55, 1])
        with izquierda:
            st.subheader("Tiempo hipotético de fuerza bruta")
            filas = []
            for tasa in VELOCIDADES:
                medio, maximo = tiempos(r.combinaciones, tasa)
                filas.append({"Escenario": "✓ Seleccionado" if tasa == velocidad else "Simulación", "Intentos/s": f"{tasa:,}", "Promedio ≈ C/(2r)": formato_tiempo(medio), "Máximo C/r": formato_tiempo(maximo)})
            st.dataframe(filas, hide_index=True, width="stretch", alt="Comparación de escenarios matemáticos hipotéticos")
            st.caption("Tasas arbitrarias del proyecto; no representan equipos ni sistemas concretos.")
        with derecha:
            st.subheader(f"Entropía según longitud · S = {r.alfabeto}")
            largos = sorted(set([6, 8, 10, 12, 14, 16, r.longitud]))
            datos = pd.DataFrame({"Longitud": largos, "Bits": [entropia(r.alfabeto, n) for n in largos], "Actual": [n == r.longitud for n in largos]})
            chart = alt.Chart(datos).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(x=alt.X("Longitud:O", title="Longitud L (caracteres)"), y=alt.Y("Bits:Q", title="Entropía ideal (bits)"), color=alt.condition(alt.datum.Actual, alt.value("#26a269"), alt.value("#a5dfb7")), tooltip=["Longitud", alt.Tooltip("Bits", format=".2f")]).properties(height=235)
            st.altair_chart(chart, width="stretch", alt="Entropía ideal por longitud con alfabeto fijo; el ejemplo actual aparece en verde")
            st.caption("Con S fijo, H crece linealmente; C = S^L crece exponencialmente. La barra verde marca el ejemplo actual.")
        st.info(f"Con el mismo alfabeto, añadir un carácter multiplica las combinaciones por {r.alfabeto} y suma {entropia(r.alfabeto, 1):.2f} bits ideales.")
        if procedimiento:
            with st.expander("Procedimiento matemático", expanded=True):
                st.code(f"S = {r.alfabeto}; L = {r.longitud}\nC = {r.alfabeto}^{r.longitud} = {r.combinaciones}\nH = {r.longitud} × log₂({r.alfabeto}) = {r.bits:.2f} bits\nr = {velocidad:,} intentos/s\nT máximo = C/r; T promedio ≈ C/(2r)", language=None)
                st.caption("Media exacta: (C+1)/(2r), si cada posición del orden de búsqueda es igualmente probable. Se conserva la aproximación original C/(2r).")
        with st.expander("Recomendaciones", expanded=True):
            for consejo in recomendaciones(r):
                st.write("• " + consejo)

elif pagina == "Comparar ejemplos":
    st.subheader("Comparar dos ejemplos ficticios")
    with st.form("comparar"):
        a = st.text_input("Ejemplo A", "abcdefgh", type="password", max_chars=LONGITUD_MAXIMA)
        b = st.text_input("Ejemplo B", "abcdefghi", type="password", max_chars=LONGITUD_MAXIMA)
        st.form_submit_button("Comparar", type="primary")
    ra, rb = resultado(a), resultado(b)
    if ra and rb:
        st.dataframe([{"Ejemplo": label, "L": r.longitud, "S estimado": r.alfabeto, "Combinaciones": cientifico(r.combinaciones), "Bits ideales": round(r.bits, 2), "Nivel por longitud": r.nivel} for label, r in [("A", ra), ("B", rb)]], hide_index=True, width="stretch", alt="Comparación de escenarios matemáticos hipotéticos")
        st.info(f"B/A: {rb.combinaciones / ra.combinaciones:.4g} veces el espacio teórico. Diferencia: {rb.bits - ra.bits:.2f} bits ideales.")
        st.caption("La comparación usa elecciones uniformes e independientes. No demuestra resistencia real.")

elif pagina == "Cómo funciona (C = S^L)":
    st.subheader("Una potencia para contar posibilidades")
    st.write("L es la cantidad de posiciones; S es el tamaño del conjunto permitido en cada una. Si cada posición admite S alternativas independientes, el principio multiplicativo da:")
    st.latex(r"C=S^L, \qquad H=\log_2(C)=L\log_2(S)")
    st.write("El programa estima S a partir de los grupos presentes. Un alfabeto permitido real podría ser distinto. La entropía ideal requiere selección uniforme e independiente y no describe fielmente una contraseña humana predecible.")
    st.dataframe([{"S": s, "L": l, "C": str(s**l), "H (bits)": round(entropia(s,l),2)} for s,l in [(26,8),(26,9),(62,8)]], hide_index=True)
    st.info("De 26^8 a 26^9: ×26. De 26^8 a 62^8: ×1.045,55 aproximadamente. Cada bit adicional duplica el espacio ideal.")
    st.write("Python valida y calcula. Streamlit presenta los controles, resultados y gráficos en el navegador.")

elif pagina == "Tipos de ataque":
    st.subheader("Qué simplifica el modelo")
    st.write("En línea: los intentos se dirigen a un servicio y pueden existir límites, bloqueos y autenticación adicional. Fuera de línea: el contexto depende del algoritmo de hash, su coste y el hardware.")
    st.write("La fuerza bruta ideal recorre candidatos sin repetir, a tasa constante. Los diccionarios y ataques que priorizan patrones no siguen la distribución uniforme del modelo.")
    st.latex(r"T_{max}=C/r, \qquad T_{prom}=(C+1)/(2r)\approx C/(2r)")
    st.write("Con S=26, L=8 y r=1.000.000: máximo ≈58,01 horas; promedio ≈29,00 horas. Estos tiempos son estrictamente hipotéticos.")

elif pagina == "Consejos de seguridad":
    st.subheader("Hábitos para proteger tus cuentas")
    for consejo in ["Usa una contraseña distinta para cada cuenta.", "Prioriza longitud y evita datos personales, secuencias y patrones comunes.", "Considera un gestor de contraseñas y activa autenticación multifactor.", "No introduzcas claves reales en este simulador."]:
        st.write("• " + consejo)
    st.info("Una etiqueta verde no certifica seguridad. El modelo no detecta filtraciones ni estima la probabilidad real de una elección humana.")

elif pagina == "Chatea con la IA":
    st.subheader("Consejos de IA 🤖")
    st.write("¡Hola! soy el asistente de IA de fuerza digital. Hazme la consulta que quieras")
    respuesta = st.chat_input("Consulta...")
    if respuesta:
     holi = chatbot(respuesta)
     st.chat_message("user").write(respuesta)
     st.chat_message("assistant").write(holi)
        

st.divider()
st.caption("Fortaleza Digital · Simulador pedagógico · Sin ataques reales · Solo contraseñas ficticias")


