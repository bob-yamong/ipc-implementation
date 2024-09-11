#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <errno.h>

#define FIFO_NAME "/tmp/myfifo"
#define BUFFER_SIZE 256

int main() {
    int fd;
    char input[BUFFER_SIZE];
    
    // Create the named pipe
    if (mkfifo(FIFO_NAME, 0666) == -1) {
        if (errno != EEXIST) {
            perror("mkfifo");
            exit(1);
        }
    }
    
    printf("Waiting for receiver...\n");
    
    // Open the pipe for writing, with blocking mode
    fd = open(FIFO_NAME, O_WRONLY);
    if (fd == -1) {
        perror("open");
        exit(1);
    }
    
    printf("Connected to receiver. Ready to send messages.\n");
    
    while (1) {
        printf("Enter message (or 'exit' to quit): ");
        if (fgets(input, sizeof(input), stdin) == NULL) {
            break;
        }
        
        // Remove newline character
        input[strcspn(input, "\n")] = 0;
        
        // Write to the pipe
        ssize_t bytes_written = write(fd, input, strlen(input) + 1);
        if (bytes_written == -1) {
            perror("write");
            break;
        }
        
        printf("Sent: %s\n", input);
        
        if (strcmp(input, "exit") == 0) break;
    }
    
    close(fd);
    // Don't unlink the FIFO here, let the receiver do it
    return 0;
}