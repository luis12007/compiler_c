/* INCLUDES */
#include <stdio.h>

/* DEFINES */
#define vector<int> vi
#define loop(x,n) for(int x = 0; x < n; ++x) 
#define macro(x) (x < 10)
#define macro3(x) (x * 10)

/* FUNCTIONS */
int factorial(int n) {

    /* VARIABLES */
    int result = 1, result2 = 2;
    float result2 = 20.2, result3 = 3.3f;
    char a = 'a';
    int eq = 2/3*result^-2;



    /* ASINGNACION CON VARIABLES */
    int sum = result / 1  + result3 + 2;
    /* float sum2 = result2 + result3 + 3; */

    /* FOR LOOP */
    for (int i = 1; i <= n; i++) {
        result = result * i;
    }

    /* IF STATEMENT */
    if (result2 >= 10.0) {
        result = 10;
        char b = 'b';
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