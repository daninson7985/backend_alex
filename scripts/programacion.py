from datetime import datetime


def calcular_total(items):
    total = 0
    for item in items:
        total += item
    return total


def validar_estado(estado):
    estados_validos = ["Pendiente", "Aprobada", "Revisión"]
    if estado in estados_validos:
        return True
    return False


if __name__ == "__main__":
    precios = [1200, 800, 1500]
    total = calcular_total(precios)
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    print(f"Total acumulado: ${total}")
    print(f"Fecha actual: {fecha_actual}")
    print(validar_estado("Aprobada"))
