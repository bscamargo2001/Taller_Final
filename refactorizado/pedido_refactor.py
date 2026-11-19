IVA_PORCENTAJE = 0.19
CIUDADES_PRINCIPALES = {"BOGOTA", "SOACHA", "CHIA"}

REGLAS_CLIENTE = {
    "VIP": [(500000, 0.20), (200000, 0.15), (0, 0.10)],
    "FRECUENTE": [(500000, 0.12), (200000, 0.08), (0, 0.05)],
}


def _validar_y_calcular_subtotal(items):
    if not items:
        raise ValueError("El pedido debe tener al menos un producto")

    subtotal = 0.0
    total_unidades = 0

    for item in items:
        precio = item["precio"]
        cantidad = item["cantidad"]
        if precio <= 0 or cantidad <= 0:
            raise ValueError("Precio y cantidad deben ser mayores que cero")
        subtotal += precio * cantidad
        total_unidades += cantidad

    return subtotal, total_unidades


def _calcular_descuento_cliente(tipo_cliente, subtotal, total_unidades):
    if tipo_cliente in REGLAS_CLIENTE:
        for umbral, porcentaje in REGLAS_CLIENTE[tipo_cliente]:
            if subtotal >= umbral:
                return subtotal * porcentaje
        return 0.0

    if tipo_cliente == "NUEVO":
        if subtotal >= 300000 and total_unidades >= 5:
            return subtotal * 0.07
        if subtotal >= 300000:
            return subtotal * 0.05
        return 0.0

    raise ValueError("Tipo de cliente no válido")


def _calcular_descuento_cupon(cupon, base_actual):
    if not cupon:
        return 0.0

    codigo = cupon.strip().upper()
    if codigo == "VERANO10" and base_actual >= 100000:
        return base_actual * 0.10

    if codigo == "FIJO20" and base_actual >= 150000:
        tope_maximo = base_actual * 0.5
        return min(20000.0, tope_maximo)

    return 0.0


def _calcular_envio(subtotal, envio_express, ciudad):
    ciudad_limpia = (ciudad or "").strip().upper()
    es_principal = ciudad_limpia in CIUDADES_PRINCIPALES

    if es_principal:
        costo_envio = 12000.0 if subtotal < 180000 else 0.0
        recargo_express = 15000.0
    else:
        costo_envio = 25000.0 if subtotal < 250000 else 10000.0
        recargo_express = 30000.0

    if envio_express:
        costo_envio += recargo_express

    return costo_envio


def procesar_pedido(items, tipo_cliente, cupon, envio_express, ciudad):
    subtotal, total_unidades = _validar_y_calcular_subtotal(items)

    descuento_cliente = _calcular_descuento_cliente(tipo_cliente, subtotal, total_unidades)
    base_tras_cliente = subtotal - descuento_cliente

    descuento_cupon = _calcular_descuento_cupon(cupon, base_tras_cliente)
    base_impuestos = max(0.0, base_tras_cliente - descuento_cupon)

    impuestos = base_impuestos * IVA_PORCENTAJE
    costo_envio = _calcular_envio(subtotal, envio_express, ciudad)
    total = base_impuestos + impuestos + costo_envio

    return {
        "subtotal": round(subtotal, 2),
        "descuento": round(descuento_cliente + descuento_cupon, 2),
        "impuestos": round(impuestos, 2),
        "envio": round(costo_envio, 2),
        "total": round(total, 2),
    }