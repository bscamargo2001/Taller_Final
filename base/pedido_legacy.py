def procesar_pedido_legacy(items, tipo_cliente, cupon, envio_express, ciudad):
    if items is None or len(items) == 0:
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

    # Descuento por volumen y tipo de cliente
    descuento_porcentaje = 0.0
    if tipo_cliente == "VIP":
        if subtotal >= 500000:
            descuento_porcentaje = 0.20
        elif subtotal >= 200000:
            descuento_porcentaje = 0.15
        else:
            descuento_porcentaje = 0.10
    elif tipo_cliente == "FRECUENTE":
        if subtotal >= 500000:
            descuento_porcentaje = 0.12
        elif subtotal >= 200000:
            descuento_porcentaje = 0.08
        else:
            descuento_porcentaje = 0.05
    elif tipo_cliente == "NUEVO":
        if subtotal >= 300000 and total_unidades >= 5:
            descuento_porcentaje = 0.07
        elif subtotal >= 300000:
            descuento_porcentaje = 0.05
    else:
        raise ValueError("Tipo de cliente no válido")

    monto_descuento = subtotal * descuento_porcentaje
    subtotal_con_descuento = subtotal - monto_descuento

    # Descuento adicional por cupón
    descuento_cupon = 0.0
    if cupon is not None and cupon != "":
        codigo = cupon.strip().upper()
        if codigo == "VERANO10" and subtotal_con_descuento >= 100000:
            descuento_cupon = subtotal_con_descuento * 0.10
        elif codigo == "FIJO20" and subtotal_con_descuento >= 150000:
            descuento_cupon = 20000.0
            if descuento_cupon > subtotal_con_descuento * 0.5:
                descuento_cupon = subtotal_con_descuento * 0.5

    base_impuestos = subtotal_con_descuento - descuento_cupon
    if base_impuestos < 0:
        base_impuestos = 0.0

    impuestos = base_impuestos * 0.19

    # Cálculo de envío
    ciudad_limpia = (ciudad or "").strip().upper()
    if ciudad_limpia in ("BOGOTA", "SOACHA", "CHIA"):
        costo_envio = 12000.0 if subtotal < 180000 else 0.0
    else:
        costo_envio = 25000.0 if subtotal < 250000 else 10000.0

    if envio_express:
        if ciudad_limpia in ("BOGOTA", "SOACHA", "CHIA"):
            costo_envio += 15000.0
        else:
            costo_envio += 30000.0

    total = round(base_impuestos + impuestos + costo_envio, 2)

    return {
        "subtotal": round(subtotal, 2),
        "descuento": round(monto_descuento + descuento_cupon, 2),
        "impuestos": round(impuestos, 2),
        "envio": round(costo_envio, 2),
        "total": total,
    }