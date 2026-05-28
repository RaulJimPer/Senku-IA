(define (domain dominio_senku)

  (:requirements :strips)

  (:predicates
    ; La casilla ?c contiene una pieza sobre el tablero
    (pieza ?c)

    ; La casilla ?c existe en el tablero y está vacía
    (vacio ?c)

    ; Las tres casillas forman una línea recta (horizontal o vertical)
    ; con ?c2 en el centro; es decir, un salto desde ?c1 pasando por
    ; ?c2 aterriza en ?c3.
    (adyacente ?c1 ?c2 ?c3)
  )

  ; ----------------------------------------------------------
  ;  Única acción del dominio: saltar
  ;
  ;  Una pieza en ?origen salta sobre la pieza en ?intermedia
  ;  y aterriza en ?destino. La pieza saltada es capturada
  ;  (eliminada del tablero).
  ; ----------------------------------------------------------
  (:action saltar
    :parameters (?origen ?intermedia ?destino)

    :precondition (and
      ; La pieza que salta debe estar en ?origen
      (pieza ?origen)
      ; Debe haber una pieza en ?intermedia para poder capturarla
      (pieza ?intermedia)
      ; El destino del salto debe ser una casilla vacía del tablero
      (vacio ?destino)
      ; Las tres casillas deben formar una línea válida de salto
      (adyacente ?origen ?intermedia ?destino)
    )

    :effect (and
      ; ?origen queda libre al moverse la pieza
      (not (pieza ?origen))
      (vacio ?origen)

      ; ?intermedia queda libre al ser capturada la pieza
      (not (pieza ?intermedia))
      (vacio ?intermedia)

      ; ?destino pasa a estar ocupada por la pieza que saltó
      (pieza ?destino)
      (not (vacio ?destino))
    )
  )

)