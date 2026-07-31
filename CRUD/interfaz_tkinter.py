import tkinter as tk
from tkinter import messagebox, ttk


class InterfazTkinter:
    """Interfaz gráfica; delega la lógica al controlador."""

    def __init__(self, controlador):
        self.controlador = controlador
        self.ventana = tk.Tk()
        self.ventana.title("Taller mecánico - Control de servicios")
        self.ventana.geometry("920x610")
        self.ventana.minsize(820, 560)
        self._crear_estilos()
        self._crear_componentes()
        self.cargar_tabla()

    def _crear_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", font=("Arial", 20, "bold"), foreground="#17324d")
        estilo.configure("TButton", padding=8, font=("Arial", 10))
        estilo.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def _crear_componentes(self):
        contenedor = ttk.Frame(self.ventana, padding=20)
        contenedor.pack(fill="both", expand=True)
        ttk.Label(contenedor, text="Control de servicios", style="Titulo.TLabel").pack(pady=(0, 15))

        formulario = ttk.LabelFrame(contenedor, text="Datos del servicio", padding=15)
        formulario.pack(fill="x")
        self.variables = {nombre: tk.StringVar() for nombre in ("id", "cliente", "vehiculo", "tipo", "costo")}
        campos = [("ID", "id"), ("Cliente", "cliente"), ("Vehículo", "vehiculo"),
                  ("Tipo de servicio", "tipo"), ("Costo", "costo")]
        for indice, (texto, clave) in enumerate(campos):
            ttk.Label(formulario, text=texto).grid(row=0, column=indice, padx=5, sticky="w")
            estado = "readonly" if clave == "id" else "normal"
            ttk.Entry(formulario, textvariable=self.variables[clave], state=estado, width=18).grid(
                row=1, column=indice, padx=5, pady=5, sticky="ew"
            )
            formulario.columnconfigure(indice, weight=1)

        botones = ttk.Frame(contenedor)
        botones.pack(fill="x", pady=14)
        ttk.Button(botones, text="Registrar", command=self.registrar).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=4)
        ttk.Button(botones, text="Consultar", command=self.cargar_tabla).pack(side="right", padx=4)

        columnas = ("id", "cliente", "vehiculo", "tipo", "costo")
        self.tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", height=14)
        encabezados = {"id": "ID", "cliente": "Cliente", "vehiculo": "Vehículo",
                       "tipo": "Tipo de servicio", "costo": "Costo"}
        for columna in columnas:
            self.tabla.heading(columna, text=encabezados[columna])
        self.tabla.column("id", width=55, anchor="center")
        self.tabla.column("cliente", width=180)
        self.tabla.column("vehiculo", width=180)
        self.tabla.column("tipo", width=210)
        self.tabla.column("costo", width=110, anchor="e")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)
        ttk.Label(contenedor, text="Selecciona una fila para actualizarla o eliminarla.").pack(anchor="w", pady=(7, 0))

    def _datos_formulario(self):
        return (self.variables["cliente"].get(), self.variables["vehiculo"].get(),
                self.variables["tipo"].get(), self.variables["costo"].get())

    def registrar(self):
        try:
            self.controlador.registrar(*self._datos_formulario())
        except Exception as error:
            messagebox.showerror("No se pudo registrar", str(error))
        else:
            messagebox.showinfo("Registro", "Servicio registrado correctamente.")
            self.limpiar()
            self.cargar_tabla()
        finally:
            self.ventana.focus_force()

    def actualizar(self):
        try:
            if not self.variables["id"].get():
                raise ValueError("Selecciona primero un servicio de la tabla.")
            self.controlador.actualizar(self.variables["id"].get(), *self._datos_formulario())
        except Exception as error:
            messagebox.showerror("No se pudo actualizar", str(error))
        else:
            messagebox.showinfo("Actualización", "Servicio actualizado correctamente.")
            self.limpiar()
            self.cargar_tabla()
        finally:
            self.ventana.focus_force()

    def eliminar(self):
        try:
            servicio_id = self.variables["id"].get()
            if not servicio_id:
                raise ValueError("Selecciona primero un servicio de la tabla.")
            if not messagebox.askyesno("Confirmar", "¿Deseas eliminar el servicio seleccionado?"):
                return
            self.controlador.eliminar(servicio_id)
        except Exception as error:
            messagebox.showerror("No se pudo eliminar", str(error))
        else:
            messagebox.showinfo("Eliminación", "Servicio eliminado correctamente.")
            self.limpiar()
            self.cargar_tabla()
        finally:
            self.ventana.focus_force()

    def cargar_tabla(self):
        try:
            servicios = self.controlador.consultar_todos()
            for elemento in self.tabla.get_children():
                self.tabla.delete(elemento)
            for servicio in servicios:
                self.tabla.insert("", "end", values=(servicio.id, servicio.cliente, servicio.vehiculo,
                                                       servicio.tipo_servicio, f"${servicio.costo:,.2f}"))
        except Exception as error:
            messagebox.showerror("Error de conexión", f"No se pudo consultar la base de datos.\n{error}")

    def seleccionar_fila(self, _evento=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        for clave, valor in zip(("id", "cliente", "vehiculo", "tipo", "costo"), valores):
            self.variables[clave].set(str(valor).replace("$", "").replace(",", ""))

    def limpiar(self):
        for variable in self.variables.values():
            variable.set("")
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)

    def ejecutar(self):
        self.ventana.mainloop()
