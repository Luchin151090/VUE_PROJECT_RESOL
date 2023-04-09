from models.connection_pool import MYSQLPool
from flask import request, Flask
from flask import render_template
from flask import send_file
from os import remove
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os.path
import pathlib

llave_documento = 0

class ResolucionModel:
    def __init__(self):
        self.mysql_pool=MYSQLPool()

    def get_cantidad(self):
        query=self.mysql_pool.execute('select * from documento;')
        tamanio=len(query)
        return tamanio
 
    def upload_file(self,id):  
        print("DENTRO DE UPLOAD")
        if request.method == 'POST':
            ruta_servidor = 'D:/TEST_SERVIDOR/'
            
            documento = request.files['file']
            nombre_documento = secure_filename(documento.filename)
            documento.save(os.path.join(ruta_servidor,nombre_documento))

            archivo = ruta_servidor+documento.filename
            query = "update documento set archivo ='"+archivo+"'"+" where id="+str(id)+";"
            cursor=self.mysql_pool.execute(query,commit=True)

            print(archivo)
            print(ruta_servidor)
            print(query)

            return 'file uploaded successfully'
    
    def download_file(self,id):
        query = self.mysql_pool.execute('select archivo from documento where id='+str(id))
        # ESTE PATH EMULA LA DIRECCIÓN DEL ARCHIVO EN EL DISCO DURO DEL SERVIDOR LOCAL
        path = query[0][0]

        
        print(path)
        #print(type(path))
        
        return send_file(path,as_attachment=True)

    def get_file_distrito(self):
        query=self.mysql_pool.execute('select count(*),distrito from documento group by distrito;')
 

        data=list()
        contenido = dict()
        datafound = len(query)
        #print(datafound)
        if(datafound>0):
            for row in query:
                    contenido={
                            'cantidad':row[0],
                            'distrito':row[1],
                        }
                    data.append(contenido)
                    contenido={}
            return data 
        elif(datafound==0):
            return None
      
    def get_top5(self):
        query=self.mysql_pool.execute('select * from documento order by id desc limit 5;')
        data=list()
        contenido=dict()
        for row in query:
            contenido={
                    'id':row[0],
                    'nproyecto':row[1],
                    'Femision':row[2],
                    'Fnotificacion':row[3],
                    'concepto':row[4],
                    'descripcion':row[5],
                    'distrito':row[6],
                    'monto':row[7]
                }
            data.append(contenido)
            contenido={}
                
        return data

    def get_last(self):
        query=self.mysql_pool.execute('SELECT * from documento order by id desc limit 1;')
        data=list()
        contenido=dict()
        for row in query:
            contenido={
                    'id':row[0],
                    'nproyecto':row[1],
                    'Femision':row[2],
                    'Fnotificacion':row[3],
                    'concepto':row[4],
                    'descripcion':row[5],
                    'distrito':row[6],
                    'monto':row[7]
                }
            data.append(contenido)
            contenido={}
             
        return data

    def get_monto(self):
        query=self.mysql_pool.execute('select round(sum(monto),2) from documento;')
        data=list()
        contenido=dict()
        for row in query:
            contenido={
                    'total':row[0]
                }
            data.append(contenido)
            contenido={}
             
        return data

    def get_resolucion(self,code):
        if code!=None:
            query=self.mysql_pool.execute('select * from documento where nproyecto="'+str(code)+'"'+";")
            data=list()
            contenido=dict()
           
            for row in query:
                contenido={
                    'id':row[0],
                    'nproyecto':row[1],
                    'Femision':row[2],
                    'Fnotificacion':row[3],
                    'concepto':row[4],
                    'descripcion':row[5],
                    'distrito':row[6],
                    'monto':row[7]
                }
                data.append(contenido)
                contenido={}
             
            return data
        else:
            query=self.mysql_pool.execute("""select d.id,d.nproyecto,d.concepto,d.monto,d.descripcion,d.distrito,d.fecha_emision,d.fecha_notificacion,u.apellidos,o.nombre 
            from documento d inner join usuario u on d.usuario_id=u.id inner join oficina o on o.id=u.oficina_id order by d.id asc;""")

            data=list()
            contenido=dict()
            for row in query:
                contenido={
                    'id':row[0],
                    'nproyecto':row[1],
                    'concepto':row[2],
                    'monto':row[3],
                    'descripcion':row[4],
                    'distrito':row[5],
                    'Femision':row[6],
                    'Fnotificacion':row[7],
                    'apellidos':row[8],
                    'nombre':row[9] 
                }
                data.append(contenido)
                contenido={}
            print("",len(data)) 
            #print(data[0])    
            return data
    
    def post_resolucion(self,nproyecto,usuario_id,fecha_emision,fecha_notificacion,concepto,descripcion,distrito,monto):
        

        entrada={
            'np':nproyecto,
            'u_id':usuario_id,
            'fe':fecha_emision,
            'fn':fecha_notificacion,
            'conpto':concepto,
            'desc':descripcion,
            'dis':distrito,
            'monto':monto

        }
        query="insert into documento(nproyecto,usuario_id,fecha_emision,fecha_notificacion,concepto,descripcion,distrito,monto)values(%(np)s,%(u_id)s,%(fe)s,%(fn)s,%(conpto)s,%(desc)s,%(dis)s,%(monto)s);"
        cursor=self.mysql_pool.execute(query,entrada,commit=True)
        contenido = {
            'id':cursor.lastrowid,
            'np':entrada['np'],
            'u_id':entrada['u_id'],
            'fe':entrada['fe'],
            'fn':entrada['fn'],
            'conpto':entrada['conpto'],
            'desc':entrada['desc'],
            'dis':entrada['dis'],
            'monto':entrada['monto']

        }
        global llave_documento
        llave_documento = cursor.lastrowid
        print(llave_documento,"---llave documento")
        #print(contenido['np'])
        return contenido

    def put_resolucion(self,id):
        enter ={
            'np':request.json['nproyecto'],
            'uid':request.json['usuario_id'],
            'fe':request.json['Femision'],
            'fn':request.json['Fnotificacion'],
            'cp':request.json['concepto'],
            'de':request.json['descripcion'],
            'di':request.json['distrito'],
            'monto':request.json['monto']
        }
        query = "update documento set nproyecto=%(np)s,usuario_id=%(uid)s,fecha_emision=%(fe)s,fecha_notificacion=%(fn)s,concepto=%(cp)s,descripcion=%(de)s,distrito=%(di)s,monto=%(monto)s where id="+str(id)+";"
        cursor = self.mysql_pool.execute(query,enter,commit=True)
        salida={
            'mensaje':'actualizado'
        }
        return salida
    
    def delete_resolucion(self,id):
        
        
        query = 'delete from documento where id ='+str(id)+';'

        cursor = self.mysql_pool.execute(query,commit=True)
       
        contenido={
            'mensaje':'resolucion eliminada'
        }
        
        return contenido


if __name__=="__main__":
    resolucion_model=ResolucionModel()