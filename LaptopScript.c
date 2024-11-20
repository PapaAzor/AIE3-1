#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sqlite3.h>

#define PORT 8000
#define BUFFER_SIZE 1024



int server_fd, new_socket;
struct sockaddr_in address;
int addrlen = sizeof(address);
char buffer[BUFFER_SIZE] = {0};


//db stuff
sqlite3 *db;
sqlite3_stmt *stmt;
const char *sql = "SELECT x_position, y_position FROM qr_positions WHERE shape = ?"; 
int db_connection;
int rc;


void setup() {
    
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }


    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

  
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    rc = sqlite3_open("sia.db", &db);
    if (rc) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        exit(EXIT_FAILURE);
    } else {
        fprintf(stdout, "Opened database successfully\n");
    }
}

int check_if_exists_in_db(char search_value[]) {
    const char *sql = "SELECT x_position, y_position FROM qr_positions WHERE shape = ?";  // SQL query

    // Prepare the SQL query
    rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
        return 0;  // Return 0 to indicate failure
    }

    // Bind the search value to the SQL query
    sqlite3_bind_text(stmt, 1, search_value, -1, SQLITE_STATIC);

    // Execute the query and fetch results
    rc = sqlite3_step(stmt);
    if (rc == SQLITE_ROW) {
        // Retrieve the x_position and y_position
        int x_position = sqlite3_column_int(stmt, 0);  // First column is x_position
        int y_position = sqlite3_column_int(stmt, 1);  // Second column is y_position
        printf("Shape: '%s' -> x_position: %d, y_position: %d\n", search_value, x_position, y_position);
        sqlite3_finalize(stmt);  // Clean up after query
        return 1;  // Return 1 to indicate success
    } else {
        printf("No positions found for shape: '%s'\n", search_value);
        sqlite3_finalize(stmt);  // Clean up after query
        return 0;  // Return 0 to indicate no match found
    }
}


void algorythm(int arg1[], int arg2[], int size1, int size2) {
    char arg1c[size1 + 1];  // +1 for the null terminator
    char arg2c[size2 + 1];  
    
    for (int i = 0; i < size1; i++) {
        arg1c[i] = arg1[i] + '0';  
    }
    arg1c[size1] = '\0';  // Null-terminate the string

    for (int i = 0; i < size2; i++) {
        arg2c[i] = arg2[i] + '0';  
    }
    arg2c[size2] = '\0';  

    // Format the command string
    char command[256];
    snprintf(command, sizeof(command), "./Algorytm '%s' '%s'", arg1c, arg2c);

    // Execute the command
    int result = system(command);

    // Check execution result
    if (result == -1) {
        perror("Error executing path_finder");
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

int startingPos[3] = {2, 3, 90};
char startingPosChar[10];
char endPos[2];
int endPosInt[2];
int startSet = 0;
int endSet = 0;

void *tcp_server_thread_function(void *arg) {
    while (1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("Accept failed");
            continue;
        }
        snprintf(startingPosChar, sizeof(startingPosChar), "%d,%d,%d", startingPos[0], startingPos[1], startingPos[2]);
        send_command(new_socket, startingPosChar);
        printf("Client connected.\n");

        int valread;
        #define arr_size 126
        int arr_index = 0;
        char arr[arr_size] = {0};

        while ((valread = read(new_socket, buffer, BUFFER_SIZE - 1)) > 0) {
            buffer[valread] = '\0';
            printf("Received data: %s\n", buffer);

            for (int i = 0; i < valread; i++) {
                if (arr_index < arr_size - 1) {
                    arr[arr_index] = buffer[i];
                    arr_index++;
                }
            }

            if (arr[0] == 'e') {
                endPos[0] = arr[1];
                endPos[1] = arr[3];
                endPosInt[0] = endPos[0] - '0';
                endPosInt[1] = endPos[1] - '0';
                endSet = 1;
                
            }

            if (arr[0] == 's') {
                startingPos[0] = arr[2] - '0';
                startingPos[1] = arr[5] - '0';
                startingPos[2] = arr[8] - '0';
                startingPos[2] *= 90;
                startSet = 1;
                send_command(new_socket, startingPosChar);
            }

            if (startSet == 1 && endSet == 1) {
                algorythm(startingPos, endPosInt, 3, 2);
            }
            
           /* int found = check_if_exists_in_db(buffer);
			if (found) {
			printf("Shape '%s' found in the database.\n", buffer);
			} else {
			printf("Shape '%s' not found in the database.\n", buffer);
			}

			// Close the database after finishing all operations
			sqlite3_close(db);*/
            
        }

        if (valread == 0) {
            printf("Client disconnected.\n");
        }

        close(new_socket);
    }

    return NULL;
}

int main() {
    setup();
    /* this was for testing and it worked 
    char shape[]="Circle";
    int found = check_if_exists_in_db(shape);
			if (found) {
			printf("Shape '%s' found in the database.\n", shape);
			} else {
			printf("Shape '%s' not found in the database.\n", shape);
			}

			// Close the database after finishing all operations
			sqlite3_close(db);*/
    
    
    pthread_t tcp_server_thread;

    if (pthread_create(&tcp_server_thread, NULL, tcp_server_thread_function, NULL) != 0) {
        fprintf(stderr, "Error creating TCP server thread\n");
        return 1;
    }

    if (pthread_join(tcp_server_thread, NULL) != 0) {
        fprintf(stderr, "Error joining TCP server thread\n");
        return 1;
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);
    close(server_fd);
    return 0;
}
