def automata_finito_no_determinista(cadena):
    alfabeto = {"a", "b", "ε"}
    estado_actual = 0 
    estados_aceptacion = 13
    
    if not all(caracter in alfabeto for caracter in cadena):
        print("La cadena NO es aceptada")     
    else:

        i = 0
        while i != len(cadena):
            simbolo = cadena[i]
            
            if estado_actual == 0:
                if simbolo == "a":
                    estado_siguiente = 2
                    print(f"[{estado_actual}]-- (ε)--> [{estado_siguiente}]")
                    estado_actual = estado_siguiente
                elif simbolo == "b":
                    estado_siguiente = 1
                    print(f"[{estado_actual}]-- (ε)--> [{estado_siguiente}]")
                    estado_actual = estado_siguiente
                elif simbolo == "ε":
                    estado_siguiente = 5
                    print(f"[{estado_actual}]-- (ε)--> [{estado_siguiente}]")
                    estado_actual = estado_siguiente
                    if len(cadena) > 1:
                        i += 1
                else:
                    estado_siguiente = None
                    print(f"[{estado_actual}]-- (ε)--> [{estado_siguiente}]")
                    print("La cadena no es aceptada")
                    return
            
            elif estado_actual == 1:
                estado_siguiente = 3
                print(f"[{estado_actual}]-- ({simbolo})--> [{estado_siguiente}]")
                estado_actual = estado_siguiente
                if len(cadena) > 1:
                    i += 1
            
            elif estado_actual == 2:
                estado_siguiente = 4
                print(f"[{estado_actual}]-- ({simbolo})--> [{estado_siguiente}]")
                estado_actual = estado_siguiente
                if len(cadena) > 1:
                    i += 1
                
            elif estado_actual == 3 or estado_actual == 4:
                estado_siguiente = 5
                print(f"[{estado_actual}]-- (ε)--> [{estado_siguiente}]")
                estado_actual = estado_siguiente
                
            elif estado_actual == 5 and i != len(cadena) - 1:
                estado_siguiente = 0
                print(f"[{estado_actual}]-- (ε)--> [{estado_siguiente}]")
                estado_actual = estado_siguiente
                
                
            elif estado_actual == 5 and i == len(cadena) - 1:
                estado_siguiente = 6
                print(f"[{estado_actual}]-- (ε)--> [{estado_siguiente}]")
                estado_actual = estado_siguiente
                    
            elif estado_actual == 6 and simbolo == "a":
                estado_siguiente = 7
                print(f"[{estado_actual}]-- (ε)--> [{estado_siguiente}]")
                estado_actual = estado_siguiente
                
            elif estado_actual == 6 and simbolo == "b":
                estado_siguiente = 8
                print(f"[{estado_actual}]-- (ε)--> [{estado_siguiente}]")
                estado_actual = estado_siguiente
                
            elif estado_actual == 6 and simbolo == "ε":
                estado_siguiente = 9
                print(f"[{estado_actual}]-- (ε)--> [{estado_siguiente}]")
                estado_actual = estado_siguiente
            

            elif estado_actual == 7:
                estado_siguiente = 10
                print(f"[{estado_actual}]-- ({simbolo})--> [{estado_siguiente}]")
                estado_actual = estado_siguiente
            
            elif estado_actual == 8:
                estado_siguiente = 11
                print(f"[{estado_actual}]-- ({simbolo})--> [{estado_siguiente}]")
                estado_actual = estado_siguiente
            
            elif estado_actual == 9:
                estado_siguiente = 12
                print(f"[{estado_actual}]-- (ε)--> [{estado_siguiente}]")
                estado_actual = estado_siguiente

            elif estado_actual in [10, 11, 12]:
                estado_siguiente = 13
                print(f"[{estado_actual}]-- (ε)--> [{estado_siguiente}]")
                estado_actual = estado_siguiente
                break
        
        
        if estado_actual == estados_aceptacion:
            print("La cadena es aceptada")
        else:
            print("La cadena NO es aceptada")



cadena = input("Ingrese una cadena: ")
cadena_minus = cadena.lower()
automata_finito_no_determinista(cadena_minus)