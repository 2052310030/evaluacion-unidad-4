from CRUD.excepciones import (
    CostoInvalidoError,
    DatosIncompletosError,
    ServicioDuplicadoError,
    ServicioNoEncontradoError,
)
from CRUD.servicio import Servicio


class ControladorServicios:
    """Contiene validaciones y reglas de negocio."""

    def __init__(self, repositorio):
        self.repositorio = repositorio

    @staticmethod
    def validar_datos(cliente, vehiculo, tipo_servicio, costo):
        if not cliente.strip() or not vehiculo.strip() or not tipo_servicio.strip():
            raise DatosIncompletosError("Todos los campos son obligatorios.")
        try:
            costo_numero = float(costo)
        except (TypeError, ValueError) as error:
            raise CostoInvalidoError("El costo debe ser un número.") from error
        if costo_numero <= 0:
            raise CostoInvalidoError("El costo debe ser mayor a 0.")
        return costo_numero

    def registrar(self, cliente, vehiculo, tipo_servicio, costo):
        costo_numero = self.validar_datos(cliente, vehiculo, tipo_servicio, costo)
        servicio = Servicio(cliente.strip(), vehiculo.strip(), tipo_servicio.strip(), costo_numero)
        if self.repositorio.existe_duplicado(servicio):
            raise ServicioDuplicadoError("Este servicio ya se encuentra registrado.")
        return self.repositorio.crear(servicio)

    def consultar_todos(self):
        return self.repositorio.listar()

    def consultar_por_id(self, servicio_id):
        servicio = self.repositorio.buscar_por_id(int(servicio_id))
        if servicio is None:
            raise ServicioNoEncontradoError(f"No existe el servicio con ID {servicio_id}.")
        return servicio

    def actualizar(self, servicio_id, cliente, vehiculo, tipo_servicio, costo):
        costo_numero = self.validar_datos(cliente, vehiculo, tipo_servicio, costo)
        servicio_id = int(servicio_id)
        if self.repositorio.buscar_por_id(servicio_id) is None:
            raise ServicioNoEncontradoError(f"No existe el servicio con ID {servicio_id}.")
        servicio = Servicio(cliente.strip(), vehiculo.strip(), tipo_servicio.strip(), costo_numero, servicio_id)
        if self.repositorio.existe_duplicado(servicio, excluir_id=servicio_id):
            raise ServicioDuplicadoError("Ya existe otro servicio con esos datos.")
        return self.repositorio.actualizar(servicio)

    def eliminar(self, servicio_id):
        return self.repositorio.eliminar(int(servicio_id))
