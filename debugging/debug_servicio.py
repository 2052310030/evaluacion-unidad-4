from CRUD.controlador_servicios import ControladorServicios
from CRUD.repositorio_servicios import RepositorioServicios


repositorio = RepositorioServicios()
controlador = ControladorServicios(repositorio)

servicio_id = 1
breakpoint()  # Equivale a pdb.set_trace(). Quitar o comentar después de la evidencia.
servicio = controlador.consultar_por_id(servicio_id)
print(servicio)
