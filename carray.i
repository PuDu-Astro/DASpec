%module carray
%{
double *newarray(int n);
void delarray(double *array);
void setelement(double *array, int n, double p);
double getelement(double *array, int n);
%}

double *newarray(int n);
void delarray(double *array);
void setelement(double *array, int n, double p);
double getelement(double *array, int n);
