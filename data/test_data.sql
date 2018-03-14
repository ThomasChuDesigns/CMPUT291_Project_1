
INSERT INTO personnel VALUES('111111','Dan Brown','matloff@sbcglobal.net','Windsor Drive','222222');
INSERT INTO account_managers VALUES('111111','large accounts manager','8th Street South');

INSERT INTO personnel VALUES('111110','Bushy Brown','bby@sbcglobal.net','Windsor Drive','222222');
INSERT INTO account_managers VALUES('111110','medium accounts manager','8th Street South');

INSERT INTO personnel VALUES('222222', 'Thomas Chu', 'test@gmail.com', 'Not Windsor Drive', '0');

INSERT INTO accounts VALUES('142','111111','Bob','(201) 111-1111','industrial','2006-05-19','2018-02-25',837646.52);
INSERT INTO accounts VALUES('1','111110','Jane','(201) 222-2222','residential','2006-05-19','2018-01-01',837646.52);


INSERT INTO personnel VALUES('12', 'Add Me 1', 'test1@gmail.com', 'Not Windsor Drive 1', '0');
INSERT INTO personnel VALUES('13', 'Add Me 2', 'test2@gmail.com', 'Not Windsor Drive 2', '0');
INSERT INTO personnel VALUES('14', 'Add Me 3', 'test3@gmail.com', 'Not Windsor Drive 3', '0');
INSERT INTO account_managers VALUES('13','medium accounts manager','69th Street South');
INSERT INTO drivers VALUES('14','bus school','111');

INSERT INTO service_agreements VALUES('0', '142', 'Wendys', 'metal', 'everyday', '(780) 111-1111', 30, 50);
INSERT INTO service_agreements VALUES('1', '142', 'Wendys', 'metal', 'everyday', '(780) 111-1111', 30, 50);
INSERT INTO service_agreements VALUES('2', '1', 'Wendys', 'paper', 'everyday', '(780) 111-1111', 20, 50);
INSERT INTO service_agreements VALUES('3', '1', 'Wendys', 'mixed waste', 'everyday', '(780) 111-1111', 0, 50);

INSERT INTO containers VALUES('3', 'roll-off', '2017-05-23');
INSERT INTO containers VALUES('2', 'roll-off', '2017-05-23');
INSERT INTO containers VALUES('1', 'roll-off', '2017-05-23');

INSERT INTO container_waste_types VALUES('3', 'metal');
INSERT INTO container_waste_types VALUES('2', 'paper');
INSERT INTO container_waste_types VALUES('1', 'metal');

INSERT INTO service_fulfillments VALUES('2010-3-11', '1', '1', '1', '1', '2', '1');
INSERT INTO service_fulfillments VALUES('2010-3-10', '0', '2', '1', '1', '1', '0000');
INSERT INTO service_fulfillments VALUES('2010-3-10', '0', '3', '1', '0', '1', '0000');

INSERT INTO personnel VALUES('100', 'Driver 1', 'test2@gmail.com', 'Not Windsor Drive 2', '0');
INSERT INTO personnel VALUES('101', 'Driver 2', 'test3@gmail.com', 'Not Windsor Drive 3', '0');
INSERT INTO drivers VALUES('100','Single Trailer','12');
INSERT INTO drivers VALUES('101','Single Trailer','0');

INSERT INTO trucks VALUES('12','McLaren F1','front loader');
INSERT INTO trucks VALUES('14','Benz F1','front loader');

