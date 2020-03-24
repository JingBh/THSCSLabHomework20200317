CREATE TABLE `data`
(
    `date`      DATE,
    `province`  VARCHAR,
    `total`     INT,
    `death`     INT,
    `recovered` INT,
    `confirmed` INT,
    CONSTRAINT `primary`
        PRIMARY KEY (`date`, `province`)
);
