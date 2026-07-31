from contextlib import contextmanager

import mysql.connector
from mysql.connector import Error

from CRUD.excepciones import ServicioNoEncontradoError
from CRUD.servicio import Servicio


class RepositorioServicios:
    """Se encarga únicamente del acceso a la base de datos."""

    def __init__(self, host="localhost", user="root", password="", database="taller_mecanico"):
        self.configuracion = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
        }

    @contextmanager
    def _conexion(self):
        conexion = None
        try:
            conexion = mysql.connector.connect(**self.configuracion)
            yield conexion
        except Error:
            if conexion and conexion.is_connected():
                conexion.rollback()
            raise
        finally:
            if conexion and conexion.is_connected():
                conexion.close()

    def crear(self, servicio):
        with self._conexion() as conexion:
            cursor = conexion.cursor()
            consulta = """
                INSERT INTO servicios (cliente, vehiculo, tipo_servicio, costo)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(consulta, servicio.como_tupla())
            conexion.commit()
            servicio.id = cursor.lastrowid
            cursor.close()
            return servicio

    def listar(self):
        with self._conexion() as conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id, cliente, vehiculo, tipo_servicio, costo FROM servicios ORDER BY id")
            filas = cursor.fetchall()
            cursor.close()
        return [Servicio(**fila) for fila in filas]

    def buscar_por_id(self, servicio_id):
        with self._conexion() as conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, cliente, vehiculo, tipo_servicio, costo FROM servicios WHERE id = %s",
                (servicio_id,),
            )
            fila = cursor.fetchone()
            cursor.close()
        return Servicio(**fila) if fila else None

    def existe_duplicado(self, servicio, excluir_id=None):
        consulta = """
            SELECT COUNT(*) AS total FROM servicios
            WHERE LOWER(cliente) = LOWER(%s)
              AND LOWER(vehiculo) = LOWER(%s)
              AND LOWER(tipo_servicio) = LOWER(%s)
        """
        parametros = [servicio.cliente, servicio.vehiculo, servicio.tipo_servicio]
        if excluir_id is not None:
            consulta += " AND id <> %s"
            parametros.append(excluir_id)
        with self._conexion() as conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(consulta, tuple(parametros))
            resultado = cursor.fetchone()["total"] > 0
            cursor.close()
        return resultado

    def actualizar(self, servicio):
        with self._conexion() as conexion:
            cursor = conexion.cursor()
            consulta = """
                UPDATE servicios
                SET cliente=%s, vehiculo=%s, tipo_servicio=%s, costo=%s
                WHERE id=%s
            """
            cursor.execute(consulta, servicio.como_tupla() + (servicio.id,))
            if cursor.rowcount == 0:
                cursor.close()
                raise ServicioNoEncontradoError(f"No existe el servicio con ID {servicio.id}.")
            conexion.commit()
            cursor.close()
            return servicio

    def eliminar(self, servicio_id):
        with self._conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM servicios WHERE id = %s", (servicio_id,))
            if cursor.rowcount == 0:
                cursor.close()
                raise ServicioNoEncontradoError(f"No existe el servicio con ID {servicio_id}.")
            conexion.commit()
            cursor.close()
            return True
