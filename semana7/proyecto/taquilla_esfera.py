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

import datetime
import os
import time

# ---- Constantes ----
MAX_BOLETOS = 10   # RN4

# Días que tiene cada mes (enero a diciembre)
DIAS_POR_MES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

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

# Menú de la venta, también como matriz
MENU_VENTA = [
    ["1", "Boleto adulto"],
    ["2", "Boleto niño"],
    ["3", "Boleto tercera edad"],
    ["4", "Combo dulcería"],
    ["5", "Cobrar orden"],
    ["0", "Cancelar orden"],
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
            if mes < 1 or mes > 12:
                print("El mes debe estar entre 1 y 12. Intenta de nuevo.")
            elif anio < 2000:
                print("Revisa el año, debe tener 4 dígitos. Intenta de nuevo.")
            else:
                limite = DIAS_POR_MES[mes - 1]        # la lista empieza en 0
                if mes == 2 and anio % 4 == 0:         # año bisiesto: febrero tiene 29
                    limite = 29
                if dia < 1 or dia > limite:
                    print(f"El mes {mes} solo tiene {limite} días. Intenta de nuevo.")
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


def calcular_miercoles(fecha):
    """RN2: revisa con la fecha si el día es miércoles para el 2x1 de adulto.
    weekday() regresa 0 = lunes, 1 = martes, 2 = miércoles..."""
    dia, mes, anio = fecha              # desempaquetar la tupla
    return datetime.date(anio, mes, dia).weekday() == 2


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
#  REQ 7 y 8: archivos y excepciones
# ==============================================================

def archivos_disponibles():
    """Req 7a: regresa la lista ordenada de los .txt de la carpeta."""
    lista = []
    for nombre in os.listdir("."):      # "." = carpeta donde corre el programa
        if nombre.endswith(".txt"):
            lista.append(nombre)
    lista.sort()
    return lista


def mostrar_archivos():
    """Req 7a: muestra los archivos .txt numerados y regresa la lista."""
    lista = archivos_disponibles()
    print("\n--- Archivos disponibles ---")
    if len(lista) == 0:
        print("(no hay archivos .txt en la carpeta)")
    numero = 0
    for nombre in lista:
        numero = numero + 1
        print(f"{numero}. {nombre}")
    return lista


def elegir_archivo():
    """Muestra los archivos y deja elegir uno por número o por nombre.
    Regresa el nombre elegido, o "" si la elección no sirve."""
    lista = mostrar_archivos()
    eleccion = input("Escribe el número o el nombre del archivo: ").strip()
    if eleccion == "":
        print("No escribiste nada.")
        return ""
    if eleccion.isdigit():
        try:
            posicion = int(eleccion) - 1        # la lista empieza en 0
            if posicion < 0:                    # el 0 daría -1 = el último archivo
                print("Los números empiezan en 1.")
                return ""
            return lista[posicion]
        except IndexError:
            print(f"No hay un archivo con el número {eleccion}. Elige del 1 al {len(lista)}.")
            return ""
    return eleccion                             # escribió el nombre


def ver_archivo():
    """Req 7b: deja elegir un archivo y muestra su contenido."""
    nombre = elegir_archivo()
    if nombre == "":
        return
    try:
        with open(nombre, "r", encoding="utf-8") as f:
            contenido = f.read()
        print(f"\n----- {nombre} -----")
        if contenido == "":
            print("(el archivo está vacío)")
        else:
            print(contenido, end="")
        print("-" * (len(nombre) + 12))
    except FileNotFoundError:
        print(f"El archivo '{nombre}' no existe. Revisa cómo lo escribiste.")
    except PermissionError:
        print(f"No tengo permiso para abrir '{nombre}' (o es una carpeta).")
    except IsADirectoryError:
        print(f"'{nombre}' es una carpeta, no un archivo.")
    except UnicodeDecodeError:
        print(f"'{nombre}' no es un archivo de texto que se pueda leer.")


def anexar(nombre_archivo, texto, fecha):
    """Req 7d: agrega un renglón con la fecha al final del archivo.
    Usa el modo "a" (append): conserva lo anterior. Con "w" se borraría."""
    try:
        with open(nombre_archivo, "a", encoding="utf-8") as f:
            f.write(f"[{fecha_texto(fecha)}] {texto}\n")
        return True
    except PermissionError:
        print(f"No tengo permiso para escribir en '{nombre_archivo}'.")
    except IsADirectoryError:
        print(f"'{nombre_archivo}' es una carpeta, no un archivo.")
    except OSError:
        print(f"No se pudo escribir en '{nombre_archivo}'.")
    return False


def crear_archivo(fecha):
    """Req 7c: crea un archivo nuevo con la fecha de creación en el primer renglón."""
    nombre = input("Nombre del archivo nuevo: ").strip()
    if nombre == "":
        print("No escribiste ningún nombre.")
        return
    if not nombre.endswith(".txt"):
        nombre = nombre + ".txt"
    # Cuidado: el modo "w" borra un archivo que ya existe, por eso se revisa antes
    if nombre in archivos_disponibles():
        print(f"'{nombre}' ya existe. No lo creo para no borrar su contenido.")
        return
    try:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(f"[{fecha_texto(fecha)}] Archivo creado\n")
        print(f"Se creó '{nombre}'.")
    except FileNotFoundError:
        print(f"No se pudo crear '{nombre}': la carpeta no existe.")
    except PermissionError:
        print(f"No tengo permiso para crear '{nombre}'.")
    except OSError:
        print(f"'{nombre}' no es un nombre válido. Evita caracteres como : * ? \" < > |")


def agregar_registro(fecha):
    """Req 7d: agrega un registro escrito por el usuario a un archivo existente."""
    nombre = elegir_archivo()
    if nombre == "":
        return
    if nombre not in archivos_disponibles():
        print(f"El archivo '{nombre}' no existe. Para crearlo usa la opción 4.")
        return
    texto = input("Escribe el registro: ").strip()
    if texto == "":
        print("El registro está vacío, no se agregó nada.")
        return
    if anexar(nombre, texto, fecha):
        print(f"Registro agregado a '{nombre}' con la fecha {fecha_texto(fecha)}.")


def cargar_precios():
    """RN1: lee precios.txt (producto,precio) y regresa un diccionario.
    Si el archivo no existe o un renglón trae error, usa los precios base."""
    precios = PRECIOS_BASE.copy()
    try:
        with open("precios.txt", "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea == "":
                    continue
                try:
                    producto, precio = linea.split(",")
                    precios[producto.strip()] = float(precio)
                except ValueError:
                    print(f"Renglón con error en precios.txt: '{linea}' (se ignora)")
    except FileNotFoundError:
        print("No encontré precios.txt; uso los precios base.")
    return precios


# ==============================================================
#  Venta y corte (lógica del prototipo de la semana 3)
# ==============================================================

def pedir_cantidad(mensaje):
    """Pide una cantidad entera; si escriben letras, vuelve a preguntar."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Eso no es un número entero. Escribe solo números.")


def registrar_venta(fecha, es_miercoles, precios):
    """Arma una orden, la cobra con ticket y la guarda en ventas.txt."""
    adultos = 0
    ninos = 0
    tercera = 0
    combos = 0
    while True:
        dibujar_tabla(MENU_VENTA, "NUEVA ORDEN")
        opcion = input("Opción: ").strip()

        if not opcion_valida(opcion, MENU_VENTA):
            print("Opción no válida.")

        # Opciones 1 a 3: boletos (RN4: máximo 10 por orden)
        elif opcion == "1" or opcion == "2" or opcion == "3":
            cantidad = pedir_cantidad("Cantidad de boletos: ")
            if cantidad < 1 or adultos + ninos + tercera + cantidad > MAX_BOLETOS:
                print(f"Cantidad no válida o excede {MAX_BOLETOS} boletos por orden.")
            else:
                if opcion == "1":
                    adultos += cantidad
                elif opcion == "2":
                    ninos += cantidad
                else:
                    tercera += cantidad
                print("Agregado. Boletos en la orden:", adultos + ninos + tercera)

        # Opción 4: combos (RN3)
        elif opcion == "4":
            cantidad = pedir_cantidad("Cantidad de combos: ")
            if cantidad < 1:
                print("Cantidad no válida.")
            else:
                combos += cantidad
                print("Agregado. Combos en la orden:", combos)

        # Opción 5: cobrar con ticket
        elif opcion == "5":
            if adultos + ninos + tercera + combos == 0:
                print("La orden está vacía.")
            else:
                # RN2: 2x1 solo en adultos y solo en miércoles
                if es_miercoles:
                    adultos_a_pagar = adultos // 2 + adultos % 2
                else:
                    adultos_a_pagar = adultos

                total = (adultos_a_pagar * precios["adulto"] + ninos * precios["niño"]
                         + tercera * precios["tercera"] + combos * precios["combo"])

                print("\n----------- TICKET -----------")
                print(f"Fecha: {fecha_texto(fecha)}")
                if adultos > 0:
                    print(f"Adulto x{adultos}        ${adultos_a_pagar * precios['adulto']:.2f}")
                if adultos_a_pagar < adultos:
                    print(f"  (2x1 miércoles: se cobran {adultos_a_pagar} de {adultos})")
                if ninos > 0:
                    print(f"Niño x{ninos}          ${ninos * precios['niño']:.2f}")
                if tercera > 0:
                    print(f"Tercera edad x{tercera}  ${tercera * precios['tercera']:.2f}")
                if combos > 0:
                    print(f"Combo x{combos}         ${combos * precios['combo']:.2f}")
                print(f"TOTAL: ${total:.2f}")
                print("------------------------------")

                # Se guarda la venta con la fecha en ventas.txt (modo "a")
                detalle = f"{adultos} adulto, {ninos} niño, {tercera} tercera edad, {combos} combo, ${total:.2f}"
                if anexar("ventas.txt", detalle, fecha):
                    print("Venta guardada en ventas.txt")
                return

        # Opción 0: cancelar
        else:
            print("Orden cancelada.")
            return


def corte_turno(fecha):
    """RN5: suma las ventas del día en ventas.txt y guarda el corte en cortes.txt."""
    hoy = "[" + fecha_texto(fecha) + "]"
    total = 0.0
    ordenes = 0
    try:
        with open("ventas.txt", "r", encoding="utf-8") as f:
            for linea in f:
                if linea.startswith(hoy):       # solo las ventas de la fecha de hoy
                    try:
                        # El total es lo que va después del signo $
                        monto = linea.strip().split("$")[1]
                        total = total + float(monto)
                        ordenes = ordenes + 1
                    except (ValueError, IndexError):
                        print(f"Renglón con error en ventas.txt: '{linea.strip()}'")
    except FileNotFoundError:
        print("Todavía no existe ventas.txt: no hay ventas para el corte.")
        return

    print("\n======= CORTE DE TURNO =======")
    print(f"Fecha:            {fecha_texto(fecha)}")
    print(f"Órdenes cobradas: {ordenes}")
    print(f"Total vendido:    ${total:.2f}")
    print("==============================")
    # Revisar si ya hay un corte con esta fecha para no guardarlo dos veces
    ya_existe = False
    try:
        with open("cortes.txt", "r", encoding="utf-8") as f:
            for linea in f:
                if linea.startswith(hoy):
                    ya_existe = True
    except FileNotFoundError:
        pass                    # si no existe cortes.txt, no hay cortes previos
    if ya_existe:
        print("El corte de esta fecha ya estaba guardado; no se duplica.")
    elif anexar("cortes.txt", f"{ordenes} órdenes, ${total:.2f}", fecha):
        print("Corte guardado en cortes.txt")


# ==============================================================
#  PROGRAMA PRINCIPAL
# ==============================================================

def main():
    """Controla el programa con dos ciclos: inicio (externo) y menú (interno)."""
    precios = cargar_precios()
    salir_programa = False

    # Ciclo externo: la pantalla de inicio. Se repite cuando la
    # inactividad responde "no", para pedir el nombre otra vez.
    while not salir_programa:
        nombre = pedir_nombre()
        bienvenida(nombre)
        pantalla_carga(3)
        Fecha = pedir_fecha()
        es_miercoles = calcular_miercoles(Fecha)
        if es_miercoles:
            print("Hoy es miércoles: aplica 2x1 en boletos de adulto.")

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
            elif opcion == "1":
                registrar_venta(Fecha, es_miercoles, precios)
            elif opcion == "2":
                mostrar_archivos()
            elif opcion == "3":
                ver_archivo()
            elif opcion == "4":
                crear_archivo(Fecha)
            elif opcion == "5":
                agregar_registro(Fecha)
            elif opcion == "6":
                corte_turno(Fecha)
            elif opcion == "0":
                en_menu = False
                salir_programa = True
                print(f"Fin del turno. ¡Hasta luego, {nombre.title()}!")


main()
