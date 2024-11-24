### Plantillas para realizar cuentas contables


"""
Parameter Definition




"""

dict_precios_1 = {
    # Combinaciones de "MKT" como vendedor
    ("MKT", "ZF", "materia_prima"): 5,
    ("MKT", "NCT", "materia_prima"): 5,
    # Combinaciones de "MKT" como comprador
    ("NCT", "MKT", "bien_final"): 7,
    ("ZF", "MKT", "bien_final"): 7,
    # Combinaciones de "NCT" como vendedor
    ("NCT", "ZF", "materia_prima"): 3,
    ("NCT", "ZF", "bien_intermedio"): 5,
    ("NCT", "ZF", "bien_final"): 6,
    ("NCT", "NCT", "materia_prima"): 20,
    ("NCT", "NCT", "bien_intermedio"): 80,
    ("NCT", "NCT", "bien_final"): 100,
    # Combinaciones de "ZF" como vendedor
    ("ZF", "NCT", "materia_prima"): 2,
    ("ZF", "NCT", "bien_intermedio"): 4,
    ("ZF", "NCT", "bien_final"): 6,
    ("ZF", "ZF", "materia_prima"): 20,
    ("ZF", "ZF", "bien_intermedio"): 80,
    ("ZF", "ZF", "bien_final"): 100,
}


plantillas_contables_1 = {
    "materia_prima": {
        "compra": {
            "debito": [("1405", "precio")],
            "credito": [("1105", "precio")],
        },
        "venta": {
            "debito": [("1105", "precio"), ("6135", "costo")],
            "credito": [("4135", "precio"), ("1405", "costo")],
        },
        "produccion": {
            "debito": [("71", "costo"), ("1410", "costo")],
            "credito": [("1405", "costo"), ("71", "costo")],
        },
    },
    "bien_intermedio": {
        "compra": {
            "debito": [("1405", "precio")],
            "credito": [("1105", "precio")],
        },
        "venta": {
            "debito": [("1105", "precio"), ("6135", "costo")],
            "credito": [("4135", "precio"), ("1410", "costo")],
        },
        "produccion": {
            "debito": [("71", "costo"), ("1430", "costo")],
            "credito": [("1410", "costo"), ("71", "costo")],
        },
    },
    "bien_final": {
        "compra": {
            "debito": [("1405", "precio")],
            "credito": [("1105", "precio")],
        },
        "venta": {
            "debito": [("1105", "precio"), ("6120", "costo")],
            "credito": [("4120", "precio"), ("1430", "costo")],
        },
    },
}


dict_precios_2 = {
    # Combinaciones de "MKT" como vendedor
    ("MKT", "ZF", "materia_prima"): 1,
    ("MKT", "NCT", "materia_prima"): 1,
    # Combinaciones de "MKT" como comprador
    ("NCT", "MKT", "bien_final"): 7,
    ("ZF", "MKT", "bien_final"): 7,
    # Combinaciones de "NCT" como vendedor
    ("NCT", "ZF", "materia_prima"): 3,
    ("NCT", "ZF", "bien_intermedio"): 5,
    ("NCT", "ZF", "bien_final"): 6,
    # Combinaciones de "ZF" como vendedor
    ("ZF", "NCT", "materia_prima"): 2,
    ("ZF", "NCT", "bien_intermedio"): 4,
    ("ZF", "NCT", "bien_final"): 6,
}
