#ifndef __KECCAK_HH
#define __KECCAK_HH

#include <stdint.h>

/* Constants */
struct param_t {
    uint32_t n;
    uint32_t N;
    uint32_t r;
    uint32_t R;
    uint32_t C;
    uint32_t B;     // bitrate = R + C
    uint32_t W;     // width   = B / 25
    uint32_t L;     // log2(W)
    uint32_t Nr;    // number of rounds
};

/* Rounding Constants */
const uint64_t RC[] = {
    0x0000000000000001L, 0x0000000000008082L, 0x800000000000808AL,
    0x8000000080008000L, 0x000000000000808BL, 0x0000000080000001L,
    0x8000000080008081L, 0x8000000000008009L, 0x000000000000008AL,
    0x0000000000000088L, 0x0000000080008009L, 0x000000008000000AL,
    0x000000008000808BL, 0x800000000000008BL, 0x8000000000008089L,
    0x8000000000008003L, 0x8000000000008002L, 0x8000000000000080L,
    0x000000000000800AL, 0x800000008000000AL, 0x8000000080008081L,
    0x8000000000008080L, 0x0000000080000001L, 0x8000000080008008L,
};

/* Rotational Offset*/
const uint64_t R[][5] = {
    {0, 36, 3, 41, 18},
    {1, 44, 10, 45, 2},
    {62, 6, 43, 15, 61},
    {28, 55, 25, 21, 56},
    {27, 20, 39, 8, 14}
};

uint8_t *sponge(uint8_t*, int32_t);

uint8_t *padding(uint8_t*, int32_t*);

uint64_t **sha3round(uint64_t **, uint64_t);

uint64_t **keccak_f(uint64_t**);

#endif
