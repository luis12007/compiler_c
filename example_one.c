/* Function to calculate factorial */
int factorial(int n) {
    // Check if number is negative
    if (n < 0) {
        return -1; // Invalid input
    }

    int result = 1;
    for (int i = 1; i <= n; i++) {
        result = result * i; // Multiply result by i
    }
    return result; // Return the factorial
}