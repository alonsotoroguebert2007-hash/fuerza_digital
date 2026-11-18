from dataclasses import dataclass
from config import GRUPOS, LONGITUD_MAXIMA
from calculos import combinaciones, entropia


@dataclass(frozen=True)
class Resultado:
    longitud: int
    alfabeto: int
    combinaciones: int
    bits: float
    nivel: str


class EvaluadorContrasena:
    def evaluar(self, ejemplo: str) -> Resultado:
        if not isinstance(ejemplo, str) or not ejemplo:
            raise ValueError("Escribe un ejemplo ficticio no vacío.")
        if len(ejemplo) > LONGITUD_MAXIMA:
            raise ValueError(f"Máximo permitido: {LONGITUD_MAXIMA} caracteres.")
        if any(not 32 <= ord(caracter) <= 126 for caracter in ejemplo):
            raise ValueError("Usa solo caracteres ASCII imprimibles.")

        longitud = len(ejemplo)
        alfabeto = sum(len(grupo) for grupo in GRUPOS
                       if any(caracter in grupo for caracter in ejemplo))
        nivel = "Débil" if longitud < 8 else "Moderada" if longitud < 15 else "Fuerte"
        return Resultado(longitud, alfabeto,
                         combinaciones(alfabeto, longitud),
                         entropia(alfabeto, longitud), nivel)


def recomendaciones(resultado: Resultado) -> list[str]:
    consejos = []
    if resultado.longitud < 15:
        consejos.append("Prueba una frase de paso ficticia más larga.")
    consejos.extend((
        "Evita secuencias, patrones conocidos y datos personales.",
        "Usa una contraseña distinta para cada cuenta real.",
        "Considera un gestor de contraseñas.",
    ))
    return consejos
