import cgi
import json
import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def conectar_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='skate_shop',
            user='tu_usuario',
            password='tu_password'
        )
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def crear_tabla_usuarios():
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    fecha_nacimiento DATE,
                    nivel_skate VARCHAR(50),
                    ciudad VARCHAR(100),
                    pais VARCHAR(100),
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    activo BOOLEAN DEFAULT TRUE
                )
            """)
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error al crear tabla: {e}")

def registrar_usuario(datos):
    connection = conectar_db()
    if not connection:
        return {"success": False, "message": "Error de conexión a la base de datos"}
    
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM usuarios WHERE email = %s OR username = %s", 
                      (datos['email'], datos['username']))
        if cursor.fetchone():
            return {"success": False, "message": "El email o nombre de usuario ya está registrado"}

        password_hash = hash_password(datos['password'])

        query = """
            INSERT INTO usuarios (nombre, email, username, password, fecha_nacimiento, 
                                 nivel_skate, ciudad, pais)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            datos['nombre'],
            datos['email'],
            datos['username'],
            password_hash,
            datos['fecha_nacimiento'],
            datos['nivel_skate'],
            datos['ciudad'],
            datos['pais']
        )
        
        cursor.execute(query, valores)
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return {"success": True, "message": "Usuario registrado exitosamente"}
        
    except Error as e:
        return {"success": False, "message": f"Error al registrar usuario: {str(e)}"}

print("Content-Type: application/json\n")

try:
    crear_tabla_usuarios()
    content_length = int(os.environ.get('CONTENT_LENGTH', 0))
    if content_length > 0:
        input_data = sys.stdin.read(content_length)
        datos = json.loads(input_data)
        resultado = registrar_usuario(datos)
        print(json.dumps(resultado))
    else:
        print(json.dumps({"success": False, "message": "No se recibieron datos"}))
        
except Exception as e:
    print(json.dumps({"success": False, "message": f"Error del servidor: {str(e)}"}))