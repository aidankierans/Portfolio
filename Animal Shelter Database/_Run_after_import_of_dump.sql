USE shelter;

CREATE USER IF NOT EXISTS admin1 IDENTIFIED WITH sha256_password BY "admin-password";
CREATE USER IF NOT EXISTS smithl IDENTIFIED WITH sha256_password BY "pass1!";
CREATE USER IF NOT EXISTS wildej IDENTIFIED WITH sha256_password BY "pass2!";
CREATE USER IF NOT EXISTS williamsr IDENTIFIED WITH sha256_password BY "pass3!";
CREATE USER IF NOT EXISTS dickm IDENTIFIED WITH sha256_password BY "pass4!";
CREATE USER IF NOT EXISTS dumasa IDENTIFIED WITH sha256_password BY "pass5!";
CREATE USER IF NOT EXISTS doylec IDENTIFIED WITH sha256_password BY "pass6!";
CREATE USER IF NOT EXISTS kings IDENTIFIED WITH sha256_password BY "pass7!";

CREATE EVENT IF NOT EXISTS `remove_old_reservations` ON SCHEDULE EVERY 1 DAY STARTS '2019-11-27 18:18:55'
	ON COMPLETION NOT PRESERVE ENABLE DO DELETE FROM reserved WHERE DATEDIFF(CURDATE(), r_date) > 180;

delimiter //

CREATE TRIGGER I_check_start_date BEFORE INSERT ON adopted FOR EACH ROW BEGIN
IF (NEW.start_date > CURDATE()) THEN SET NEW.start_date = CURDATE(); END IF; END;
CREATE TRIGGER I_check_end_date BEFORE INSERT ON adopted FOR EACH ROW BEGIN
IF (NEW.end_date > CURDATE()) THEN SET NEW.end_date = CURDATE(); END IF; END;
CREATE TRIGGER I_check_animal_birth_date BEFORE INSERT ON animal FOR EACH ROW BEGIN
IF (NEW.birth_date > CURDATE()) THEN SET NEW.birth_date = CURDATE(); END IF; END;
CREATE TRIGGER I_check_person_birth_date BEFORE INSERT ON person FOR EACH ROW BEGIN
IF (NEW.birth_date > CURDATE()) THEN SET NEW.birth_date = CURDATE(); END IF; END;
CREATE TRIGGER I_check_date_sheltered BEFORE INSERT ON animal FOR EACH ROW BEGIN
IF (NEW.date_sheltered > CURDATE()) THEN SET NEW.date_sheltered = CURDATE(); END IF; END;
CREATE TRIGGER I_check_cat_i_date BEFORE INSERT ON cat_immunizations FOR EACH ROW BEGIN
IF (NEW.i_date > CURDATE()) THEN SET NEW.i_date = CURDATE(); END IF; END;
CREATE TRIGGER I_check_dog_i_date BEFORE INSERT ON dog_immunizations FOR EACH ROW BEGIN
IF (NEW.i_date > CURDATE()) THEN SET NEW.i_date = CURDATE(); END IF; END;
CREATE TRIGGER I_check_r_date BEFORE INSERT ON reserved FOR EACH ROW BEGIN
IF (NEW.r_date > CURDATE()) THEN SET NEW.r_date = CURDATE(); END IF; END;
CREATE TRIGGER I_check_t_date BEFORE INSERT ON treated FOR EACH ROW BEGIN
IF (NEW.t_date > CURDATE()) THEN SET NEW.t_date = CURDATE(); END IF; END;
CREATE TRIGGER I_check_date_written BEFORE INSERT ON prescribed FOR EACH ROW BEGIN
IF (NEW.date_written > CURDATE()) THEN SET NEW.date_written = CURDATE(); END IF; END;

CREATE TRIGGER U_check_start_date BEFORE UPDATE ON adopted FOR EACH ROW BEGIN
IF (NEW.start_date > CURDATE()) THEN SET NEW.start_date = CURDATE(); END IF; END;
CREATE TRIGGER U_check_end_date BEFORE UPDATE ON adopted FOR EACH ROW BEGIN
IF (NEW.end_date > CURDATE()) THEN SET NEW.end_date = CURDATE(); END IF; END;
CREATE TRIGGER U_check_animal_birth_date BEFORE UPDATE ON animal FOR EACH ROW BEGIN
IF (NEW.birth_date > CURDATE()) THEN SET NEW.birth_date = CURDATE(); END IF; END;
CREATE TRIGGER U_check_person_birth_date BEFORE UPDATE ON person FOR EACH ROW BEGIN
IF (NEW.birth_date > CURDATE()) THEN SET NEW.birth_date = CURDATE(); END IF; END;
CREATE TRIGGER U_check_date_sheltered BEFORE UPDATE ON animal FOR EACH ROW BEGIN
IF (NEW.date_sheltered > CURDATE()) THEN SET NEW.date_sheltered = CURDATE(); END IF; END;
CREATE TRIGGER U_check_cat_i_date BEFORE UPDATE ON cat_immunizations FOR EACH ROW BEGIN
IF (NEW.i_date > CURDATE()) THEN SET NEW.i_date = CURDATE(); END IF; END;
CREATE TRIGGER U_check_dog_i_date BEFORE UPDATE ON dog_immunizations FOR EACH ROW BEGIN
IF (NEW.i_date > CURDATE()) THEN SET NEW.i_date = CURDATE(); END IF; END;
CREATE TRIGGER U_check_r_date BEFORE UPDATE ON reserved FOR EACH ROW BEGIN
IF (NEW.r_date > CURDATE()) THEN SET NEW.r_date = CURDATE(); END IF; END;
CREATE TRIGGER U_check_t_date BEFORE UPDATE ON treated FOR EACH ROW BEGIN
IF (NEW.t_date > CURDATE()) THEN SET NEW.t_date = CURDATE(); END IF; END;
CREATE TRIGGER U_check_date_written BEFORE UPDATE ON prescribed FOR EACH ROW BEGIN
IF (NEW.date_written > CURDATE()) THEN SET NEW.date_written = CURDATE(); END IF; END;

CREATE TRIGGER I_check_email BEFORE INSERT ON person FOR EACH ROW BEGIN
IF (NEW.email NOT LIKE '%@%') THEN UPDATE EMAIL SET email = NULL WHERE human_id = NEW.human_id; END IF; END;
CREATE TRIGGER U_check_email BEFORE UPDATE ON person FOR EACH ROW BEGIN
IF (NEW.email NOT LIKE '%@%') THEN UPDATE EMAIL SET email = NULL WHERE human_id = NEW.human_id; END IF; END;

CREATE TRIGGER U_log_employee BEFORE UPDATE ON employee FOR EACH ROW INSERT INTO employee_info_changes 
	VALUES (NEW.human_id, USER(), NOW(), OLD.job_title, NEW.job_title, OLD.salary, NEW.salary);

DROP FUNCTION IF EXISTS CheckCompatible;
CREATE FUNCTION CheckCompatible (human_id bigint(20) unsigned, id_number mediumint(8) unsigned) RETURNS TINYINT(1) unsigned READS SQL DATA
BEGIN
IF EXISTS(SELECT * FROM customer WHERE customer.human_id = human_id AND customer.allowed_to_adopt = 0)
THEN RETURN 0;
ELSEIF EXISTS(SELECT * FROM customer WHERE customer.human_id = human_id AND customer.sex = 'male') AND EXISTS(SELECT * FROM incompatible WHERE should_avoid = 'men')
THEN RETURN 0;
ELSEIF EXISTS(SELECT * FROM customer WHERE customer.human_id = human_id AND customer.has_young_children = 1) AND EXISTS(SELECT * FROM incompatible WHERE should_avoid = 'small_children')
THEN RETURN 0;
ELSEIF EXISTS(SELECT * FROM pet_types_owned AS pto, incompatible AS i WHERE pto.human_id = human_id AND i.id_number = id_number AND i.should_avoid LIKE CONCAT(pto.pet_type, "%"))
THEN RETURN 0;
ELSE RETURN 1;
END IF; END;// 

DROP PROCEDURE IF EXISTS RecordBite;
CREATE PROCEDURE RecordBite (human_id bigint(20) unsigned, id_number mediumint(8) unsigned)
BEGIN UPDATE bit SET n_times = n_times + 1 WHERE bit.human_id = human_id AND bit.id_number = id_number;
IF ROW_COUNT() = 0 
THEN INSERT INTO bit (ssn, id_number, n_times) VALUES (human_id, id_number, 1);
END IF; END;// 
delimiter ;


CREATE OR REPLACE VIEW `human_names` AS 
SELECT `person`.`human_id` AS `human_id`,`person`.`first_name` AS `first_name`,`person`.`last_name` AS `last_name` 
FROM `person`;

CREATE OR REPLACE VIEW `compatible_pairs` AS 
SELECT `customer`.`human_id` AS `human_id`,`animal`.`id_number` AS `animal_id` 
FROM (`customer` JOIN `animal`) WHERE (`CheckCompatible`(`customer`.`human_id`,`animal`.`id_number`) IS TRUE);

CREATE OR REPLACE VIEW `bite_record` AS 
SELECT `animal`.`name` AS `animal_name`,CONCAT(`human_names`.`first_name`,' ',`human_names`.`last_name`) AS `human_name`,`bit`.`n_times` AS `n_times` 
FROM ((`human_names` JOIN `bit` ON((`human_names`.`human_id` = `bit`.`human_id`))) JOIN `animal` ON((`bit`.`id_number` = `animal`.`id_number`)));

GRANT DELETE, INSERT, SELECT, UPDATE ON animal TO smithl;
GRANT DELETE, INSERT, SELECT, UPDATE ON dog TO smithl;
GRANT DELETE, SELECT, UPDATE ON dog_immunizations TO smithl;
GRANT DELETE, INSERT, SELECT, UPDATE ON cat TO smithl;
GRANT DELETE, INSERT, SELECT, UPDATE ON cat_immunizations TO smithl;
GRANT DELETE, INSERT, SELECT, UPDATE ON treated TO smithl;
GRANT DELETE, INSERT, SELECT, UPDATE ON prescribed TO smithl;
GRANT SELECT, UPDATE ON bit TO smithl;
GRANT SELECT ON human_names TO smithl;
GRANT SELECT ON bite_record TO smithl;
GRANT EXECUTE ON PROCEDURE RecordBite TO smithl;


GRANT SELECT, UPDATE ON animal TO dickm;
GRANT SELECT, UPDATE ON incompatible TO dickm;
GRANT SELECT, UPDATE ON dog TO dickm;
GRANT SELECT, UPDATE ON dog_immunizations TO dickm;
GRANT SELECT, UPDATE ON cat TO dickm;
GRANT SELECT, UPDATE ON cat_immunizations TO dickm;
GRANT SELECT, UPDATE ON bit TO dickm;
GRANT SELECT ON human_names TO dickm;
GRANT SELECT ON bite_record TO dickm;
GRANT EXECUTE ON PROCEDURE RecordBite TO dickm;


GRANT DELETE, INSERT, SELECT, UPDATE ON adopted TO wildej;
GRANT DELETE, INSERT, SELECT, UPDATE ON customer TO wildej;
GRANT DELETE, INSERT, SELECT, UPDATE ON pet_types_owned TO wildej;
GRANT DELETE, INSERT, SELECT, UPDATE ON reserved TO wildej;
GRANT SELECT, UPDATE, DELETE ON bit TO wildej;
GRANT INSERT ON person TO wildej;
GRANT SELECT ON incompatible TO wildej;
GRANT SELECT ON human_names TO wildej;
GRANT SELECT ON bite_record TO wildej;
GRANT SELECT ON compatible_pairs TO wildej;
GRANT EXECUTE ON PROCEDURE RecordBite TO wildej;
GRANT EXECUTE ON FUNCTION CheckCompatible TO wildej;


GRANT DELETE, INSERT, SELECT, UPDATE ON animal TO williamsr;
GRANT DELETE, INSERT, SELECT, UPDATE ON dog TO williamsr;
GRANT DELETE, INSERT, SELECT, UPDATE ON dog_immunizations TO williamsr;
GRANT DELETE, INSERT, SELECT, UPDATE ON cat TO williamsr;
GRANT DELETE, INSERT, SELECT, UPDATE ON cat_immunizations TO williamsr;
GRANT DELETE, INSERT, SELECT, UPDATE ON incompatible TO williamsr;
GRANT SELECT, UPDATE, DELETE ON bit TO williamsr;
GRANT SELECT ON human_names TO williamsr;
GRANT SELECT ON bite_record TO williamsr;
GRANT EXECUTE ON PROCEDURE RecordBite TO williamsr;

GRANT SELECT ON animal TO dumasa;
GRANT SELECT ON incompatible TO dumasa;
GRANT SELECT ON dog TO dumasa;
GRANT SELECT ON dog_immunizations TO dumasa;
GRANT SELECT ON cat TO dumasa;
GRANT SELECT ON cat_immunizations TO dumasa;
GRANT SELECT ON bit TO dumasa;
GRANT SELECT ON human_names TO dumasa;
GRANT SELECT ON bite_record TO dumasa;
GRANT EXECUTE ON PROCEDURE RecordBite TO dumasa;

GRANT SELECT, INSERT, UPDATE ON incompatible TO doylec;
GRANT SELECT, UPDATE ON animal TO doylec;
GRANT SELECT, UPDATE ON dog TO doylec;
GRANT SELECT, UPDATE ON dog_immunizations TO doylec;
GRANT SELECT, UPDATE ON cat TO doylec;
GRANT SELECT, UPDATE ON cat_immunizations TO doylec;
GRANT SELECT, UPDATE ON bit TO doylec;
GRANT SELECT ON human_names TO doylec;
GRANT SELECT ON bite_record TO doylec;
GRANT EXECUTE ON PROCEDURE RecordBite TO doylec;

GRANT DELETE, INSERT, SELECT, UPDATE ON employee TO kings;
GRANT DELETE, INSERT, SELECT, UPDATE ON medical TO kings;
GRANT INSERT, SELECT, UPDATE ON person TO kings;
GRANT SELECT ON employee_info_changes TO kings;
GRANT SELECT ON bit TO kings;
GRANT SELECT ON bite_record TO kings;