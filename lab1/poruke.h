#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>

#define MSGLEN 32

/*
 * Podatkovna struktura poruke
 */
typedef struct poruka_t_ {
    long type;
    char data[MSGLEN];
} poruka_t;

/*
 * StvoriPoruku
 *
 * Dobiveni sadrzaj poruke sprema u strukturu poruke.
 */
poruka_t StvoriPoruku(char *poruka, int tip);

/*
 * StvoriRedPoruka
 *
 * Stvara novi red poruka ili vraca identifikator ako vec postoji.
 * U slucaju pojave pogreske program izlazi s kodom 1.
 */
int StvoriRedPoruka(key_t key);

/*
 * PosaljiPoruku
 *
 * Salje poruku u red ciji nam je ID poznat.
 * U slucaju pojave pogreske ispsuje se taj nemili dogadaj i program nastavlja
 * s radom.
 *
 * Pretpostavljena vrijednost zastavice je 0;
 */
int PosaljiPoruku(int id, poruka_t msg);

/*
 * PrimiPoruku
 *
 * Prima poruku iz reda ciji nam je ID poznat.
 * U slucaju pojave pogreske ispisuje se taj nemili dogadaj i program nastavlja
 * s radom.
 *
 * Pretpostavljena vrijednost zastavice je 0;
 */
int PrimiPoruku(int id, poruka_t *msg, int tip);

/*
 * PrimiPorukuBezCekanja
 *
 * Prima poruku iz reda ciji nam je ID poznat.
 * U slucaju pojave pogreske ispisuje se taj nemili dogadaj i program nastavlja
 * s radom.
 *
 * Pretpostavljena vrijednost zastavice je 0;
 */
int PrimiPorukuBezCekanja(int id, poruka_t *msg, int tip);

/*
 * ObrisiRedPoruka
 *
 * Brise red poruka.
 */
void ObrisiRedPoruka(int id);
