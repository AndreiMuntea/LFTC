%option noyywrap

IDENTIFIER [a-zA-Z][a-zA-Z0-9_]*
NUMERIC_CONSTANT ([-\+]{0,1}[1-9][0-9]*)|0 
CHAR_CONSTANT '[0-9a-zA-Z]'

%{
#include <stdio.h>
#include <iostream>
#include <windows.h>
#include <shlwapi.h>
#include <stdio.h>
#include "hello.tab.h"

using namespace std;

#define YY_DECL extern "C" int yylex()

%}

%%

[ \t\n]+ ;
"==" { return EQ;  }
"!=" { return NE;  }
"<" { return LT;  }
"<=" { return LE;  }
">" { return GT; }
">=" { return GE; }
"+" { return ADDITION; }
"-" { return SUBTRACTION; }
"*" { return MULTIPLICATION; }
"/" { return DIVISION; }
"%" { return MODULO; }
")" { return CLOSED_ROUND_BRACKET; }
"(" { return OPENED_ROUND_BRACKET; }
"]" { return CLOSED_SQUARED_BRACKET; }
"[" { return OPENED_SQUARED_BRACKET; }
"}" { return CLOSED_CURLY_BRACKET; }
"{" { return OPENED_CURLY_BRACKET; }
"=" { return ASSIGN; }
";" { return SEMICOLON; }
"BEGIN" { return BEGIN_TOK; }
"END" { return END_TOK; }
"INT" { return INT_TYPE; }
"CHAR" { return CHAR_TYPE; }
"IF" { return IF; }
"WHILE"  { return WHILE; }
"READ"  { return READ; }
"WRITE" { return WRITE; }
{IDENTIFIER} { yylval.ival = strdup(yytext); return IDENTIFIER; }
{NUMERIC_CONSTANT} { yylval.nval = atoi(yytext); return NUMERIC_CONSTANT; }
{CHAR_CONSTANT} { yylval.cval = strdup(yytext); return CHAR_CONSTANT; }
. { printf("error %s ", yytext); }

%%