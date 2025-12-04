from conexionbd import ConexionBD

class UsuarioDAO:
    def __init__(self):
        self.bd = ConexionBD()
    
    def validarLogin(self, nombre, contraseña):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        
        try:
            sp = 'EXEC [dbo].[sp_ValidarLogin] ?, ?'
            cursor.execute(sp, (nombre, contraseña))
            resultado = cursor.fetchone()
            
            if resultado and resultado[0] == 1:
                return True
            else:
                return False
                
        except Exception as ex:
            return False
        finally:
            self.bd.cerrarConexionBD()
    
    def registrarUsuario(self, nombre, contraseña):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        
        try:
            sp = 'EXEC [dbo].[sp_RegistrarUsuario] ?, ?'
            cursor.execute(sp, (nombre, contraseña))
            self.bd.conexion.commit()
            resultado = cursor.fetchone()
            
            if resultado and resultado[0] == 1:
                return True
            else:
                return False
                
        except Exception as ex:
            self.bd.conexion.rollback()
            return False
        finally:
            self.bd.cerrarConexionBD()