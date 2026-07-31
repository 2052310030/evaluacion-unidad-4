# Proyecto CRUD del taller mecánico

Aplicación de escritorio con Python, Tkinter y MySQL para registrar, consultar, actualizar y eliminar servicios.

## Preparación

1. Inicia Apache y MySQL desde XAMPP.
2. Entra a `http://localhost/phpmyadmin`.
3. Abre **Importar**, selecciona `CRUD/db_taller.sql` y presiona **Importar**.
4. Abre una terminal en la carpeta `Evaluacion_U4`.
5. Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

6. Si MySQL tiene contraseña, escríbela en `CRUD/main.py`.
7. Ejecuta la aplicación:

```bash
python -m CRUD.main
```

## Organización SOLID

- `Servicio`: entidad que almacena los datos.
- `RepositorioServicios`: única clase responsable de MySQL.
- `ControladorServicios`: validaciones y lógica de negocio.
- `InterfazTkinter`: presentación e interacción con el usuario.

Cada clase tiene una responsabilidad principal y recibe sus dependencias desde el exterior.
