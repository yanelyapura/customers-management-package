"""
Interfaz web para el Sistema de Gestión de Clientes.

Esta aplicación web demuestra las funcionalidades del paquete
mi_paquete_clientes de manera visual e interactiva.
"""

from flask import Flask, redirect, url_for
import webbrowser
import threading
import time

app = Flask(__name__)

@app.route('/')
def index():
    """Redirige a la demo de GitHub Pages."""
    return redirect('https://yanelyapura.github.io/customers-management-package/', code=302)

@app.route('/demo')
def demo():
    """Redirige a la demo de GitHub Pages."""
    return redirect('https://yanelyapura.github.io/customers-management-package/', code=302)

@app.route('/health')
def health():
    """Endpoint de salud para verificar que el servidor está funcionando."""
    return {'status': 'ok', 'message': 'Sistema de Gestión de Clientes funcionando correctamente'}

def abrir_navegador():
    """Abre el navegador después de un breve delay."""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    print("🚀 Iniciando Sistema de Gestión de Clientes...")
    print("📱 Abriendo navegador automáticamente...")
    print("🌐 Demo disponible en: https://yanelyapura.github.io/customers-management-package/")
    print("🔧 Servidor local en: http://127.0.0.1:5000")
    print("⏹️  Presiona Ctrl+C para detener")
    
    # Abrir navegador en un hilo separado
    threading.Thread(target=abrir_navegador, daemon=True).start()
    
    # Iniciar servidor
    app.run(debug=True, host='0.0.0.0', port=5000)
