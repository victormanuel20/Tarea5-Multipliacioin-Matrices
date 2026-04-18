import numpy as np
import subprocess
import os
import pandas as pd
import re

SIZES        = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
REPS         = 3
VAL_MIN      = -10
VAL_MAX      = 10
STRASSEN_BIN = "./strassen"
BRUTE_BIN    = "./brute_force"
INPUT_DIR    = "instances"
OUTPUT_DIR   = "outputs"

os.makedirs(INPUT_DIR,  exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_instance(n, rep):
    A = np.random.randint(VAL_MIN, VAL_MAX + 1, size=(n, n))
    B = np.random.randint(VAL_MIN, VAL_MAX + 1, size=(n, n))
    fname = os.path.join(INPUT_DIR, f"matrix_n{n}_r{rep}.txt")
    with open(fname, "w") as f:
        f.write(f"{n}\n")
        for row in A:
            f.write(" ".join(map(str, row)) + "\n")
        for row in B:
            f.write(" ".join(map(str, row)) + "\n")
    return fname

def parse_output(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    tiempo        = float(re.search(r"tiempo:\s*([\d.e+\-]+)", lines[0]).group(1))
    instrucciones = int(re.search(r"instrucciones:\s*(\d+)",   lines[1]).group(1))
    return tiempo, instrucciones

def run_program(binary, input_file, output_file):
    result = subprocess.run([binary, input_file, output_file], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        return None, None
    return parse_output(output_file)

records = []

for n in SIZES:
    for rep in range(1, REPS + 1):
        print(f"  n={n:4d}  rep={rep}/{REPS}", end=" ... ", flush=True)
        input_file   = generate_instance(n, rep)
        out_strassen = os.path.join(OUTPUT_DIR, f"out_strassen_n{n}_r{rep}.txt")
        out_brute    = os.path.join(OUTPUT_DIR, f"out_brute_n{n}_r{rep}.txt")
        t_str, i_str = run_program(STRASSEN_BIN, input_file, out_strassen)
        t_bru, i_bru = run_program(BRUTE_BIN,    input_file, out_brute)
        records.append({
            "n":                       n,
            "rep":                     rep,
            "tiempo_strassen":         t_str,
            "instrucciones_strassen":  i_str,
            "tiempo_bruta":            t_bru,
            "instrucciones_bruta":     i_bru,
        })
        print(f"Strassen: {t_str:.6f}s/{i_str} instr | Bruta: {t_bru:.6f}s/{i_bru} instr")

df = pd.DataFrame(records)
summary = (
    df.groupby("n")
      .agg(
          tiempo_strassen_avg        = ("tiempo_strassen",       "mean"),
          instrucciones_strassen_avg = ("instrucciones_strassen", "mean"),
          tiempo_bruta_avg           = ("tiempo_bruta",          "mean"),
          instrucciones_bruta_avg    = ("instrucciones_bruta",   "mean"),
      )
      .reset_index()
)

df.to_csv("resultados.csv", index=False)
summary.to_csv("resumen.csv", index=False)

print("\n=== Resumen por tamaño ===")
print(summary.to_string(index=False))
print("\nArchivos generados: resultados.csv y resumen.csv")