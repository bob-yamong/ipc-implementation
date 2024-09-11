#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>

#define FILE_NAME "/tmp/mmaptest"
#define MSG_SIZE 256

int main() {
    int fd;
    char *addr;
    
    fd = open(FILE_NAME, O_RDWR | O_CREAT, S_IRUSR | S_IWUSR);
    if (fd == -1) {
        perror("open");
        exit(1);
    }
    
    if (ftruncate(fd, MSG_SIZE) == -1) {
        perror("ftruncate");
        exit(1);
    }
    
    addr = mmap(NULL, MSG_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (addr == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }
    
    while (1) {
        printf("Enter message (or 'exit' to quit): ");
        fgets(addr, MSG_SIZE, stdin);
        if (strcmp(addr, "exit\n") == 0) break;
    }
    
    munmap(addr, MSG_SIZE);
    close(fd);
    return 0;
}