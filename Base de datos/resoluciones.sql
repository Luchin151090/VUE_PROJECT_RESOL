DROP DATABASE IF EXISTS RESOLUCIONES;
CREATE DATABASE RESOLUCIONES;
USE RESOLUCIONES;

create table usuario(
	id int not null primary key auto_increment,
    nombres varchar(100),
    apellidos varchar(200),
    nickname varchar(30),
    contraseña varchar(12),
    email_usuario varchar(100),
    oficina_id int
);
create table documento(
	id int not null primary key auto_increment,
    nproyecto varchar(50),
    usuario_id int,
    fecha_emision varchar(30),
    fecha_notificacion varchar(30),
    concepto varchar(100),
    descripcion varchar(200),
    distrito varchar(50),
    monto float,
    archivo varchar(1000)
);

create table oficina (
	id int not null primary key auto_increment,
    nombre varchar(100)
);
create table roles(
id int not null primary key auto_increment,
nombre varchar(200)
);
create table usuario_rol(
	id int not null primary key auto_increment,
    usuario_id int,
    rol_id int
);


alter table documento add foreign key(usuario_id) references usuario(id) on delete cascade on update cascade;
alter table usuario_rol add foreign key(usuario_id) references usuario(id);
alter table usuario_rol add foreign key(rol_id) references roles(id);
alter table usuario add foreign key (oficina_id) references oficina(id) on delete cascade on update cascade;
