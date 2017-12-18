bison -d hello.y
flex hello.l 
C:\work\mingw\bin\g++ hello.tab.c lex.yy.c -o hello
hello.exe