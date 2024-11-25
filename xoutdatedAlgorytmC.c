#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

// Global variables for instructions and drive arrays
char instructions[256];
char drive[256];
int ins_index = 0, drive_index = 0;

// Append to instructions
void append_instruction(char instruction) {
    instructions[ins_index++] = instruction;
    instructions[ins_index] = '\0';
}

// Append to drive array
void append_drive(char step) {
    drive[drive_index++] = step;
    drive[drive_index] = '\0';
}


// Function to generate instructions
void dist_way(int x1, int y1, int x2, int y2) {
    int cur_x = x1, cur_y = y1;
    int tar_x = x2, tar_y = y2;

    while (cur_x != tar_x || cur_y != tar_y) {
        if (cur_y != tar_y) {
            if (tar_y > cur_y) {
                append_instruction('u');
                cur_y++;
            } else if (tar_y < cur_y) {
                append_instruction('d');
                cur_y--;
            }
        } else if (cur_x != tar_x) {
            if (tar_x > cur_x) {
                append_instruction('r');
                cur_x++;
            } else if (tar_x < cur_x) {
                append_instruction('l');
                cur_x--;
            }
        }
    }
}

// Convert instructions to drive commands
void list_dir() {
    char direction = 'u'; // Initial direction

    for (int i = 0; i < ins_index; i++) {
        char current = instructions[i];
        if (current == direction) {
            append_drive('F');
        } else {
            if (current == 'u') {
                if (direction == 'l') append_drive('R');
                if (direction == 'r') append_drive('L');
                if (direction == 'd') append_drive('T');
                direction = 'u';
            } else if (current == 'd') {
                if (direction == 'l') append_drive('L');
                if (direction == 'r') append_drive('R');
                if (direction == 'u') append_drive('T');
                direction = 'd';
            } else if (current == 'l') {
                if (direction == 'd') append_drive('R');
                if (direction == 'u') append_drive('L');
                if (direction == 'r') append_drive('T');
                direction = 'l';
            } else if (current == 'r') {
                if (direction == 'u') append_drive('R');
                if (direction == 'd') append_drive('L');
                if (direction == 'l') append_drive('T');
                direction = 'r';
            }
        }
    }
}


void send_command(int socket, const char *command) {
    ssize_t bytes_sent = send(socket, command, strlen(command), 0);
    if (bytes_sent == -1) {
        perror("send failed");
    } else {
        printf("Sent %ld bytes\n", bytes_sent);
    }
}
int main(int argc, char *argv[]) {
    // Check if enough arguments were provided
    if (argc < 4) {
        fprintf(stderr, "Usage: %s <startPos> <endPos> <server_fd>\n", argv[0]);
        return 1;
    }

    // Print the arguments for debugging
    for (int i = 0; i < argc; i++) {
        printf("argv[%d]: %s\n", i, argv[i]);
    }

    // Parse the start and end positions from command-line arguments
    char *startPos = argv[1];
    char *endPos = argv[2];
    char *server_fd = argv[3];

    // Convert start and end positions to integer arrays
    int startPosReceived[3] = {0};  // Assuming the positions contain 3 digits
    int endPosReceived[2] = {0};    // Assuming the positions contain 2 digits
    
    for (int i = 0; startPos[i] != '\0' && i < 3; i++) {
        startPosReceived[i] = startPos[i] - '0';  // Convert char to int by subtracting '0'
        //printf("startPosReceived[%d] = %d\n", i, startPosReceived[i]);
    }

    for (int i = 0; endPos[i] != '\0' && i < 2; i++) {
        endPosReceived[i] = endPos[i] - '0';  // Convert char to int by subtracting '0'
        //printf("endPosReceived[%d] = %d\n", i, endPosReceived[i]);
    }

    // Convert server_fd (string) to an integer file descriptor
    int serverFdInt = atoi(server_fd);
    if (serverFdInt <= 0) {
        fprintf(stderr, "Invalid server file descriptor: %s\n", server_fd);
        return 1;
    }

    printf("ServerFd: %d\n", serverFdInt);

    // Send a sample command to the server
    printf("Sending data...\n");
    send_command(serverFdInt, "hello");

    // Optional: Print instructions or any other message (you must define it)
    // char instructions[] = "These are your instructions.";
    // printf("Instructions: %s\n", instructions);

    return 0;
}

