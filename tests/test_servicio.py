import pytest

from CRUD.controlador_servicios import ControladorServicios
from CRUD.excepciones import CostoInvalidoError, DatosIncompletosError, ServicioDuplicadoError


class RepositorioFalso:
    def __init__(self):
        self.datos = []
        self.siguiente_id = 1

    def existe_duplicado(self, servicio, excluir_id=None):
        return any(s.cliente.lower() == servicio.cliente.lower()
                   and s.vehiculo.lower() == servicio.vehiculo.lower()
                   and s.tipo_servicio.lower() == servicio.tipo_servicio.lower()
                   and s.id != excluir_id for s in self.datos)

    def crear(self, servicio):
        servicio.id = self.siguiente_id
        self.siguiente_id += 1
        self.datos.append(servicio)
        return servicio

    def listar(self):
        return self.datos

    def buscar_por_id(self, servicio_id):
        return next((s for s in self.datos if s.id == servicio_id), None)

    def actualizar(self, servicio):
        indice = next(i for i, actual in enumerate(self.datos) if actual.id == servicio.id)
        self.datos[indice] = servicio
        return servicio

    def eliminar(self, servicio_id):
        self.datos = [s for s in self.datos if s.id != servicio_id]
        return True


@pytest.fixture
def controlador():
    return ControladorServicios(RepositorioFalso())


def test_registrar_servicio_correctamente(controlador):
    # Arrange
    cliente, vehiculo, tipo, costo = "Ana", "Nissan", "Afinación", 900
    # Act
    servicio = controlador.registrar(cliente, vehiculo, tipo, costo)
    # Assert
    assert servicio.id == 1
    assert servicio.costo == 900.0


def test_rechazar_costo_negativo(controlador):
    # Arrange
    costo = -50
    # Act y Assert
    with pytest.raises(CostoInvalidoError):
        controlador.registrar("Ana", "Nissan", "Afinación", costo)


def test_rechazar_costo_no_numerico(controlador):
    # Arrange, Act y Assert
    with pytest.raises(CostoInvalidoError):
        controlador.registrar("Ana", "Nissan", "Afinación", "mucho")


def test_rechazar_campos_vacios(controlador):
    # Arrange, Act y Assert
    with pytest.raises(DatosIncompletosError):
        controlador.registrar("", "Nissan", "Afinación", 800)


def test_rechazar_servicio_duplicado(controlador):
    # Arrange
    controlador.registrar("Ana", "Nissan", "Afinación", 800)
    # Act y Assert
    with pytest.raises(ServicioDuplicadoError):
        controlador.registrar("Ana", "Nissan", "Afinación", 950)


def test_actualizar_servicio(controlador):
    # Arrange
    original = controlador.registrar("Ana", "Nissan", "Afinación", 800)
    # Act
    actualizado = controlador.actualizar(original.id, "Ana López", "Nissan", "Frenos", 1200)
    # Assert
    assert actualizado.cliente == "Ana López"
    assert actualizado.tipo_servicio == "Frenos"
    assert actualizado.costo == 1200.0


def test_eliminar_servicio(controlador):
    # Arrange
    servicio = controlador.registrar("Ana", "Nissan", "Afinación", 800)
    # Act
    controlador.eliminar(servicio.id)
    # Assert
    assert controlador.consultar_todos() == []
