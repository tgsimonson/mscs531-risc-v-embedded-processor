#include <stdio.h>
#include <stdlib.h>

#define ITERATIONS 1000
#define KP 2
#define KI 1
#define KD 1

int sensor_read(int i) {
    return (i % 100) - 50;
}

int main() {
    int setpoint = 0;
    int integral = 0;
    int prev_error = 0;
    int actuator = 0;
    int i;

    for (i = 0; i < ITERATIONS; i++) {
        int measured = sensor_read(i);
        int error = setpoint - measured;
        integral += error;
        int derivative = error - prev_error;
        actuator = (KP * error) + (KI * integral) + (KD * derivative);
        prev_error = error;
    }

    printf("Control loop complete. Final actuator output: %d\n", actuator);
    return 0;
}