class Cliente:
    def __init__(self, nombre, correo, direccion, saldo=0):
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion
        self.saldo = saldo

    def realizar_compra(self, monto):
        if monto > self.saldo:
            return f"No tienes suficiente saldo. Saldo disponible: {self.saldo}"
        self.saldo -= monto
        return f"Compra realizada por {monto}. Saldo restante: {self.saldo}"

    def recargar_saldo(self, monto):
        self.saldo += monto
        return f"Saldo recargado. Saldo actual: {self.saldo}"

    def __str__(self):
        return f"Cliente: {self.nombre}, Correo: {self.correo}, Saldo: {self.saldo}"


class ClienteVIP(Cliente):
    def __init__(self, nombre, correo, direccion, saldo=0, descuento=0.1):
        super().__init__(nombre, correo, direccion, saldo)
        self.descuento = descuento

    def realizar_compra(self, monto):
        monto_con_descuento = monto * (1 - self.descuento)
        return super().realizar_compra(monto_con_descuento)

    def __str__(self):
        return super().__str__() + f", Descuento: {self.descuento * 100}%"
