class ServicioError(Exception):
    """Error base del módulo de servicios."""


class ServicioNoEncontradoError(ServicioError):
    """Se produce cuando no existe el servicio solicitado."""


class CostoInvalidoError(ServicioError):
    """Se produce cuando el costo no es un número mayor a cero."""


class DatosIncompletosError(ServicioError):
    """Se produce cuando falta un dato obligatorio."""


class ServicioDuplicadoError(ServicioError):
    """Se produce cuando ya existe un servicio equivalente."""
