%{
	#include<stdio.h>
	#include<string.h>
	#include<stdlib.h>
	FILE *fp, *fp1;
%}

%%

[scanf\(\".*\"\)\;]	{fprintf(fp1,"Input :"); fprintf(fp1,"%s",yytext)}}

.*	{fprintf(fp1,"%s",yytext);}

[\n \t\!\@\#\$\%\^\&\*\(\)\-\+\=\\\|\~\`\?\/\>\.\<\,]	{fprintf(fp1,"%s",yytext);}

%%

int main(int argc, char **argv)
{
	char *str;
	str = (char *) malloc (strlen(argv[1])+8);
	strcpy(str,"temp");
	strcat(str,argv[1]);
	fp = fopen(argv[1],"r");
	fp1 = fopen(str,"w");
	yyin = fp;
	yylex();
	fclose(fp);
	fclose(fp1);
	return 0;
}

int yywrap()
{
	return 1;
}
