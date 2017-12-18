%{

#include <cstdio>
#include <iostream>
using namespace std;

extern "C" int yylex();
extern "C" int yyparse();
extern "C" FILE* yyin;

void yyerror(const char* s);
%}

%union {
	char* ival;
	char* cval;
	int nval;
}

%token EQ
%token NE
%token LT
%token LE
%token GT
%token GE
%token ADDITION
%token SUBTRACTION
%token MULTIPLICATION
%token DIVISION
%token MODULO
%token CLOSED_ROUND_BRACKET
%token OPENED_ROUND_BRACKET
%token CLOSED_SQUARED_BRACKET
%token OPENED_SQUARED_BRACKET
%token CLOSED_CURLY_BRACKET
%token OPENED_CURLY_BRACKET
%token ASSIGN
%token SEMICOLON
%token BEGIN_TOK
%token END_TOK
%token INT_TYPE
%token CHAR_TYPE
%token IF
%token WHILE
%token READ
%token WRITE

%token <ival> IDENTIFIER
%token <nval> NUMERIC_CONSTANT
%token <cval> CHAR_CONSTANT

%%

program:
	BEGIN_TOK aux_decl aux_statement END_TOK {cout << "Works";}
	;
aux_decl:
	/* empty */
	| aux_decl declaration
	;
aux_statement:
	/* empty */
	| aux_statement statement
	;
declaration: 
	type IDENTIFIER SEMICOLON		{ cout << "A variable was declared: " << $2 << endl;}
	;
type:
	INT_TYPE
	| CHAR_TYPE
	;

statement: 
	assignment
	| input
	| output
	| conditional
	| loop
	;

conditional:
	IF OPENED_ROUND_BRACKET condition CLOSED_ROUND_BRACKET OPENED_CURLY_BRACKET aux_statement CLOSED_CURLY_BRACKET  { cout << "CONDITIONAL STATEMENT ENCOUNTERED" << endl;}
	;
assignment:
	IDENTIFIER ASSIGN expression SEMICOLON		{ cout << "ASSIGNMENT ENCOUNTERED" << endl;}
	;

expression:
	expr_m_var 
	| expression expr_operator expr_m_var
	;

condition :
	expression relation expression
	;

loop: 
	WHILE OPENED_ROUND_BRACKET condition CLOSED_ROUND_BRACKET OPENED_CURLY_BRACKET aux_statement CLOSED_CURLY_BRACKET		{ cout << "LOOP ENCOUNTERED" << endl;}
	;

input:
	READ OPENED_ROUND_BRACKET IDENTIFIER CLOSED_ROUND_BRACKET SEMICOLON			{ cout << "INPUT ENCOUNTERED" << endl;}
	;

output:
	WRITE OPENED_ROUND_BRACKET expr_member CLOSED_ROUND_BRACKET SEMICOLON		{ cout << "OUTPUT ENCOUNTERED" << endl;}
	;

expr_operator:
	ADDITION
	| SUBTRACTION
	| MULTIPLICATION
	| DIVISION
	| MODULO
	;
expr_member:
	IDENTIFIER | NUMERIC_CONSTANT | CHAR_CONSTANT
	;
expr_m_var:
	expr_member
	| OPENED_ROUND_BRACKET expr_member expr_operator expr_member CLOSED_ROUND_BRACKET
	;
relation:
	EQ
	| NE
	| LT 
	| LE 
	| GT
	| GE
	;

%%

int main() {
	FILE *myfile = fopen("programel.txt", "r");
	if (!myfile) {
		cout << "I can't open a.snazzle.file!" << endl;
		return -1;
	}

	yyin = myfile;

	do {
		yyparse();
	} while(!feof(yyin));
	return 0;
}

void yyerror(const char* s) {
	fprintf(stderr, "Parse error: %s\n", s);
	exit(1);
}