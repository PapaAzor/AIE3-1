#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
// Not all of those libraries are necessary , but I dont remember which
#define PORT 8000  // Define the port for TCP connection

int sock = 0;
struct sockaddr_in serv_addr;




// Function to send a command to the server
void send_command(const char *command) {
    send(sock, command, strlen(command), 0);  // Send command to server
}

/*void *camera_thread_function(void *arg){
    system("rpicam-vid -t 0 -n --framerate 20 --saturation 0 --denoise cdn_fast --contrast 0.2 --sharpness 0.1 --inline -o - | gst-launch-1.0 fdsrc fd=0 ! udpsink host=192.168.28.196 port=6433");
    return NULL;
}*/

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <server_ip>\n", argv[0]);
        return -1;
    }
    char *server_ip = argv[1];

    // Create socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\nSocket creation error\n");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Convert IPv4 and IPv6 addresses from text to binary form
    if (inet_pton(AF_INET, server_ip, &serv_addr.sin_addr) <= 0) {
        printf("\nInvalid address/ Address not supported\n");
        return -1;
    }

    // Connect to the server
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        printf("\nConnection Failed\n");
        return -1;
    }

    
char str[]="uddp";// get this from algorithm
send_command(str);
        
        
    

    // Uncomment the camera thread code if needed:
    /*
    pthread_t camera_thread;
    if (pthread_create(&camera_thread, NULL, camera_thread_function, NULL) != 0) {
        fprintf(stderr, "Error creating camera thread\n");
        return 1;
    } 
    
    if (pthread_join(camera_thread, NULL) != 0) {
        fprintf(stderr, "Error joining camera thread\n");
        return 1;
    }
    */

    // Close the socket
    close(sock);
    printf("Connection closed.\n");
    return 0;
}
