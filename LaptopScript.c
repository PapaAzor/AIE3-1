#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

//#include <wiringPi.h>



//#define PWM_RANGE 250
#define PORT 8000  



int server_fd, new_socket;
struct sockaddr_in address;
int addrlen = sizeof(address);
char buffer[1024] = {0};

void setup() {
    // Initialize WiringPi
    //wiringPiSetupGpio();  
    // Set PWM mode as mark-space
   // pwmSetMode(PWM_MODE_MS); 
   // pwmSetRange(PWM_RANGE);  
    // Set PWM clock divisor for 100 kHz 
   // pwmSetClock(192);   
	

	
    // Initialize TCP server
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

    printw("Server is listening on port %d\n", PORT);
    //refresh();
}



void *tcp_server_thread_function(void *arg) {
    while (1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("accept");
            continue;
        }

        
    }
    return NULL;
}

 void *camera_thread_function(void *arg){
	
	system(" rpicam-vid -t 0 -n --framerate 40 --saturation 0 --denoise cdn_fast --contrast 0.2 --sharpness 0.1 --inline -o - | gst-launch-1.0 fdsrc fd=0 ! udpsink host=10.45.0.1 port=6433");
	//change the protocol
    return NULL;
	}

int main() {
    setup();
	
    pthread_t  tcp_server_thread,camera_thread; //

    

    // Create thread for TCP server
    if (pthread_create(&tcp_server_thread, NULL, tcp_server_thread_function, NULL) != 0) {
        fprintf(stderr, "Error creating TCP server thread\n");
        return 1;
    }
    if (pthread_create(&camera_thread, NULL, camera_thread_function, NULL) != 0) {
        fprintf(stderr, "Error creating camera thread\n");
        return 1;
    } 

    // Wait for the threads to finish
   
    if (pthread_join(tcp_server_thread, NULL) != 0) {
        fprintf(stderr, "Error joining TCP server thread\n");
        return 1;
    }
    if (pthread_join(camera_thread, NULL) != 0) {
        fprintf(stderr, "Error joining camera thread\n");
        return 1;
    } 
    

   
    close(server_fd);
    return 0;
}
