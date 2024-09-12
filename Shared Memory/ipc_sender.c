#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#define SHM_SIZE 1024

int main() {
    key_t key = ftok("/tmp", 'R');
    int shmid = shmget(key, SHM_SIZE, 0644 | IPC_CREAT);
    char *shm = shmat(shmid, NULL, 0);
    
    if (shm == (char *) -1) {
        perror("shmat");
        exit(1);
    }

    while (1) {
        printf("Enter message (or 'exit' to quit): ");
        fgets(shm, SHM_SIZE, stdin);
        if (strcmp(shm, "exit\n") == 0) break;
    }

    shmdt(shm);
    return 0;
}