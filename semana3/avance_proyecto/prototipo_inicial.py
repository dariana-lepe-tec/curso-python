# Prototipo de taquilla - Cinepolis Esfera Queretaro
# Reglas: RN1 precios, RN2 miercoles 2x1 adulto, RN3 combo,
#         RN4 restriccion de cantidad, RN5 corte de turno

# ---- 1. Constantes y acumuladores (RN1, RN3, RN4) ----
PRECIO_ADULTO = 90.0
PRECIO_NINO = 69.0
PRECIO_TERCERA = 69.0
PRECIO_COMBO = 112.0
MAX_BOLETOS = 10

total_turno = 0.0
ordenes_turno = 0
boletos_turno = 0
salir = False

adultos = 0
ninos = 0
tercera = 0
combos = 0

# ---- 2. Dia de operacion (R1) ----
respuesta = input("¿Hoy es miércoles? (s/n): ")
es_miercoles = respuesta == "s" or respuesta == "S"

# ---- 3. Menu principal (R2) ----
while not salir:
    print()
    print("===== TAQUILLA CINÉPOLIS ESFERA =====")
    print(f"1. Boleto adulto       ${PRECIO_ADULTO:.2f}")
    print(f"2. Boleto niño         ${PRECIO_NINO:.2f}")
    print(f"3. Boleto tercera edad ${PRECIO_TERCERA:.2f}")
    print(f"4. Combo dulcería      ${PRECIO_COMBO:.2f}")
    print("5. Cobrar orden")
    print("6. Corte de turno")
    print("0. Salir")
    opcion = input("Opción: ")

    # ---- 4. Opciones 1 a 3: boletos (R3, RN4) ----
    if opcion == "1" or opcion == "2" or opcion == "3":
        cantidad = int(input("Cantidad: "))
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

    # ---- Opcion 4: combos (RN3, RN4) ----
    elif opcion == "4":
        cantidad = int(input("Cantidad de combos: "))
        if cantidad < 1:
            print("Cantidad no válida.")
        else:
            combos += cantidad
            print("Agregado. Combos en la orden:", combos)

    # ---- 5. Opcion 5: cobrar con ticket (R4, R5, RN2) ----
    elif opcion == "5":
        if adultos + ninos + tercera + combos == 0:
            print("La orden está vacía.")
        else:
            # Regla 2x1: solo adultos y solo en miercoles
            if es_miercoles and adultos > 0:
                adultos_a_pagar = adultos // 2 + adultos % 2
            else:
                adultos_a_pagar = adultos

            total_orden = 0.0
            print()
            print("----------- TICKET -----------")
            for i in range(1, 4):
                if i == 1:
                    nombre = "Adulto"
                    cant = adultos
                    importe = adultos_a_pagar * PRECIO_ADULTO
                elif i == 2:
                    nombre = "Niño"
                    cant = ninos
                    importe = ninos * PRECIO_NINO
                else:
                    nombre = "Tercera edad"
                    cant = tercera
                    importe = tercera * PRECIO_TERCERA
                if cant > 0:
                    print(f"{nombre} x{cant}   ${importe:.2f}")
                total_orden += importe

            if adultos_a_pagar < adultos:
                print(f"  (2x1 miércoles: se cobran {adultos_a_pagar} de {adultos} adultos)")

            if combos > 0:
                importe = combos * PRECIO_COMBO
                print(f"Combo x{combos}   ${importe:.2f}")
                total_orden += importe

            print(f"TOTAL: ${total_orden:.2f}")
            print("------------------------------")

            # Acumular al turno (RN5)
            total_turno += total_orden
            ordenes_turno += 1
            boletos_turno += adultos + ninos + tercera

            # Reiniciar la orden
            adultos = 0
            ninos = 0
            tercera = 0
            combos = 0

    # ---- 6. Opcion 6: corte de turno (R6, RN5) ----
    elif opcion == "6":
        print()
        print("======= CORTE DE TURNO =======")
        print(f"Total vendido:     ${total_turno:.2f}")
        print("Órdenes cobradas: ", ordenes_turno)
        print("Boletos vendidos: ", boletos_turno)
        print("==============================")

    # ---- 7. Opcion 0: salir / otra opcion ----
    elif opcion == "0":
        salir = True
        print("Fin del turno.")
    else:
        print("Opción no válida.")
