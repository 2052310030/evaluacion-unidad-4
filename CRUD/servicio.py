from dataclasses import dataclass
from typing import Optional


@dataclass
class Servicio:
    cliente: str
    vehiculo: str
    tipo_servicio: str
    costo: float
    id: Optional[int] = None

    def como_tupla(self):
        return self.cliente, self.vehiculo, self.tipo_servicio, self.costo
