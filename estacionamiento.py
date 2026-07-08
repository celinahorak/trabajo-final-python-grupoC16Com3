"""
Sistema de Gestión de Estacionamiento
Trabajo Final Integrador - Algoritmos y Estructuras de Datos - ISI 2026

Funcionalidades:
- Ingreso y egreso de vehículos
- Control de espacios disponibles (capacidad total configurable)
- Cálculo de tiempo de permanencia e importe a pagar
- Estadísticas: vehículos atendidos, tiempo promedio, recaudación total
- Persistencia del historial en archivo .txt (módulo Manejo de Archivos)
"""

from datetime import datetime

# ---------------------------------------------------------------------------
# CONFIGURACIÓN GENERAL (constantes fáciles de modificar)
# ---------------------------------------------------------------------------
CAPACIDAD_TOTAL = 20          # cantidad de espacios del estacionamiento
TARIFA_POR_HORA = 500         # pesos por hora (o fracción)
ARCHIVO_HISTORIAL = "historial_estacionamiento.txt"


# ---------------------------------------------------------------------------
# FUNCIONES DE VALIDACIÓN
# ---------------------------------------------------------------------------
def validar_patente(patente):
    """Valida que la patente no esté vacía y sea alfanumérica."""
    patente = patente.strip().upper()
    if patente == "":
        return False
    if not patente.isalnum():
        return False
    if len(patente) < 6:
        return False
    return True


def pedir_patente():
    """Pide la patente por consola hasta que sea válida (bucle + validación)."""
    while True:
        patente = input("Ingrese la patente del vehículo: ").strip().upper()
        if validar_patente(patente):
            return patente
        else:
            print("⚠ Patente inválida. Debe tener al menos 6 caracteres alfanuméricos, sin espacios.\n")


def pedir_opcion_menu():
    """Pide una opción numérica del menú, controlando errores de tipo."""
    while True:
        opcion = input("Seleccione una opción: ").strip()
        try:
            opcion = int(opcion)
            if 1 <= opcion <= 6:
                return opcion
            else:
                print("⚠ Ingrese un número entre 1 y 6.\n")
        except ValueError:
            print("⚠ Debe ingresar un número válido.\n")


# ---------------------------------------------------------------------------
# FUNCIONES PRINCIPALES DEL SISTEMA
# ---------------------------------------------------------------------------
def mostrar_menu():
    print("\n" + "=" * 45)
    print("      SISTEMA DE GESTIÓN DE ESTACIONAMIENTO")
    print("=" * 45)
    print("1. Ingresar vehículo")
    print("2. Registrar egreso de vehículo")
    print("3. Ver estado del estacionamiento")
    print("4. Ver estadísticas")
    print("5. Ver historial completo")
    print("6. Salir")
    print("=" * 45)


def ingresar_vehiculo(estacionamiento):
    """Registra el ingreso de un vehículo, validando espacio y duplicados."""
    if len(estacionamiento) >= CAPACIDAD_TOTAL:
        print("\n❌ No hay espacios disponibles en este momento.")
        return

    patente = pedir_patente()

    if patente in estacionamiento:
        print(f"\n❌ El vehículo con patente {patente} ya se encuentra dentro del estacionamiento.")
        return

    estacionamiento[patente] = datetime.now()
    print(f"\n✅ Vehículo {patente} ingresado correctamente a las "
          f"{estacionamiento[patente].strftime('%H:%M:%S')}.")


def calcular_importe(minutos):
    """Calcula el importe a pagar. Cobra por hora o fracción, con mínimo de 1 hora."""
    horas = minutos / 60
    horas_a_cobrar = int(horas) + (1 if horas % 1 > 0 else 0)
    if horas_a_cobrar == 0:
        horas_a_cobrar = 1  # mínimo 1 hora
    return horas_a_cobrar * TARIFA_POR_HORA


def egresar_vehiculo(estacionamiento, historial):
    """Registra el egreso, calcula tiempo e importe, y actualiza historial y archivo."""
    if len(estacionamiento) == 0:
        print("\n❌ No hay vehículos dentro del estacionamiento.")
        return

    patente = input("Ingrese la patente del vehículo que egresa: ").strip().upper()

    if patente not in estacionamiento:
        print(f"\n❌ No se encontró el vehículo con patente {patente} dentro del estacionamiento.")
        return

    hora_ingreso = estacionamiento[patente]
    hora_egreso = datetime.now()
    minutos = (hora_egreso - hora_ingreso).total_seconds() / 60
    importe = calcular_importe(minutos)

    # Se libera el espacio
    del estacionamiento[patente]

    # Se registra el movimiento en el historial (memoria) y en el archivo
    registro = {
        "patente": patente,
        "ingreso": hora_ingreso,
        "egreso": hora_egreso,
        "minutos": minutos,
        "importe": importe
    }
    historial.append(registro)
    guardar_movimiento(registro)

    print("\n🧾 TICKET DE SALIDA")
    print(f"Patente: {patente}")
    print(f"Ingreso: {hora_ingreso.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Egreso:  {hora_egreso.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Tiempo de permanencia: {minutos:.1f} minutos")
    print(f"Importe a pagar: ${importe}")


def mostrar_estado(estacionamiento):
    ocupados = len(estacionamiento)
    disponibles = CAPACIDAD_TOTAL - ocupados

    print("\n📊 ESTADO DEL ESTACIONAMIENTO")
    print(f"Capacidad total: {CAPACIDAD_TOTAL}")
    print(f"Espacios ocupados: {ocupados}")
    print(f"Espacios disponibles: {disponibles}")

    if ocupados > 0:
        print("\nVehículos actualmente dentro:")
        for patente, hora in estacionamiento.items():
            print(f" - {patente} (ingresó a las {hora.strftime('%H:%M:%S')})")
    else:
        print("\nNo hay vehículos dentro en este momento.")


def mostrar_estadisticas(historial):
    """Calcula estadísticas usando acumuladores y contadores."""
    if len(historial) == 0:
        print("\n📊 Todavía no se registraron egresos, no hay estadísticas disponibles.")
        return

    cantidad_vehiculos = 0
    total_minutos = 0
    total_recaudado = 0

    for registro in historial:
        cantidad_vehiculos += 1
        total_minutos += registro["minutos"]
        total_recaudado += registro["importe"]

    promedio_minutos = total_minutos / cantidad_vehiculos

    print("\n📊 ESTADÍSTICAS DEL ESTACIONAMIENTO")
    print(f"Vehículos atendidos (con egreso registrado): {cantidad_vehiculos}")
    print(f"Tiempo promedio de permanencia: {promedio_minutos:.1f} minutos")
    print(f"Recaudación total: ${total_recaudado}")


def mostrar_historial(historial):
    if len(historial) == 0:
        print("\n📊 No hay movimientos registrados todavía.")
        return

    print("\n📋 HISTORIAL COMPLETO DE MOVIMIENTOS")
    for registro in historial:
        print(f" - {registro['patente']} | "
              f"Ingreso: {registro['ingreso'].strftime('%d/%m/%Y %H:%M:%S')} | "
              f"Egreso: {registro['egreso'].strftime('%d/%m/%Y %H:%M:%S')} | "
              f"Importe: ${registro['importe']}")


# ---------------------------------------------------------------------------
# MANEJO DE ARCHIVOS (persistencia del historial entre ejecuciones)
# ---------------------------------------------------------------------------
def guardar_movimiento(registro):
    """Agrega una línea al archivo de historial (modo 'a' = agregar)."""
    try:
        with open(ARCHIVO_HISTORIAL, "a", encoding="utf-8") as archivo:
            linea = (f"{registro['patente']};"
                     f"{registro['ingreso'].strftime('%d/%m/%Y %H:%M:%S')};"
                     f"{registro['egreso'].strftime('%d/%m/%Y %H:%M:%S')};"
                     f"{registro['minutos']:.1f};"
                     f"{registro['importe']}\n")
            archivo.write(linea)
    except IOError:
        print("⚠ No se pudo guardar el movimiento en el archivo de historial.")


def cargar_historial():
    """Lee el archivo de historial al iniciar el programa, si existe."""
    historial = []
    try:
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea == "":
                    continue
                partes = linea.split(";")
                if len(partes) != 5:
                    continue  # línea con formato inválido, se ignora
                patente, ingreso_str, egreso_str, minutos_str, importe_str = partes
                registro = {
                    "patente": patente,
                    "ingreso": datetime.strptime(ingreso_str, "%d/%m/%Y %H:%M:%S"),
                    "egreso": datetime.strptime(egreso_str, "%d/%m/%Y %H:%M:%S"),
                    "minutos": float(minutos_str),
                    "importe": float(importe_str)
                }
                historial.append(registro)
        print(f"📂 Se cargaron {len(historial)} registros del historial previo.")
    except FileNotFoundError:
        # Es normal la primera vez que se ejecuta el programa
        print("📂 No se encontró historial previo. Se creará uno nuevo.")
    return historial


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------
def main():
    estacionamiento = {}          # vehículos actualmente adentro {patente: hora_ingreso}
    historial = cargar_historial()  # movimientos ya cerrados, cargados desde el archivo

    print("\n🚗 Bienvenido/a al Sistema de Gestión de Estacionamiento 🚗")

    continuar = True
    while continuar:
        mostrar_menu()
        opcion = pedir_opcion_menu()

        if opcion == 1:
            ingresar_vehiculo(estacionamiento)
        elif opcion == 2:
            egresar_vehiculo(estacionamiento, historial)
        elif opcion == 3:
            mostrar_estado(estacionamiento)
        elif opcion == 4:
            mostrar_estadisticas(historial)
        elif opcion == 5:
            mostrar_historial(historial)
        elif opcion == 6:
            print("\n👋 Gracias por usar el sistema. ¡Hasta luego!")
            continuar = False


if __name__ == "__main__":
    main()
