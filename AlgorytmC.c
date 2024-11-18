#include <stdio.h>
#include <string.h>

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

int main(int argc, char *argv[]) {
   
    char *startPos = argv[1];
    int startPosReceived[3];
    char *endPos = argv[2];
    int endPosReceived[2];
    for (int i = 0; startPos[i] != '\0'; i++) {
        startPosReceived[i] = startPos[i] - '0';  // Convert char to int by subtracting '0'
        printf("startPosReceived[%d] = %d\n", i, startPosReceived[i]);
    }
    
    for (int i = 0; endPos[i] != '\0'; i++) {
        endPosReceived[i] = startPos[i] - '0';  // Convert char to int by subtracting '0'
        printf("endPosReceived[%d] = %d\n", i, endPosReceived[i]);
    }
    
    //printf("StartPos : %s\n",startPos);
    //printf("EndPos : %s\n",endPos);
    
    


    // Print instructions
    printf("Instructions: %s\n", instructions);


    return 0;
}
