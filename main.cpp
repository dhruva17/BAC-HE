#include <iostream>
#include <cmath>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <cassert>
#include <random>
#include <cstdio>
#include "BGV/bgv.h"
#include "BGV/matrixfull.h"
#include "pyhelper.hpp"

using namespace std;
using namespace NTL;
/*Bgv::Bgv() {
EncryptionParameters parms(scheme_type::bgv);
    size_t poly_modulus_degree = 8192;
    parms.set_poly_modulus_degree(poly_modulus_degree);

    parms.set_coeff_modulus(CoeffModulus::BFVDefault(poly_modulus_degree));
    parms.set_plain_modulus(PlainModulus::Batching(poly_modulus_degree, 20));
    SEALContext context(parms);
    }
    
Bgv bgv;*/
int main() {
    Vec<int> finger;
    Vec<Ciphertext> Vector;
    vector<int> v;
    Matrixfull matrix(v.size());
    
    cout << "Anonymous Biometric Authentication System\n";
    cout << "Select an option\n";
    cout << "1. Enroll yourself\n";
    cout << "2. Get authenticated\n";
       
    int option, euclideanDistance=0, threshold=0;
    cin >> option;

    setenv("PYTHONPATH",".",1);

    CPyInstance hInstance;
    CPyObject pValue;

	CPyObject pName = PyUnicode_FromString("finger");
	CPyObject pModule = PyImport_Import(pName);

	if(pModule)
	{
		CPyObject pFunc = PyObject_GetAttrString(pModule, "final");
		if(pFunc && PyCallable_Check(pFunc))
		{
			pValue = PyObject_CallObject(pFunc, NULL);
		}
		else
		{
			printf("ERROR: function getInteger()\n");
		}

	}
	else
	{
		printf("ERROR: Module not imported\n");
		PyErr_Print();
	
	}
    
    
    
    switch(option){
    case 1: 
    		for (int j = 0; j < 8; j++){

	    		PyObject * list = PyList_GetItem(pValue, j);
	    		for (int i = 0; i<80; i++){
	    			v.push_back(PyLong_AsLong(PyList_GetItem(list, i)));
	    			}
	    		
	    		finger.SetLength(v.size());       
	    		for(int i=0; i<v.size(); i++)
		   		finger.put(i, v[i]);
	    		
	    		Vector.SetLength(v.size());
	    		Vector = matrix.vectorEncrypt(finger);
	    		matrix.saveCiphertext(Vector, "store.txt");
	    		
	    		//store in DB
	    		
    		}	
    		break;
    
    case 2:
    		for (int j = 0; j < 8; j++){
    		
	    		PyObject * list = PyList_GetItem(pValue, j);
	    		for (int i = 0; i<80; i++){
	    			v.push_back(PyLong_AsLong(PyList_GetItem(list, i))); 
	    			}
	    		finger.SetLength(v.size());       
	    		for(int i=0; i<v.size(); i++)
		 		finger.put(i, v[i]);
	    	
    			Vector.SetLength(v.size());
    			Vector = matrix.vectorEncrypt(finger);
    			//check against DB
    			//Vec<Ciphertext> stored = matrix.unsafe_loadCiphertext("store.txt", context);
    			//euclideanDistance = matrix.EuclideanDistance(Vector,stored);
    			cout << "Euclidean distance ";
    			cout << euclideanDistance << endl;
    			if(euclideanDistance < threshold) {
    				cout << "Access granted\n";
    				return 0;
    			}
    		}
    		cout << "Access denied\n";
    		break;
    
    default: cout << "please select a valid option";
    	     return(0);
    }
    return 0;
}



