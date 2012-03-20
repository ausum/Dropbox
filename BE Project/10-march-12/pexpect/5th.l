%{
	#include<stdio.h>
	#include<stdlib.h>
	int line;
%}

%%
[a-zA-Z]+	{ECHO;}	

[ \t]+	{ECHO;}

[\n]	{ECHO; line++;}

[\.]+	{ECHO;}

[^a-zA-Z \t\n]+	{ECHO; yywrap();}
%%

int main()
{
	line=0;
	yyin=fopen("abc.txt","r");
	yylex();
	fclose(yyin);
	return 0;
}

int yywrap()
{
	if(yyin==NULL)
		return 1;
	printf("\n(Error occured at line: %d - Unrecognised symbol %s)\n",line,yytext);	
	yyin++;
	yylex();
}
