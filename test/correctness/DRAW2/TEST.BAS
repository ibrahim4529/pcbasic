10 REM PC-BASIC test 
20 REM DRAW syntax
30 SCREEN 9
35 OPEN "OUTPUT.TXT" FOR OUTPUT AS 1
40 ON ERROR GOTO 1000
50 DRAW
60 DRAW 10
70 DRAW "1"
80 DRAW "1", "2"
90 X$="u1d1l1r1": DRAW X$
100 DRAW "U1u1D1d1L1l1R1r1ULDRE1e1F1f1G1g1H1h1EFGHBU1ND1M+1,1M+1,-1M10,10"
110 DRAW "S8U1D1TA0U1D1A0U1D1"
120 DRAW "A0A1A2A3"
130 DRAW "A4"
140 DRAW "A-1"
150 DRAW "TA-360TA0TA360"
160 DRAW "TA400"
170 DRAW "S-1"
180 DRAW "S256"
190 DRAW "C0"
200 DRAW "C256"
210 DRAW "C32768"
220 DRAW "P1,0"
230 DRAW "P9999,0"
240 DRAW "P10000,0"
250 DRAW "XX$;"
260 DRAW "XA;"
270 DRAW "X"+VARPTR$(X$)
280 A=1: B(0) = 1
290 DRAW "U=A;"
300 DRAW "U=B(0);"
310 DRAW "U="+VARPTR$(A)
320 END
1000 PRINT#1, ERR, ERL
1010 RESUME NEXT
