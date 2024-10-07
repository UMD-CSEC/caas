#include <stdio.h>
#include <string.h>

int main(void) {
    FILE *flag = fopen("./flag.txt", "r");

    char buf[100];
    fgets(buf, sizeof(buf), flag);
    buf[strcspn(buf, "\n")] = 0;

    printf("%s\n", buf);
    return 0;
}
