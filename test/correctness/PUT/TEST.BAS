40 DIM TWO%(35), A%(100)
50 KEY OFF: SCREEN 1
60 FOR I = 0 TO 35: READ TWO%(I): NEXT I
70 PUT (0,0), TWO%
80 LOCATE 5,1
90 DATA 32,16,0,0,0,0,16128,252,-253,255,-16369,15
100 DATA 15,15,0,63,0,252,768,240,3840,192,16128,0
110 DATA -1024,0,-253,255,-241,255,0,0,0,0,0,0
135 OPEN "OUTPUT.DAT" FOR OUTPUT AS 1
140 GET(0,0)-(20,20),A%
145 GOSUB 2000
148 CLOSE 1
999 END
2000 REM
2010 FOR K=0 TO 100
2020 PRINT#1, MKI$(A%[K]);
2030 NEXT
2050 RETURN



