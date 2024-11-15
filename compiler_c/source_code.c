/* INCLUDES */
#include <stdio.h>
/* DEFINES */
#define vector<int> vi
#define loop(x,n) for(int x = 0; x < n; ++x) 
#define macro(x) (x < 10)
#define macro3(x) (x * 10)

/* FUNCTIONS */
int mult(int x, int y){return (x * y);}
int factorial(int n) {
    /* VARIABLES */
    int result = 1;
    float result2 = 20.2, result3 = 3.3f;
    char a = 'a';
    /* FOR LOOP */
    for (int i = 1; i <= n; i++) {
        result = result * i;
    }
    /* IF STATEMENT */
    // Printf no existe en la gramatica xd
    if (result2 >= 10.0f) {
        result = 2;
        //printf("y is greater than or equal to 10.0\n");
    } else {
        result = 3;
        //printf("y is less than 10.0\n");
    }
    switch(result){
        case 2:
            result = 4;
            break;
        case 3:
            result = 9;
            break;
        default:
            break;
    }
    result = mult(result, 2);
    return result;
}

/* MAIN FUNCTION */
void main() {
    return;
}
