#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#define FIFO_NAME "/tmp/myfifo"

int main() {
    int fd;
    char input[256];
    
    mkfifo(FIFO_NAME, 0666);
    
    while (1) {
        fd = open(FIFO_NAME, O_WRONLY);
        printf("Enter message (or 'exit' to quit): ");
        fgets(input, sizeof(input), stdin);
        write(fd, input, strlen(input) + 1);
        close(fd);
        
        if (strcmp(input, "exit\n") == 0) break;
    }
    
    return 0;
}