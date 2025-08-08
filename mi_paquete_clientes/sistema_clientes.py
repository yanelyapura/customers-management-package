"""
Sistema de gestión de clientes para comercio electrónico.

Este módulo proporciona la clase SistemaClientes que maneja la gestión
completa de clientes, incluyendo registro, búsqueda, estadísticas y
persistencia de datos.
"""

import json
import os
from typing import Dict, List, Optional, Union
from datetime import datetime
from mi_paquete_clientes.cliente import Cliente, ClienteVIP


class SistemaClientes:
    """
    Sistema completo de gestión de clientes.
    
    Attributes:
        clientes (Dict): Diccionario de clientes indexado por correo
        archivo_datos (str): Ruta del archivo de persistencia
    """
    
    def __init__(self, archivo_datos: str = "clientes.json"):
        """
        Inicializa el sistema de clientes.
        
        Args:
            archivo_datos: Ruta del archivo para persistir datos
        """
        self.clientes: Dict[str, Union[Cliente, ClienteVIP]] = {}
        self.archivo_datos = archivo_datos
        self._cargar_datos()
    
    def registrar_cliente(self, cliente: Union[Cliente, ClienteVIP]) -> str:
        """
        Registra un nuevo cliente en el sistema.
        
        Args:
            cliente: Instancia de Cliente o ClienteVIP
            
        Returns:
            str: Mensaje de confirmación o error
            
        Raises:
            ValueError: Si el cliente ya existe
        """
        if cliente.correo in self.clientes:
            return f"❌ El cliente con correo {cliente.correo} ya está registrado."
        
        self.clientes[cliente.correo] = cliente
        self._guardar_datos()
        
        tipo = "VIP" if isinstance(cliente, ClienteVIP) else "Regular"
        return f"✅ Cliente {tipo} '{cliente.nombre}' registrado exitosamente."
    
    def buscar_cliente(self, correo: str) -> Optional[Union[Cliente, ClienteVIP]]:
        """
        Busca un cliente por su correo electrónico.
        
        Args:
            correo: Correo electrónico del cliente
            
        Returns:
            Cliente o ClienteVIP si se encuentra, None en caso contrario
        """
        return self.clientes.get(correo.lower().strip())
    
    def listar_clientes(self, solo_activos: bool = True) -> List[Union[Cliente, ClienteVIP]]:
        """
        Lista todos los clientes del sistema.
        
        Args:
            solo_activos: Si True, solo retorna clientes activos
            
        Returns:
            Lista de clientes
        """
        if solo_activos:
            return [cliente for cliente in self.clientes.values() if cliente.es_activo()]
        return list(self.clientes.values())
    
    def listar_clientes_vip(self) -> List[ClienteVIP]:
        """Retorna solo los clientes VIP."""
        return [cliente for cliente in self.clientes.values() 
                if isinstance(cliente, ClienteVIP) and cliente.es_activo()]
    
    def eliminar_cliente(self, correo: str) -> str:
        """
        Elimina un cliente del sistema.
        
        Args:
            correo: Correo electrónico del cliente
            
        Returns:
            str: Mensaje de confirmación o error
        """
        cliente = self.buscar_cliente(correo)
        if not cliente:
            return f"❌ Cliente con correo {correo} no encontrado."
        
        del self.clientes[correo]
        self._guardar_datos()
        return f"🗑️ Cliente '{cliente.nombre}' eliminado exitosamente."
    
    def desactivar_cliente(self, correo: str) -> str:
        """
        Desactiva un cliente (no lo elimina).
        
        Args:
            correo: Correo electrónico del cliente
            
        Returns:
            str: Mensaje de confirmación o error
        """
        cliente = self.buscar_cliente(correo)
        if not cliente:
            return f"❌ Cliente con correo {correo} no encontrado."
        
        cliente.desactivar()
        self._guardar_datos()
        return f"🔴 Cliente '{cliente.nombre}' desactivado."
    
    def activar_cliente(self, correo: str) -> str:
        """
        Activa un cliente previamente desactivado.
        
        Args:
            correo: Correo electrónico del cliente
            
        Returns:
            str: Mensaje de confirmación o error
        """
        cliente = self.buscar_cliente(correo)
        if not cliente:
            return f"❌ Cliente con correo {correo} no encontrado."
        
        cliente.activar()
        self._guardar_datos()
        return f"🟢 Cliente '{cliente.nombre}' activado."
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas del sistema de clientes.
        
        Returns:
            Diccionario con estadísticas del sistema
        """
        total_clientes = len(self.clientes)
        clientes_activos = len([c for c in self.clientes.values() if c.es_activo()])
        clientes_vip = len(self.listar_clientes_vip())
        
        saldo_total = sum(c.saldo for c in self.clientes.values())
        total_compras = sum(c.obtener_total_compras() for c in self.clientes.values())
        
        # Estadísticas VIP
        ahorro_total_vip = sum(c.obtener_ahorro_total() for c in self.listar_clientes_vip())
        
        return {
            "total_clientes": total_clientes,
            "clientes_activos": clientes_activos,
            "clientes_inactivos": total_clientes - clientes_activos,
            "clientes_vip": clientes_vip,
            "clientes_regular": total_clientes - clientes_vip,
            "saldo_total_sistema": saldo_total,
            "total_compras_sistema": total_compras,
            "ahorro_total_vip": ahorro_total_vip,
            "promedio_saldo": saldo_total / total_clientes if total_clientes > 0 else 0,
            "promedio_compras": total_compras / total_clientes if total_clientes > 0 else 0
        }
    
    def buscar_por_nombre(self, nombre: str) -> List[Union[Cliente, ClienteVIP]]:
        """
        Busca clientes por nombre (búsqueda parcial).
        
        Args:
            nombre: Nombre o parte del nombre a buscar
            
        Returns:
            Lista de clientes que coinciden
        """
        nombre_lower = nombre.lower()
        return [cliente for cliente in self.clientes.values() 
                if nombre_lower in cliente.nombre.lower()]
    
    def clientes_con_mayor_saldo(self, limite: int = 5) -> List[Union[Cliente, ClienteVIP]]:
        """
        Retorna los clientes con mayor saldo.
        
        Args:
            limite: Número máximo de clientes a retornar
            
        Returns:
            Lista de clientes ordenados por saldo
        """
        return sorted(self.clientes.values(), key=lambda x: x.saldo, reverse=True)[:limite]
    
    def clientes_mas_antiguos(self, limite: int = 5) -> List[Union[Cliente, ClienteVIP]]:
        """
        Retorna los clientes más antiguos.
        
        Args:
            limite: Número máximo de clientes a retornar
            
        Returns:
            Lista de clientes ordenados por fecha de registro
        """
        return sorted(self.clientes.values(), key=lambda x: x.fecha_registro)[:limite]
    
    def _cargar_datos(self) -> None:
        """Carga los datos desde el archivo de persistencia."""
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                for correo, cliente_data in datos.items():
                    if cliente_data['tipo'] == 'VIP':
                        cliente = ClienteVIP(
                            cliente_data['nombre'],
                            cliente_data['correo'],
                            cliente_data['direccion'],
                            cliente_data['saldo'],
                            cliente_data['descuento']
                        )
                    else:
                        cliente = Cliente(
                            cliente_data['nombre'],
                            cliente_data['correo'],
                            cliente_data['direccion'],
                            cliente_data['saldo']
                        )
                    
                    # Restaurar estado
                    cliente.fecha_registro = datetime.fromisoformat(cliente_data['fecha_registro'])
                    cliente.activo = cliente_data['activo']
                    
                    self.clientes[correo] = cliente
                    
            except Exception as e:
                print(f"⚠️ Error al cargar datos: {e}")
    
    def _guardar_datos(self) -> None:
        """Guarda los datos en el archivo de persistencia."""
        try:
            datos = {}
            for correo, cliente in self.clientes.items():
                cliente_data = {
                    'nombre': cliente.nombre,
                    'correo': cliente.correo,
                    'direccion': cliente.direccion,
                    'saldo': cliente.saldo,
                    'fecha_registro': cliente.fecha_registro.isoformat(),
                    'activo': cliente.activo,
                    'tipo': 'VIP' if isinstance(cliente, ClienteVIP) else 'Regular'
                }
                
                if isinstance(cliente, ClienteVIP):
                    cliente_data['descuento'] = cliente.descuento
                    cliente_data['nivel_vip'] = cliente.nivel_vip
                
                datos[correo] = cliente_data
            
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ Error al guardar datos: {e}")
    
    def __str__(self) -> str:
        """Representación en string del sistema."""
        stats = self.obtener_estadisticas()
        return (f"📊 Sistema de Clientes | Total: {stats['total_clientes']} | "
                f"Activos: {stats['clientes_activos']} | VIP: {stats['clientes_vip']}")
    
    def __repr__(self) -> str:
        """Representación técnica del sistema."""
        return f"SistemaClientes(archivo_datos='{self.archivo_datos}')"
