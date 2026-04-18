#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <cmath>
#include <string>

using namespace std;

typedef vector<vector<long long>> Matrix;

long long instruction_count = 0;
const int THRESHOLD = 32; // umbral híbrido

Matrix add(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, vector<long long>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            instruction_count++;
            C[i][j] = A[i][j] + B[i][j];
        }
    return C;
}

Matrix sub(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, vector<long long>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            instruction_count++;
            C[i][j] = A[i][j] - B[i][j];
        }
    return C;
}

// Fuerza bruta para caso base
Matrix bruteForce(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, vector<long long>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            for (int k = 0; k < n; k++) {
                instruction_count++;
                C[i][j] += A[i][k] * B[k][j];
            }
    return C;
}

Matrix strassen(const Matrix& A, const Matrix& B) {
    int n = A.size();
    instruction_count++;

    // Caso base hibrido
    if (n <= THRESHOLD) {
        instruction_count++;
        return bruteForce(A, B);
    }

    int half = n / 2;

    Matrix A11(half, vector<long long>(half));
    Matrix A12(half, vector<long long>(half));
    Matrix A21(half, vector<long long>(half));
    Matrix A22(half, vector<long long>(half));
    Matrix B11(half, vector<long long>(half));
    Matrix B12(half, vector<long long>(half));
    Matrix B21(half, vector<long long>(half));
    Matrix B22(half, vector<long long>(half));

    for (int i = 0; i < half; i++)
        for (int j = 0; j < half; j++) {
            instruction_count += 4;
            A11[i][j] = A[i][j];
            A12[i][j] = A[i][j + half];
            A21[i][j] = A[i + half][j];
            A22[i][j] = A[i + half][j + half];
            B11[i][j] = B[i][j];
            B12[i][j] = B[i][j + half];
            B21[i][j] = B[i + half][j];
            B22[i][j] = B[i + half][j + half];
            instruction_count += 4;
        }

    Matrix M1 = strassen(add(A11, A22), add(B11, B22));
    Matrix M2 = strassen(add(A21, A22), B11);
    Matrix M3 = strassen(A11, sub(B12, B22));
    Matrix M4 = strassen(A22, sub(B21, B11));
    Matrix M5 = strassen(add(A11, A12), B22);
    Matrix M6 = strassen(sub(A21, A11), add(B11, B12));
    Matrix M7 = strassen(sub(A12, A22), add(B21, B22));

    Matrix C11 = add(sub(add(M1, M4), M5), M7);
    Matrix C12 = add(M3, M5);
    Matrix C21 = add(M2, M4);
    Matrix C22 = add(sub(add(M1, M3), M2), M6);

    Matrix C(n, vector<long long>(n, 0));
    for (int i = 0; i < half; i++)
        for (int j = 0; j < half; j++) {
            instruction_count += 4;
            C[i][j]               = C11[i][j];
            C[i][j + half]        = C12[i][j];
            C[i + half][j]        = C21[i][j];
            C[i + half][j + half] = C22[i][j];
        }

    return C;
}

Matrix pad(const Matrix& A, int newSize) {
    Matrix P(newSize, vector<long long>(newSize, 0));
    for (int i = 0; i < (int)A.size(); i++)
        for (int j = 0; j < (int)A[0].size(); j++)
            P[i][j] = A[i][j];
    return P;
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cerr << "Uso: " << argv[0] << " <entrada.txt> <salida.txt>" << endl;
        return 1;
    }

    ifstream fin(argv[1]);
    if (!fin) {
        cerr << "No se pudo abrir: " << argv[1] << endl;
        return 1;
    }

    int n;
    fin >> n;

    Matrix A(n, vector<long long>(n));
    Matrix B(n, vector<long long>(n));

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            fin >> A[i][j];

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            fin >> B[i][j];

    fin.close();

    int newSize = 1;
    while (newSize < n) newSize *= 2;

    Matrix Apad = pad(A, newSize);
    Matrix Bpad = pad(B, newSize);

    auto start = chrono::high_resolution_clock::now();
    Matrix Cpad = strassen(Apad, Bpad);
    auto end = chrono::high_resolution_clock::now();

    double elapsed = chrono::duration<double>(end - start).count();

    Matrix C(n, vector<long long>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            C[i][j] = Cpad[i][j];

    ofstream fout(argv[2]);
    fout << "tiempo: " << elapsed << " segundos" << endl;
    fout << "instrucciones: " << instruction_count << endl;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            fout << C[i][j];
            if (j < n - 1) fout << " ";
        }
        fout << endl;
    }
    fout.close();

    cout << "Strassen hibrido listo. Tiempo: " << elapsed << "s | Instrucciones: " << instruction_count << endl;
    return 0;
}