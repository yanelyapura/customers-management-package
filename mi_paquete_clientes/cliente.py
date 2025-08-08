"""
Módulo de gestión de clientes para sistema de comercio electrónico.

Este módulo contiene las clases Cliente y ClienteVIP que implementan
la funcionalidad básica de gestión de clientes con diferentes niveles
de beneficios y descuentos.
"""

import re
from typing import Optional, Union
from datetime import datetime


class Cliente:
    """
    Clase base para representar un cliente en el sistema.
    
    Attributes:
        nombre (str): Nombre completo del cliente
        correo (str): Dirección de correo electrónico
        direccion (str): Dirección física del cliente
        saldo (float): Saldo disponible para compras
        fecha_registro (datetime): Fecha de registro del cliente
        activo (bool): Estado activo/inactivo del cliente
    """
    
    def __init__(self, nombre: str, correo: str, direccion: str, saldo: float = 0.0):
        """
        Inicializa un nuevo cliente.
        
        Args:
            nombre: Nombre completo del cliente
            correo: Dirección de correo electrónico válida
            direccion: Dirección física del cliente
            saldo: Saldo inicial (por defecto 0.0)
            
        Raises:
            ValueError: Si el correo no es válido o el saldo es negativo
        """
        self._validar_correo(correo)
        self._validar_saldo(saldo)
        
        self.nombre = nombre.strip().title()
        self.correo = correo.lower().strip()
        self.direccion = direccion.strip()
        self.saldo = float(saldo)
        self.fecha_registro = datetime.now()
        self.activo = True
        self._historial_compras = []
    
    @staticmethod
    def _validar_correo(correo: str) -> None:
        """Valida el formato del correo electrónico."""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, correo):
            raise ValueError("Formato de correo electrónico inválido")
    
    @staticmethod
    def _validar_saldo(saldo: Union[int, float]) -> None:
        """Valida que el saldo no sea negativo."""
        if saldo < 0:
            raise ValueError("El saldo no puede ser negativo")
    
    def realizar_compra(self, monto: float) -> str:
        """
        Realiza una compra con el saldo disponible.
        
        Args:
            monto: Cantidad a gastar en la compra
            
        Returns:
            str: Mensaje de confirmación o error
            
        Raises:
            ValueError: Si el monto es negativo
        """
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        
        if monto > self.saldo:
            return f"❌ Saldo insuficiente. Disponible: ${self.saldo:.2f}, Requerido: ${monto:.2f}"
        
        self.saldo -= monto
        compra = {
            'fecha': datetime.now(),
            'monto': monto,
            'saldo_restante': self.saldo
        }
        self._historial_compras.append(compra)
        
        return f"✅ Compra exitosa por ${monto:.2f}. Saldo restante: ${self.saldo:.2f}"
    
    def recargar_saldo(self, monto: float) -> str:
        """
        Recarga saldo en la cuenta del cliente.
        
        Args:
            monto: Cantidad a recargar
            
        Returns:
            str: Mensaje de confirmación
            
        Raises:
            ValueError: Si el monto es negativo
        """
        if monto <= 0:
            raise ValueError("El monto de recarga debe ser mayor a 0")
        
        self.saldo += monto
        return f"💰 Saldo recargado: ${monto:.2f}. Total: ${self.saldo:.2f}"
    
    def obtener_historial_compras(self) -> list:
        """Retorna el historial de compras del cliente."""
        return self._historial_compras.copy()
    
    def obtener_total_compras(self) -> float:
        """Calcula el total gastado en compras."""
        return sum(compra['monto'] for compra in self._historial_compras)
    
    def desactivar(self) -> None:
        """Desactiva la cuenta del cliente."""
        self.activo = False
    
    def activar(self) -> None:
        """Activa la cuenta del cliente."""
        self.activo = True
    
    def es_activo(self) -> bool:
        """Verifica si el cliente está activo."""
        return self.activo
    
    def obtener_antiguedad(self) -> int:
        """Retorna los días desde el registro."""
        return (datetime.now() - self.fecha_registro).days
    
    def __str__(self) -> str:
        """Representación en string del cliente."""
        estado = "🟢 Activo" if self.activo else "🔴 Inactivo"
        return (f"👤 {self.nombre} | 📧 {self.correo} | "
                f"💰 ${self.saldo:.2f} | {estado}")
    
    def __repr__(self) -> str:
        """Representación técnica del cliente."""
        return f"Cliente(nombre='{self.nombre}', correo='{self.correo}', saldo={self.saldo})"


class ClienteVIP(Cliente):
    """
    Cliente con beneficios especiales y descuentos.
    
    Attributes:
        descuento (float): Porcentaje de descuento (0.0 a 1.0)
        nivel_vip (str): Nivel VIP del cliente
    """
    
    NIVELES_VIP = {
        0.05: "Bronce",
        0.10: "Plata", 
        0.15: "Oro",
        0.20: "Platino",
        0.25: "Diamante"
    }
    
    def __init__(self, nombre: str, correo: str, direccion: str, 
                 saldo: float = 0.0, descuento: float = 0.1):
        """
        Inicializa un cliente VIP.
        
        Args:
            nombre: Nombre completo del cliente
            correo: Dirección de correo electrónico
            direccion: Dirección física del cliente
            saldo: Saldo inicial
            descuento: Porcentaje de descuento (0.0 a 1.0)
            
        Raises:
            ValueError: Si el descuento está fuera del rango válido
        """
        super().__init__(nombre, correo, direccion, saldo)
        self._validar_descuento(descuento)
        self.descuento = descuento
        self.nivel_vip = self._calcular_nivel_vip()
    
    @staticmethod
    def _validar_descuento(descuento: float) -> None:
        """Valida que el descuento esté en el rango válido."""
        if not 0 <= descuento <= 1:
            raise ValueError("El descuento debe estar entre 0 y 1")
    
    def _calcular_nivel_vip(self) -> str:
        """Calcula el nivel VIP basado en el descuento."""
        for desc, nivel in sorted(ClienteVIP.NIVELES_VIP.items(), reverse=True):
            if self.descuento >= desc:
                return nivel
        return "Bronce"
    
    def realizar_compra(self, monto: float) -> str:
        """
        Realiza una compra con descuento VIP.
        
        Args:
            monto: Cantidad original de la compra
            
        Returns:
            str: Mensaje con el descuento aplicado
        """
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        
        monto_original = monto
        monto_con_descuento = monto * (1 - self.descuento)
        ahorro = monto_original - monto_con_descuento
        
        if monto_con_descuento > self.saldo:
            return (f"❌ Saldo insuficiente. Disponible: ${self.saldo:.2f}, "
                   f"Requerido con descuento: ${monto_con_descuento:.2f}")
        
        self.saldo -= monto_con_descuento
        compra = {
            'fecha': datetime.now(),
            'monto_original': monto_original,
            'monto_final': monto_con_descuento,
            'ahorro': ahorro,
            'saldo_restante': self.saldo
        }
        self._historial_compras.append(compra)
        
        return (f"✨ Compra VIP exitosa! | Original: ${monto_original:.2f} | "
                f"Descuento: {self.descuento*100:.0f}% | Final: ${monto_con_descuento:.2f} | "
                f"Ahorro: ${ahorro:.2f} | Saldo: ${self.saldo:.2f}")
    
    def obtener_ahorro_total(self) -> float:
        """Calcula el total ahorrado por descuentos VIP."""
        return sum(compra.get('ahorro', 0) for compra in self._historial_compras)
    
    def actualizar_descuento(self, nuevo_descuento: float) -> str:
        """
        Actualiza el descuento VIP del cliente.
        
        Args:
            nuevo_descuento: Nuevo porcentaje de descuento
            
        Returns:
            str: Mensaje de confirmación
        """
        self._validar_descuento(nuevo_descuento)
        descuento_anterior = self.descuento
        self.descuento = nuevo_descuento
        self.nivel_vip = self._calcular_nivel_vip()
        
        return (f"🎯 Descuento actualizado: {descuento_anterior*100:.0f}% → "
                f"{self.descuento*100:.0f}% | Nuevo nivel: {self.nivel_vip}")
    
    def __str__(self) -> str:
        """Representación en string del cliente VIP."""
        estado = "🟢 Activo" if self.activo else "🔴 Inactivo"
        return (f"👑 {self.nombre} (VIP {self.nivel_vip}) | 📧 {self.correo} | "
                f"💰 ${self.saldo:.2f} | 🎯 {self.descuento*100:.0f}% desc. | {estado}")
    
    def __repr__(self) -> str:
        """Representación técnica del cliente VIP."""
        return (f"ClienteVIP(nombre='{self.nombre}', correo='{self.correo}', "
                f"saldo={self.saldo}, descuento={self.descuento})")
