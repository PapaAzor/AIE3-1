#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <sys/types.h>
#include <signal.h>

#define PORT 8000  // Define the port for TCP connection
#define BUFFER_SIZE 1024

int sock = 0;
struct sockaddr_in serv_addr;
char buffer[BUFFER_SIZE] = {0};

void send_command(const char *command) {
    send(sock, command, strlen(command), 0);  // Send command to server
}

// Thread to receive data from the server
void *receive_data_thread_function(void *arg) {
    printf("New\n");
    int valread;
    while ((valread = read(sock, buffer, BUFFER_SIZE - 1)) > 0) {
        buffer[valread] = '\0';  // Null-terminate the received string
        printf("Received data from server: %s\n", buffer);  // Print the received data
        if(buffer[0]=='c'){
            int ClientX=buffer[1]-'0';
            int ClientY=buffer[2]-'0';
            printf("Received x: %d \n",ClientX);
            printf("Received y: %d \n",ClientY);
            }
    }
    return NULL;
}

void *run_command(void *arg) {
    int socket = *(int *)arg;  
    printf("socket: %d",socket);
    char command[100];
    snprintf(command, sizeof(command), "python3 -u QrDetect.py %d", socket);
    system(command);  
    return NULL;
}


int main(int argc, char *argv[]) {
    
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <server_ip>\n", argv[0]);
        return -1;
    }
    char *server_ip = argv[1];

    // Create socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Socket creation error");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Convert IPv4 and IPv6 addresses from text to binary form
    if (inet_pton(AF_INET, server_ip, &serv_addr.sin_addr) <= 0) {
        perror("Invalid address/ Address not supported");
        return -1;
    }


    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connection failed");
        return -1;
    }
   

     pthread_t thread;
    
    if (pthread_create(&thread, NULL, run_command, &sock) != 0) {
        perror("pthread_create failed");
        return 1;
    }

    printf("Command is running in the background...\n");

    pthread_join(thread, NULL);
    
    
        
   

    

    pthread_t receive_thread;
    

    
    if (pthread_create(&receive_thread, NULL, receive_data_thread_function, NULL) != 0) {
        fprintf(stderr, "Error creating receive thread\n");
        return 1;
    }
    
    
    pthread_join(receive_thread, NULL);
    

    // Close the socket
    close(sock);
    printf("Connection closed.\n");
    return 0;
}
