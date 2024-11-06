#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8000
#define BUFFER_SIZE 1024  // Define BUFFER_SIZE

int server_fd, new_socket;
struct sockaddr_in address;
int addrlen = sizeof(address);
char buffer[BUFFER_SIZE] = {0};
int sock = 0;

void setup() {
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("listen");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Server is listening on port %d\n", PORT);
}



char getch() {
    char ch;
    read(STDIN_FILENO, &ch, 1);  // Read a single character
    return ch;
}

// Function to send a command to the server
void send_command(const char *command) {
    send(sock, command, strlen(command), 0);  // Send command to server
}

// Thread function to handle TCP connections and read commands
void *tcp_server_thread_function(void *arg) {
    while (1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("accept");
            continue;
        }

        // Read the incoming command from the client
        int valread[10];  // Array to store the number of bytes read for each command

for (int i = 0; i < 10; i++) {  // Loop without going out of bounds
    valread[i] = read(new_socket, buffer, BUFFER_SIZE);  // Read from socket into buffer

    if (valread[i] > 0) {
        // Safely null-terminate the buffer
        if (valread[i] < BUFFER_SIZE) {
            buffer[valread[i]] = '\0';  // Null-terminate after the last byte read
        } else {
            buffer[BUFFER_SIZE - 1] = '\0';  // Null-terminate at buffer limit
        }

        // Print each character in the buffer separately
        printf("Received command: ");
        for (int j = 0; j < valread[i]; j++) {
            printf("%c\n", buffer[j]);  
				if(buffer[j]=='u'){
					printf("Going Up");
					}
				if(buffer[j]=='d'){
					printf("Going Down");
					}
				if(buffer[j]=='l'){
					printf("Going Left");
					}
				if(buffer[j]=='r'){
					printf("Going Right");
					}
        }
    } else if (valread[i] == 0) {
        printf("Client disconnected.\n");
        break;  // Exit the loop if the client has disconnected
    } else {
        perror("read failed");
        break;  // Exit the loop on read failure
    }
}


        // Close the client connection
        close(new_socket);
    }
    return NULL;
}

int main() {
    setup();
    
    pthread_t tcp_server_thread;

    // Create thread for TCP server
    if (pthread_create(&tcp_server_thread, NULL, tcp_server_thread_function, NULL) != 0) {
        fprintf(stderr, "Error creating TCP server thread\n");
        return 1;
    }

    // Wait for the thread to finish
    if (pthread_join(tcp_server_thread, NULL) != 0) {
        fprintf(stderr, "Error joining TCP server thread\n");
        return 1;
    }

    close(server_fd);
    return 0;
}
