// Prototipo de taquilla - Cinepolis Esfera Queretaro
// Reglas: RN1 precios, RN2 miercoles 2x1 adulto, RN3 combo,
//         RN4 restriccion de cantidad, RN5 corte de turno
Algoritmo TaquillaCinepolis

	// ---- Variables (Req. 4) ----
	Definir PRECIO_ADULTO, PRECIO_NINO, PRECIO_TERCERA, PRECIO_COMBO Como Real
	Definir MAX_BOLETOS Como Entero
	Definir es_miercoles, salir Como Logico
	Definir opcion, respuesta, nombre Como Caracter
	Definir cantidad, adultos, ninos, tercera, combos, adultos_a_pagar Como Entero
	Definir total_orden, total_turno, importe Como Real
	Definir ordenes_turno, boletos_turno, i, cant Como Entero

	// ---- 1. Valores iniciales (RN1, RN3, RN4) ----
	PRECIO_ADULTO <- 90.0
	PRECIO_NINO <- 69.0
	PRECIO_TERCERA <- 69.0
	PRECIO_COMBO <- 112.0
	MAX_BOLETOS <- 10

	total_turno <- 0
	ordenes_turno <- 0
	boletos_turno <- 0
	salir <- Falso

	adultos <- 0
	ninos <- 0
	tercera <- 0
	combos <- 0

	// ---- 2. Dia de operacion (R1) ----
	Escribir "Hoy es miercoles? (s/n): " Sin Saltar
	Leer respuesta
	es_miercoles <- respuesta = "s" O respuesta = "S"

	// ---- 3. Menu principal (R2) ----
	Mientras NO salir Hacer
		Escribir ""
		Escribir "===== TAQUILLA CINEPOLIS ESFERA ====="
		Escribir "1. Boleto adulto       $", PRECIO_ADULTO
		Escribir "2. Boleto nino         $", PRECIO_NINO
		Escribir "3. Boleto tercera edad $", PRECIO_TERCERA
		Escribir "4. Combo dulceria      $", PRECIO_COMBO
		Escribir "5. Cobrar orden"
		Escribir "6. Corte de turno"
		Escribir "0. Salir"
		Escribir "Opcion: " Sin Saltar
		Leer opcion

		// ---- 4. Opciones 1 a 3: boletos (R3, RN4) ----
		Si opcion = "1" O opcion = "2" O opcion = "3" Entonces
			Escribir "Cantidad: " Sin Saltar
			Leer cantidad
			Si cantidad < 1 O adultos + ninos + tercera + cantidad > MAX_BOLETOS Entonces
				Escribir "Cantidad no valida o excede ", MAX_BOLETOS, " boletos por orden."
			SiNo
				Si opcion = "1" Entonces
					adultos <- adultos + cantidad
				SiNo
					Si opcion = "2" Entonces
						ninos <- ninos + cantidad
					SiNo
						tercera <- tercera + cantidad
					FinSi
				FinSi
				Escribir "Agregado. Boletos en la orden: ", adultos + ninos + tercera
			FinSi

		SiNo
			// ---- 5. Opcion 4: combos (RN3, RN4) ----
			Si opcion = "4" Entonces
				Escribir "Cantidad de combos: " Sin Saltar
				Leer cantidad
				Si cantidad < 1 Entonces
					Escribir "Cantidad no valida."
				SiNo
					combos <- combos + cantidad
					Escribir "Agregado. Combos en la orden: ", combos
				FinSi

			SiNo
				// ---- 6. Opcion 5: cobrar (R4, R5, RN2) ----
				Si opcion = "5" Entonces
					Si adultos + ninos + tercera + combos = 0 Entonces
						Escribir "La orden esta vacia."
					SiNo
						// Regla 2x1: solo adultos y solo en miercoles
						Si es_miercoles Y adultos > 0 Entonces
							adultos_a_pagar <- trunc(adultos / 2) + adultos MOD 2
						SiNo
							adultos_a_pagar <- adultos
						FinSi

						total_orden <- 0
						Escribir ""
						Escribir "----------- TICKET -----------"
						Para i <- 1 Hasta 3 Con Paso 1 Hacer
							Si i = 1 Entonces
								nombre <- "Adulto"
								cant <- adultos
								importe <- adultos_a_pagar * PRECIO_ADULTO
							SiNo
								Si i = 2 Entonces
									nombre <- "Nino"
									cant <- ninos
									importe <- ninos * PRECIO_NINO
								SiNo
									nombre <- "Tercera edad"
									cant <- tercera
									importe <- tercera * PRECIO_TERCERA
								FinSi
							FinSi
							Si cant > 0 Entonces
								Escribir nombre, " x", cant, "   $", importe
							FinSi
							total_orden <- total_orden + importe
						FinPara

						Si adultos_a_pagar < adultos Entonces
							Escribir "  (2x1 miercoles: se cobran ", adultos_a_pagar, " de ", adultos, " adultos)"
						FinSi

						Si combos > 0 Entonces
							importe <- combos * PRECIO_COMBO
							Escribir "Combo x", combos, "   $", importe
							total_orden <- total_orden + importe
						FinSi

						Escribir "TOTAL: $", total_orden
						Escribir "------------------------------"

						// Acumular al turno (RN5)
						total_turno <- total_turno + total_orden
						ordenes_turno <- ordenes_turno + 1
						boletos_turno <- boletos_turno + adultos + ninos + tercera

						// Reiniciar la orden
						adultos <- 0
						ninos <- 0
						tercera <- 0
						combos <- 0
					FinSi

				SiNo
					// ---- 7. Opcion 6: corte de turno (R6, RN5) ----
					Si opcion = "6" Entonces
						Escribir ""
						Escribir "======= CORTE DE TURNO ======="
						Escribir "Total vendido:     $", total_turno
						Escribir "Ordenes cobradas:  ", ordenes_turno
						Escribir "Boletos vendidos:  ", boletos_turno
						Escribir "=============================="

					SiNo
						// ---- 8. Opcion 0: salir / otra opcion ----
						Si opcion = "0" Entonces
							salir <- Verdadero
							Escribir "Fin del turno."
						SiNo
							Escribir "Opcion no valida."
						FinSi
					FinSi
				FinSi
			FinSi
		FinSi
	FinMientras

FinAlgoritmo
