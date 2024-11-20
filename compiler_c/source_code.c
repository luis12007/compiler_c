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
    int result = 1
    float result2 = 20.2, result3 = 3.3f;
    char a = 'a';

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
    return;
}