# Documentación técnica - Sistema de Gestión de Estacionamiento

Este documento explica en detalle el funcionamiento del archivo `estacionamiento.py`, bloque por bloque, y cómo cada parte del código responde a los contenidos pedidos en el Trabajo Final Integrador (condicionales, iterativas, funciones, validaciones, acumuladores/contadores, modularización, manejo de errores y manejo de archivos).

---

## 1. Estructura general del programa

El sistema se organiza en **cinco grandes bloques**:

1. **Configuración general**: constantes del sistema.
2. **Funciones de validación**: controlan los datos que ingresa el usuario.
3. **Funciones principales**: implementan cada operación del estacionamiento (ingreso, egreso, estado, estadísticas, historial).
4. **Manejo de archivos**: guardan y recuperan el historial en un `.txt`.
5. **Programa principal (`main`)**: contiene el menú y el bucle de ejecución.

Esta separación en funciones es la **modularización** pedida en el enunciado: cada función resuelve una única responsabilidad, en lugar de tener todo el código en un solo bloque.

---

## 2. Configuración general

```python
CAPACIDAD_TOTAL = 20
TARIFA_POR_HORA = 500
ARCHIVO_HISTORIAL = "historial_estacionamiento.txt"
```

Son **constantes** (se escriben en mayúsculas por convención) que definen los parámetros del negocio: cuántos espacios tiene el estacionamiento, cuánto se cobra por hora, y el nombre del archivo donde se guarda el historial. Están arriba de todo para que se puedan modificar fácilmente sin tocar el resto del código.

---

## 3. Funciones de validación

### `validar_patente(patente)`

Corresponde a la **validación de datos ingresados** pedida en el enunciado (guía teórica de Condicionales). Devuelve `True` o `False` según si la patente:

- No está vacía.
- Es alfanumérica (`isalnum()`).
- Tiene al menos 6 caracteres.

Usa **condicionales** (`if`) para ir descartando casos inválidos.

### `pedir_patente()`

Implementa un **bucle de validación** (`while True`): le sigue pidiendo la patente al usuario hasta que `validar_patente()` devuelva `True`. Es el patrón típico visto en la guía de estructuras repetitivas: "repetir mientras el dato no sea válido".

### `pedir_opcion_menu()`

Controla que la opción elegida en el menú sea un número entero entre 1 y 6. Usa:

- **`try/except ValueError`**: si el usuario escribe una letra en vez de un número, `int()` lanza una excepción que el programa captura en vez de romperse (esto es el **manejo de errores** pedido en el enunciado, visto en la guía teórica correspondiente).
- Un **condicional** para verificar que el número esté en el rango permitido.
- Un **bucle `while True`** para volver a preguntar si el dato no es válido.

---

## 4. Funciones principales

### `mostrar_menu()`

Solo imprime las opciones por pantalla. No recibe ni devuelve nada; su única responsabilidad es mostrar información.

### `ingresar_vehiculo(estacionamiento)`

Recibe el diccionario `estacionamiento` (que representa los vehículos que están adentro en este momento) y:

1. Con un **condicional**, verifica si ya se llegó a `CAPACIDAD_TOTAL` (no hay lugar).
2. Pide y valida la patente con `pedir_patente()`.
3. Con otro **condicional**, verifica que esa patente no esté ya registrada (para no duplicar un mismo vehículo).
4. Si todo está bien, guarda la hora actual (`datetime.now()`) como valor asociado a esa patente en el diccionario.

El diccionario `estacionamiento` funciona como una tabla `patente → hora_de_ingreso`.

### `calcular_importe(minutos)`

Función que **recibe un parámetro y devuelve un valor** (no imprime nada, solo calcula). Convierte los minutos de permanencia en horas, redondea hacia arriba si hay una fracción de hora (`horas % 1 > 0`), y aplica un mínimo de una hora de cobro. Después multiplica por `TARIFA_POR_HORA`.

Esta separación (una función que solo calcula, sin mezclar entrada/salida de datos) es buena práctica de modularización: se puede probar y reutilizar de forma independiente.

### `egresar_vehiculo(estacionamiento, historial)`

Es la función más completa del sistema. Combina:

- **Condicionales**: si no hay vehículos adentro, o si la patente no está registrada, se avisa con un mensaje y se corta la función (`return`).
- Cálculo del tiempo transcurrido con `datetime`, restando la hora de ingreso a la hora de egreso.
- Llamado a `calcular_importe()` (reutilización de funciones).
- Actualización del diccionario `estacionamiento` (se elimina la patente con `del`, liberando el espacio).
- Se arma un **diccionario `registro`** con todos los datos del movimiento, se agrega a la lista `historial` (**acumulador** de datos históricos) y se guarda en el archivo con `guardar_movimiento()`.
- Se imprime el "ticket" final con toda la información.

### `mostrar_estado(estacionamiento)`

Calcula ocupados y disponibles a partir de `len(estacionamiento)`, y con una **estructura repetitiva (`for`)** recorre el diccionario para listar cada patente que está adentro junto con su hora de ingreso.

### `mostrar_estadisticas(historial)`

Es el ejemplo más claro de **acumuladores y contadores** pedidos en el enunciado:

```python
cantidad_vehiculos = 0
total_minutos = 0
total_recaudado = 0

for registro in historial:
    cantidad_vehiculos += 1
    total_minutos += registro["minutos"]
    total_recaudado += registro["importe"]
```

- `cantidad_vehiculos` es un **contador** (suma 1 en cada vuelta del bucle).
- `total_minutos` y `total_recaudado` son **acumuladores** (van sumando valores en cada vuelta).

Después se calcula el promedio dividiendo el acumulador de minutos por el contador de vehículos.

### `mostrar_historial(historial)`

Recorre con un `for` toda la lista de movimientos cerrados y los imprime uno por uno, mostrando el detalle completo de cada operación.

---

## 5. Manejo de archivos

Esta parte del sistema responde directamente a la guía teórica de **Manejo de Archivos (Módulo 4)**.

### `guardar_movimiento(registro)`

Abre el archivo en **modo `"a"` (append/agregar)**, para no borrar lo que ya había, y agrega una línea nueva por cada egreso registrado. Los datos se separan con `;` para poder volver a leerlos fácilmente después (formato tipo CSV simple).

Está envuelto en un **`try/except IOError`**: si por algún motivo no se puede escribir en el archivo (por ejemplo, problemas de permisos), el programa avisa con un mensaje en vez de romperse.

### `cargar_historial()`

Se ejecuta **una sola vez, al iniciar el programa**, dentro de `main()`. Intenta abrir el archivo en **modo `"r"` (lectura)**:

- Si el archivo **no existe todavía** (primera vez que se corre el programa), se captura la excepción `FileNotFoundError` y se empieza con un historial vacío, sin que el programa falle.
- Si el archivo existe, se lee línea por línea con un `for`, se separa cada línea por `;` con `.split(";")`, se reconstruyen los tipos de datos originales (`datetime.strptime()` para las fechas, `float()` para los números) y se arma de nuevo la lista `historial` tal como estaba antes de cerrar el programa.

Esto es lo que le da **persistencia** al sistema: los datos no se pierden al cerrar la consola.

---

## 6. Programa principal (`main`)

```python
def main():
    estacionamiento = {}
    historial = cargar_historial()

    continuar = True
    while continuar:
        mostrar_menu()
        opcion = pedir_opcion_menu()
        ...
```

- `estacionamiento` arranca vacío en cada ejecución (representa quién está *físicamente* adentro ahora, tiene sentido que se reinicie).
- `historial` se recupera del archivo con `cargar_historial()`.
- El **bucle `while continuar`** es el corazón del programa: se repite indefinidamente mostrando el menú, hasta que el usuario elige la opción 6 y se cambia `continuar` a `False`.
- Dentro del bucle, una cadena de **condicionales (`if/elif`)** decide qué función ejecutar según la opción elegida.

---

## 7. Relación con los contenidos pedidos en el enunciado

| Requisito del enunciado | Dónde está implementado |
|---|---|
| Estructuras condicionales | `if/elif` en casi todas las funciones (validaciones, menú, control de espacio) |
| Estructuras repetitivas | `while True` en `pedir_patente()` y `pedir_opcion_menu()`, `while continuar` en `main()`, `for` en `mostrar_estado()`, `mostrar_estadisticas()`, `mostrar_historial()`, `cargar_historial()` |
| Funciones | Todo el programa está modularizado en funciones con una responsabilidad cada una |
| Validaciones | `validar_patente()`, `pedir_patente()`, `pedir_opcion_menu()` |
| Acumuladores y contadores | `mostrar_estadisticas()`: `cantidad_vehiculos`, `total_minutos`, `total_recaudado` |
| Modularización básica | Separación en bloques: configuración, validación, funciones principales, archivos, `main` |
| Manejo de errores | `try/except ValueError` (opción de menú), `try/except IOError` (guardado), `try/except FileNotFoundError` (lectura inicial) |
| Manejo de archivos (Módulo 4) | `guardar_movimiento()` y `cargar_historial()`, usando `open()` en modos `"a"` y `"r"` |

---

## 8. Posibles mejoras a futuro

Ideas para justificar en el coloquio si preguntan "¿qué mejorarían?":

- Diferenciar tarifas según tipo de vehículo (auto, moto, camioneta).
- Agregar un sistema de reservas o abonos mensuales.
- Exportar estadísticas por rango de fechas.
- Migrar la persistencia de `.txt` a una base de datos simple (por ejemplo, `sqlite3`) o a formato JSON, para facilitar la lectura de datos más complejos.
