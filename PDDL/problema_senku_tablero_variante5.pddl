(define (problem problema5)
  (:domain dominio_senku)
  (:objects
    c51
    c42 c52 c62
    c33 c43 c53 c63 c73
    c24 c34 c44 c54 c64 c74 c84
    c15 c25 c35 c45 c55 c65 c75 c85 c95
    c26 c36 c46 c56 c66 c76 c86
    c37 c47 c57 c67 c77
    c48 c58 c68
    c59
  )

  (:init
    ;; ADYACENCIAS HORIZONTALES
    (adyacente c42 c52 c62) (adyacente c62 c52 c42)
    (adyacente c33 c43 c53) (adyacente c53 c43 c33)
    (adyacente c43 c53 c63) (adyacente c63 c53 c43)
    (adyacente c53 c63 c73) (adyacente c73 c63 c53)
    (adyacente c24 c34 c44) (adyacente c44 c34 c24)
    (adyacente c34 c44 c54) (adyacente c54 c44 c34)
    (adyacente c44 c54 c64) (adyacente c64 c54 c44)
    (adyacente c54 c64 c74) (adyacente c74 c64 c54)
    (adyacente c64 c74 c84) (adyacente c84 c74 c64)
    (adyacente c15 c25 c35) (adyacente c35 c25 c15)
    (adyacente c25 c35 c45) (adyacente c45 c35 c25)
    (adyacente c35 c45 c55) (adyacente c55 c45 c35)
    (adyacente c45 c55 c65) (adyacente c65 c55 c45)
    (adyacente c55 c65 c75) (adyacente c75 c65 c55)
    (adyacente c65 c75 c85) (adyacente c85 c75 c65)
    (adyacente c75 c85 c95) (adyacente c95 c85 c75)
    (adyacente c26 c36 c46) (adyacente c46 c36 c26)
    (adyacente c36 c46 c56) (adyacente c56 c46 c36)
    (adyacente c46 c56 c66) (adyacente c66 c56 c46)
    (adyacente c56 c66 c76) (adyacente c76 c66 c56)
    (adyacente c66 c76 c86) (adyacente c86 c76 c66)
    (adyacente c37 c47 c57) (adyacente c57 c47 c37)
    (adyacente c47 c57 c67) (adyacente c67 c57 c47)
    (adyacente c57 c67 c77) (adyacente c77 c67 c57)
    (adyacente c48 c58 c68) (adyacente c68 c58 c48)

    ;; ADYACENCIAS VERTICALES
    (adyacente c24 c25 c26) (adyacente c26 c25 c24)
    (adyacente c33 c34 c35) (adyacente c35 c34 c33)
    (adyacente c34 c35 c36) (adyacente c36 c35 c34)
    (adyacente c35 c36 c37) (adyacente c37 c36 c35)
    (adyacente c42 c43 c44) (adyacente c44 c43 c42)
    (adyacente c43 c44 c45) (adyacente c45 c44 c43)
    (adyacente c44 c45 c46) (adyacente c46 c45 c44)
    (adyacente c45 c46 c47) (adyacente c47 c46 c45)
    (adyacente c46 c47 c48) (adyacente c48 c47 c46)
    (adyacente c51 c52 c53) (adyacente c53 c52 c51)
    (adyacente c52 c53 c54) (adyacente c54 c53 c52)
    (adyacente c53 c54 c55) (adyacente c55 c54 c53)
    (adyacente c54 c55 c56) (adyacente c56 c55 c54)
    (adyacente c55 c56 c57) (adyacente c57 c56 c55)
    (adyacente c56 c57 c58) (adyacente c58 c57 c56)
    (adyacente c57 c58 c59) (adyacente c59 c58 c57)
    (adyacente c62 c63 c64) (adyacente c64 c63 c62)
    (adyacente c63 c64 c65) (adyacente c65 c64 c63)
    (adyacente c64 c65 c66) (adyacente c66 c65 c64)
    (adyacente c65 c66 c67) (adyacente c67 c66 c65)
    (adyacente c66 c67 c68) (adyacente c68 c67 c66)
    (adyacente c73 c74 c75) (adyacente c75 c74 c73)
    (adyacente c74 c75 c76) (adyacente c76 c75 c74)
    (adyacente c75 c76 c77) (adyacente c77 c76 c75)
    (adyacente c84 c85 c86) (adyacente c86 c85 c84)

    ;; ESTADO INICIAL
    (pieza c51)
    (pieza c42) (pieza c52) (pieza c62)
    (pieza c33) (pieza c43) (pieza c53) (pieza c63) (pieza c73)
    (pieza c24) (pieza c34) (pieza c44) (pieza c54) (pieza c64) (pieza c74) (pieza c84)
    (pieza c15) (pieza c25) (pieza c35) (pieza c45) (vacio c55) (pieza c65) (pieza c75) (pieza c85) (pieza c95)
    (pieza c26) (pieza c36) (pieza c46) (pieza c56) (pieza c66) (pieza c76) (pieza c86)
    (pieza c37) (pieza c47) (pieza c57) (pieza c67) (pieza c77)
    (pieza c48) (pieza c58) (pieza c68)
    (pieza c59)
  )

  (:goal
    (and
      ;; ESTADO OBJETIVO
      (vacio c51)
      (vacio c42) (vacio c52) (vacio c62)
      (vacio c33) (vacio c43) (vacio c53) (vacio c63) (vacio c73)
      (vacio c24) (vacio c34) (vacio c44) (vacio c54) (vacio c64) (vacio c74) (vacio c84)
      (vacio c15) (vacio c25) (vacio c35) (vacio c45) (pieza c55) (vacio c65) (vacio c75) (vacio c85) (vacio c95)
      (vacio c26) (vacio c36) (vacio c46) (vacio c56) (vacio c66) (vacio c76) (vacio c86)
      (vacio c37) (vacio c47) (vacio c57) (vacio c67) (vacio c77)
      (vacio c48) (vacio c58) (vacio c68)
      (vacio c59)
    )
  )
)