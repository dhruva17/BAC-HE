#ifndef COMPMATRIX_MATRIXFULL_H
#define COMPMATRIX_MATRIXFULL_H
#include "bgv.h"
#include<iostream>
#include<NTL/ZZ.h>
#include <NTL/matrix.h>
#include <NTL/mat_ZZ.h>
#include <ctime>

using namespace std;
using namespace NTL;

class Matrixfull {
public:
    Matrixfull(int rows);
    void matrixGenHrt();
    void matrixGenD();
    void matrixMulhrt();  // Hrt = H * rt
    void matrixMulhrtD(); // V = Hrt * D
    void matrixGenY();    // U^d
    void matrixDec(Mat<Ciphertext> M);    // decrypt Y
    void vectorDec(Vec<Ciphertext> V);
    Mat<Ciphertext> matrixEncrypt(Mat<int> m);
    Vec<Ciphertext> vectorEncrypt(Vec<int> v);
    void MyMakeMatrix(Mat<int>& x, const vector< vector<int> > a);
    int EuclideanDistance(Vec<Ciphertext> v,Vec<Ciphertext> w);
    Vec<Ciphertext> vectorSub(Vec<Ciphertext> v,Vec<Ciphertext> w);
    void saveCiphertext(Vec<Ciphertext> encrypted, string filename);
    Vec<Ciphertext> unsafe_loadCiphertext(string filename, const seal::SEALContext &context);

private:
    Bgv bgv;
    Mat<Ciphertext> H, rt, Hrt, D, V;
    Mat<Plaintext>  Dprime;
    Vec<Ciphertext> Y;
    Vec<Plaintext> C;
};


#endif //COMPMATRIX_MATRIXFULL_H
