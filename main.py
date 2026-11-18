from calculos import formato_tiempo, tiempos
from config import VELOCIDADES
from evaluador import EvaluadorContrasena, recomendaciones


def mostrar(resultado):
    print(f"\nLongitud: {resultado.longitud}")
    print(f"Alfabeto estimado: {resultado.alfabeto}")
    print(f"Combinaciones: {resultado.combinaciones:,}")
    print(f"Entropía ideal: {resultado.bits:.2f} bits")
    print(f"Nivel orientativo por longitud: {resultado.nivel}")
    print("\nEscenarios hipotéticos:")
    for velocidad in VELOCIDADES:
        promedio, maximo = tiempos(resultado.combinaciones, velocidad)
        print(f"{velocidad:,} intentos/s | promedio: {formato_tiempo(promedio)}"
              f" | máximo: {formato_tiempo(maximo)}")
    print("\nRecomendaciones:")
    for consejo in recomendaciones(resultado):
        print(f"- {consejo}")
    print("\nModelo educativo: no predice la seguridad real.")


def ejecutar():
    evaluador = EvaluadorContrasena()
    print("FORTALEZA DIGITAL | Solo ejemplos inventados, nunca claves reales.")
    while True:
        print("\n1. Evaluar\n2. Comparar\n3. Ver fórmulas\n0. Salir")
        try:
            opcion = input("Opción: ").strip()
            if opcion == "0":
                break
            if opcion == "1":
                mostrar(evaluador.evaluar(input("Ejemplo ficticio: ")))
            elif opcion == "2":
                primero = evaluador.evaluar(input("Primer ejemplo ficticio: "))
                segundo = evaluador.evaluar(input("Segundo ejemplo ficticio: "))
                print("\nPrimer ejemplo:")
                mostrar(primero)
                print("\nSegundo ejemplo:")
                mostrar(segundo)
                if primero.combinaciones == segundo.combinaciones:
                    print("Ambos tienen el mismo espacio teórico de búsqueda.")
                else:
                    mayor = "primero" if primero.combinaciones > segundo.combinaciones else "segundo"
                    print(f"El {mayor} tiene mayor espacio teórico de búsqueda.")
            elif opcion == "3":
                print("C = S^L (combinaciones)")
                print("H = L × log₂(S) (entropía ideal)")
                print("T máximo = C/r; T promedio aproximado = C/(2r)")
                print("S: alfabeto, L: longitud, r: intentos por segundo.")
            else:
                print("Opción no válida.")
        except ValueError as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma finalizado.")
            break


if __name__ == "__main__":
    ejecutar()
