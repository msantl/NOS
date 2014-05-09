#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <err.h>
#include <fcntl.h>

#include <sys/types.h>
#include <sys/stat.h>

#include "kriptiraj.h"
#include "dekriptiraj.h"

#define MAX_BUFF    256

#define CITANJE     0
#define PISANJE     1

#define PIPELINE_R  "cevovod_r"
#define PIPELINE_W  "cevovod_w"

#define CMD_EXIT    "?!"

int kriptiraj_fd[2], upravljac_fd[2];
int dekriptiraj_fd, deupravljac_fd;

void StvoriNeimenovaniCjevovod(int pfd[2]) {
    if (pipe(pfd) == -1) {
        errx(1, "pipe(): error while creating pipe");
    }
    return;
}

void StvoriImenovaniCjevovod(char *name) {
    if (mknod(name, S_IFIFO | 00600, 0) == -1) {
        errx(1, "mknod(): error while creating pipe");
    }
    return;
}

void K() {
    char buff[MAX_BUFF];

    while (1) {
        memset(buff, 0, sizeof buff);

        fprintf(stderr, "Proces kriptiranja\n");

        read(kriptiraj_fd[CITANJE], buff, MAX_BUFF);
        fprintf(stderr, "Primio: %s\n", buff);

        if (strcmp(buff, CMD_EXIT) == 0) break;

        kriptiraj(buff);

        write(upravljac_fd[PISANJE], buff, strlen(buff));
        fprintf(stderr, "Saljem: %s\n", buff);
    }
    return;
}

void D() {
    char buff[MAX_BUFF];

    while (1) {
        memset(buff, 0, sizeof buff);

        fprintf(stderr, "Proces dekriptiranja\n");

        read(dekriptiraj_fd, buff, MAX_BUFF);
        fprintf(stderr, "Primio: %s\n", buff);

        if (strcmp(buff, CMD_EXIT) == 0) break;

        dekriptiraj(buff);

        write(deupravljac_fd, buff, strlen(buff));
        fprintf(stderr, "Saljem: %s\n", buff);
    }
    return;
}

void U() {
    char buff[MAX_BUFF], cmd[2];

    while (1) {
        memset(buff, 0, sizeof buff);

        printf("Ucitaj poruku koja se salje: ");                        fflush(stdout);
        scanf("%s", buff);
        printf("Odaberi (K)riptiranje, (D)ekriptiranje ili (E)xit: ");  fflush(stdout);
        scanf("%s", cmd);

        if (*cmd == 'K') {
            write(kriptiraj_fd[PISANJE], buff, strlen(buff));
            read(upravljac_fd[CITANJE], buff, MAX_BUFF);

            printf("Primio: %s\n", buff);
        } else if (*cmd == 'D'){
            write(dekriptiraj_fd, buff, strlen(buff));
            read(deupravljac_fd, buff, MAX_BUFF);

            printf("Primio: %s\n", buff);
        } else if (*cmd == 'E') {
            strcpy(buff, CMD_EXIT);

            write(dekriptiraj_fd, buff, strlen(buff));
            write(kriptiraj_fd[PISANJE], buff, strlen(buff));

            break;

        } else {
            warnx("Unknown command!");
        }
    }
    return;
}

int main(int argc, char **argv) {
    /* stvori cjevovode */
    StvoriNeimenovaniCjevovod(upravljac_fd);
    StvoriNeimenovaniCjevovod(kriptiraj_fd);

    StvoriImenovaniCjevovod(PIPELINE_R);
    StvoriImenovaniCjevovod(PIPELINE_W);

    /* stvori procese */
    switch(fork()) {
        case -1:
            errx(1, "fork(): error while creating process");
            break;
        case 0:
            /* pripremi cjevovod */
            close(upravljac_fd[CITANJE]);
            close(kriptiraj_fd[PISANJE]);

            /* proces za kriptiranje */
            K();

            exit(0);
            break;
        default:
            /* pripremi cjevovod */
            close(kriptiraj_fd[CITANJE]);
            close(upravljac_fd[PISANJE]);

            /* roditelj */
            break;
    }

    switch(fork()) {
        case -1:
            errx(1, "fork(): error while creating process");
            break;
        case 0:
            /* pripremi cjevovod */
            dekriptiraj_fd = open(PIPELINE_W, O_RDONLY);
            deupravljac_fd = open(PIPELINE_R, O_WRONLY);

            /* proces za dekriptiranje */
            D();

            exit(0);
            break;
        default:
            /* pripremi cjevovod */
            dekriptiraj_fd = open(PIPELINE_W, O_WRONLY);
            deupravljac_fd = open(PIPELINE_R, O_RDONLY);

            /* roditelj */
            break;
    }

    /* upravljac */
    U();

    /* cekamo da procesi zavrse */
    wait(NULL);
    wait(NULL);

    exit(0);
}
