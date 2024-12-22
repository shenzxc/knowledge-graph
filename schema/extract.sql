SELECT cui,str,tty 
FROM mrconso
WHERE sab='SNOMEDCT_US' and tty in ('PT','SY')
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/SNOMEDCT_US.txt'
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\n';

SELECT cui,str,tty 
FROM mrconso
WHERE sab='HPO' and tty in ('PT','SY','ET')
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/HPO.txt'
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\n';

SELECT cui,str,tty 
FROM mrconso
WHERE sab='MEDLINEPLUS' and tty in ('PT','SY')
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/MEDLINEPLUS.txt'
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\n';

SELECT cui,str,tty 
FROM mrconso
WHERE sab='NCI' and tty in ('PT','SY','BN','FBD','AB')
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/NCI.txt'
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\n';

SELECT cui,str,tty 
FROM mrconso
WHERE sab='RXNORM' and tty in ('SY','SCD','PSN','SCDC','TMSY','SBDG','SCDG','SCDF','IN','PIN','DF','DFG','BN')
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/RXNORM.txt'
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\n';

SELECT cui,str,tty 
FROM mrconso
WHERE sab='MTH' and tty in ('PT','SY','PN')
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/MTH.txt'
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\n';

SELECT cui,str,tty 
FROM mrconso
WHERE sab='MSH' and tty in ('ET','MH','PEP','CE','PCE','NM')
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/MSH.txt'
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\n';

SELECT cui,str,tty 
FROM mrconso
WHERE sab='CPT' and tty in ('ETCLIN','SY','PT','ETCF')
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/CPT.txt'
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\n';

SELECT cui,sty
FROM mrsty
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/UMLS_semtypes.txt'
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\n';