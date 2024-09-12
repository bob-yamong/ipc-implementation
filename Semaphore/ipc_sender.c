#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <sys/types.h>

#define SHM_SIZE 1024

union semun {
    int val;
    struct semid_ds *buf;
    unsigned short *array;
};

int main() {
    key_t key = ftok("/tmp", 'R');
    int shmid = shmget(key, SHM_SIZE, 0644 | IPC_CREAT);
    char *shm = shmat(shmid, NULL, 0);

    int semid = semget(key, 1, 0644 | IPC_CREAT);

    union semun sem_arg;
    sem_arg.val = 1;
    if (semctl(semid, 0, SETVAL, sem_arg) == -1) {
        perror("semctl");
        exit(1);
    }

    struct sembuf sb = {0, -1, SEM_UNDO};

    while (1) {
        printf("Enter message (or 'exit' to quit): ");
        fgets(shm, SHM_SIZE, stdin);

        if (semop(semid, &sb, 1) == -1) {
            perror("semop");
            exit(1);
        }

        sb.sem_op = 1;
        if (semop(semid, &sb, 1) == -1) {
            perror("semop");
            exit(1);
        }

        if (strcmp(shm, "exit\n") == 0) break;
    }

    shmdt(shm);
    shmctl(shmid, IPC_RMID, NULL);
    semctl(semid, 0, IPC_RMID);

    return 0;
}