#include "keccak.hh"

#include <stdlib.h>
#include <stdio.h>

extern struct param_t PARAMS;

uint8_t *sponge(uint8_t *msg, int32_t size) {
    uint64_t *new_msg = (uint64_t *) msg;
    uint8_t padded = 0;

    if (size % PARAMS.r != 0) {
        new_msg = (uint64_t *) padding(msg, &size);
        padded = 1;
    }

    uint64_t **S = (uint64_t **) calloc(5, sizeof(uint64_t *));
    for (uint8_t i = 0; i < 5; ++i) {
        S[i] = (uint64_t *) calloc(5, sizeof(uint64_t));
    }

    for (uint32_t i = 0; i < size / PARAMS.r; ++i) {

        for (uint8_t y = 0; y < 5; ++y) {
            for (uint8_t x = 0; x < 5; ++x) {
                if (x + 5*y < PARAMS.R / PARAMS.W) {
                    S[x][y] = S[x][y] ^ new_msg[9 * i + x + 5*y];
                }
            }
        }
        S = keccak_f(S);
    }


    uint32_t b = 0;
    uint64_t *Z = (uint64_t *) calloc(PARAMS.n / 8, sizeof(uint64_t));

    while (b < PARAMS.n / 8) {
        for (uint8_t y = 0; y < 5; ++y) {
            for (uint8_t x = 0; x < 5; ++x) {
                if (x + 5*y < PARAMS.R / PARAMS.W) {
                    Z[b] ^= S[x][y];
                    b += 1;
                }
            }
        }
    }

    if (padded) {
        free(new_msg);
    }

    free(S);
    return (uint8_t *) Z;
}

uint8_t *padding(uint8_t *msg, int32_t *size) {
    int32_t new_size = *size + PARAMS.r - (*size % PARAMS.r);
    uint8_t *new_msg = (uint8_t *) malloc(new_size * sizeof(uint8_t));

    for (uint8_t i = 0; i < *size; ++i) {
        new_msg[i] = msg[i];
    }

    new_msg[(*size)++] = 0x01;

    while (*size < new_size - 1) {
        new_msg[(*size)++] = 0x00;
    }

    new_msg[(*size)++] = 0x80;

    *size = new_size;
    return new_msg;
}

uint64_t **sha3round(uint64_t **A, uint64_t rc) {
    uint64_t C[5];
    uint64_t D[5];
    uint64_t B[5][5];

    /* Theta step */
    for (uint8_t x = 0; x < 5; ++x) {
        C[x] = A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4];
    }

    for (uint8_t x = 0; x < 5; ++x) {
        D[x] = C[(x + 4) % 5] ^ ((C[(x + 1) % 5] << 1) | (C[(x + 1) % 5] >> 63));
    }

    for (uint8_t x = 0; x < 5; ++x) {
        for (uint8_t y = 0; y < 5; ++y) {
            A[x][y] = A[x][y] ^ D[x];
        }
    }

    /* Rho and Pi step */
    for (uint8_t x = 0; x < 5; ++x) {
        for (uint8_t y = 0; y < 5; ++y) {
            B[y][(2*x + 3*y) % 5] = ((A[x][y] << R[x][y]) | (A[x][y] >> (64 - R[x][y])));
        }
    }

    /* Chi step */
    for (uint8_t x = 0; x < 5; ++x) {
        for (uint8_t y = 0; y < 5; ++y) {
            A[x][y] = B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y]);
        }
    }

    A[0][0] = A[0][0] ^ rc;

    return A;
}

uint64_t **keccak_f(uint64_t **A) {
    for (int32_t i = 0; i < PARAMS.Nr; ++i) {
        A = sha3round(A, RC[i]);
    }
    return A;
}
