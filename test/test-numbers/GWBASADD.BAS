10 OPEN "failures.dat" FOR RANDOM AS 1 LEN=4
20 FIELD#1, 4 AS A$
30 OPEN "gwbasfai.dat" FOR RANDOM AS 2 LEN=20
40 FIELD#2, 4 AS B$, 4 AS C$, 4 AS D$, 4 AS E$, 4 AS F$
50 FOR I = 1 TO 2048
60   GET#1, I
70   L = R: R = CVS(A$)
75   LSET B$ = MKS$(L+R)
76   LSET C$ = MKS$(L-R)
77   LSET D$ = MKS$(-L+R)
78   LSET E$ = MKS$(-L-R)
79   LSET F$ = MKS$(2*L+2*R)
80   PUT#2, I
90 NEXT
100 CLOSE
