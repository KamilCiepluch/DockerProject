drop table IF EXISTS SKINS;
create table SKINS
(
    ID         int auto_increment primary key,
    NAME       varchar(50) not null,
    WEAR       varchar(20) not null,
    QUALITY    VARCHAR(30) NULL,
    STATTRACK  boolean  null,
    SUVENIR    boolean  null,
    COLLECTION varchar(50) null,
    IMG        blob        null,
    DATA       JSON NOT NULL,
    UPDATE_DATE TIMESTAMP NOT NULL,
    check (regexp_like(`WEAR`, '^(Factory New|Minimal Wear|Field-Tested|Well-Worn|Battle-Scarred)$'))
);


select * from SKINS;

DROP FUNCTION IF EXISTS check_skin_exists;
create function check_skin_exists(skin_name varchar(50), skin_wear varchar(20), skin_quality varchar(30),
                                    skin_st tinyint(1),skin_sv tinyint(1), skin_collection varchar(50))
    returns int deterministic
BEGIN
    DECLARE tmp INT;

    SELECT COUNT(*)
    INTO tmp
    FROM SKINS
    WHERE NAME = skin_name
      AND WEAR = skin_wear
      AND QUALITY = skin_quality
      AND STATTRACK = skin_st
      AND SUVENIR = skin_sv
      AND COLLECTION = skin_collection;

    IF tmp = 0 THEN
        RETURN 0;
    ELSE
        RETURN 1;
    END IF;
END;




DROP PROCEDURE IF EXISTS add_skin;
create procedure add_skin(IN skin_name varchar(50), IN skin_wear varchar(20),
                                          IN skin_quality varchar(30), IN st tinyint(1), IN sv tinyint(1),
                                          IN skin_collection varchar(50), IN skin_data json)
BEGIN
    DECLARE result INT;
    SELECT check_skin_exists(skin_name,skin_wear,skin_quality,st,sv,skin_collection) INTO result;
    IF result = 0 THEN
        -- Jeśli nie istnieje, dodaj nowy skin
        INSERT INTO SKINS (NAME, WEAR,QUALITY, STATTRACK, SUVENIR, COLLECTION, DATA, UPDATE_DATE)
        VALUES (skin_name, skin_wear,skin_quality, st, sv, skin_collection, skin_data, NOW());
    ELSE
        -- Jeśli istnieje, zwróć wartość 0 jako rezultat
        SELECT 0 AS Result;
    END IF;
END;


drop procedure if exists update_skin_data;
create procedure update_skin_data(IN skin_name varchar(50), IN skin_wear varchar(20),
                          IN skin_quality varchar(30), IN st tinyint(1), IN sv tinyint(1),
                          IN skin_collection varchar(50), IN skin_data json)
BEGIN
    DECLARE result INT;
    SELECT check_skin_exists(skin_name,skin_wear,skin_quality,st,sv,skin_collection) INTO result;
    IF result = 0 THEN
        -- Jeśli istnieje, zwróć wartość 0 jako rezultat
        SELECT 0 AS Result;
    ELSE
        -- Jeśli nie istnieje, dodaj nowy skin
        UPDATE SKINS set DATA= skin_data, UPDATE_DATE = NOW()
        WHERE  NAME=skin_name AND WEAR =skin_wear AND QUALITY = skin_quality and STATTRACK = st AND SUVENIR = sv AND
               COLLECTION = skin_collection;
    END IF;
END;



DROP FUNCTION IF EXISTS check_skin_name_exists;
CREATE FUNCTION check_skin_name_exists(skin_name VARCHAR(50))
    RETURNS BOOLEAN
    DETERMINISTIC
BEGIN
    DECLARE tmp INT;

    SELECT COUNT(*)
    INTO tmp
    FROM SKINS
    WHERE NAME = skin_name;
    IF tmp = 0 THEN
        RETURN FALSE;
    ELSE
        RETURN TRUE;
    END IF;
END;


drop procedure IF EXISTS get_skin_by_collection;
CREATE PROCEDURE get_skin_by_collection(
    IN prefix VARCHAR(50))
BEGIN
    IF prefix IS NULL THEN
        SELECT ID, NAME, WEAR, QUALITY, STATTRACK, SUVENIR, COLLECTION, IMG, DATA, UPDATE_DATE
        FROM SKINS
        WHERE COLLECTION IS NULL;
    ELSE
        SELECT ID, NAME, WEAR, QUALITY, STATTRACK, SUVENIR, COLLECTION, IMG, DATA, UPDATE_DATE
        FROM SKINS
        WHERE COLLECTION LIKE CONCAT(prefix, '%');
    END IF;
END;


DROP procedure IF EXISTS get_skin_by_quality;
CREATE PROCEDURE get_skin_by_quality(
    IN prefix VARCHAR(50))
BEGIN
    SELECT ID, NAME, WEAR, QUALITY, STATTRACK, SUVENIR, COLLECTION, IMG, DATA
    FROM SKINS
    WHERE QUALITY LIKE CONCAT(prefix, '%');
END;


DROP PROCEDURE IF EXISTS update_collection_for_skins;
CREATE PROCEDURE update_collection_for_skins(
    IN skin_name VARCHAR(50),
    IN skin_collection VARCHAR(50)
)
BEGIN
    UPDATE SKINS
    SET COLLECTION = skin_collection
    WHERE NAME = skin_name;
END;





DROP PROCEDURE IF EXISTS update_quality_for_skins;
CREATE PROCEDURE update_quality_for_skins(
    IN skin_name VARCHAR(50),
    IN skin_quality VARCHAR(50))
BEGIN
    UPDATE SKINS
    SET QUALITY = skin_quality
    WHERE NAME = skin_name;
END;




drop function IF EXISTS get_skin_data;
create
    definer = root@`%` function get_skin_data(skin_name varchar(50), skin_wear varchar(20),
                                              is_stattrack boolean, is_souvenir boolean) returns json deterministic
BEGIN
    DECLARE jsonTmp JSON;
    SELECT DATA INTO jsonTmp FROM SKINS
    WHERE NAME = skin_name AND WEAR = skin_wear AND STATTRACK = is_stattrack
      AND SUVENIR = is_souvenir;
    RETURN jsonTmp;
END;



drop PROCEDURE IF EXISTS get_collections_names;
CREATE PROCEDURE get_collections_names()
BEGIN
    Select DISTINCT COLLECTION From SKINS;
END;



drop function if exists check_if_souvenir_exists;
CREATE FUNCTION check_if_souvenir_exists(skin_name varchar(50),skin_quality varchar(30), skin_collection varchar(50))
RETURNS INT
BEGIN
        DECLARE RESULT INT;
        select COUNT(*) INTO RESULT from SKINS WHERE COLLECTION=skin_collection
                AND NAME LIKE CONCAT(skin_name,'%') AND QUALITY LIKE CONCAT(skin_quality,'%') AND SUVENIR=1;
        RETURN RESULT;
END;


drop function if exists check_if_stattrack_exists;
CREATE FUNCTION check_if_stattrack_exists(skin_name varchar(50),skin_quality varchar(30), skin_collection varchar(50))
    RETURNS INT
BEGIN
    DECLARE RESULT INT;
    select COUNT(*) INTO RESULT from SKINS WHERE COLLECTION=skin_collection
                                             AND NAME LIKE CONCAT(skin_name,'%') AND QUALITY LIKE CONCAT(skin_quality,'%') AND STATTRACK=1;
    RETURN RESULT;
END;


select * from SKINS;
select check_if_souvenir_exists('AWP','Covert Skins','The Control Collection');
select check_if_stattrack_exists('AWP','Covert Skins','The Control Collection');