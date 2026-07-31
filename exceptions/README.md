# Manejo de excepciones

Las excepciones personalizadas están en `CRUD/excepciones.py`:

- `CostoInvalidoError`: costo no numérico, igual a cero o negativo.
- `ServicioNoEncontradoError`: el ID solicitado no existe.
- `DatosIncompletosError`: falta un campo obligatorio.
- `ServicioDuplicadoError`: el servicio ya está registrado.

`ejemplo_excepciones.py` contiene casos con `try`, `except`, `else` y `finally`. Los errores también aparecen en ventanas claras dentro de la interfaz.
