# Elysion

## Descripción del lenguaje

Es un lenguaje de dominio específico diseñado para monitoreo y administración básica de sistemas informáticos. Su sintaxis es clara y expresiva, pensada para facilitar la supervisión de recursos del sistema y la automatización de tareas administrativas simples en un entorno simulado.

## Tipos de datos

- **porcentaje** → valor decimal que representa un porcentaje (ej: 85.0).

- **bytes** → valor entero que representa una cantidad de bytes (ej: 1073741824).

- **segundos** → valor entero que representa una duración en segundos (ej: 300).

- **comando** → cadena de texto que representa un comando del sistema operativo (ej: "df -h").

- **estado** → cadena de texto con valores posibles: "running", "stopped", "degraded", "down".

- **booleano** → verdadero / falso.

- **entero** → valor numérico entero.

- **texto** → cadena de texto entre comillas dobles.

- **recurso** → tipo genérico para representar un recurso del sistema.

## Estructura de programa

Un programa comienza con **inicio** y termina con **fin**. Todas las sentencias válidas van entre esas dos palabras clave.

### Sentencias principales
### Declaración y asignación

- Declaración con tipo: ```identificador: tipo = expresion```

- Reasignación: ```identificador = expresion```

### Impresión y salida

**mostrar** acepta una expresión que puede concatenar partes con + (variables, cadenas, números).
Ej.: ```mostrar("CPU: " + obtener_uso_cpu() + "%")```

### Condicional

```si expresion { bloques }``` ejecuta un bloque si la condición es verdadera. Opcionalmente se encadenan ```sino si expresion { bloques }``` y ```sino { bloques }```.

Negación: ```no expresion```

### Iteración

- **Repetir con rango:** ```repetir identificador desde expresion hasta expresion { bloques }```

- **Mientras:** ```mientras expresion { bloques }```

## Funciones built-in del sistema

- ```obtener_uso_cpu()``` → retorna el uso actual de CPU como porcentaje.

- ```obtener_memoria_libre()``` → retorna la memoria libre en bytes.

- ```obtener_uso_disco(path)``` → retorna el uso de disco de una ruta como porcentaje.

- ```obtener_uso_memoria()``` → retorna el uso de memoria como porcentaje.

- ```estado_servicio(nombre)``` → retorna el estado de un servicio como estado.

- ```ejecutar_comando(cmd)``` → ejecuta un comando del sistema operativo.

- ```registrar_alerta(mensaje)``` → registra una alerta en el log del sistema.

- ```registrar_incidente(mensaje)``` → registra un incidente en el log del sistema.

- ```mostrar(expresion)``` → imprime un valor o mensaje en consola.

- ```esperar(segundos)``` → pausa la ejecución durante una cantidad de segundos.

- ```leer_metricas(archivo)``` → lee métricas desde un archivo del sistema.

- ```exportar_log(archivo)``` → exporta el log a un archivo.

- ```formatear_bytes(valor)``` → convierte bytes a formato legible.

- ```mostrar_estado()``` → muestra el estado general del sistema.

## Funciones definidas por el usuario

Las funciones se definen con **funcion**, reciben parámetros tipados y retornan un valor con **retornar**.
```
funcion identificador(parametros): tipo {
    sentencias
    retornar expresion
}
```

Llamada: ```identificador(argumentos)```

## Comentarios

- De línea: ```# comentario```

## Operadores

- **Aritméticos:** +, -, *, / con precedencia: * / > + - (asociatividad izquierda).
  Se admiten paréntesis para agrupar: ( … ).

- **Relacionales:** ==, !=, <, >, <=, >= (se permiten en ambos lados valores/expresiones).

- **Lógicos:** y, o, y prefijo no.

## Reglas semánticas

- Tipado estático: las variables deben declararse con tipo explícito.

- Los tipos del dominio (porcentaje, bytes, segundos) previenen errores en la gestión de recursos.

- Las funciones built-in operan en un entorno simulado, no afectan el sistema real.

- El programa se ejecuta secuencialmente entre `inicio` y `fin`.

- Las operaciones y comandos de sistema son simulados con fines educativos.

## Ejemplo
```
inicio

# Configuración de umbrales
umbral_cpu: porcentaje = 85.0
umbral_memoria: bytes = 1073741824
tiempo_check: segundos = 300

# Monitoreo de CPU en 10 ciclos
repetir chequeo desde 1 hasta 10 {
  estado_cpu: porcentaje = obtener_uso_cpu()
  estado_mem: bytes = obtener_memoria_libre()

  si estado_cpu > umbral_cpu {
    registrar_alerta("CPU sobrecargada: " + estado_cpu + "%")
  }

  esperar(tiempo_check)
}

# Verificar estado de un servicio
si estado_servicio("nginx") == "down" {
  ejecutar_comando("systemctl start nginx")
  registrar_incidente("nginx reiniciado automáticamente")
} sino si estado_servicio("nginx") == "degraded" {
  mostrar("Nginx en estado degradado - revisar logs")
} sino {
  mostrar("Nginx funcionando correctamente")
}

# Función personalizada
funcion verificar_disco(path: texto, umbral: porcentaje): booleano {
  uso_actual: porcentaje = obtener_uso_disco(path)
  retornar uso_actual > umbral
}

disco_lleno: booleano = verificar_disco("/", 90.0)
si disco_lleno {
  mostrar("Disco lleno - ejecutar limpieza")
}

# Reporte final
reporte: texto = generar_reporte_sistema()
exportar_log("monitoreo_final.log")
mostrar("Monitoreo completado - Reporte guardado")

fin
```
## Salida (simulada)
```
CPU sobrecargada: 92.3%
nginx reiniciado automáticamente
Disco lleno - ejecutar limpieza
Monitoreo completado - Reporte guardado
```


## BNF
```
<programa> ::= inicio <bloque> fin

<bloque> ::= <sentencia> <bloque> | λ

<sentencia> ::= <declaracion>
              | <asignacion>
              | <condicional>
              | <bucle>
              | <definicion_funcion>
              | <llamada_funcion>
              | <io>

# -----------------------------
# Declaración, asignación y tipos
# -----------------------------
<declaracion> ::= <identificador> : <tipo> = <expresion>
<asignacion> ::= <identificador> = <expresion>

<tipo> ::= recurso | porcentaje | bytes | segundos | comando | estado | booleano | entero | texto

# -----------------------------
# Entrada / Salida del sistema
# -----------------------------
<io> ::= leer_metricas ( <expresion> )
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
<condicional> ::= si <condicion> { <bloque> } <cadena_sino>

<cadena_sino> ::= sino si <condicion> { <bloque> } <cadena_sino>
               | sino { <bloque> }
               | λ

<condicion> ::= <condicion_o>

<condicion_o> ::= <condicion_y> <mas_o>
<mas_o> ::= o <condicion_y> <mas_o> | λ

<condicion_y> ::= <condicion_no> <mas_y>
<mas_y> ::= y <condicion_no> <mas_y> | λ

<condicion_no> ::= no <condicion_no> | <comparacion>

<comparacion> ::= <expresion> <cola_comparacion>
<cola_comparacion> ::= <operador_relacional> <expresion> | λ

# -----------------------------
# Bucles (repetir y mientras)
# -----------------------------
<bucle> ::= repetir <identificador> desde <expresion> hasta <expresion> { <bloque> }
          | mientras <condicion> { <bloque> }

# -----------------------------
# Expresiones aritméticas (sin recursión izquierda)
# -----------------------------
<expresion> ::= <termino> <suma_opcional>
<suma_opcional> ::= <op_suma> <termino> <suma_opcional> | λ

<termino> ::= <factor> <producto_opcional>
<producto_opcional> ::= <op_mul> <factor> <producto_opcional> | λ

<factor> ::= <numero>
           | <decimal>
           | <cadena>
           | <booleano>
           | ( <expresion> )
           | <identificador> <uso_variable>

<uso_variable> ::= ( <argumentos> )    # llamada a función
                 | λ                    # variable simple

<op_suma> ::= + | -
<op_mul>  ::= * | / | %

# -----------------------------
# Funciones
# -----------------------------
<definicion_funcion> ::= funcion <identificador> ( <parametros> ) : <tipo> { <bloque> retornar <expresion> }

<llamada_funcion> ::= <identificador> ( <argumentos> )

<parametros> ::= <lista_parametros> | λ
<lista_parametros> ::= <parametro> <parametros_extra>
<parametros_extra> ::= , <parametro> <parametros_extra> | λ
<parametro> ::= <identificador> : <tipo>

<argumentos> ::= <lista_argumentos> | λ
<lista_argumentos> ::= <expresion> <argumentos_extra>
<argumentos_extra> ::= , <expresion> <argumentos_extra> | λ

# -----------------------------
# Valores especiales de estado
# -----------------------------
<estado_valor> ::= "running" | "stopped" | "degraded" | "down"

# -----------------------------
# Léxico y operadores
# -----------------------------
<booleano> ::= verdadero | falso
<operador_relacional> ::= == | != | < | > | <= | >=

<numero> ::= <digito> { <digito> }
<decimal> ::= <numero> . <numero>
<cadena> ::= '"' { <caracter> } '"'
<identificador> ::= <letra> { <letra> | <digito> | _ }

<letra> ::= a | b | ... | z | A | B | ... | Z
<digito> ::= 0 | 1 | ... | 9

<comentario_linea> ::= "#" {cualquier_caracter_excepto_salto}
```
