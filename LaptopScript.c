#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
// Not all of those libraries are necessary , but I dont remember which
#define PORT 65432  // Define the port for TCP connection

int sock = 0;
struct sockaddr_in serv_addr;



	
/*void *receive_image_thread_function(void *arg){
	system("gst-launch-1.0 udpsrc address=10.45.0.1 port=6433 ! h264parse ! decodebin ! autovideosink");
	} */

int main() {
    //Reference the Ip from python to this script
    char smth; // something
    char *server_ip = smth;

    // Create socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\n Socket creation error \n");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Convert IPv4 and IPv6 addresses from text to binary form
    if (inet_pton(AF_INET, server_ip, &serv_addr.sin_addr) <= 0) {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    // Connect to the server
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        printf("\nConnection Failed \n");
        return -1;
    }

   

    // Close the socket
    close(sock);

    printf("Connection closed.\n");
    return 0;
}
