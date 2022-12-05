#include "matrixfull.h"

class MyVec : public  Vec<int>
{
public:
        MyVec(std::initializer_list<int> input);
};

MyVec::MyVec(std::initializer_list<int> input)
{
        int n = input.size();
        this->SetLength(n);
        std::vector<int> v;
        v.insert(v.end(), input.begin(), input.end());

        for(int i=0; i<n; i++)
                this->put(i, v[i]);
}

Matrixfull::Matrixfull(int n) {
    Bgv bgv1;
    bgv = bgv1;
}

/*void Matrixfull::MyMakeMatrix(Mat<int>& x, const vector< vector<int> > a)  
{  
   long n = a.size();  
  
   if (n == 0) {  
      x.SetDims(0, 0);  
      return;  
   }  
  
   long m = a[0].size();  
   long i;  
  
   for (i = 1; i < n; i++)  
      if (a[i].size() != m)  
         LogicError("nonrectangular matrix");  
  
   x.SetDims(n, m);  
   vector<int> z;
   for (i = 0; i < n; i++) {
      MyVec v = {1,2,3,4}; //How to make this dynamic??
      for(int j = 0; j< m; j++){ v[j] = a[i][j]; }
      x[i] = v;  
      //cout << v;
      }
}  */

void Matrixfull::saveCiphertext(Vec<Ciphertext> encrypted, string filename){
for(int i=0; i<80; i++){
  ofstream ct;
  ct.open(filename, ios::binary);
  (encrypted.get(i)).save(ct);
  }
};

Vec<Ciphertext> Matrixfull::unsafe_loadCiphertext(string filename, const seal::SEALContext &context){
Vec<Ciphertext> fromFile;
for(int i=0; i<80; i++){
  ifstream ct;
  ct.open(filename, ios::binary);
  Ciphertext result;
  result.unsafe_load(context, ct);
  fromFile.put(i,result);
}
  return fromFile;
};


Mat<Ciphertext> Matrixfull::matrixEncrypt(Mat<int> m) {
    Mat<Ciphertext> matrix;
    long rows = m.NumRows();
    long cols = m.NumCols();
    matrix.SetDims(rows, cols);
    for(int i = 0; i < rows; i++){
        for(int j = 0; j < cols; j++){
            Plaintext plaintext(uint64_to_hex_string(m[i][j]));
            Ciphertext envalue = bgv.encrypt(plaintext);
            matrix.put(i, j, envalue);
        }
    }
    return matrix;
}

Vec<Ciphertext> Matrixfull::vectorEncrypt(Vec<int> v){
	Vec<Ciphertext> vec;
	long len = v.length();
	vec.SetLength(len);
	for (int i = 0; i<len; i++){
	    Plaintext plaintext(uint64_to_hex_string(v[i]));
            Ciphertext envalue = bgv.encrypt(plaintext);
            vec.put(i, envalue);
	}
	return vec;
}


void Matrixfull::matrixDec(Mat<Ciphertext> M) {
    for(int i = 0; i < M.NumRows(); i++){
    	for(int j =0; j < M.NumCols();j++){
        Plaintext p = bgv.decrypt(M[i][j]);
        cout << p.to_string()<< endl;
    }
    }
}


Vec<Ciphertext> Matrixfull::vectorSub(Vec<Ciphertext> v,Vec<Ciphertext> w) {
    Vec<Ciphertext> Res;
    Res.SetLength(v.length());
    for(int i = 0; i < v.length(); i++) {
            Ciphertext res = bgv.subtract(v.get(i), w.get(i));
            Res.put(i, res);
    }
    return Res;
}

void Matrixfull::vectorDec(Vec<Ciphertext> V) {
    for(int i = 0; i < V.length(); i++){
        Plaintext p = bgv.decrypt(V.get(i));
        cout << p.to_string();
        cout << " ";
    }
}

int Matrixfull::EuclideanDistance(Vec<Ciphertext> v,Vec<Ciphertext> w){
	Vec<Ciphertext>Res = vectorSub(v,w);
	Plaintext p(uint64_to_hex_string(0));
	Ciphertext distance = bgv.encrypt(p);
	Ciphertext temp;
	for(int i = 0; i < Res.length(); i++) {
		temp = bgv.mult(Res.get(i), Res.get(i));
		distance = bgv.add(distance, temp);
	}
	Plaintext euc_distance = bgv.decrypt(distance);
	return stoi(euc_distance.to_string(),0, 16); 
}

