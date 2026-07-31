import pdb

from CRUD.repositorio_servicios import RepositorioServicios


repositorio = RepositorioServicios()
pdb.set_trace()
servicios = repositorio.listar()
print(f"Registros encontrados: {len(servicios)}")
