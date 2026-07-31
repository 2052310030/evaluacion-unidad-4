from CRUD.controlador_servicios import ControladorServicios
from CRUD.excepciones import CostoInvalidoError, ServicioNoEncontradoError


def demostrar_costo_negativo(controlador):
    try:
        controlador.registrar("Laura", "Ford Fiesta", "Afinación", -500)
    except CostoInvalidoError as error:
        print(f"Error controlado: {error}")
    else:
        print("El servicio fue registrado.")
    finally:
        print("Terminó el intento de registro.")


def demostrar_eliminacion_inexistente(controlador):
    try:
        controlador.eliminar(99999)
    except ServicioNoEncontradoError as error:
        print(f"Error controlado: {error}")
    else:
        print("El servicio fue eliminado.")
    finally:
        print("Terminó el intento de eliminación.")
