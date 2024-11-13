#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8000
#define BUFFER_SIZE 1024

int server_fd, new_socket;
struct sockaddr_in address;
int addrlen = sizeof(address);
char buffer[BUFFER_SIZE] = {0};

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

void *tcp_server_thread_function(void *arg) { // kolejnosc to wczytaj dane ze strony(start i end )-> polacz sie z rpi i przeslij. Start sie przsyla end do zrobienia i rozpoznawanie
    while (1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("Accept failed");
            continue;
        }
        snprintf(startingPosChar, sizeof(startingPosChar), "%d,%d,%d", startingPos[0], startingPos[1], startingPos[2]);
		send_command(new_socket, startingPosChar);
        printf("Client connected.\n");
        for(int i=0;i<3;i++){
				startingPosChar[i]=startingPos[i]+ '0';
				printf("startingPosChar[i]: %d\n", startingPosChar[i]);
				}
		
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
            }
            if (arr[0] == 's') {
                startingPos[0] = arr[2] - '0';
                startingPos[1] = arr[5] - '0';
                startingPos[2] = arr[8] - '0';
                startingPos[2] *= 90;
                //printf("startingPos[0]: %d, startingPos[1]: %d, startingPos[2]: %d\n", startingPos[0], startingPos[1], startingPos[2]);

                
            
            send_command(new_socket, startingPosChar);
            }
            
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
	
    pthread_t tcp_server_thread;

    if (pthread_create(&tcp_server_thread, NULL, tcp_server_thread_function, NULL) != 0) {
        fprintf(stderr, "Error creating TCP server thread\n");
        return 1;
    }

    if (pthread_join(tcp_server_thread, NULL) != 0) {
        fprintf(stderr, "Error joining TCP server thread\n");
        return 1;
    }

    close(server_fd);
    return 0;
}
