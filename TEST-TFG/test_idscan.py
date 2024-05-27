import pytest
from idscan import generar_id_scan

def test_generar_id_scan_length():
    """
    Verifica que el ID generado tenga la longitud esperada de un hash SHA-256 (64 caracteres hexadecimales).
    """
    id_scan = generar_id_scan()
    assert len(id_scan) == 64

def test_generar_id_scan_uniqueness():
    """
    Verifica que dos IDs generados consecutivamente no sean iguales.
    """
    id_scan1 = generar_id_scan()
    id_scan2 = generar_id_scan()
    assert id_scan1 != id_scan2

def test_generar_id_scan_format():
    """
    Verifica que el ID generado solo contenga caracteres hexadecimales.
    """
    id_scan = generar_id_scan()
    hex_chars = set("0123456789abcdef")
    assert all(c in hex_chars for c in id_scan)

# Puedes agregar más pruebas según sea necesario para cubrir otros casos.
