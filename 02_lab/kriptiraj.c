#include <stdlib.h>
#include <string.h>

#include "kriptiraj.h"

void kriptiraj(char *arr) {
    for(; *arr; ++arr) {
        *arr += 1;
    }
    return;
}
