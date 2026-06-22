# scanner.py
import ply.lex as lex

# Palabras reservadas
reserved = {
    'inicio': 'INICIO',
    'fin': 'FIN',
    'si': 'SI',
    'sino': 'SINO',
    'repetir': 'REPETIR',
    'desde': 'DESDE',
    'hasta': 'HASTA',
    'mientras': 'MIENTRAS',
    'funcion': 'FUNCION',
    'retornar': 'RETORNAR',
    'verdadero': 'VERDADERO',
    'falso': 'FALSO',
    'porcentaje': 'PORCENTAJE',
    'bytes': 'BYTES',
    'segundos': 'SEGUNDOS',
    'comando': 'COMANDO',
    'estado': 'ESTADO',
    'booleano': 'BOOLEANO',
    'entero': 'ENTERO',
    'texto': 'TEXTO',
    'recurso': 'RECURSO',
    'obtener_uso_cpu': 'OBTENER_USO_CPU',
    'obtener_memoria_libre': 'OBTENER_MEMORIA_LIBRE',
    'obtener_uso_disco': 'OBTENER_USO_DISCO',
    'obtener_uso_memoria': 'OBTENER_USO_MEMORIA',
    'estado_servicio': 'ESTADO_SERVICIO',
    'ejecutar_comando': 'EJECUTAR_COMANDO',
    'registrar_alerta': 'REGISTRAR_ALERTA',
    'registrar_incidente': 'REGISTRAR_INCIDENTE',
    'mostrar': 'MOSTRAR',
    'esperar': 'ESPERAR',
    'leer_metricas': 'LEER_METRICAS',
    'exportar_log': 'EXPORTAR_LOG',
    'formatear_bytes': 'FORMATEAR_BYTES',
    'verificar_disco': 'VERIFICAR_DISCO',
    'generar_reporte_sistema': 'GENERAR_REPORTE_SISTEMA',
    'mostrar_estado': 'MOSTRAR_ESTADO'
}

# Lista de tokens
tokens = [
    'ID', 'NUMERO', 'DECIMAL', 'CADENA', 'COMENTARIO',
    'MAS', 'MENOS', 'POR', 'DIVIDIDO', 'PORCENTAJE_SIMB',
    'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL', 
    'IGUAL', 'DIFERENTE', 'ASIGNACION',
    'AND', 'OR', 'NOT',
    'PAREN_IZQ', 'PAREN_DER', 'LLAVE_IZQ', 'LLAVE_DER',
    'CORCHETE_IZQ', 'CORCHETE_DER', 'COMA', 'PUNTO_COMA',
    'DOS_PUNTOS'
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_PORCENTAJE_SIMB = r'%'

t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_IGUAL = r'=='
t_DIFERENTE = r'!='
t_ASIGNACION = r'='

t_AND = r'y'
t_OR = r'o'
t_NOT = r'no'

t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_COMA = r','
t_PUNTO_COMA = r';'
t_DOS_PUNTOS = r':'

# Expresión regular para identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Expresión regular para números decimales
def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Expresión regular para números enteros
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Expresión regular para cadenas de texto
def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove the quotes
    return t

# Expresión regular para comentarios
def t_COMENTARIO(t):
    r'\#.*'
    pass  # Los comentarios se ignoran

# Caracteres a ignorar (espacios y tabs)
t_ignore = ' \t'

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Función para probar el scanner
def test_scanner(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

# Ejemplo de uso
if __name__ == '__main__':
    data = '''
    inicio
    umbral_cpu: porcentaje = 80.0
    umbral_memoria: bytes = 1073741824
    
    repetir chequeo desde 1 hasta 10 {
        estado_cpu: porcentaje = obtener_uso_cpu()
        si estado_cpu > umbral_cpu {
            registrar_alerta("CPU sobrecargada: " + estado_cpu + "%")
        }
        esperar(300)
    }
    fin
    '''
    
    print("=== TESTING SCANNER ===")
    test_scanner(data)