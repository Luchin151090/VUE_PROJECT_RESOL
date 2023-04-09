insert into roles(nombre)
values("admin"),("usuario");

insert into oficina(nombre)
values("ADMINISTRACIÓN"),("PERSONAL"),("ASESORÍA JURÍDICA"),("PROCESOS");

insert into usuario(nombres,apellidos,nickname,contraseña,email_usuario,oficina_id)
values("JOSE","MARTINEZ ESPINOZA","pepin","1234","pepin@gmail.com",1),
("BOB","ARMANDO PAREDES","jorgo","1234","jorgo@gmail.com",2),
("ROSA","ZAMBRANO VAZQUEZ","rosita","1234","rosita@gmail.com",3);

INSERT INTO documento (nproyecto,usuario_id,fecha_emision,fecha_notificacion,concepto,descripcion,distrito,monto,archivo)
VALUES
  ('1160-2021',1,'02/28/2023','07/05/2022','ASCENDER','reconocimiento por años de servicio','YANAHUARA',23519,'D:/TEST_SERVIDOR/x.pdf'),
  ('2321-2022',1,'01/24/2023','03/07/2023','AUTORIZAR','cese por enfermedad','CAYMA',19491,'D:\\TEST_SERVIDOR\\x.pdf'),
  ('3186-2022',2,'07/12/2022','06/16/2023','CESE','reconocimiento por años de servicio','SACHACA',29269,'D:\\TEST_SERVIDOR\\x.pdf'),
  ('3280-2022',3,'02/03/2022','12/21/2021','PERMUTA','ascenso por merito','CHARACATO',2665,'D:\\TEST_SERVIDOR\\x.pdf');


insert into usuario_rol(usuario_id,rol_id)
values(1,1),(2,2),(3,1);

DROP PROCEDURE IF EXISTS eliminar_usuario;
DELIMITER $$
CREATE PROCEDURE eliminar_usuario(IN id_user INT)
BEGIN
	delete from usuario_rol where usuario_id= id_user;
	delete from usuario  where id = id_user;
END
$$

