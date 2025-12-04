import pyodbc

class ConexionBD:
    def __init__(self):
        self.conexion = ''

    def establecerConexionBD(self):
        try:

            #self.conexion = pyodbc.connect(r'DRIVER={SQL Server};SERVER=TZIENA_JR\SQLEXPRESS;Trusted_Connection=yes')
            #self.conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOPSEBAS;DATABASE=Top Flow;Trusted_Connection=yes')
            self.conexion = pyodbc.connect(r'DRIVER={SQL Server};SERVER=TZIENA_JR\SQLEXPRESS;DATABASE=Top Flow;Trusted_Connection=yes;')
            print("Conexion establecida")
        except Exception as ex:
            print("Error de conexión: " + str(ex))

    def cerrarConexionBD(self):
        self.conexion.close()