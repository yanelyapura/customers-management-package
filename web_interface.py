"""
Interfaz web para el Sistema de Gestión de Clientes.

Esta aplicación web demuestra las funcionalidades del paquete
mi_paquete_clientes de manera visual e interactiva.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from mi_paquete_clientes.sistema_clientes import SistemaClientes
from mi_paquete_clientes.cliente import Cliente, ClienteVIP
import json

app = Flask(__name__)
sistema = SistemaClientes("clientes_web.json")

@app.route('/')
def index():
    """Página principal con estadísticas del sistema."""
    stats = sistema.obtener_estadisticas()
    return render_template('index.html', stats=stats)

@app.route('/clientes')
def listar_clientes():
    """Lista todos los clientes."""
    clientes = sistema.listar_clientes(solo_activos=False)
    return render_template('clientes.html', clientes=clientes)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar_cliente():
    """Formulario para registrar un nuevo cliente."""
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            correo = request.form['correo']
            direccion = request.form['direccion']
            saldo = float(request.form['saldo'])
            tipo = request.form['tipo']
            
            if tipo == 'vip':
                descuento = float(request.form['descuento'])
                cliente = ClienteVIP(nombre, correo, direccion, saldo, descuento)
            else:
                cliente = Cliente(nombre, correo, direccion, saldo)
            
            resultado = sistema.registrar_cliente(cliente)
            return jsonify({'success': True, 'message': resultado})
            
        except ValueError as e:
            return jsonify({'success': False, 'message': str(e)})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'})
    
    return render_template('registrar.html')

@app.route('/buscar')
def buscar_cliente():
    """Busca un cliente por correo."""
    correo = request.args.get('correo', '')
    if correo:
        cliente = sistema.buscar_cliente(correo)
        if cliente:
            return render_template('cliente_detalle.html', cliente=cliente)
        else:
            return render_template('buscar.html', error="Cliente no encontrado")
    
    return render_template('buscar.html')

@app.route('/api/estadisticas')
def api_estadisticas():
    """API endpoint para obtener estadísticas."""
    return jsonify(sistema.obtener_estadisticas())

@app.route('/api/clientes')
def api_clientes():
    """API endpoint para obtener lista de clientes."""
    clientes = sistema.listar_clientes(solo_activos=False)
    return jsonify([{
        'nombre': c.nombre,
        'correo': c.correo,
        'saldo': c.saldo,
        'activo': c.es_activo(),
        'tipo': 'VIP' if isinstance(c, ClienteVIP) else 'Regular',
        'fecha_registro': c.fecha_registro.strftime('%Y-%m-%d %H:%M')
    } for c in clientes])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
