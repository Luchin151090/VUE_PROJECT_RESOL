from models.connection_pool import MYSQLPool
from flask import request
import mysql.connector

llave_usuario = 0

# EL SISTEMA YA INICIA CON 2 ROLES POR DEFAULT :  ADMIN 1 y USUARIO 2

class UsuarioModel:
    def __init__(self):
        self.mysql_pool=MYSQLPool()
    
    def get_usuarios(self):
        query=self.mysql_pool.execute("""select u.id,u.nombres,u.apellidos,u.nickname,u.contraseña,u.email_usuario,o.nombre
            from usuario u 
            inner join oficina o on u.oficina_id=o.id;""")
        data =list()
        contenido=dict()
        for row in query:
            contenido={
                'id':row[0],
                'nombres':row[1],
                'apellidos':row[2],
                'nickname':row[3],
                'contrasena':row[4],
                'email':row[5],
                'oficina':row[6]
            }
            data.append(contenido)
            contenido={}
        return data
    
    def post_user(self,nombre,apellidos,nickname,contrasena,email,oficina_id):
        entrada = {
            'nombre':nombre,
            'apellidos':apellidos,
            'nickname':nickname,
            'contraseña':contrasena,
            'email_user':email,
            'oficina_id':oficina_id
        }
        query ="""insert into usuario(nombres,apellidos,nickname,contraseña,email_usuario,oficina_id)
         values(%(nombre)s,%(apellidos)s,%(nickname)s,%(contraseña)s,%(email_user)s,%(oficina_id)s);"""
        cursor = self.mysql_pool.execute(query,entrada,commit=True)
        salida = {
            "ID_USER":cursor.lastrowid,
            "message":"Usuario OK"
        }
        global llave_usuario
        llave_usuario = cursor.lastrowid
        return salida
   # AL MOMENTO DE CREAR EL USUARIO... NO SABES SU ID...PERO CON LASTROWID...
   # LLAMARIAS A ESTE METODO OBLIGATORIO...
   # YA QUE NINGUN USUARIO PUEDE ESTAR SIN UN ROL ASIGNADO
    def post_rol_user(self,id_rol):
        print("fk_user :",llave_usuario)
        FK_USER = llave_usuario
        entrada={
            'usuario_id':FK_USER,
            'rol_id':id_rol
        }
        query="""insert into usuario_rol(usuario_id,rol_id)
        values(%(usuario_id)s,%(rol_id)s);"""
        cursor=self.mysql_pool.execute(query,entrada,commit=True)
        salida = {
            "ID_REGISTER":cursor.lastrowid,
            "message":"Assigned OK!"
        }


    def delete_user_rol(self,user_id):
        # Los argumentos se pasan como array
        argu = [user_id]
        cursor = self.mysql_pool.call_procedure("eliminar_usuario",argu,commit=True)

        contenido = {
            "mensaje":"Eliminado"
        }
        return contenido
            

    def post_login(self,nickname,contrasena):
        query =self.mysql_pool.execute('select u.id,u.oficina_id,u.nombres,u.apellidos,u.nickname,u.contraseña,ur.rol_id,o.nombre from usuario u inner join usuario_rol ur on u.id=ur.usuario_id inner join oficina o on u.oficina_id=o.id where u.nickname="'+str(nickname)+'"'+' and u.contraseña="'+str(contrasena)+'"')
        contenido=dict()
        if query:
            contenido={
                'ID':query[0][0],
                'oficina':query[0][7],
                'apellidos':query[0][3],
                'nickname':query[0][4],
                'rol':query[0][6],
                'message':'ok'
            }
        else:
            contenido={
                'message':'incorrecto'
            }
        
        return contenido
    
if __name__=="__main__":
    usuario_model=UsuarioModel()
