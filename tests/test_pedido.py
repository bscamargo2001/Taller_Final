import pytest

from base.pedido_legacy import procesar_pedido_legacy
from refactorizado.pedido_refactor import procesar_pedido

IMPLEMENTACIONES = [procesar_pedido_legacy, procesar_pedido]


@pytest.mark.parametrize("fn", IMPLEMENTACIONES)
def test_cliente_vip_con_envio_gratis_ciudad_principal(fn):
    items = [{"precio": 120000, "cantidad": 2}]  # subtotal 240000 -> VIP 15% = 36000
    resultado = fn(
        items=items,
        tipo_cliente="VIP",
        cupon=None,
        envio_express=False,
        ciudad="Soacha",
    )
    # base_impuestos = 204000 | iva = 38760 | envio = 0 (subtotal >= 180000)
    assert resultado == {
        "subtotal": 240000.0,
        "descuento": 36000.0,
        "impuestos": 38760.0,
        "envio": 0.0,
        "total": 242760.0,
    }


@pytest.mark.parametrize("fn", IMPLEMENTACIONES)
def test_cliente_nuevo_con_volumen_y_cupon_verano10(fn):
    items = [{"precio": 65000, "cantidad": 5}]  # subtotal 325000, 5 unidades -> NUEVO 7% = 22750
    resultado = fn(
        items=items,
        tipo_cliente="NUEVO",
        cupon=" verano10 ",
        envio_express=True,
        ciudad="Bogotá",
    )
    # base_tras_cliente = 302250 | cupon 10% = 30225 | base_impuestos = 272025
    # iva = 51684.75 | envio = 0 + 15000 express = 15000
    assert resultado == {
        "subtotal": 325000.0,
        "descuento": 52975.0,
        "impuestos": 51684.75,
        "envio": 40000.0,
        "total": 363709.75,
    }


@pytest.mark.parametrize("fn", IMPLEMENTACIONES)
def test_cliente_frecuente_fuera_de_ciudad_principal_y_cupon_fijo20(fn):
    items = [{"precio": 100000, "cantidad": 2}]  # subtotal 200000 -> FRECUENTE 8% = 16000
    resultado = fn(
        items=items,
        tipo_cliente="FRECUENTE",
        cupon="FIJO20",
        envio_express=False,
        ciudad="Medellín",
    )
    # base_tras_cliente = 184000 | cupon = 20000 | base_impuestos = 164000
    # iva = 31160.0 | envio = 25000 (subtotal < 250000)
    assert resultado == {
        "subtotal": 200000.0,
        "descuento": 36000.0,
        "impuestos": 31160.0,
        "envio": 25000.0,
        "total": 220160.0,
    }


@pytest.mark.parametrize("fn", IMPLEMENTACIONES)
def test_errores_de_validacion(fn):
    with pytest.raises(ValueError):
        fn([], "VIP", None, False, "Bogota")

    with pytest.raises(ValueError):
        fn([{"precio": 0, "cantidad": 1}], "VIP", None, False, "Bogota")

    with pytest.raises(ValueError):
        fn([{"precio": 10000, "cantidad": 1}], "DESCONOCIDO", None, False, "Bogota")