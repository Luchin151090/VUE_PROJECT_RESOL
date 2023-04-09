import mysql.connector.pooling

dbconfig = {
    "host":"127.0.0.1",
    "port":"3306",
    "user":"root",
    "password":"1234",
    "database":"resoluciones",
}
class MYSQLPool(object):
    def __init__(self):
        self.pool = self.create_pool(pool_name='resol_direc_pool',pool_size=30)
    
    def create_pool(self,pool_name,pool_size):
        pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            pool_reset_session=True,
            **dbconfig)
        return pool
    
    def close(self,conn,cursor):
        cursor.close()
        conn.close()

    def call_procedure(self, procedure, args=None,commit=False):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        if args:
            cursor.callproc(procedure,args)
        else:
            cursor.callproc(procedure)
        if commit is True:
            conn.commit()
            self.close(conn, cursor)
            return cursor
        else:
            res = cursor.fetchall()
            self.close(conn, cursor)
            return res
        
    
    def execute(self,sql,args=None,commit=False):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        if args:
            cursor.execute(sql,args)
        else:
            cursor.execute(sql)

        if commit is True:
            conn.commit()
            self.close(conn, cursor)
            return cursor
        else:
            res = cursor.fetchall()
            self.close(conn, cursor)
            return res

    def executemany(self,sql,args,commit=False):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        cursor.executemany(sql,args)
        if commit is True:
            conn.commit()
            self.close(conn,cursor)
            return None
        else:
            res = cursor.fetchall()
            self.close(conn,cursor)
            return res

if __name__ == "__main__":
    mysql_pool = MYSQLPool()
    