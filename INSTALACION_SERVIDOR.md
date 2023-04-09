# <div align="center>Instalación del servidor web"</div>
Primero, debemos instalar y configurar un servidor web en nuestro servidor de producción. Los dos servidores web más populares son Apache y Nginx.

Apache
Para instalar Apache en Ubuntu, ejecute los siguientes comandos en su terminal:

bash
Copy code
sudo apt-get update
sudo apt-get install apache2
Una vez instalado, puede verificar que Apache se está ejecutando ejecutando el siguiente comando:

bash
Copy code
sudo systemctl status apache2
Nginx
Para instalar Nginx en Ubuntu, ejecute los siguientes comandos en su terminal:

bash
Copy code
sudo apt-get update
sudo apt-get install nginx
Una vez instalado, puede verificar que Nginx se está ejecutando ejecutando el siguiente comando:

bash
Copy code
sudo systemctl status nginx
Preparación del proyecto Vue.js
Antes de copiar el proyecto de Vue.js en el servidor, debemos preparar el proyecto para su implementación. Primero, necesitamos compilar el proyecto en modo de producción. Para ello, navegue hasta el directorio del proyecto en su máquina local y ejecute el siguiente comando:

bash
Copy code
npm run build
Esto creará una carpeta llamada dist que contiene los archivos estáticos del proyecto.

Configuración del servidor web
Ahora que el servidor web está instalado y el proyecto de Vue.js está preparado, debemos configurar el servidor web para que sirva los archivos del proyecto.

Apache
Para configurar Apache, debemos crear un archivo de host virtual para el proyecto. Cree un archivo llamado myproject.conf en el directorio /etc/apache2/sites-available/ con el siguiente contenido:

apache
Copy code
<VirtualHost *:80>
    ServerName myproject.com
    DocumentRoot /var/www/myproject/dist

    <Directory /var/www/myproject/dist/>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/myproject_error.log
    CustomLog ${APACHE_LOG_DIR}/myproject_access.log combined
</VirtualHost>
Asegúrese de reemplazar myproject.com con el nombre de dominio que se utilizará para acceder al sitio web.

Habilitar el host virtual:

bash
Copy code
sudo a2ensite myproject.conf
Reinicie Apache para que los cambios surtan efecto:

bash
Copy code
sudo systemctl restart apache2
Nginx
Para configurar Nginx, debemos crear un archivo de configuración en el directorio /etc/nginx/sites-available/. Cree un archivo llamado myproject con el siguiente contenido:

nginx
Copy code
server {
    listen 80;
    server_name myproject.com;

    root /var/www/myproject/dist;

    location / {
        try_files $uri $uri/ /index.html;
    }

    error_log /var/log/nginx/myproject_error.log;
    access_log /var/log/nginx/myproject_access.log;
}
Asegúrese de reemplazar myproject.com con el nombre de dominio que se utilizará para acceder al sitio web.

Cree un enlace simbólico en el directorio /etc/nginx/sites-enabled/:

bash
Copy code
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
