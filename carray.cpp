#include <iostream>
#include <string>

double *newarray(int n)
{
    return new double[n];
}

void delarray(double *array)
{
    delete array;
}

void setelement(double *array, int n, double p)
{
    array[n] = p;
}

double getelement(double *array, int n)
{
    return array[n];
}

std::string string(std::string x)
{
    //std::cout << x << std::endl;
    return x;
}
