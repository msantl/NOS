#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>

#include "keccak.hh"

using namespace std;

void print_usage(void) {
    puts("+----------------------------------------+");
    puts("| Advanced Operating Systems:            |");
    puts("|   3. Laboratory Assignment - SHA3      |");
    puts("+----------------------------------------+");
    puts("| Usage:                                 |");
    puts("|  ./sha3sum <input string>              |");
    puts("+----------------------------------------+");

    exit(1);
}

struct param_t PARAMS;

int main(int argc, char** argv) {
    if (argc != 2) {
        print_usage();
    } else {
        PARAMS.N = 256;
        PARAMS.n = PARAMS.N >> 3;
        PARAMS.R = 1088;
        PARAMS.r = PARAMS.R >> 3;
        PARAMS.C = 1600 - PARAMS.R;
        PARAMS.B = PARAMS.C + PARAMS.R;
        PARAMS.W = PARAMS.B / 25;
        PARAMS.L = (uint32_t) log2(PARAMS.W);
        PARAMS.Nr = 12 + 2 * PARAMS.L;

        fprintf(stderr,
                "N = %d\nR = %d\nC = %d\nB = %d\nW = %d\nL = %d\nNr = %d\n",
                PARAMS.N, PARAMS.R, PARAMS.C, PARAMS.B,
                PARAMS.W, PARAMS.L, PARAMS.Nr);
    }

    int32_t size = strlen(argv[1]);

    uint8_t *sha3sum = sponge((uint8_t *)argv[1], size);

    for (uint32_t i = 0; i < PARAMS.n; ++i) {
        printf("%.2x", sha3sum[i]);
    }   printf("\n");

    free(sha3sum);

    return 0;
}
