import unittest
from unittest.mock import patch
from io import StringIO

from tasks import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    validar_task_id
)

from models import is_completed


class TestTaskFlow(unittest.TestCase):

    def setUp(self):
        # Lista limpia antes de cada prueba
        self.tasks = []

    # ==========================
    # PRUEBAS: AGREGAR TAREAS
    # ==========================

    def test_agregar_tarea(self):
        resultado = add_task(self.tasks, "Estudiar Python")

        self.assertTrue(resultado)
        self.assertEqual(len(self.tasks), 1)
        self.assertEqual(self.tasks[0]["id"], 1)
        self.assertEqual(self.tasks[0]["title"], "Estudiar Python")
        self.assertFalse(is_completed(self.tasks[0]))

    def test_no_agregar_tarea_duplicada(self):
        add_task(self.tasks, "Estudiar Python")
        resultado = add_task(self.tasks, "estudiar python")

        self.assertFalse(resultado)
        self.assertEqual(len(self.tasks), 1)

    # ==========================
    # PRUEBAS: LISTAR TAREAS
    # ==========================

    def test_listar_tareas(self):
        add_task(self.tasks, "Hacer tarea")

        with patch("sys.stdout", new=StringIO()) as salida:
            list_tasks(self.tasks)

        resultado = salida.getvalue()

        self.assertIn("ID: 1", resultado)
        self.assertIn("Nombre: Hacer tarea", resultado)
        self.assertIn("Estado: Pendiente", resultado)

    def test_listar_tareas_vacias(self):
        with patch("sys.stdout", new=StringIO()) as salida:
            list_tasks(self.tasks)

        self.assertIn("No hay tareas", salida.getvalue())

    # ==========================
    # PRUEBAS: COMPLETAR TAREAS
    # ==========================

    def test_completar_tarea(self):
        add_task(self.tasks, "Terminar proyecto")

        resultado = complete_task(self.tasks, 1)

        self.assertTrue(resultado)
        self.assertTrue(is_completed(self.tasks[0]))

    def test_completar_id_inexistente(self):
        add_task(self.tasks, "Terminar proyecto")

        resultado = complete_task(self.tasks, 99)

        self.assertFalse(resultado)
        self.assertFalse(is_completed(self.tasks[0]))

    # ==========================
    # PRUEBAS: VALIDACIONES
    # ==========================

    def test_validar_id_correcto(self):
        resultado = validar_task_id("1")

        self.assertEqual(resultado, 1)

    def test_validar_id_con_letras(self):
        resultado = validar_task_id("abc")

        self.assertIsNone(resultado)

    def test_validar_id_negativo(self):
        resultado = validar_task_id("-5")

        self.assertIsNone(resultado)

    # ==========================
    # PRUEBAS: ELIMINAR TAREAS
    # ==========================

    @patch("builtins.input", return_value="s")
    def test_eliminar_tarea(self, mock_input):
        add_task(self.tasks, "Tarea uno")
        add_task(self.tasks, "Tarea dos")

        resultado = delete_task(self.tasks, 1)

        self.assertTrue(resultado)
        self.assertEqual(len(self.tasks), 1)
        self.assertEqual(self.tasks[0]["title"], "Tarea dos")
        self.assertEqual(self.tasks[0]["id"], 1)

    @patch("builtins.input", return_value="n")
    def test_cancelar_eliminacion(self, mock_input):
        add_task(self.tasks, "Tarea importante")

        resultado = delete_task(self.tasks, 1)

        self.assertFalse(resultado)
        self.assertEqual(len(self.tasks), 1)

    def test_eliminar_id_invalido(self):
        add_task(self.tasks, "Tarea de prueba")

        resultado = delete_task(self.tasks, "abc")

        self.assertFalse(resultado)
        self.assertEqual(len(self.tasks), 1)


if __name__ == "__main__":
    unittest.main()