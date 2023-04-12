# PascalToCConverter
Converts simple programs written in Pascal to C.  
## Example
### Input
```
program Parzystosc;
type
    liczba=integer;
var
    i:liczba;
procedure czyParzysta(a:integer);
begin
   if a mod 2 = 0 then writeln('Parzysta')
   else writeln('Nieparzysta');
end;
begin
    for i:=1 to 10 do
    begin
        czyParzysta(i);
    end;
end.
```
### Output
```
//Program: Parzystosc
#include <stdio.h>
#include <stdbool.h>
typedef int liczba;
liczba i;
void czyParzysta(int a)
{
	if (a%2==0)
	printf("%s \n","Parzysta");
	else
	printf("%s \n","Nieparzysta");
}
void main()
{
	for(i=1;i<=10;++i){
	
	czyParzysta(i);
	}
}
```
