#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#define SOCKET_NAME "/tmp/ipc_socket"

int main() {
    struct sockaddr_un addr;
    int fd;

    fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (fd == -1) {
        perror("socket");
        exit(1);
    }

    memset(&addr, 0, sizeof(struct sockaddr_un));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, SOCKET_NAME, sizeof(addr.sun_path) - 1);

    if (connect(fd, (struct sockaddr *)&addr, sizeof(struct sockaddr_un)) == -1) {
        perror("connect");
        exit(1);
    }

    char input[256];
    while (1) {
        printf("Enter message (or 'exit' to quit): ");
        fgets(input, sizeof(input), stdin);
        if (write(fd, input, strlen(input) + 1) == -1) {
            perror("write");
            exit(1);
        }
        if (strcmp(input, "exit\n") == 0) break;
    }

    close(fd);
    return 0;
}