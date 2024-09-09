#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BUFFER_SIZE 256

typedef int pid_t;

int main() {
    int pipefd[2];
    pid_t pid;
    char input[BUFFER_SIZE];

    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(1);
    }

    pid = fork();

    if (pid == -1) {
        perror("fork");
        exit(1);
    } else if (pid == 0) {  // Child process
        close(pipefd[1]);  // Close write end
        dup2(pipefd[0], STDIN_FILENO);
        close(pipefd[0]);
        execlp("python3", "python3", "ipc_receiver.py", NULL);
        perror("execlp");
        exit(1);
    } else {  // Parent process
        close(pipefd[0]);  // Close read end

        while (1) {
            printf("Enter message (or 'exit' to quit): ");
            fgets(input, BUFFER_SIZE, stdin);
            write(pipefd[1], input, strlen(input) + 1);
            if (strcmp(input, "exit\n") == 0) break;
        }

        close(pipefd[1]);
        wait(NULL);
    }

    return 0;
}