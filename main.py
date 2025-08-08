"""
Interfaz de consola para el Sistema de Gestión de Clientes.

Este script proporciona una interfaz interactiva para gestionar clientes
desde la línea de comandos con una experiencia de usuario mejorada.
"""

import os
import sys
from datetime import datetime
from mi_paquete_clientes.sistema_clientes import SistemaClientes
from mi_paquete_clientes.cliente import Cliente, ClienteVIP

# Colores para la consola
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Imprime el encabezado del sistema."""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 60)
    print("    SISTEMA DE GESTIÓN DE CLIENTES - v2.0")
    print("=" * 60)
    print(f"{Colors.ENDC}")

def print_menu():
    """Imprime el menú principal."""
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}📋 MENÚ PRINCIPAL{Colors.ENDC}")
    print("1. 👤 Registrar cliente regular")
    print("2. 👑 Registrar cliente VIP")
    print("3. 📋 Listar todos los clientes")
    print("4. 🔍 Buscar cliente por correo")
    print("5. 📊 Ver estadísticas del sistema")
    print("6. 💰 Realizar compra")
    print("7. 💳 Recargar saldo")
    print("8. 🗑️ Eliminar cliente")
    print("9. 🔄 Activar/Desactivar cliente")
    print("10. 🏆 Top clientes con mayor saldo")
    print("11. 🌐 Abrir interfaz web")
    print("0. 🚪 Salir")
    print("-" * 40)

def obtener_datos_cliente():
    """Obtiene los datos básicos de un cliente."""
    print(f"\n{Colors.OKCYAN}📝 Ingrese los datos del cliente:{Colors.ENDC}")
    
    nombre = input("Nombre completo: ").strip()
    while not nombre:
        print(f"{Colors.FAIL}❌ El nombre no puede estar vacío{Colors.ENDC}")
        nombre = input("Nombre completo: ").strip()
    
    correo = input("Correo electrónico: ").strip()
    while not correo:
        print(f"{Colors.FAIL}❌ El correo no puede estar vacío{Colors.ENDC}")
        correo = input("Correo electrónico: ").strip()
    
    direccion = input("Dirección: ").strip()
    while not direccion:
        print(f"{Colors.FAIL}❌ La dirección no puede estar vacía{Colors.ENDC}")
        direccion = input("Dirección: ").strip()
    
    while True:
        try:
            saldo = float(input("Saldo inicial: $"))
            if saldo < 0:
                print(f"{Colors.FAIL}❌ El saldo no puede ser negativo{Colors.ENDC}")
                continue
            break
        except ValueError:
            print(f"{Colors.FAIL}❌ Ingrese un número válido{Colors.ENDC}")
    
    return nombre, correo, direccion, saldo

def registrar_cliente_regular(sistema):
    """Registra un cliente regular."""
    try:
        nombre, correo, direccion, saldo = obtener_datos_cliente()
        cliente = Cliente(nombre, correo, direccion, saldo)
        resultado = sistema.registrar_cliente(cliente)
        print(f"{Colors.OKGREEN}{resultado}{Colors.ENDC}")
    except ValueError as e:
        print(f"{Colors.FAIL}❌ Error: {e}{Colors.ENDC}")

def registrar_cliente_vip(sistema):
    """Registra un cliente VIP."""
    try:
        nombre, correo, direccion, saldo = obtener_datos_cliente()
        
        print(f"\n{Colors.OKCYAN}👑 Configuración VIP:{Colors.ENDC}")
        print("Niveles disponibles:")
        print("• Bronce: 5% descuento")
        print("• Plata: 10% descuento")
        print("• Oro: 15% descuento")
        print("• Platino: 20% descuento")
        print("• Diamante: 25% descuento")
        
        while True:
            try:
                descuento = float(input("Descuento (0.05 a 0.25): "))
                if 0.05 <= descuento <= 0.25:
                    break
                else:
                    print(f"{Colors.FAIL}❌ El descuento debe estar entre 0.05 y 0.25{Colors.ENDC}")
            except ValueError:
                print(f"{Colors.FAIL}❌ Ingrese un número válido{Colors.ENDC}")
        
        cliente = ClienteVIP(nombre, correo, direccion, saldo, descuento)
        resultado = sistema.registrar_cliente(cliente)
        print(f"{Colors.OKGREEN}{resultado}{Colors.ENDC}")
    except ValueError as e:
        print(f"{Colors.FAIL}❌ Error: {e}{Colors.ENDC}")

def listar_clientes(sistema):
    """Lista todos los clientes."""
    clientes = sistema.listar_clientes(solo_activos=False)
    
    if not clientes:
        print(f"{Colors.WARNING}📭 No hay clientes registrados{Colors.ENDC}")
        return
    
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}📋 LISTA DE CLIENTES{Colors.ENDC}")
    print("=" * 80)
    
    for i, cliente in enumerate(clientes, 1):
        estado = "🟢" if cliente.es_activo() else "🔴"
        tipo = "👑 VIP" if isinstance(cliente, ClienteVIP) else "👤 Regular"
        
        print(f"{i}. {estado} {tipo} | {cliente}")
        
        if isinstance(cliente, ClienteVIP):
            print(f"   🎯 Nivel: {cliente.nivel_vip} | Ahorro total: ${cliente.obtener_ahorro_total():.2f}")
        
        print(f"   📅 Registrado: {cliente.fecha_registro.strftime('%Y-%m-%d %H:%M')}")
        print(f"   📍 Dirección: {cliente.direccion}")
        print("-" * 80)

def buscar_cliente(sistema):
    """Busca un cliente por correo."""
    correo = input("Ingrese el correo del cliente: ").strip()
    
    if not correo:
        print(f"{Colors.FAIL}❌ Debe ingresar un correo{Colors.ENDC}")
        return
    
    cliente = sistema.buscar_cliente(correo)
    
    if cliente:
        print(f"\n{Colors.OKGREEN}✅ CLIENTE ENCONTRADO{Colors.ENDC}")
        print("=" * 50)
        print(f"👤 {cliente.nombre}")
        print(f"📧 {cliente.correo}")
        print(f"💰 Saldo: ${cliente.saldo:.2f}")
        print(f"📅 Registrado: {cliente.fecha_registro.strftime('%Y-%m-%d %H:%M')}")
        print(f"📍 Dirección: {cliente.direccion}")
        print(f"🔄 Estado: {'Activo' if cliente.es_activo() else 'Inactivo'}")
        
        if isinstance(cliente, ClienteVIP):
            print(f"👑 Nivel VIP: {cliente.nivel_vip}")
            print(f"🎯 Descuento: {cliente.descuento*100:.0f}%")
            print(f"💰 Ahorro total: ${cliente.obtener_ahorro_total():.2f}")
        
        print(f"📊 Total compras: ${cliente.obtener_total_compras():.2f}")
        print(f"📈 Antigüedad: {cliente.obtener_antiguedad()} días")
    else:
        print(f"{Colors.FAIL}❌ Cliente no encontrado{Colors.ENDC}")

def mostrar_estadisticas(sistema):
    """Muestra las estadísticas del sistema."""
    stats = sistema.obtener_estadisticas()
    
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}📊 ESTADÍSTICAS DEL SISTEMA{Colors.ENDC}")
    print("=" * 50)
    print(f"👥 Total clientes: {stats['total_clientes']}")
    print(f"🟢 Clientes activos: {stats['clientes_activos']}")
    print(f"🔴 Clientes inactivos: {stats['clientes_inactivos']}")
    print(f"👑 Clientes VIP: {stats['clientes_vip']}")
    print(f"👤 Clientes regulares: {stats['clientes_regular']}")
    print(f"💰 Saldo total: ${stats['saldo_total_sistema']:.2f}")
    print(f"🛒 Total compras: ${stats['total_compras_sistema']:.2f}")
    print(f"🎯 Ahorro VIP: ${stats['ahorro_total_vip']:.2f}")
    print(f"📈 Promedio saldo: ${stats['promedio_saldo']:.2f}")
    print(f"📊 Promedio compras: ${stats['promedio_compras']:.2f}")

def realizar_compra(sistema):
    """Realiza una compra para un cliente."""
    correo = input("Correo del cliente: ").strip()
    cliente = sistema.buscar_cliente(correo)
    
    if not cliente:
        print(f"{Colors.FAIL}❌ Cliente no encontrado{Colors.ENDC}")
        return
    
    try:
        monto = float(input("Monto de la compra: $"))
        if monto <= 0:
            print(f"{Colors.FAIL}❌ El monto debe ser mayor a 0{Colors.ENDC}")
            return
        
        resultado = cliente.realizar_compra(monto)
        print(f"{Colors.OKGREEN}{resultado}{Colors.ENDC}")
        sistema._guardar_datos()
    except ValueError as e:
        print(f"{Colors.FAIL}❌ Error: {e}{Colors.ENDC}")

def recargar_saldo(sistema):
    """Recarga saldo a un cliente."""
    correo = input("Correo del cliente: ").strip()
    cliente = sistema.buscar_cliente(correo)
    
    if not cliente:
        print(f"{Colors.FAIL}❌ Cliente no encontrado{Colors.ENDC}")
        return
    
    try:
        monto = float(input("Monto a recargar: $"))
        if monto <= 0:
            print(f"{Colors.FAIL}❌ El monto debe ser mayor a 0{Colors.ENDC}")
            return
        
        resultado = cliente.recargar_saldo(monto)
        print(f"{Colors.OKGREEN}{resultado}{Colors.ENDC}")
        sistema._guardar_datos()
    except ValueError as e:
        print(f"{Colors.FAIL}❌ Error: {e}{Colors.ENDC}")

def eliminar_cliente(sistema):
    """Elimina un cliente del sistema."""
    correo = input("Correo del cliente a eliminar: ").strip()
    resultado = sistema.eliminar_cliente(correo)
    print(f"{Colors.OKGREEN}{resultado}{Colors.ENDC}")

def gestionar_estado_cliente(sistema):
    """Activa o desactiva un cliente."""
    correo = input("Correo del cliente: ").strip()
    cliente = sistema.buscar_cliente(correo)
    
    if not cliente:
        print(f"{Colors.FAIL}❌ Cliente no encontrado{Colors.ENDC}")
        return
    
    if cliente.es_activo():
        resultado = sistema.desactivar_cliente(correo)
    else:
        resultado = sistema.activar_cliente(correo)
    
    print(f"{Colors.OKGREEN}{resultado}{Colors.ENDC}")

def top_clientes_saldo(sistema):
    """Muestra los clientes con mayor saldo."""
    top_clientes = sistema.clientes_con_mayor_saldo(5)
    
    if not top_clientes:
        print(f"{Colors.WARNING}📭 No hay clientes registrados{Colors.ENDC}")
        return
    
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}🏆 TOP 5 CLIENTES CON MAYOR SALDO{Colors.ENDC}")
    print("=" * 60)
    
    for i, cliente in enumerate(top_clientes, 1):
        tipo = "👑 VIP" if isinstance(cliente, ClienteVIP) else "👤 Regular"
        print(f"{i}. {tipo} | {cliente.nombre} | ${cliente.saldo:.2f}")

def abrir_interfaz_web():
    """Abre la interfaz web."""
    try:
        import webbrowser
        import threading
        import time
        
        print(f"{Colors.OKCYAN}🌐 Iniciando servidor web...{Colors.ENDC}")
        
        # Iniciar servidor en un hilo separado
        def start_server():
            from web_interface import app
            app.run(debug=False, host='127.0.0.1', port=5000)
        
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Esperar un momento para que el servidor inicie
        time.sleep(2)
        
        # Abrir navegador
        webbrowser.open('http://127.0.0.1:5000')
        print(f"{Colors.OKGREEN}✅ Interfaz web abierta en http://127.0.0.1:5000{Colors.ENDC}")
        print(f"{Colors.WARNING}💡 Presiona Ctrl+C para detener el servidor{Colors.ENDC}")
        
        # Mantener el programa corriendo
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Colors.OKGREEN}👋 Servidor detenido{Colors.ENDC}")
            
    except ImportError:
        print(f"{Colors.FAIL}❌ Error: Flask no está instalado. Instala con: pip install flask{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}❌ Error al iniciar la interfaz web: {e}{Colors.ENDC}")

def main():
    """Función principal del programa."""
    sistema = SistemaClientes()
    
    print_header()
    
    while True:
        print_menu()
        
        try:
            opcion = input(f"{Colors.OKCYAN}Selecciona una opción: {Colors.ENDC}").strip()
            
            if opcion == "1":
                registrar_cliente_regular(sistema)
            elif opcion == "2":
                registrar_cliente_vip(sistema)
            elif opcion == "3":
                listar_clientes(sistema)
            elif opcion == "4":
                buscar_cliente(sistema)
            elif opcion == "5":
                mostrar_estadisticas(sistema)
            elif opcion == "6":
                realizar_compra(sistema)
            elif opcion == "7":
                recargar_saldo(sistema)
            elif opcion == "8":
                eliminar_cliente(sistema)
            elif opcion == "9":
                gestionar_estado_cliente(sistema)
            elif opcion == "10":
                top_clientes_saldo(sistema)
            elif opcion == "11":
                abrir_interfaz_web()
            elif opcion == "0":
                print(f"\n{Colors.OKGREEN}👋 ¡Hasta luego!{Colors.ENDC}")
                break
            else:
                print(f"{Colors.FAIL}❌ Opción no válida{Colors.ENDC}")
                
        except KeyboardInterrupt:
            print(f"\n{Colors.OKGREEN}👋 ¡Hasta luego!{Colors.ENDC}")
            break
        except Exception as e:
            print(f"{Colors.FAIL}❌ Error inesperado: {e}{Colors.ENDC}")

if __name__ == "__main__":
    main()
