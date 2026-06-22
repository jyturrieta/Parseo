## 🎯 Objetivo
**Elysion** es un lenguaje de dominio específico diseñado para monitoreo y administración básica de sistemas informáticos. Su sintaxis es clara y expresiva, pensada para facilitar la supervisión de recursos y la automatización de tareas administrativas simples.

## 🧠 Filosofía
- Sintaxis intuitiva para operaciones de system administration.

- Tipado estático para prevenir errores en gestión de recursos.

- Control de flujo estructurado para scripts de automatización.

- Inspirado en comandos de shell y herramientas de monitoring.

- Se ejecuta entre inicio y fin.

---

## 🎯 Dominio Específico y Alcance
##### Dominio: 
Monitoreo y administración básica de sistemas.

##### Alcance:

- Permite monitorear recursos del sistema (CPU, memoria, disco, red).

- Soporta ejecución de comandos básicos del sistema operativo.

- Implementa checks de estado y alertas condicionales.

- Gestiona logs y reportes de sistema.

- No soporta administración de usuarios ni permisos avanzados.

- No interactúa con bases de datos ni servicios enterprise.

- Ejecución local con enfoque en aprendizaje conceptual.

## 🔠 Tipos de Datos
    recurso, porcentaje, bytes, segundos, comando, estado, booleano, entero

Ejemplos:

``` Elysion
cpu_usage: porcentaje = 25.5
memoria_libre: bytes = 4096000000
tiempo_activo: segundos = 86400
servicio_web: estado = "running"
check_disk: comando = "df -h"
critico: booleano = falso
intentos: entero = 0
```
---
## 🔧 Asignación y Monitoreo
``` Elysion
umbral_cpu: porcentaje = 80.0
umbral_memoria: bytes = 1073741824  # 1GB
tiempo_check: segundos = 300
```

Reasignación:

``` Elysion
umbral_cpu = 85.0
critico = verdadero
```
---

## 🔁 Bucles para Monitoreo Continuo
```Elysion
repetir chequeo desde 1 hasta 10 {
  estado_cpu: porcentaje = obtener_uso_cpu()
  estado_mem: bytes = obtener_memoria_libre()
  
  si estado_cpu > umbral_cpu {
    registrar_alerta("CPU sobrecargada: " + estado_cpu + "%")
  }
  
  esperar(tiempo_check)
}

```

## 🔀 Condicionales de Alertas

``` Elysion
si estado_servicio("nginx") == "down" {
  ejecutar_comando("systemctl start nginx")
  registrar_incidente("nginx reiniciado automáticamente")
} sino si estado_servicio("nginx") == "degraded" {
  mostrar("⚠️  Nginx en estado degradado - revisar logs")
} sino {
  mostrar("✅ Nginx funcionando correctamente")
}
```
---

## ✨ Funciones de Administración


```Elysion
funcion verificar_disco(path: texto, umbral: porcentaje): booleano {
  uso_actual: porcentaje = obtener_uso_disco(path)
  retornar uso_actual > umbral
}

funcion generar_reporte_sistema(): texto {
  reporte: texto = "Reporte del Sistema:\n"
  reporte = reporte + "CPU: " + obtener_uso_cpu() + "%\n"
  reporte = reporte + "Memoria libre: " + formatear_bytes(obtener_memoria_libre()) + "\n"
  retornar reporte
}
```

Llamada:

```Elysion
disco_lleno: booleano = verificar_disco("/", 90.0)
reporte: texto = generar_reporte_sistema()
```
--- 

## 📊 Entrada / Salida del Sistema
```Elysion
leer_metricas_desde_archivo("/proc/meminfo")
mostrar_estado_sistema()
exportar_log("system_check.log")
ejecutar_comando("apt update")
```
---

## 📐 BNF (Fragmento Actualizado)
```bnf
<programa> ::= inicio <bloques>* fin

<bloques> ::= <declaracion> | <asignacion> | <condicional> | <bucle> | <funcion> | <llamada> | <io>

<declaracion> ::= <identificador>: <tipo> = <expresion>
<asignacion> ::= <identificador> = <expresion>

<condicional> ::= si <expresion> { <bloques>* } (sino si <expresion> { <bloques>* })* (sino { <bloques>* })?

<bucle> ::= repetir <identificador> desde <expresion> hasta <expresion> { <bloques>* }
          | mientras <expresion> { <bloques>* }

<funcion> ::= funcion <identificador>(<parametros>?) : <tipo> { <bloques>* retornar <expresion> }

<io> ::= leer_metricas(<cadena>) | mostrar_estado() | exportar_log(<cadena>) | ejecutar_comando(<cadena>)

<expresion> ::= <expresion> <operador> <expresion>
              | ( <expresion> )
              | <valor>
              | <identificador>
              | <llamada_funcion>

<valor> ::= <numero> | <cadena> | verdadero | falso | <porcentaje> | <bytes>

<porcentaje> ::= <numero>.<numero>
<bytes> ::= <numero>
<segundos> ::= <numero>

<tipo> ::= recurso | porcentaje | bytes | segundos | comando | estado | booleano | entero | texto

<estado> ::= "running" | "stopped" | "degraded" | "down"

<operador> ::= > | < | >= | <= | == | != 
             | y | o | no

<llamada_funcion> ::= <identificador>(<argumentos>?)

<argumentos> ::= <expresion> (, <argumentos>)*

```

---


## 🛠️ Ejemplo de Script de Monitoreo
```Elysion
inicio

// Configuración de umbrales
umbral_cpu: porcentaje = 85.0
umbral_memoria: porcentaje = 90.0
umbral_disco: porcentaje = 80.0
intervalo: segundos = 60

// Servicios críticos a monitorear
servicios: texto[] = ["nginx", "mysql", "ssh"]

mostrar("🚀 Iniciando monitoreo del sistema...")

repetir ciclo desde 1 hasta 12 {  // Monitorear por 12 ciclos (12 minutos)
  
  // Check de CPU
  cpu_actual: porcentaje = obtener_uso_cpu()
  si cpu_actual > umbral_cpu {
    registrar_alerta("ALTA CPU: " + cpu_actual + "%")
  }
  
  // Check de memoria
  mem_actual: porcentaje = obtener_uso_memoria()
  si mem_actual > umbral_memoria {
    registrar_alerta("ALTA MEMORIA: " + mem_actual + "%")
  }
  
  // Check de servicios
  para cada servicio en servicios {
    estado_actual: estado = estado_servicio(servicio)
    si estado_actual != "running" {
      ejecutar_comando("systemctl restart " + servicio)
      registrar_incidente(servicio + " reiniciado")
    }
  }
  
  // Check de disco
  disco_lleno: booleano = verificar_disco("/", umbral_disco)
  si disco_lleno {
    ejecutar_comando("rm -f /tmp/*.tmp")
    mostrar("🧹 Limpieza de archivos temporales realizada")
  }
  
  // Esperar para próximo check
  esperar(intervalo)
}

// Generar reporte final
reporte: texto = generar_reporte_sistema()
exportar_log("monitoreo_final.log")
mostrar("✅ Monitoreo completado - Reporte guardado")

fin
```
---

## 📊 Características Técnicas
| Aspecto	| Descripción |
| --------- | ----------- |
| Dominio	| Monitoreo y administración básica de sistemas |
| Paradigma	| Imperativo, estructurado |
| Tipado	| Estático |
| Ejecución	| Local (simulación de comandos de sistema) |
| Persistencia	| Archivos de log y reportes

--- 

## ⚠️ Consideraciones
- Elysion simula operaciones de sistema para fines educativos.
- Los comandos se ejecutan en un entorno simulado/seguro.
- No realiza operaciones reales que puedan afectar el sistema.
- Ideal para aprender parsing con un dominio técnico relevante.
