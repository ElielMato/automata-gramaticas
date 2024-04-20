def automata_finito(cadena):
    
  def transicion(estado, simbolo):
    if estado == 'A':
      if simbolo == 'a':
        return 'B'
      elif simbolo == 'b':
        return 'C'
    elif estado == 'B':
      if simbolo == 'a':
        return 'B'
      elif simbolo == 'b':
        return 'C'
    elif estado == 'C':
      if simbolo == 'a':
        return 'B'
      elif simbolo == 'b':
        return 'C'
    else:
      return None

  estado_actual = 'A' 

  estados_aceptacion = {"A", "B", "C"} 

  for simbolo in cadena:
    estado_siguiente = transicion(estado_actual, simbolo)
    print(f"[{estado_actual}]-- ({simbolo})--> [{estado_siguiente}]")

    estado_actual = estado_siguiente

    if estado_actual is None:
      print("La cadena NO es aceptada")
      return

  if estado_actual in estados_aceptacion:
    print("La cadena es aceptada")
  else:
    print("La cadena NO es aceptada")

cadena = input("Ingrese una cadena: ")
cadena_minus = cadena.lower()
automata_finito(cadena_minus)
    
    