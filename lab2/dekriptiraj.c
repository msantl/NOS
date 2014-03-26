#include <stdlib.h>
#include <string.h>

#include "dekriptiraj.h"

void dekriptiraj(char *arr) {
    for(; *arr; ++arr) {
        *arr -= 1;
    }
    return;
}
