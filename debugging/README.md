# Debugging con pdb

## Procedimiento realizado

1. Se ejecutó desde `Evaluacion_U4`:

```bash
python -m debugging.debug_servicio
```

2. La ejecución se detuvo en `breakpoint()` antes de buscar el servicio.
3. Se utilizaron estos comandos:

```text
p servicio_id   muestra el ID que se buscará
n               ejecuta la siguiente línea
s               entra en la función llamada
p servicio      inspecciona el objeto encontrado
c               continúa hasta terminar
```

La inspección permite comprobar que el ID sea un entero y que el objeto recuperado contenga cliente, vehículo, tipo de servicio y costo correctos. Si la búsqueda no encuentra el registro, el controlador genera `ServicioNoEncontradoError`.

Para tomar evidencia, ejecuta el archivo, escribe los comandos y captura la terminal. Después puedes comentar la línea `breakpoint()` para que no detenga la aplicación.
