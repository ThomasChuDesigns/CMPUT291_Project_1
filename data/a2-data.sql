-- Data prepared by <Yuan Wang>,<wang17@ualberta.ca>,and published on <2018.2.6>
-- Made some revisions for my queries

--"front loader", "roll-off", or "garbage bin collector"".

INSERT INTO trucks VALUES('4T1BE','McLaren F1','front loader');
INSERT INTO trucks VALUES('1FAHP','toyota','roll-off');
INSERT INTO trucks VALUES('9BWBT','honda','garbage-collector');
INSERT INTO trucks VALUES('F150A','honda','g-wagon');
INSERT INTO trucks VALUES('AAAAA','ford','roll-off');
INSERT INTO trucks VALUES('BBBBB','chevy','garbage-collector');
INSERT INTO trucks VALUES('CCCCC','dodge','roll-off');

INSERT INTO personnel VALUES('34725','Dan Brown','matloff@sbcglobal.net','Windsor Drive','55263');
INSERT INTO personnel VALUES('12345','John Doe','matloff@sbcglobal.net','Windsor Drive','55263');
INSERT INTO personnel VALUES('23456','Jane Doe','matloff@sbcglobal.net','Windsor Drive','55263');
INSERT INTO personnel VALUES('43743','Driver 1','matloff@sbcglobal.net','Windsor Drive','55263');
INSERT INTO personnel VALUES('23769','Driver 2','matloff@sbcglobal.net','Windsor Drive','55263');

INSERT INTO account_managers VALUES('34725','small accounts manager','8th Street South');
INSERT INTO account_managers VALUES('12345','medium accounts manager','8th Street South');
INSERT INTO account_managers VALUES('23456','large accounts manager','8th Street South');

INSERT INTO drivers VALUES('43743','Single Trailer','4T1BE');
INSERT INTO drivers VALUES('23769','Single Trailer','F150A');

INSERT INTO accounts VALUES('87625036','34725','Bushy Brown','(201) 874-4399','residential','2006-05-19 13:16:14.559','2018-03-01 06:50:29',837646.52);
INSERT INTO accounts VALUES('11111111','12345','Ben Brown','(201) 111-1111','residential','2006-05-19 13:16:14.559','2018-02-25 06:50:29',837646.52);
INSERT INTO accounts VALUES('22222222','23456','Bob Brown','(201) 222-2222','residential','2006-05-19 13:16:14.559','2018-01-01 06:50:29',837646.52);
