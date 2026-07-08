# Trabajo Final Integrador - Laboratorio de Python

## Sistema de Gestión de Estacionamiento

### Materia
Algoritmos y Estructuras de Datos

### Carrera
Ingeniería en Sistemas de Información (ISI)

### Comisión
Comisión 3

---

## Integrantes del grupo

- Horak Celina 
- Deydar Lautaro Agustin 
- Ruiz Leiva Lourdes Soledad 
- Torres Ocampo Franco 
- Pared Priscila Siomara 

---

## Presentación del Proyecto 

Este proyecto fue desarrollado como Trabajo Final Integrador de la materia Algoritmos y Estructuras de Datos. El objetivo fue aplicar los contenidos vistos durante el cursado mediante la implementación de un sistema de gestión de estacionamiento utilizando Python.

## Descripción general del sistema 

El sistema gestiona el funcionamiento de un estacionamiento a través de una aplicación de consola desarrollada en Python. Permite:

- Registrar el **ingreso** de vehículos, validando la patente ingresada y controlando que exista espacio disponible.
- Registrar el **egreso** de vehículos, calculando automáticamente el tiempo de permanencia y el importe a pagar según una tarifa por hora.
- Consultar el **estado actual** del estacionamiento (espacios ocupados y disponibles, vehículos dentro).
- Consultar **estadísticas** generales: cantidad de vehículos atendidos, tiempo promedio de permanencia y recaudación total.
- Consultar el **historial completo** de movimientos.

Todos los movimientos de egreso se guardan en un archivo de texto (`historial_estacionamiento.txt`), que se lee automáticamente cada vez que se inicia el programa, de modo que la información persiste entre ejecuciones.

---

## Funcionalidades

- Registro de ingreso de vehículos.
- Registro de egreso de vehículos.
- Cálculo del tiempo de permanencia.
- Cálculo automático del importe a pagar.
- Control de espacios disponibles.
- Consulta de estadísticas generales.
- Validación de datos ingresados por el usuario.
- Mensajes de error para mejorar la interacción con el usuario.

---

## Tecnologías utilizadas

- Python 3.8
- Git
- GitHub
- Visual Studio Code

---

## Estructura del proyecto

```
trabajo-final-python-grupoC16Com3
│
├── estacionamiento.py
├── README.md
└── DOCUMENTACION.md
```

---

## Instrucciones de ejecución

### Requisitos

- Python 3.8 o superior instalado (no requiere librerías externas ni instalación con `pip`).

### Pasos

1. Clonar o descargar este repositorio.
2. Abrir una terminal y ubicarse en la carpeta del proyecto:

   cd ruta/a/la/carpeta/del/proyecto
   
3. Ejecutar el programa:
   - En Windows:

     py estacionamiento.py
   
   - En Linux/Mac:
     
     python3 estacionamiento.py
     
4. Utilizar el menú numérico que aparece en pantalla para interactuar con el sistema (ingresar vehículo, registrar egreso, ver estado, ver estadísticas, ver historial, salir).

El archivo `historial_estacionamiento.txt` se genera automáticamente en la misma carpeta la primera vez que se registra un egreso. No es necesario crearlo manualmente.


---

## Uso de Inteligencia Artificial

Durante el desarrollo del proyecto se utilizó ChatGPT (OpenAI) y Claude (Anthropic) como herramienta de apoyo para:

- Resolver dudas relacionadas con la sintaxis de Python.
- Analizar y corregir errores del código.
- Proponer mejoras en la organización del programa.
- Colaborar en la documentación del proyecto.
- Explicar conceptos de programación necesarios para comprender la solución implementada.

---

## Repositorio GitHub

https://github.com/celinahorak/trabajo-final-python-grupoC16Com3.git

---

## Video de demostración

https://youtu.be/Vyjsi4NDLXs

---

## Documentación técnica

Ver el archivo [`DOCUMENTACION.md`](./DOCUMENTACION.md) para una explicación detallada del código, función por función.

---

## Observaciones

Este proyecto fue desarrollado como Trabajo Final Integrador de la asignatura Algoritmos y Estructuras de Datos, siguiendo los requisitos establecidos por la cátedra para el ciclo lectivo 2026.
