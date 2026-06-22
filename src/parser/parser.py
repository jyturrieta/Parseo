# parser.py
# Parser para el lenguaje Elysion usando PLY (yacc)
# Coherente con el scanner y la GIC definida para Elysion

import sys
import os

# Agregar el directorio src al path para importar el scanner
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import ply.yacc as yacc
from scanner.scanner import tokens, lexer

# ============================
# Precedencia de operadores
# ============================
# De menor a mayor precedencia (PLY resuelve de abajo hacia arriba)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL', 'IGUAL', 'DIFERENTE'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO', 'PORCENTAJE_SIMB'),
)

# ============================
# Programa principal
# ============================
def p_programa(p):
    '''programa : INICIO bloque FIN'''
    p[0] = ('programa', p[2])

# ============================
# Bloque (lista de sentencias)
# ============================
def p_bloque(p):
    '''bloque : sentencia bloque'''
    p[0] = [p[1]] + p[2]

def p_bloque_vacio(p):
    '''bloque : '''
    p[0] = []

# ============================
# Sentencias
# ============================
def p_sentencia(p):
    '''sentencia : declaracion
                 | asignacion
                 | condicional
                 | bucle_repetir
                 | bucle_mientras
                 | definicion_funcion
                 | io
                 | llamada_sentencia'''
    p[0] = p[1]

# ============================
# Declaración: identificador : tipo = expresion
# ============================
def p_declaracion(p):
    '''declaracion : ID DOS_PUNTOS tipo ASIGNACION expresion'''
    p[0] = ('declaracion', p[1], p[3], p[5])

# ============================
# Asignación: identificador = expresion
# ============================
def p_asignacion(p):
    '''asignacion : ID ASIGNACION expresion'''
    p[0] = ('asignacion', p[1], p[3])

# ============================
# Tipos de datos
# ============================
def p_tipo(p):
    '''tipo : RECURSO
            | PORCENTAJE
            | BYTES
            | SEGUNDOS
            | COMANDO
            | ESTADO
            | BOOLEANO
            | ENTERO
            | TEXTO'''
    p[0] = p[1]

# ============================
# Entrada / Salida del sistema (funciones built-in)
# ============================
def p_io_mostrar(p):
    '''io : MOSTRAR PAREN_IZQ expresion PAREN_DER'''
    p[0] = ('io', 'mostrar', p[3])

def p_io_mostrar_estado(p):
    '''io : MOSTRAR_ESTADO PAREN_IZQ PAREN_DER'''
    p[0] = ('io', 'mostrar_estado')

def p_io_registrar_alerta(p):
    '''io : REGISTRAR_ALERTA PAREN_IZQ expresion PAREN_DER'''
    p[0] = ('io', 'registrar_alerta', p[3])

def p_io_registrar_incidente(p):
    '''io : REGISTRAR_INCIDENTE PAREN_IZQ expresion PAREN_DER'''
    p[0] = ('io', 'registrar_incidente', p[3])

def p_io_ejecutar_comando(p):
    '''io : EJECUTAR_COMANDO PAREN_IZQ expresion PAREN_DER'''
    p[0] = ('io', 'ejecutar_comando', p[3])

def p_io_esperar(p):
    '''io : ESPERAR PAREN_IZQ expresion PAREN_DER'''
    p[0] = ('io', 'esperar', p[3])

def p_io_leer_metricas(p):
    '''io : LEER_METRICAS PAREN_IZQ expresion PAREN_DER'''
    p[0] = ('io', 'leer_metricas', p[3])

def p_io_exportar_log(p):
    '''io : EXPORTAR_LOG PAREN_IZQ expresion PAREN_DER'''
    p[0] = ('io', 'exportar_log', p[3])

# ============================
# Condicional: si / sino si / sino
# ============================
def p_condicional(p):
    '''condicional : SI expresion LLAVE_IZQ bloque LLAVE_DER cadena_sino'''
    p[0] = ('condicional', p[2], p[4], p[6])

def p_cadena_sino_si(p):
    '''cadena_sino : SINO SI expresion LLAVE_IZQ bloque LLAVE_DER cadena_sino'''
    p[0] = ('sino_si', p[3], p[5], p[7])

def p_cadena_sino(p):
    '''cadena_sino : SINO LLAVE_IZQ bloque LLAVE_DER'''
    p[0] = ('sino', p[3])

def p_cadena_sino_vacio(p):
    '''cadena_sino : '''
    p[0] = None

# ============================
# Bucle repetir: repetir id desde expr hasta expr { bloque }
# ============================
def p_bucle_repetir(p):
    '''bucle_repetir : REPETIR ID DESDE expresion HASTA expresion LLAVE_IZQ bloque LLAVE_DER'''
    p[0] = ('repetir', p[2], p[4], p[6], p[8])

# ============================
# Bucle mientras: mientras expresion { bloque }
# ============================
def p_bucle_mientras(p):
    '''bucle_mientras : MIENTRAS expresion LLAVE_IZQ bloque LLAVE_DER'''
    p[0] = ('mientras', p[2], p[4])

# ============================
# Nombre de función (ID o built-in reutilizable)
# ============================
def p_nombre_funcion(p):
    '''nombre_funcion : ID
                      | OBTENER_USO_CPU
                      | OBTENER_MEMORIA_LIBRE
                      | OBTENER_USO_DISCO
                      | OBTENER_USO_MEMORIA
                      | ESTADO_SERVICIO
                      | EJECUTAR_COMANDO
                      | REGISTRAR_ALERTA
                      | REGISTRAR_INCIDENTE
                      | MOSTRAR
                      | ESPERAR
                      | LEER_METRICAS
                      | EXPORTAR_LOG
                      | FORMATEAR_BYTES
                      | VERIFICAR_DISCO
                      | GENERAR_REPORTE_SISTEMA
                      | MOSTRAR_ESTADO'''
    p[0] = p[1]

# ============================
# Definición de función
# ============================
def p_definicion_funcion(p):
    '''definicion_funcion : FUNCION nombre_funcion PAREN_IZQ parametros PAREN_DER DOS_PUNTOS tipo LLAVE_IZQ bloque RETORNAR expresion LLAVE_DER'''
    p[0] = ('funcion', p[2], p[4], p[7], p[9], p[11])

# ============================
# Parámetros de función
# ============================
def p_parametros(p):
    '''parametros : lista_parametros'''
    p[0] = p[1]

def p_parametros_vacio(p):
    '''parametros : '''
    p[0] = []

def p_lista_parametros(p):
    '''lista_parametros : parametro COMA lista_parametros'''
    p[0] = [p[1]] + p[3]

def p_lista_parametros_unico(p):
    '''lista_parametros : parametro'''
    p[0] = [p[1]]

def p_parametro(p):
    '''parametro : ID DOS_PUNTOS tipo'''
    p[0] = ('parametro', p[1], p[3])

# ============================
# Llamada a función como sentencia
# ============================
def p_llamada_sentencia(p):
    '''llamada_sentencia : nombre_funcion PAREN_IZQ argumentos PAREN_DER'''
    p[0] = ('llamada', p[1], p[3])

# ============================
# Argumentos de llamada
# ============================
def p_argumentos(p):
    '''argumentos : lista_argumentos'''
    p[0] = p[1]

def p_argumentos_vacio(p):
    '''argumentos : '''
    p[0] = []

def p_lista_argumentos(p):
    '''lista_argumentos : expresion COMA lista_argumentos'''
    p[0] = [p[1]] + p[3]

def p_lista_argumentos_unico(p):
    '''lista_argumentos : expresion'''
    p[0] = [p[1]]

# ============================
# Expresiones
# ============================

# --- Operadores lógicos ---
def p_expresion_or(p):
    '''expresion : expresion OR expresion'''
    p[0] = ('or', p[1], p[3])

def p_expresion_and(p):
    '''expresion : expresion AND expresion'''
    p[0] = ('and', p[1], p[3])

def p_expresion_not(p):
    '''expresion : NOT expresion'''
    p[0] = ('not', p[2])

# --- Operadores relacionales ---
def p_expresion_mayor(p):
    '''expresion : expresion MAYOR expresion'''
    p[0] = ('>', p[1], p[3])

def p_expresion_menor(p):
    '''expresion : expresion MENOR expresion'''
    p[0] = ('<', p[1], p[3])

def p_expresion_mayor_igual(p):
    '''expresion : expresion MAYOR_IGUAL expresion'''
    p[0] = ('>=', p[1], p[3])

def p_expresion_menor_igual(p):
    '''expresion : expresion MENOR_IGUAL expresion'''
    p[0] = ('<=', p[1], p[3])

def p_expresion_igual(p):
    '''expresion : expresion IGUAL expresion'''
    p[0] = ('==', p[1], p[3])

def p_expresion_diferente(p):
    '''expresion : expresion DIFERENTE expresion'''
    p[0] = ('!=', p[1], p[3])

# --- Operadores aritméticos ---
def p_expresion_suma(p):
    '''expresion : expresion MAS expresion'''
    p[0] = ('+', p[1], p[3])

def p_expresion_resta(p):
    '''expresion : expresion MENOS expresion'''
    p[0] = ('-', p[1], p[3])

def p_expresion_multiplicacion(p):
    '''expresion : expresion POR expresion'''
    p[0] = ('*', p[1], p[3])

def p_expresion_division(p):
    '''expresion : expresion DIVIDIDO expresion'''
    p[0] = ('/', p[1], p[3])

def p_expresion_modulo(p):
    '''expresion : expresion PORCENTAJE_SIMB expresion'''
    p[0] = ('%', p[1], p[3])

# --- Agrupación con paréntesis ---
def p_expresion_paren(p):
    '''expresion : PAREN_IZQ expresion PAREN_DER'''
    p[0] = p[2]

# --- Llamada a función como expresión ---
def p_expresion_llamada_builtin_obtener_uso_cpu(p):
    '''expresion : OBTENER_USO_CPU PAREN_IZQ argumentos PAREN_DER'''
    p[0] = ('llamada', 'obtener_uso_cpu', p[3])

def p_expresion_llamada_builtin_obtener_memoria_libre(p):
    '''expresion : OBTENER_MEMORIA_LIBRE PAREN_IZQ argumentos PAREN_DER'''
    p[0] = ('llamada', 'obtener_memoria_libre', p[3])

def p_expresion_llamada_builtin_obtener_uso_disco(p):
    '''expresion : OBTENER_USO_DISCO PAREN_IZQ argumentos PAREN_DER'''
    p[0] = ('llamada', 'obtener_uso_disco', p[3])

def p_expresion_llamada_builtin_obtener_uso_memoria(p):
    '''expresion : OBTENER_USO_MEMORIA PAREN_IZQ argumentos PAREN_DER'''
    p[0] = ('llamada', 'obtener_uso_memoria', p[3])

def p_expresion_llamada_builtin_estado_servicio(p):
    '''expresion : ESTADO_SERVICIO PAREN_IZQ argumentos PAREN_DER'''
    p[0] = ('llamada', 'estado_servicio', p[3])

def p_expresion_llamada_builtin_formatear_bytes(p):
    '''expresion : FORMATEAR_BYTES PAREN_IZQ argumentos PAREN_DER'''
    p[0] = ('llamada', 'formatear_bytes', p[3])

def p_expresion_llamada_builtin_verificar_disco(p):
    '''expresion : VERIFICAR_DISCO PAREN_IZQ argumentos PAREN_DER'''
    p[0] = ('llamada', 'verificar_disco', p[3])

def p_expresion_llamada_builtin_generar_reporte(p):
    '''expresion : GENERAR_REPORTE_SISTEMA PAREN_IZQ argumentos PAREN_DER'''
    p[0] = ('llamada', 'generar_reporte_sistema', p[3])

def p_expresion_llamada_id(p):
    '''expresion : ID PAREN_IZQ argumentos PAREN_DER'''
    p[0] = ('llamada', p[1], p[3])

# --- Valores literales ---
def p_expresion_numero(p):
    '''expresion : NUMERO'''
    p[0] = ('numero', p[1])

def p_expresion_decimal(p):
    '''expresion : DECIMAL'''
    p[0] = ('decimal', p[1])

def p_expresion_cadena(p):
    '''expresion : CADENA'''
    p[0] = ('cadena', p[1])

def p_expresion_verdadero(p):
    '''expresion : VERDADERO'''
    p[0] = ('booleano', True)

def p_expresion_falso(p):
    '''expresion : FALSO'''
    p[0] = ('booleano', False)

# --- Identificador (variable) ---
def p_expresion_id(p):
    '''expresion : ID'''
    p[0] = ('id', p[1])

# ============================
# Manejo de errores sintácticos
# ============================
def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' (token {p.type}) en la línea {p.lineno}")
    else:
        print("Error de sintaxis: fin de archivo inesperado")

# ============================
# Construir el parser
# ============================
parser = yacc.yacc()

# ============================
# Función para parsear código Elysion
# ============================
def parse(data):
    """Parsea código Elysion y retorna el AST."""
    lexer.lineno = 1
    result = parser.parse(data, lexer=lexer)
    return result

def print_ast(node, indent=0):
    """Imprime el AST de forma legible."""
    prefix = "  " * indent
    if isinstance(node, tuple):
        print(f"{prefix}{node[0]}")
        for child in node[1:]:
            print_ast(child, indent + 1)
    elif isinstance(node, list):
        for item in node:
            print_ast(item, indent)
    else:
        print(f"{prefix}{node}")

# ============================
# Ejemplo de uso
# ============================
if __name__ == '__main__':
    data = '''
    inicio

    umbral_cpu: porcentaje = 80.0
    umbral_memoria: bytes = 1073741824
    tiempo_check: segundos = 300

    repetir chequeo desde 1 hasta 10 {
        estado_cpu: porcentaje = obtener_uso_cpu()
        estado_mem: bytes = obtener_memoria_libre()

        si estado_cpu > umbral_cpu {
            registrar_alerta("CPU sobrecargada: " + estado_cpu + "%")
        }

        esperar(tiempo_check)
    }

    si estado_servicio("nginx") == "down" {
        ejecutar_comando("systemctl start nginx")
        registrar_incidente("nginx reiniciado automáticamente")
    } sino si estado_servicio("nginx") == "degraded" {
        mostrar("Nginx en estado degradado")
    } sino {
        mostrar("Nginx funcionando correctamente")
    }

    funcion verificar_disco(path: texto, umbral: porcentaje): booleano {
        uso_actual: porcentaje = obtener_uso_disco(path)
        retornar uso_actual > umbral
    }

    disco_lleno: booleano = verificar_disco("/", 90.0)
    si disco_lleno {
        mostrar("Disco lleno - ejecutar limpieza")
    }

    reporte: texto = generar_reporte_sistema()
    exportar_log("monitoreo_final.log")
    mostrar("Monitoreo completado")

    fin
    '''

    print("=== PARSING ELYSION ===\n")
    result = parse(data)

    if result:
        print("Parsing exitoso!\n")
        print("=== AST ===\n")
        print_ast(result)
    else:
        print("Error en el parsing.")
