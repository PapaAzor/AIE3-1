#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    // Define the two arguments
    char *arg1 = argv[1]; // Starting position
    char *arg2 = argv[2]; // Ending position

    // Construct the command to run the path_finder program
    char command[256];
    snprintf(command, sizeof(command), "./Algorithm '%s' '%s'", arg1, arg2);

    // Execute the command
    int result = system(command);

    // Check execution result
    if (result == -1) {
        perror("Error executing path_finder");
        return 1;
    }

    return 0;
}
