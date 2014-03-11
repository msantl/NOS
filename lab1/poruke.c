#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <err.h>

#include "poruke.h"

poruka_t StvoriPoruku(char *poruka, int tip) {
    poruka_t msg;

    memset(msg.data, 0, sizeof(msg.data));
    memcpy(msg.data, poruka, strlen(poruka) + 1);
    msg.type = tip;

    return msg;
}

int StvoriRedPoruka(key_t key) {
    int res;

    if ((res = msgget(key, 0600 | IPC_CREAT)) == -1) {
        errx(1, "Pogreska pri stvaranju reda poruka!");
    }
    return res;
}

int PosaljiPoruku(int id, poruka_t msg) {
    if (msgsnd(id, (struct msgbf *)&msg, strlen(msg.data) + 1, 0) == -1) {
        warnx("Nisam uspio poslati poruku!");
        return -1;
    }

    return 0;
}

int PrimiPoruku(int id, poruka_t *msg, int tip) {
    if (msgrcv(id, (struct msgbuf *)msg, sizeof(*msg) - sizeof(long), tip, 0) == -1) {
        warnx("Nisam uspio primiti poruku!");
        return -1;
    }

    return 0;
}

int PrimiPorukuBezCekanja(int id, poruka_t *msg, int tip) {
    if (msgrcv(id, (struct msgbuf *)msg, sizeof(*msg) - sizeof(long), tip, IPC_NOWAIT) == -1) {
        return -1;
    }

    return 0;
}

void ObrisiRedPoruka(int id) {
    if (msgctl(id, IPC_RMID, NULL) == -1) {
        errx(1, "Pogreska pri brisanju reda poruka!");
    }
    return;
}
