from mi_paquete_clientes.cliente import Cliente, ClienteVIP

class SistemaClientes:
    def __init__(self):
        self.clientes = {}

    def registrar_cliente(self, cliente):
        if cliente.correo in self.clientes:
            return "Cliente ya registrado."
        self.clientes[cliente.correo] = cliente
        return f"Cliente {cliente.nombre} registrado exitosamente."

    def listar_clientes(self):
        if not self.clientes:
            return "No hay clientes registrados."
        return "\n".join(str(cliente) for cliente in self.clientes.values())

    def buscar_cliente(self, correo):
        return self.clientes.get(correo, "Cliente no encontrado.")
