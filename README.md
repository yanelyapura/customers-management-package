# 👥 Sistema de Gestión de Clientes

Un paquete Python completo y profesional para la gestión de clientes en sistemas de comercio electrónico, con soporte para clientes regulares y VIP, persistencia de datos y múltiples interfaces.

## ✨ Características

### 🎯 Funcionalidades Principales
- **Gestión de Clientes**: Registro, búsqueda, actualización y eliminación
- **Sistema VIP**: Clientes con descuentos y beneficios especiales
- **Persistencia de Datos**: Almacenamiento automático en JSON
- **Validaciones**: Verificación de correos electrónicos y datos
- **Estadísticas**: Métricas completas del sistema
- **Interfaz Web**: Dashboard moderno con Flask
- **Interfaz CLI**: Consola interactiva con colores

### 🏆 Niveles VIP
- **Bronce**: 5% descuento
- **Plata**: 10% descuento  
- **Oro**: 15% descuento
- **Platino**: 20% descuento
- **Diamante**: 25% descuento

## 🚀 Instalación

### Instalación del Paquete
```bash
# Clonar el repositorio
git clone https://github.com/yanelyapura/customers-management-package.git
cd customers-management-package

# Instalar dependencias
pip install -r requirements.txt

# Instalar el paquete en modo desarrollo
pip install -e .
```

### Dependencias
```bash
pip install flask
```

## 📖 Uso

### Interfaz de Consola
```bash
python main.py
```

### Interfaz Web
```bash
python web_interface.py
# Luego abrir http://127.0.0.1:5000
```

### Uso Programático
```python
from mi_paquete_clientes.sistema_clientes import SistemaClientes
from mi_paquete_clientes.cliente import Cliente, ClienteVIP

# Crear sistema
sistema = SistemaClientes()

# Registrar cliente regular
cliente = Cliente("Juan Pérez", "juan@email.com", "Calle 123", 100.0)
sistema.registrar_cliente(cliente)

# Registrar cliente VIP
cliente_vip = ClienteVIP("María García", "maria@email.com", "Av. 456", 200.0, 0.15)
sistema.registrar_cliente(cliente_vip)

# Realizar compra
resultado = cliente_vip.realizar_compra(50.0)
print(resultado)  # ✨ Compra VIP exitosa! | Original: $50.00 | Descuento: 15% | Final: $42.50

# Ver estadísticas
stats = sistema.obtener_estadisticas()
print(f"Total clientes: {stats['total_clientes']}")
```

## 🏗️ Estructura del Proyecto

```
customers-management-package/
├── mi_paquete_clientes/
│   ├── __init__.py
│   ├── cliente.py          # Clases Cliente y ClienteVIP
│   └── sistema_clientes.py # Sistema de gestión
├── templates/              # Plantillas HTML
│   ├── base.html
│   └── index.html
├── web_interface.py        # Interfaz web con Flask
├── main.py                 # Interfaz de consola
├── setup.py               # Configuración del paquete
├── requirements.txt        # Dependencias
└── README.md              # Documentación
```

## 🔧 API del Paquete

### Clase Cliente
```python
class Cliente:
    def __init__(self, nombre: str, correo: str, direccion: str, saldo: float = 0.0)
    def realizar_compra(self, monto: float) -> str
    def recargar_saldo(self, monto: float) -> str
    def obtener_historial_compras(self) -> list
    def obtener_total_compras(self) -> float
    def desactivar(self) -> None
    def activar(self) -> None
    def es_activo(self) -> bool
    def obtener_antiguedad(self) -> int
```

### Clase ClienteVIP
```python
class ClienteVIP(Cliente):
    def __init__(self, nombre: str, correo: str, direccion: str, saldo: float = 0.0, descuento: float = 0.1)
    def obtener_ahorro_total(self) -> float
    def actualizar_descuento(self, nuevo_descuento: float) -> str
```

### Clase SistemaClientes
```python
class SistemaClientes:
    def __init__(self, archivo_datos: str = "clientes.json")
    def registrar_cliente(self, cliente) -> str
    def buscar_cliente(self, correo: str) -> Optional[Cliente]
    def listar_clientes(self, solo_activos: bool = True) -> List[Cliente]
    def listar_clientes_vip(self) -> List[ClienteVIP]
    def eliminar_cliente(self, correo: str) -> str
    def desactivar_cliente(self, correo: str) -> str
    def activar_cliente(self, correo: str) -> str
    def obtener_estadisticas(self) -> Dict
    def buscar_por_nombre(self, nombre: str) -> List[Cliente]
    def clientes_con_mayor_saldo(self, limite: int = 5) -> List[Cliente]
    def clientes_mas_antiguos(self, limite: int = 5) -> List[Cliente]
```

## 🎨 Interfaz Web

### Características del Dashboard
- **Estadísticas en tiempo real**
- **Gestión visual de clientes**
- **Formularios de registro**
- **Búsqueda avanzada**
- **Diseño responsive**

### Endpoints API
- `GET /api/estadisticas` - Obtener estadísticas del sistema
- `GET /api/clientes` - Listar todos los clientes
- `POST /registrar` - Registrar nuevo cliente
- `GET /buscar` - Buscar cliente por correo

## 📊 Estadísticas Disponibles

```python
{
    "total_clientes": 25,
    "clientes_activos": 23,
    "clientes_inactivos": 2,
    "clientes_vip": 8,
    "clientes_regular": 17,
    "saldo_total_sistema": 1250.50,
    "total_compras_sistema": 3450.75,
    "ahorro_total_vip": 450.25,
    "promedio_saldo": 50.02,
    "promedio_compras": 138.03
}
```

## 🔒 Validaciones

### Correo Electrónico
- Formato válido de email
- Conversión automática a minúsculas
- Eliminación de espacios

### Saldo
- No puede ser negativo
- Conversión automática a float
- Validación de montos de compra

### Descuentos VIP
- Rango válido: 0.05 a 0.25 (5% a 25%)
- Cálculo automático de nivel VIP
- Validación de rangos

## 🧪 Ejemplos de Uso

### Ejemplo 1: Sistema Básico
```python
from mi_paquete_clientes.sistema_clientes import SistemaClientes
from mi_paquete_clientes.cliente import Cliente

sistema = SistemaClientes()

# Registrar cliente
cliente = Cliente("Ana López", "ana@email.com", "Calle Principal 123", 100.0)
print(sistema.registrar_cliente(cliente))

# Realizar compra
resultado = cliente.realizar_compra(25.0)
print(resultado)  # ✅ Compra exitosa por $25.00. Saldo restante: $75.00
```

### Ejemplo 2: Cliente VIP
```python
from mi_paquete_clientes.cliente import ClienteVIP

# Crear cliente VIP con 15% descuento
cliente_vip = ClienteVIP("Carlos Ruiz", "carlos@email.com", "Av. Central 456", 200.0, 0.15)

# Realizar compra con descuento
resultado = cliente_vip.realizar_compra(100.0)
print(resultado)  # ✨ Compra VIP exitosa! | Original: $100.00 | Descuento: 15% | Final: $85.00
```

### Ejemplo 3: Estadísticas
```python
# Obtener estadísticas completas
stats = sistema.obtener_estadisticas()

print(f"Total de clientes: {stats['total_clientes']}")
print(f"Clientes VIP: {stats['clientes_vip']}")
print(f"Saldo total del sistema: ${stats['saldo_total_sistema']:.2f}")
print(f"Ahorro total VIP: ${stats['ahorro_total_vip']:.2f}")
```

## 🛠️ Desarrollo

### Instalación para Desarrollo
```bash
# Clonar repositorio
git clone https://github.com/yanelyapura/customers-management-package.git
cd customers-management-package

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
pip install -e .
```

### Ejecutar Tests
```bash
python -m pytest tests/
```

### Ejecutar Linter
```bash
flake8 mi_paquete_clientes/
```

## 📝 Changelog

### v2.0.0 (2025-01-XX)
- ✨ Interfaz web completa con Flask
- 🎨 Interfaz CLI mejorada con colores
- 📊 Sistema de estadísticas avanzado
- 💾 Persistencia de datos automática
- 🔒 Validaciones robustas
- 👑 Sistema VIP con niveles
- 📈 Historial de compras
- 🎯 Cálculo de ahorros VIP

### v1.0.0 (2024-XX-XX)
- 🎉 Versión inicial del paquete
- 👤 Gestión básica de clientes
- 👑 Soporte para clientes VIP
- 💰 Sistema de compras y saldo

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Yanel Yapura** - Desarrollador Full Stack
- Portfolio: [yanelyapura.github.io](https://yanelyapura.github.io)
- LinkedIn: [Yanel Yapura](https://linkedin.com/in/yanelyapura)
- Email: yanelyapura@gmail.com

## 🙏 Agradecimientos

- Python Software Foundation
- Flask Development Team
- Bootstrap Team
- Comunidad de desarrolladores

---

*Desarrollado con ❤️ y mucho ☕*
