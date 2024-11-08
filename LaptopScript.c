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

/*void *receive_image_thread_function(void *arg) {
    // Use GStreamer to receive and display the video stream
    system("gst-launch-1.0 udpsrc address=0.0.0.0 port=6433 ! h264parse ! decodebin ! autovideosink");
    return NULL;
}*/

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
int startingPos[2];
char endPos[2];

void *tcp_server_thread_function(void *arg) {
    while (1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("Accept failed");
            continue;
        }

        int valread;
        #define arr_size 126
        int arr_index = 0;
        char arr[arr_size] = {0};
        
        
        while ((valread = read(new_socket, buffer, BUFFER_SIZE - 1)) > 0) {
            buffer[valread] = '\0';  // Null-terminate the received data
            printf("Received endpoint data: %s\n", buffer);

             
            for (int i = 0; i < valread; i++) {
                if (arr_index < arr_size - 1) {  
                    arr[arr_index] = buffer[i];  
                    printf("Added to arr[%d]: %c\n", arr_index, arr[arr_index]);  
                    arr_index++;  
                }
            }
            if (arr[0] == 'u') {
                printf("\nGoing Up");
            } else if (arr[0] == 'd') {
                printf("\nGoing Down");
            } else if (arr[0] == 'l') {
                printf("\nGoing Left");
            } else if (arr[0] == 'r') {
                printf("\nGoing Right");
            }

            // e for endpoint
            if (arr[0] == 'e') {
                endPos[0] = arr[1];  
                endPos[1] = arr[3];  
               // printf("endPos[0]: %c, endPos[1]: %c\n", endPos[0], endPos[1]);  
            }
            if (arr[0] == 's') {
                startingPos[0] = arr[2]-'0';  
                startingPos[1] = arr[5]-'0';  
                //printf("startingPos[0]: %d, startingPos[1]: %d\n", startingPos[0], startingPos[1]); 
            }
            printf("\nendPos[0]: %c, endPos[1]: %c\n", endPos[0], endPos[1]);
			printf("\nstartingPos[0]: %d, startingPos[1]: %d\n", startingPos[0], startingPos[1]); 
            
        }

        if (valread == 0) {
            printf("\nClient disconnected.\n");
        }
        close(new_socket); 
    }
    
    return NULL;
}

int main() {
    setup();
    
    pthread_t tcp_server_thread;//,receive_image_thread;
    
    if (pthread_create(&tcp_server_thread, NULL, tcp_server_thread_function, NULL) != 0) {
        
        return 1;
    } 
    /*if (pthread_create(&receive_image_thread, NULL, receive_image_thread_function, NULL) != 0) {
        fprintf(stderr, "Error creating image thread\n");
        return 1;
    }*/

    
    if (pthread_join(tcp_server_thread, NULL) != 0) {
        fprintf(stderr, "Error joining TCP server thread\n");
        return 1;
    }
    
    /* if (pthread_join(receive_image_thread, NULL) != 0) {
        fprintf(stderr, "Error joining image thread\n");
        return 1;
    }*/

    close(server_fd);
    return 0;
}
