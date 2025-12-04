"""
Script de Verificación - Top Flow
Verifica que todos los requisitos estén instalados y configurados correctamente
"""
import sys
import os


def verificar_python():
    """Verificar versión de Python"""
    print("\n📌 Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.7+")
        return False


def verificar_modulos():
    """Verificar módulos requeridos"""
    print("\n📌 Verificando módulos de Python...")
    
    modulos_requeridos = {
        'PyQt5': 'PyQt5',
        'pyodbc': 'pyodbc'
    }
    
    todos_ok = True
    
    for modulo, nombre_pip in modulos_requeridos.items():
        try:
            __import__(modulo)
            print(f"   ✅ {modulo} - OK")
        except ImportError:
            print(f"   ❌ {modulo} - NO INSTALADO")
            print(f"      Instalar con: pip install {nombre_pip}")
            todos_ok = False
    
    return todos_ok


def verificar_archivos_ui():
    """Verificar que existan los archivos .ui"""
    print("\n📌 Verificando archivos de interfaz (.ui)...")
    
    archivos_ui = [
        'ui_topflow/Login_topflow.ui',
        'ui_topflow/Menu_topflow.ui',
        'ui_topflow/Productos_topflow.ui',
        'ui_topflow/Carrito_topflow.ui',
        'ui_topflow/Consultar_productos.ui'
    ]
    
    todos_ok = True
    
    for archivo in archivos_ui:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - NO ENCONTRADO")
            todos_ok = False
    
    return todos_ok


def verificar_modelo():
    """Verificar que existan los archivos del modelo"""
    print("\n📌 Verificando archivos del modelo (DAOs)...")
    
    archivos_modelo = [
        'modelo/conexionbd.py',
        'modelo/models.py',
        'modelo/productodao.py',
        'modelo/pedidodao.py',
        'modelo/usuariodao.py',
        'modelo/clientedao.py',
        'modelo/catalogodao.py'
    ]
    
    todos_ok = True
    
    for archivo in archivos_modelo:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - NO ENCONTRADO")
            todos_ok = False
    
    return todos_ok


def verificar_conexion_bd():
    """Verificar conexión a la base de datos"""
    print("\n📌 Verificando conexión a la base de datos...")
    
    try:
        # Agregar el directorio actual al path
        sys.path.insert(0, os.getcwd())
        
        from modelo.conexionbd import ConexionBD
        
        bd = ConexionBD()
        bd.establecerConexionBD()
        bd.cerrarConexionBD()
        
        print("   ✅ Conexión a la base de datos - OK")
        return True
        
    except ImportError as e:
        print(f"   ❌ Error al importar módulo de conexión: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error de conexión a la base de datos: {e}")
        print("   💡 Verifica la configuración en modelo/conexionbd.py")
        return False


def verificar_ventanas():
    """Verificar que existan los archivos de ventanas"""
    print("\n📌 Verificando archivos de ventanas Python...")
    
    archivos_ventanas = [
        'login_window.py',
        'menu_window.py',
        'productos_window.py',
        'carrito_window.py',
        'consultar_productos_window.py',
        'main_topflow.py'
    ]
    
    todos_ok = True
    
    for archivo in archivos_ventanas:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - NO ENCONTRADO")
            todos_ok = False
    
    return todos_ok


def main():
    """Función principal"""
    print("=" * 70)
    print("🔍 TOP FLOW - VERIFICACIÓN DE REQUISITOS")
    print("=" * 70)
    
    resultados = []
    
    # Realizar verificaciones
    resultados.append(("Python", verificar_python()))
    resultados.append(("Módulos", verificar_modulos()))
    resultados.append(("Archivos UI", verificar_archivos_ui()))
    resultados.append(("Modelo (DAOs)", verificar_modelo()))
    resultados.append(("Ventanas Python", verificar_ventanas()))
    resultados.append(("Conexión BD", verificar_conexion_bd()))
    
    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 70)
    
    todos_ok = True
    for nombre, resultado in resultados:
        estado = "✅ OK" if resultado else "❌ ERROR"
        print(f"   {nombre:20} {estado}")
        if not resultado:
            todos_ok = False
    
    print("=" * 70)
    
    if todos_ok:
        print("\n✅ ¡TODAS LAS VERIFICACIONES PASARON!")
        print("   Puedes ejecutar la aplicación con: python main_topflow.py")
        print("   O usar el menú de pruebas con: python test_topflow.py")
    else:
        print("\n❌ ALGUNAS VERIFICACIONES FALLARON")
        print("   Por favor, corrige los errores antes de ejecutar la aplicación")
    
    print()


if __name__ == "__main__":
    main()
