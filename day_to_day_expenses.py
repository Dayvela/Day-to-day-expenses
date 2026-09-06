import json
import os
from datetime import datetime, timedelta

# ============================================================
# DAY TO DAY EXPENSES
# ============================================================

# Colores ANSI
ROSA = "\033[38;5;213m"
AZUL_MARINO = "\033[48;5;17m"
BLANCO = "\033[97m"
ROSA_FONDO = "\033[48;5;17m\033[38;5;213m"
RESET = "\033[0m"
NEGRITA = "\033[1m"

ARCHIVO = "gastos.json"


# ============================================================
# FUNCIONES DE DATOS
# ============================================================

def cargar_gastos():
    if not os.path.exists(ARCHIVO):
        return []

    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return []


def guardar_gastos(gastos):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(gastos, archivo, ensure_ascii=False, indent=4)


# ============================================================
# DISEÑO
# ============================================================

def limpiar():
    os.system("clear")


def titulo():
    print()
    print(ROSA + NEGRITA)
    print("        ██████╗  █████╗ ██╗   ██╗")
    print("        ██╔══██╗██╔══██╗╚██╗ ██╔╝")
    print("        ██║  ██║███████║ ╚████╔╝ ")
    print("        ██║  ██║██╔══██║  ╚██╔╝  ")
    print("        ██████╔╝██║  ██║   ██║   ")
    print("        ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ")
    print()
    print("             DAY TO DAY EXPENSES")
    print("        ════════════════════════════")
    print(RESET)


def caja_inicio():
    print(AZUL_MARINO + BLANCO)
    print("╔══════════════════════════════════════════════╗")
    print("║                                              ║")
    print("║              WEEKLY EXPENSES                 ║")
    print("║                                              ║")
    print("║    ①  ➕  AGREGAR GASTO                      ║")
    print("║                                              ║")
    print("║    ②  📋  VER GASTOS                         ║")
    print("║                                              ║")
    print("║    ③  📊  RESUMEN SEMANAL                   ║")
    print("║                                              ║")
    print("║    ④  🏷️   GASTOS POR CATEGORÍA             ║")
    print("║                                              ║")
    print("║    ⑤  🗑️   ELIMINAR GASTO                   ║")
    print("║                                              ║")
    print("║    ⑥  💾  EXPORTAR DATOS                    ║")
    print("║                                              ║")
    print("║    ⑦  🚪  SALIR                             ║")
    print("║                                              ║")
    print("╚══════════════════════════════════════════════╝")
    print(RESET)


# ============================================================
# AGREGAR GASTO
# ============================================================

def agregar_gasto(gastos):
    limpiar()
    titulo()

    print(AZUL_MARINO + BLANCO)
    print("╔══════════════════════════════════════════════╗")
    print("║                 ADD EXPENSE                  ║")
    print("╠══════════════════════════════════════════════╣")
    print(RESET)

    descripcion = input("  Descripción: ").strip()

    if not descripcion:
        print(ROSA + "\n  La descripción no puede estar vacía." + RESET)
        input("\n  Presiona ENTER para continuar...")
        return

    while True:
        cantidad = input("  Cantidad: $").strip().replace(",", ".")

        try:
            cantidad = float(cantidad)

            if cantidad <= 0:
                raise ValueError

            break

        except ValueError:
            print(ROSA + "  Introduce una cantidad válida." + RESET)

    categorias = [
        "Comida",
        "Transporte",
        "Compras",
        "Entretenimiento",
        "Servicios",
        "Salud",
        "Otros"
    ]

    print("\n  Categorías:")

    for i, categoria in enumerate(categorias, 1):
        print(f"  {i}. {categoria}")

    while True:
        try:
            opcion = int(input("\n  Selecciona categoría: "))

            if 1 <= opcion <= len(categorias):
                categoria = categorias[opcion - 1]
                break

        except ValueError:
            pass

        print(ROSA + "  Selecciona una opción válida." + RESET)

    gasto = {
        "id": len(gastos) + 1,
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "descripcion": descripcion,
        "categoria": categoria,
        "cantidad": cantidad
    }

    gastos.append(gasto)
    guardar_gastos(gastos)

    print(AZUL_MARINO + BLANCO)
    print("\n  ╔══════════════════════════════════════╗")
    print("  ║       ✓ GASTO GUARDADO              ║")
    print("  ╚══════════════════════════════════════╝")
    print(RESET)

    input("  Presiona ENTER para continuar...")


# ============================================================
# VER GASTOS
# ============================================================

def ver_gastos(gastos):
    limpiar()
    titulo()

    print(AZUL_MARINO + BLANCO)
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                    MY EXPENSES                          ║")
    print("╠══════════════════════════════════════════════════════════╣")

    if not gastos:
        print("║                                                        ║")
        print("║             No hay gastos registrados.                 ║")
        print("║                                                        ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print(RESET)

        input("\n  Presiona ENTER para continuar...")
        return

    print("║ FECHA      DESCRIPCIÓN          CATEGORÍA      CANTIDAD ║")
    print("╠══════════════════════════════════════════════════════════╣")

    for gasto in gastos:
        fecha = gasto["fecha"]
        descripcion = gasto["descripcion"][:20]
        categoria = gasto["categoria"][:14]
        cantidad = gasto["cantidad"]

        print(
            f"║ {fecha:<10} "
            f"{descripcion:<20} "
            f"{categoria:<14} "
            f"${cantidad:>8.2f} ║"
        )

    total = sum(g["cantidad"] for g in gastos)

    print("╠══════════════════════════════════════════════════════════╣")
    print(f"║ TOTAL:                                      ${total:>9.2f} ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(RESET)

    input("\n  Presiona ENTER para continuar...")


# ============================================================
# RESUMEN SEMANAL
# ============================================================

def resumen_semanal(gastos):
    limpiar()
    titulo()

    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())

    gastos_semana = []

    for gasto in gastos:
        try:
            fecha = datetime.strptime(gasto["fecha"], "%d/%m/%Y")

            if fecha.date() >= inicio_semana.date():
                gastos_semana.append(gasto)

        except ValueError:
            continue

    total = sum(g["cantidad"] for g in gastos_semana)
    cantidad_gastos = len(gastos_semana)

    promedio = total / cantidad_gastos if cantidad_gastos else 0

    print(AZUL_MARINO + BLANCO)
    print("╔══════════════════════════════════════════════╗")
    print("║              WEEKLY SUMMARY                 ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║                                              ║")
    print(f"║  💰 Total gastado:       ${total:>10.2f}      ║")
    print(f"║  🧾 Número de gastos:    {cantidad_gastos:>10}      ║")
    print(f"║  📈 Promedio por gasto:  ${promedio:>10.2f}      ║")
    print(f"║                                              ║")
    print("╚══════════════════════════════════════════════╝")
    print(RESET)

    input("\n  Presiona ENTER para continuar...")


# ============================================================
# GASTOS POR CATEGORÍA
# ============================================================

def gastos_categoria(gastos):
    limpiar()
    titulo()

    categorias = {}

    for gasto in gastos:
        categoria = gasto["categoria"]

        if categoria not in categorias:
            categorias[categoria] = 0

        categorias[categoria] += gasto["cantidad"]

    print(AZUL_MARINO + BLANCO)
    print("╔══════════════════════════════════════════════╗")
    print("║             EXPENSES BY CATEGORY            ║")
    print("╠══════════════════════════════════════════════╣")

    if not categorias:
        print("║                                              ║")
        print("║          No hay gastos registrados.         ║")
        print("║                                              ║")
    else:
        for categoria, total in categorias.items():
            print(f"║  {categoria:<25} ${total:>10.2f} ║")

    print("╚══════════════════════════════════════════════╝")
    print(RESET)

    input("\n  Presiona ENTER para continuar...")


# ============================================================
# ELIMINAR GASTO
# ============================================================

def eliminar_gasto(gastos):
    limpiar()
    titulo()

    if not gastos:
        print(ROSA + "  No hay gastos para eliminar." + RESET)
        input("\n  Presiona ENTER para continuar...")
        return

    print(AZUL_MARINO + BLANCO)
    print("╔══════════════════════════════════════════════╗")
    print("║               DELETE EXPENSE                ║")
    print("╠══════════════════════════════════════════════╣")

    for i, gasto in enumerate(gastos, 1):
        print(
            f"║ {i}. {gasto['descripcion']:<20} "
            f"${gasto['cantidad']:>8.2f}      ║"
        )

    print("╚══════════════════════════════════════════════╝")
    print(RESET)

    try:
        opcion = int(input("\n  Número del gasto a eliminar: "))

        if 1 <= opcion <= len(gastos):
            eliminado = gastos.pop(opcion - 1)

            # Renumerar IDs
            for i, gasto in enumerate(gastos, 1):
                gasto["id"] = i

            guardar_gastos(gastos)

            print(
                ROSA +
                f"\n  ✓ Se eliminó: {eliminado['descripcion']}" +
                RESET
            )
        else:
            print(ROSA + "\n  Número inválido." + RESET)

    except ValueError:
        print(ROSA + "\n  Introduce un número válido." + RESET)

    input("\n  Presiona ENTER para continuar...")


# ============================================================
# EXPORTAR
# ============================================================

def exportar_datos(gastos):
    limpiar()
    titulo()

    archivo = "gastos_exportados.txt"

    try:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("DAY TO DAY EXPENSES\n")
            f.write("===================\n\n")

            for gasto in gastos:
                f.write(
                    f"{gasto['fecha']} | "
                    f"{gasto['descripcion']} | "
                    f"{gasto['categoria']} | "
                    f"${gasto['cantidad']:.2f}\n"
                )

        print(ROSA + f"✓ Datos exportados a: {archivo}" + RESET)

    except OSError:
        print(ROSA + "No se pudo exportar el archivo." + RESET)

    input("\n  Presiona ENTER para continuar...")


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    gastos = cargar_gastos()

    while True:

        limpiar()
        titulo()
        caja_inicio()

        opcion = input(
            ROSA + "\n              Selecciona una opción:\n"
            "              ❯ " + RESET
        ).strip()

        if opcion == "1":
            agregar_gasto(gastos)

        elif opcion == "2":
            ver_gastos(gastos)

        elif opcion == "3":
            resumen_semanal(gastos)

        elif opcion == "4":
            gastos_categoria(gastos)

        elif opcion == "5":
            eliminar_gasto(gastos)

        elif opcion == "6":
            exportar_datos(gastos)

        elif opcion == "7":
            limpiar()
            print(ROSA + "\n       🌸 Gracias por usar Day to day expenses 🌸\n" + RESET)
            break

        else:
            print(ROSA + "\n  Opción no válida." + RESET)
            input("  Presiona ENTER para continuar...")


if __name__ == "__main__":
    main()