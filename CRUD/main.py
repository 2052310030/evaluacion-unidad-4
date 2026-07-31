from CRUD.controlador_servicios import ControladorServicios
from CRUD.interfaz_tkinter import InterfazTkinter
from CRUD.repositorio_servicios import RepositorioServicios


def main():
    repositorio = RepositorioServicios(
        host="localhost",
        user="root",
        password="",  # Escribe aquí la contraseña de MySQL si utilizas una.
        database="taller_mecanico",
    )
    controlador = ControladorServicios(repositorio)
    InterfazTkinter(controlador).ejecutar()


if __name__ == "__main__":
    main()
