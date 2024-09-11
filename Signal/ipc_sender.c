#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>

typedef int pid_t;

#define SIGUSR1 10
#define SIGUSR2 12

void send_char(pid_t pid, char c) {
    for (int i = 7; i >= 0; i--) {
        int bit = (c >> i) & 1;
        if (kill(pid, bit ? SIGUSR2 : SIGUSR1) == -1) {
            perror("kill");
            exit(1);
        }
        usleep(1000);  // Small delay to avoid signal overlap
    }
}

void send_string(pid_t pid, const char* message) {
    for (int i = 0; message[i] != '\0'; i++) {
        send_char(pid, message[i]);
    }
    send_char(pid, '\n');  // Send newline to indicate end of message
}

int main() {
    pid_t pid;
    char message[256];

    printf("Enter the PID of the Python receiver process: ");
    scanf("%d", &pid);
    getchar();  // Consume newline

    while (1) {
        printf("Enter message to send (or 'exit' to quit): ");
        fgets(message, sizeof(message), stdin);
        message[strcspn(message, "\n")] = 0;  // Remove newline

        send_string(pid, message);

        if (strcmp(message, "exit") == 0) {
            break;
        }
    }

    return 0;
}