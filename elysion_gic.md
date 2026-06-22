## GIC

ΣT = ```{ inicio, fin, si, sino, repetir, desde, hasta, mientras, funcion, retornar,
  verdadero, falso, y, o, no,
  recurso, porcentaje, bytes, segundos, comando, estado, booleano, entero, texto,
  obtener_uso_cpu, obtener_memoria_libre, obtener_uso_disco, obtener_uso_memoria,
  estado_servicio, ejecutar_comando, registrar_alerta, registrar_incidente,
  mostrar, esperar, leer_metricas, exportar_log, formatear_bytes,
  mostrar_estado, verificar_disco, generar_reporte_sistema,
  ==, !=, <, >, <=, >=, +, -, *, /, %,
  (, ), {, }, :, ,, =, ., #,
  numero_literal, decimal_literal, cadena_literal, identificador_literal,
  cualquier_caracter_excepto_salto }```

ΣN = ```{ <programa>, <bloque>, <sentencia>, <declaracion>, <asignacion>, <tipo>,
  <condicional>, <cadena_sino>, <condicion>, <condicion_o>, <mas_o>,
  <condicion_y>, <mas_y>, <condicion_no>, <comparacion>, <cola_comparacion>,
  <bucle>, <definicion_funcion>, <llamada_funcion>, <io>,
  <expresion>, <suma_opcional>, <termino>, <producto_opcional>, <factor>,
  <uso_variable>, <op_suma>, <op_mul>,
  <parametros>, <lista_parametros>, <parametros_extra>, <parametro>,
  <argumentos>, <lista_argumentos>, <argumentos_extra>,
  <estado_valor>, <booleano>, <operador_relacional>,
  <numero>, <decimal>, <cadena>, <contenido_cadena>, <identificador>,
  <resto_identificador>, <letra>, <digito>,
  <comentario_linea>, <comentario_linea_contenido> }```

P =
```
<programa> -> inicio <bloque> fin

<bloque> -> <sentencia> <bloque> | λ

<sentencia> -> <declaracion>
             | <asignacion>
             | <condicional>
             | <bucle>
             | <definicion_funcion>
             | <llamada_funcion>
             | <io>

# -----------------------------
# Declaración, asignación y tipos
# -----------------------------
<declaracion> -> <identificador> : <tipo> = <expresion>
<asignacion> -> <identificador> = <expresion>

<tipo> -> recurso | porcentaje | bytes | segundos | comando | estado | booleano | entero | texto

# -----------------------------
# Entrada / Salida del sistema
# -----------------------------
<io> -> leer_metricas ( <expresion> )
      | mostrar_estado ( )
      | exportar_log ( <expresion> )
      | ejecutar_comando ( <expresion> )
      | mostrar ( <expresion> )
      | registrar_alerta ( <expresion> )
      | registrar_incidente ( <expresion> )
      | esperar ( <expresion> )

# -----------------------------
# Condicional con precedencia (no > y > o)
# -----------------------------
<condicional> -> si <condicion> { <bloque> } <cadena_sino>

<cadena_sino> -> sino si <condicion> { <bloque> } <cadena_sino>
               | sino { <bloque> }
               | λ

<condicion> -> <condicion_o>

<condicion_o> -> <condicion_y> <mas_o>
<mas_o> -> o <condicion_y> <mas_o> | λ

<condicion_y> -> <condicion_no> <mas_y>
<mas_y> -> y <condicion_no> <mas_y> | λ

<condicion_no> -> no <condicion_no> | <comparacion>

<comparacion> -> <expresion> <cola_comparacion>
<cola_comparacion> -> <operador_relacional> <expresion> | λ

# -----------------------------
# Bucles (repetir y mientras)
# -----------------------------
<bucle> -> repetir <identificador> desde <expresion> hasta <expresion> { <bloque> }
         | mientras <condicion> { <bloque> }

# -----------------------------
# Expresiones aritméticas (sin recursión izquierda)
# -----------------------------
<expresion> -> <termino> <suma_opcional>
<suma_opcional> -> <op_suma> <termino> <suma_opcional> | λ

<termino> -> <factor> <producto_opcional>
<producto_opcional> -> <op_mul> <factor> <producto_opcional> | λ

<factor> -> <numero>
          | <decimal>
          | <cadena>
          | <booleano>
          | ( <expresion> )
          | <identificador> <uso_variable>

<uso_variable> -> ( <argumentos> )    # llamada a función
               | λ                    # variable simple

<op_suma> -> + | -
<op_mul> -> * | / | %

# -----------------------------
# Funciones
# -----------------------------
<definicion_funcion> -> funcion <identificador> ( <parametros> ) : <tipo> { <bloque> retornar <expresion> }

<llamada_funcion> -> <identificador> ( <argumentos> )

<parametros> -> <lista_parametros> | λ
<lista_parametros> -> <parametro> <parametros_extra>
<parametros_extra> -> , <parametro> <parametros_extra> | λ
<parametro> -> <identificador> : <tipo>

<argumentos> -> <lista_argumentos> | λ
<lista_argumentos> -> <expresion> <argumentos_extra>
<argumentos_extra> -> , <expresion> <argumentos_extra> | λ

# -----------------------------
# Valores especiales de estado
# -----------------------------
<estado_valor> -> "running" | "stopped" | "degraded" | "down"

# -----------------------------
# Léxico y operadores
# -----------------------------
<booleano> -> verdadero | falso
<operador_relacional> -> == | != | < | > | <= | >=

<numero> -> <digito> | <digito> <numero>
<decimal> -> <numero> . <numero>
<cadena> -> " <contenido_cadena> "
<contenido_cadena> -> <letra> <contenido_cadena> | <digito> <contenido_cadena> | λ

<identificador> -> <letra> <resto_identificador>
<resto_identificador> -> <letra> <resto_identificador>
                       | <digito> <resto_identificador>
                       | _ <resto_identificador>
                       | λ

<letra> -> a | b | ... | z | A | B | ... | Z
<digito> -> 0 | 1 | ... | 9

<comentario_linea> -> # <comentario_linea_contenido>
<comentario_linea_contenido> -> cualquier_caracter_excepto_salto <comentario_linea_contenido> | λ
```

S= ```<programa>```

## Programa ejemplo

inicio

umbral_cpu: porcentaje = (50 + 30) * 1

fin

## Análisis Sintáctico Descendente (ASD) - Derivación por la izquierda

Programa

⇒ inicio **[Bloque]** fin

⇒ inicio **[Sentencia]** Bloque fin

⇒ inicio **[Declaracion]** Bloque fin

⇒ inicio **[Identificador : Tipo = Expresion]** Bloque fin

⇒ inicio **[umbral_cpu]** : Tipo = Expresion Bloque fin

⇒ inicio umbral_cpu : **[Tipo]** = Expresion Bloque fin

⇒ inicio umbral_cpu : **[porcentaje]** = Expresion Bloque fin

⇒ inicio umbral_cpu : porcentaje = **[Expresion]** Bloque fin

⇒ inicio umbral_cpu : porcentaje = **[Termino SumaOpcional]** Bloque fin

⇒ inicio umbral_cpu : porcentaje = **[Factor ProductoOpcional]** SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = **[( Expresion )]** ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( **[Expresion]** ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( **[Termino SumaOpcional]** ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( **[Factor ProductoOpcional]** SumaOpcional ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( **[Numero]** ProductoOpcional SumaOpcional ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( **[50]** ProductoOpcional SumaOpcional ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 **[ProductoOpcional]** SumaOpcional ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 **[λ]** SumaOpcional ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 **[SumaOpcional]** ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 **[OpSuma Termino SumaOpcional]** ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 **[+]** Termino SumaOpcional ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + **[Termino]** SumaOpcional ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + **[Factor ProductoOpcional]** SumaOpcional ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + **[Numero]** ProductoOpcional SumaOpcional ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + **[30]** ProductoOpcional SumaOpcional ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 **[ProductoOpcional]** SumaOpcional ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 **[λ]** SumaOpcional ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 **[SumaOpcional]** ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 **[λ]** ) ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) **[ProductoOpcional]** SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) **[OpMul Factor ProductoOpcional]** SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) **[*]** Factor ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) * **[Factor]** ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) * **[Numero]** ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) * **[1]** ProductoOpcional SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) * 1 **[ProductoOpcional]** SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) * 1 **[λ]** SumaOpcional Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) * 1 **[SumaOpcional]** Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) * 1 **[λ]** Bloque fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) * 1 **[Bloque]** fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) * 1 **[λ]** fin

## Análisis Sintáctico Ascendente (ASA) - Derivación por la derecha

Programa

⇒ inicio **[Bloque]** fin

⇒ inicio Sentencia **[Bloque]** fin

⇒ inicio Sentencia **[λ]** fin

⇒ inicio **[Sentencia]** fin

⇒ inicio **[Declaracion]** fin

⇒ inicio **[Identificador : Tipo = Expresion]** fin

⇒ inicio Identificador : Tipo = **[Expresion]** fin

⇒ inicio Identificador : Tipo = **[Termino SumaOpcional]** fin

⇒ inicio Identificador : Tipo = Termino **[SumaOpcional]** fin

⇒ inicio Identificador : Tipo = Termino **[λ]** fin

⇒ inicio Identificador : Tipo = **[Termino]** fin

⇒ inicio Identificador : Tipo = **[Factor ProductoOpcional]** fin

⇒ inicio Identificador : Tipo = Factor **[ProductoOpcional]** fin

⇒ inicio Identificador : Tipo = Factor **[OpMul Factor ProductoOpcional]** fin

⇒ inicio Identificador : Tipo = Factor OpMul Factor **[ProductoOpcional]** fin

⇒ inicio Identificador : Tipo = Factor OpMul Factor **[λ]** fin

⇒ inicio Identificador : Tipo = Factor OpMul **[Factor]** fin

⇒ inicio Identificador : Tipo = Factor OpMul **[Numero]** fin

⇒ inicio Identificador : Tipo = Factor OpMul **[1]** fin

⇒ inicio Identificador : Tipo = Factor **[OpMul]** 1 fin

⇒ inicio Identificador : Tipo = Factor **[*]** 1 fin

⇒ inicio Identificador : Tipo = **[Factor]** * 1 fin

⇒ inicio Identificador : Tipo = **[( Expresion )]** * 1 fin

⇒ inicio Identificador : Tipo = ( **[Expresion]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[Termino SumaOpcional]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino **[SumaOpcional]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino **[OpSuma Termino SumaOpcional]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma Termino **[SumaOpcional]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma Termino **[λ]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma **[Termino]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma **[Factor ProductoOpcional]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma Factor **[ProductoOpcional]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma Factor **[λ]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma **[Factor]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma **[Numero]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma **[30]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino **[OpSuma]** 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino **[+]** 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[Termino]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[Factor ProductoOpcional]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( Factor **[ProductoOpcional]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( Factor **[λ]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[Factor]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[Numero]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[50]** + 30 ) * 1 fin

⇒ inicio Identificador : **[Tipo]** = ( 50 + 30 ) * 1 fin

⇒ inicio Identificador : **[porcentaje]** = ( 50 + 30 ) * 1 fin

⇒ inicio **[Identificador]** : porcentaje = ( 50 + 30 ) * 1 fin

⇒ inicio **[umbral_cpu]** : porcentaje = ( 50 + 30 ) * 1 fin

⇒ inicio umbral_cpu : porcentaje = ( 50 + 30 ) * 1 fin

### Orden Inverso a la derivación por derecha

inicio umbral_cpu : porcentaje = ( 50 + 30 ) * 1 fin

⇒ inicio **[umbral_cpu]** : porcentaje = ( 50 + 30 ) * 1 fin

⇒ inicio **[Identificador]** : porcentaje = ( 50 + 30 ) * 1 fin

⇒ inicio Identificador : **[porcentaje]** = ( 50 + 30 ) * 1 fin

⇒ inicio Identificador : **[Tipo]** = ( 50 + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[50]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[Numero]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[Factor]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( Factor **[λ]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( Factor **[ProductoOpcional]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[Factor ProductoOpcional]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[Termino]** + 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino **[+]** 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino **[OpSuma]** 30 ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma **[30]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma **[Numero]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma **[Factor]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma Factor **[λ]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma Factor **[ProductoOpcional]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma **[Factor ProductoOpcional]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma **[Termino]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino **[OpSuma Termino SumaOpcional]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino OpSuma Termino **[λ]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( Termino **[SumaOpcional]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[Termino SumaOpcional]** ) * 1 fin

⇒ inicio Identificador : Tipo = ( **[Expresion]** ) * 1 fin

⇒ inicio Identificador : Tipo = **[( Expresion )]** * 1 fin

⇒ inicio Identificador : Tipo = **[Factor]** * 1 fin

⇒ inicio Identificador : Tipo = Factor **[*]** 1 fin

⇒ inicio Identificador : Tipo = Factor **[OpMul]** 1 fin

⇒ inicio Identificador : Tipo = Factor OpMul **[1]** fin

⇒ inicio Identificador : Tipo = Factor OpMul **[Numero]** fin

⇒ inicio Identificador : Tipo = Factor OpMul **[Factor]** fin

⇒ inicio Identificador : Tipo = Factor OpMul Factor **[λ]** fin

⇒ inicio Identificador : Tipo = Factor OpMul Factor **[ProductoOpcional]** fin

⇒ inicio Identificador : Tipo = Factor **[OpMul Factor ProductoOpcional]** fin

⇒ inicio Identificador : Tipo = **[Factor ProductoOpcional]** fin

⇒ inicio Identificador : Tipo = **[Termino]** fin

⇒ inicio Identificador : Tipo = Termino **[λ]** fin

⇒ inicio Identificador : Tipo = Termino **[SumaOpcional]** fin

⇒ inicio Identificador : Tipo = **[Termino SumaOpcional]** fin

⇒ inicio Identificador : Tipo = **[Expresion]** fin

⇒ inicio **[Identificador : Tipo = Expresion]** fin

⇒ inicio **[Declaracion]** fin

⇒ inicio **[Sentencia]** fin

⇒ inicio Sentencia **[λ]** fin

⇒ inicio Sentencia **[Bloque]** fin

⇒ inicio **[Sentencia Bloque]** fin

⇒ inicio **[Bloque]** fin

⇒ **[inicio Bloque fin]**

Programa
