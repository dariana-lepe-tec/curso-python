# ==============================================================
#  TAQUILLA CINÉPOLIS ESFERA QUERÉTARO - Proyecto final
# --------------------------------------------------------------
#  Problema: en la taquilla las ventas y los cortes de turno se
#  anotaban a mano y se perdían. Este programa cobra boletos y
#  combos con las reglas de precios del cine (incluido el 2x1 de
#  los miércoles) y guarda todo en archivos .txt para que la
#  información no se pierda al cerrarlo.
#  Para quién: el personal de taquilla del cine.
#  Autora: Dariana Lepe León · Matrícula 03100862
#  Curso: Fundamentos de programación · Universidad Tecmilenio
# --------------------------------------------------------------
#  Reglas de negocio:
#   RN1 Precios: adulto $90, niño $69, tercera edad $69, combo $112
#       (se leen de precios.txt)
#   RN2 Los miércoles el boleto de adulto es 2x1
#   RN3 El combo de dulcería se vende aparte
#   RN4 Máximo 10 boletos por orden
#   RN5 Al final del turno se hace un corte con el total vendido
# ==============================================================

import os
import time

# ---- Constantes ----
MAX_BOLETOS = 10   # RN4

# Precios de respaldo por si precios.txt no existe o trae errores (RN1)
PRECIOS_BASE = {"adulto": 90.0, "niño": 69.0, "tercera": 69.0, "combo": 112.0}

# Menú principal guardado como matriz: cada fila es [número, texto]
MENU = [
    ["1", "Registrar venta"],
    ["2", "Ver archivos"],
    ["3", "Leer archivo"],
    ["4", "Crear archivo"],
    ["5", "Agregar registro"],
    ["6", "Corte del turno"],
    ["0", "Salir"],
]

# ==============================================================
#  REQ 1, 2 y 3: inicio
# ==============================================================

def pedir_nombre():
    """Req 1: pide el nombre o nickname del usuario (no acepta vacío)."""
    nombre = input("\n¿Cuál es tu nombre o nickname? ").strip()
    while nombre == "":
        nombre = input("Necesito tu nombre para empezar: ").strip()
    return nombre


def bienvenida(nombre):
    """Req 2: arma la bienvenida formal con operaciones de strings."""
    nombre_bonito = nombre.strip().title()          # "dariana" -> "Dariana"
    linea = "=" * 50
    print(linea)
    print("CINÉPOLIS ESFERA QUERÉTARO".center(50))
    print(f"Bienvenido(a), {nombre_bonito}, al sistema de taquilla.")
    print("Que tengas un excelente turno.")
    print(linea)


def pantalla_carga(segundos):
    """Req 3: dibuja una barra de carga que se mueve (máximo 5 segundos)."""
    if segundos > 5:
        segundos = 5                    # el requerimiento pide máximo 5 s
    pasos = 10
    for i in range(1, pasos + 1):
        barra = "#" * i + "." * (pasos - i)
        # \r regresa al inicio del renglón, así la barra "se mueve" en el mismo lugar
        print(f"\rCargando sistema [{barra}] {i * 10}%", end="", flush=True)
        time.sleep(segundos / pasos)    # se reparte el tiempo entre los pasos
    print("\n¡Sistema listo!")


# ==============================================================
#  REQ 6: fecha en tupla
# ==============================================================

def pedir_fecha():
    """Req 6: pide la fecha dd/mm/aaaa, la valida y la regresa como tupla."""
    while True:
        texto = input("Fecha de operación (dd/mm/aaaa): ").strip()
        try:
            # split("/") separa "23/11/2026" en ["23", "11", "2026"].
            # Si no vienen 3 partes o no son números, se lanza ValueError.
            dia, mes, anio = texto.split("/")
            dia = int(dia)
            mes = int(mes)
            anio = int(anio)
            if dia < 1 or dia > 31:
                print("El día debe estar entre 1 y 31. Intenta de nuevo.")
            elif mes < 1 or mes > 12:
                print("El mes debe estar entre 1 y 12. Intenta de nuevo.")
            elif anio < 2000:
                print("Revisa el año, debe tener 4 dígitos. Intenta de nuevo.")
            else:
                # Tupla SIN paréntesis, tal como lo pide el requerimiento
                Fecha = dia, mes, anio
                return Fecha
        except ValueError:
            print(f"'{texto}' no es una fecha válida. Usa el formato dd/mm/aaaa, por ejemplo 23/11/2026.")


def fecha_texto(fecha):
    """Convierte la tupla (dia, mes, anio) en el texto dd/mm/aaaa."""
    dia, mes, anio = fecha              # desempaquetar la tupla
    return f"{dia:02d}/{mes:02d}/{anio}"   # :02d pone un 0 a la izquierda: 5 -> 05


def preguntar_miercoles():
    """RN2: pregunta si hoy es miércoles para aplicar el 2x1 de adulto."""
    while True:
        resp = input("¿Hoy es miércoles? (si/no): ").strip().lower()
        if resp == "si":
            return True
        elif resp == "no":
            return False
        print("Escribe exactamente si o no.")


# ==============================================================
#  REQ 4 y 5: menú como matriz e inactividad
# ==============================================================

def dibujar_tabla(matriz, titulo):
    """Req 4: dibuja un menú recorriendo su matriz con un for."""
    print()
    print("+-----+------------------------+")
    print(f"| {titulo:<28} |")
    print("+-----+------------------------+")
    for fila in matriz:
        print(f"|  {fila[0]}  | {fila[1]:<22} |")
    print("+-----+------------------------+")


def mostrar_menu():
    """Req 4: dibuja el menú principal."""
    dibujar_tabla(MENU, "TAQUILLA CINÉPOLIS ESFERA")
    print("(Enter sin opción = inactividad)")


def opcion_valida(opcion, matriz):
    """Req 4: revisa si la opción escrita existe en la matriz del menú."""
    for fila in matriz:
        if fila[0] == opcion:
            return True
    return False


def inactividad():
    """Req 5: simula 10 minutos sin actividad y pregunta si se continúa.
    Regresa True para seguir en el menú y False para volver al inicio."""
    print("\nNo elegiste ninguna opción...")
    # Simulado: cada vuelta del for representa 1 minuto (con una pausa corta)
    for minuto in range(1, 11):
        print(f"...{minuto} min sin actividad")
        time.sleep(0.2)
    # Se repite la pregunta hasta que escriban exactamente si o no
    while True:
        resp = input("¿Deseas continuar? (si/no): ").strip().lower()
        if resp == "si":
            return True
        elif resp == "no":
            print("Regresando a la pantalla de inicio...")
            return False
        print("Escribe exactamente si o no.")


# ==============================================================
#  PROGRAMA PRINCIPAL (versión 2: inicio + menú)
# ==============================================================

def main():
    """Controla el programa con dos ciclos: inicio (externo) y menú (interno)."""
    salir_programa = False

    # Ciclo externo: la pantalla de inicio. Se repite cuando la
    # inactividad responde "no", para pedir el nombre otra vez.
    while not salir_programa:
        nombre = pedir_nombre()
        bienvenida(nombre)
        pantalla_carga(3)
        Fecha = pedir_fecha()
        es_miercoles = preguntar_miercoles()

        # Ciclo interno: el menú principal
        en_menu = True
        while en_menu:
            mostrar_menu()
            opcion = input("Elige una opción: ").strip()

            if opcion == "":
                # Enter sin opción: True sigue en el menú, False regresa al inicio
                en_menu = inactividad()
            elif not opcion_valida(opcion, MENU):
                print(f"'{opcion}' no es una opción del menú. Elige un número de la tabla.")
            elif opcion == "0":
                en_menu = False
                salir_programa = True
                print(f"Fin del turno. ¡Hasta luego, {nombre.title()}!")
            else:
                print("(Esta opción se programa en el siguiente bloque)")


main()
