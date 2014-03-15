#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>

#include "poruke.h"

#define GRID        4
#define MAXGRID     32
#define QUEUE_KEY   12345

#define SYN         1
#define ACK         2
#define SYN_ACK     3
#define FIN         4
#define RES         5
#define REQ         6

#define BROD        'x'
#define MORE        '.'

/*
 * Opis stanja:
 * stanje = 5 -> pobjedio sam
 * stanje = 4 -> izgubio sam
 * stanje = 2 -> ja nisam na redu
 * stanje = 1 -> ja   sam na redu
 * stanje = 0 -> igra je gotova
 */
int state = 0;

/*
 * Opis polozaja brodova
 */
char grid[MAXGRID][MAXGRID];

/*
 * Globalni identifikator reda poruka
 */
int q;

void kraj(int sig) {
    state = 0;

    /* obrisi red nakon koristenja */
    ObrisiRedPoruka(q);

    exit(sig);
}

void print_usage() {
    puts("Potapljanje brodova - Prva laboratorijska vjezba @NOS");
    puts("-----------------------------------------------------");
    printf("Velicina igraceg polja %dx%d\n", GRID, GRID);
    printf("Oznaka broda: %c\n", BROD);
    printf("Oznaka mora:  %c\n", MORE);
    puts("-----------------------------------------------------");
}

int main(int argc, char **argv) {
    int i, j, preostalo_brodova = 0;
    key_t key = QUEUE_KEY;

    char buf[MSGLEN];
    poruka_t msg;

    sigset(SIGINT, kraj);

    print_usage();

    printf("Unesite polozaj brodova:\n");

    for (i = 0; i < GRID; ++i) {
        scanf("%s", grid + i);
        for (j = 0; j < GRID; ++j) {
            if (grid[i][j] == BROD) {
                preostalo_brodova += 1;
            }
        }
    }

    printf("Cekam drugog igraca ...\n");

    q = StvoriRedPoruka(key);

    /* Odredimo tko je prvi proces */
    if (PrimiPorukuBezCekanja(q, &msg, SYN) == -1) {
        /* proces 1 */
        msg = StvoriPoruku("init", SYN);
        PosaljiPoruku(q, msg);

        PrimiPoruku(q, &msg, SYN_ACK);

        msg = StvoriPoruku("ack", ACK);
        PosaljiPoruku(q, msg);

        state = 1;

    } else {
        /* proces 2 */
        msg = StvoriPoruku("syn-ack", SYN_ACK);
        PosaljiPoruku(q, msg);

        PrimiPoruku(q, &msg, ACK);

        state = 2;
    }

    printf("Proces %d\n", state);
    printf("Igra pocinje\n");

    while (state != 0) {

        if (state == 1) {
            state = 2;

            printf("Ispali na polje: "); fflush(stdout);
            scanf("%d%d", &i, &j);

            /* posalji koordinate */
            memset(buf, 0, sizeof buf);
            sprintf(buf, "%d-%d", i, j);

            msg = StvoriPoruku(buf, REQ);
            PosaljiPoruku(q, msg);

            /* cekaj odgovor */
            PrimiPoruku(q, &msg, RES);

            printf("%s\n", msg.data);

            if (strncmp(msg.data, "pobjeda", 7) == 0) {
                state = 5;
            }

        } else if (state == 2) {
            state = 1;

            /* primi koordinate */
            PrimiPoruku(q, &msg, REQ);

            sscanf(msg.data, "%d-%d", &i, &j);  --i; --j;

            /* posalji odgovor */
            if (0 <= i && i < GRID && 0 <= j && j < GRID && grid[i][j] == BROD) {
                preostalo_brodova -= 1;
                grid[i][j] = MORE;

                if (preostalo_brodova > 0) {
                    msg = StvoriPoruku("pogodak", RES);
                } else {
                    msg = StvoriPoruku("pobjeda", RES);
                    printf("poraz\n");

                    state = 4;
                }
            } else {
                msg = StvoriPoruku("promasaj", RES);
            }
            PosaljiPoruku(q, msg);

        } else if (state == 4) {
            /* cekaj pritisak bilo koje tipke */
            printf("Pritisnite bilo koju tipku za izlaz..."); fflush(stdout);
            scanf("%s", buf);

            /* posalji poruku o kraju */
            msg = StvoriPoruku("fin", FIN);
            PosaljiPoruku(q, msg);

            state = 0;

        } else if (state == 5) {
            /* cekaj poruku kraja igre */
            PrimiPoruku(q, &msg, FIN);

            /* zavrsi igru */
            kraj(0);

            state = 0;

        } else {
            /*
             * Ovdje se u pravilu ne bi trebali nikad naci, ali u slucaju da se
             * nadjemo samo izadji iz petlje
             */
            state = 0;
        }
    }

    return 0;
}
