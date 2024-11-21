from mi_paquete_clientes.sistema_clientes import SistemaClientes
from mi_paquete_clientes.cliente import Cliente, ClienteVIP

sistema = SistemaClientes()

while True:
    print("\n--- Menú ---")
    print("1. Registrar cliente")
    print("2. Registrar cliente VIP")
    print("3. Listar clientes")
    print("4. Buscar cliente")
    print("5. Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        nombre = input("Nombre: ")
        correo = input("Correo: ")
        direccion = input("Dirección: ")
        saldo = float(input("Saldo inicial: "))
        cliente = Cliente(nombre, correo, direccion, saldo)
        print(sistema.registrar_cliente(cliente))

    elif opcion == "2":
        nombre = input("Nombre: ")
        correo = input("Correo: ")
        direccion = input("Dirección: ")
        saldo = float(input("Saldo inicial: "))
        descuento = float(input("Descuento (0-1): "))
        cliente_vip = ClienteVIP(nombre, correo, direccion, saldo, descuento)
        print(sistema.registrar_cliente(cliente_vip))

    elif opcion == "3":
        print(sistema.listar_clientes())

    elif opcion == "4":
        correo = input("Correo del cliente: ")
        print(sistema.buscar_cliente(correo))

    elif opcion == "5":
        print("¡Hasta luego!")
        break

    else:
        print("Opción no válida.")
