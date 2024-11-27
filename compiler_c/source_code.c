/* INCLUDES */
#include <stdio.h>

/* DEFINES */
#define vector<int> vi
#define loop(x,n) for(int x = 0; x < n; ++x) 
#define macro(x,y) (x * y)
#define macro2(x) (x < 10)

/* FUNCTIONS */
int factorial(int n) {

    /* VARIABLES */
    float result33 = 50.0;
    int result =  1, result22 = 22;

    float result2 = 20.2, result3 = 3.3f;
    char a = 'c';
    float eq = 2.2/3.3*result^-2;

    /* TEST -----------------------------*/
    /* int int  = 50.0; */

    float floatint = 2;

    int trymacro = macro(2,30);
    /* float trymacro2 = macro2(3.2); */
    /* int varname = loop(3,2); */

    /* TEST -----------------------------*/


    /* ASINGNACION CON VARIABLES */
    int sum = result / 1  + result3 + 2;
    float sum2 = result2 + result3 + 3;

    /* FOR LOOP */
    for(int i = 1; i <= n; i++) {
        result = result * i;
    }

    /* IF STATEMENT */
    if (!result2 >= 10.0) {
        result = 10;
        char b = 's';
    } else {
        result = 20;
    } 
    return result;
}


/* MAIN FUNCTION */
void main() {
    factorial(1);
    return;
}

/* TESTING


    float invalid_eq = 5.5 / "abc";



    #include "file1.h"
    #include "file2.h"

    {
    int x = "string";
    }

    float invalid_expr = 1 / 0;
    float invalid_expr2 = 1.0 / (2 - 2);
    int logic = 10 &&;

    return 5;
    void main() {
        int val = 10;
        return val;
    }

    int factorial float (int n);
        factorial();
        factorial(1, 2);

    int result = 10 ^ 5;
    char invalidChar = 'abcd';
    float eq = 3.5 & 2.2;

 */