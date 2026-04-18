#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>

using namespace std;

typedef vector<vector<long long>> Matrix;

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

    long long instruction_count = 0;
    Matrix C(n, vector<long long>(n, 0));

    auto start = chrono::high_resolution_clock::now();

    for (int i = 0; i < n; i++) {
        instruction_count++;
        for (int j = 0; j < n; j++) {
            instruction_count++;
            C[i][j] = 0;
            instruction_count++;
            for (int k = 0; k < n; k++) {
                instruction_count++;
                C[i][j] += A[i][k] * B[k][j];
                instruction_count++;
            }
        }
    }

    auto end = chrono::high_resolution_clock::now();
    double elapsed = chrono::duration<double>(end - start).count();

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

    cout << "Fuerza Bruta lista. Tiempo: " << elapsed << "s | Instrucciones: " << instruction_count << endl;
    return 0;
}