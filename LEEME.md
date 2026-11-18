# Fortaleza Digital

Simulador educativo de combinaciones y entropía ideal, con interfaz inspirada en la captura entregada. Usa exclusivamente ejemplos ficticios. No predice la seguridad real ni ejecuta ataques.

## Ejecutar en Windows

Instala Python 3.11 o posterior. Descomprime el ZIP y abre una terminal dentro de FortalezaDigital (la carpeta que contiene app.py). Ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Abre la dirección local que muestre Streamlit, habitualmente http://127.0.0.1:8501. Para detener: Ctrl+C en la terminal. Se necesita internet para instalar dependencias; después la aplicación funciona sin servicios externos.

En macOS/Linux, usa python3 para crear el entorno y .venv/bin/python en los comandos siguientes.

## Archivos

- app.py: interfaz Streamlit, navegación, evaluación, comparación y gráfica.
- styles.css: presentación visual y adaptación a pantallas pequeñas.
- calculos.py: fórmulas originales, sin cambios.
- evaluador.py: validación, clasificación y recomendaciones originales, sin cambios.
- config.py: velocidades y límite originales; añade el espacio como grupo de un símbolo.
- main.py: conserva la aplicación original de consola. Ejecuta python main.py para usarla.
- .streamlit/config.toml: tema claro, telemetría desactivada y servidor limitado a 127.0.0.1.

## Modelo y decisiones

C=S^L; H=L log₂(S); tiempo máximo C/r; promedio aproximado C/(2r). El promedio exacto es (C+1)/(2r) bajo búsqueda uniforme sin repetición. La selección uniforme e independiente es un supuesto matemático, no una propiedad de las contraseñas humanas.

S se estima sumando los grupos presentes: minúsculas 26, mayúsculas 26, dígitos 10, puntuación ASCII 32 y espacio 1. No equivale necesariamente al alfabeto realmente permitido. Se corrigió el caso del espacio aceptado pero no contabilizado: un ejemplo compuesto solo por espacios ya no produce alfabeto cero. El ejemplo con cuatro clases sin espacios conserva S=94. Se aceptan únicamente ASCII imprimibles y hasta 128 caracteres; no se eliminan espacios de la entrada.

Se conserva la clasificación original: menos de 8 caracteres = Débil; de 8 a 14 = Moderada; desde 15 = Fuerte. Son reglas didácticas por longitud, no estándares ni garantía de resistencia. La barra tiene tres niveles para respetar esa lógica. No se copian los cinco niveles ni las cifras ilustrativas de la captura cuando difieren del modelo original.

Las tasas originales son 100, 1.000.000 y 1.000.000.000 intentos/s. Son escenarios arbitrarios y no se atribuyen a hardware concreto. La gráfica muestra H frente a L con S fijo: es lineal; C crece exponencialmente.

La guía aportada se refleja en la introducción educativa, comparación, visualización de combinaciones/bits/tasas y consejos. No se reproducen como verificadas las referencias bibliográficas incompletas de la guía.

## Privacidad y uso

El código no escribe ejemplos en archivos, registros ni bases de datos y no los envía a terceros. Streamlit mantiene los datos de los controles durante la sesión. La entrada viaja del navegador al servidor Streamlit: si se aloja en otro equipo, viaja a ese equipo. El campo oculto solo evita mostrar el texto en pantalla. Usa siempre ejemplos inventados, incluso al ejecutarlo localmente.

## Comprobación

Versión preparada para Streamlit 1.67.0. Se revisaron las fórmulas y se probaron la navegación, las entradas límite y los espacios con el ejecutor de pruebas de Streamlit. El diseño se basa en la captura; no se garantiza una reproducción exacta píxel por píxel.
