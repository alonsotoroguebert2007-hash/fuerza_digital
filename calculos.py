from math import log2


def combinaciones(alfabeto: int, longitud: int) -> int:
    if alfabeto < 1 or longitud < 1:
        raise ValueError("El alfabeto y la longitud deben ser positivos.")
    return alfabeto ** longitud


def entropia(alfabeto: int, longitud: int) -> float:
    if alfabeto < 1 or longitud < 1:
        raise ValueError("El alfabeto y la longitud deben ser positivos.")
    return longitud * log2(alfabeto)


def tiempos(combinaciones_totales: int, velocidad: int) -> tuple[float, float]:
    if combinaciones_totales < 1 or velocidad < 1:
        raise ValueError("Las combinaciones y la velocidad deben ser positivas.")
    maximo = combinaciones_totales / velocidad
    return maximo / 2, maximo


def formato_tiempo(segundos: float) -> str:
    for unidad, nombre in ((31_557_600, "años"), (86_400, "días"),
                           (3_600, "horas"), (60, "minutos")):
        if segundos >= unidad:
            return f"{segundos / unidad:,.2f} {nombre}"
    return f"{segundos:,.6f} segundos"
