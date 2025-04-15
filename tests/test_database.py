import unittest
import copy
from gestor import database as db, helpers

class TestDatabase(unittest.TestCase):
    def setUp(self):
        db.Clientes.lista = [
            db.Cliente('15J', 'Marta', 'Pérez'),
            db.Cliente('48H', 'Manolo', 'López'),
            db.Cliente('28Z', 'Ana', 'García')
        ]

    def test_buscar_cliente(self):
        self.assertIsNotNone(db.Clientes.buscar('15J'))
        self.assertIsNone(db.Clientes.buscar('00X'))

    def test_crear_cliente(self):
        cliente = db.Clientes.crear('33Z', 'Nuevo', 'Cliente')
        self.assertEqual(cliente.dni, '33Z')

    def test_modificar_cliente(self):
        cliente = db.Clientes.modificar('28Z', 'AnaMod', 'GarciaMod')
        self.assertEqual(cliente.nombre, 'AnaMod')

    def test_borrar_cliente(self):
        cliente = db.Clientes.borrar('15J')
        self.assertIsNotNone(cliente)
        self.assertIsNone(db.Clientes.buscar('15J'))

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('48H', db.Clientes.lista))
