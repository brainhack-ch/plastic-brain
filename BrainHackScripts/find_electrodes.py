import csv
import numpy as np

def read_xyz(filename):
    with open(filename) as f:
        line = f.readline()
        number_of_electrodes, inconnue = line.split()
        number_of_electrodes = int(number_of_electrodes)
        inconnue = float(inconnue)
        reader = csv.reader(f, delimiter="\t")
        d = list(reader)
        names = [elem[-1].strip().lower() for elem in d]
    return(names)

def find_indice(ch_names,filename):
    names = read_xyz(filename)
    indc = []
    for ch in ch_names:
        for i,name in enumerate(names):
            if ch == name:
                indc.append(i)
    return(indc)

def convert_matrix_to_scalar(m):
    m_scalar = np.linalg.norm(m,axis=0)
    return(m_scalar)

def pick_elec_in_solution(inverse_solution, indc):
    m = inverse_solution[:,:,indc]
    return(m)

if __name__ == '__main__':
    filename ="../Inverse Solution/waveguard_128_AntNeuro.xyz"
    ch_names = ['P3', 'C3', 'F3', 'Fz', 'F4', 'C4', 'P4', 'Cz', 'Pz', 'Fp1', 'Fp2', 'T7', 'P7', 'O1', 'O2', 'F7', 'F8', 'P8', 'T8']
    ch_names = [ch.lower() for ch in ch_names]
    indc = find_indice(ch_names,filename)
    print(len(indc))
    inverse_solution = np.load("../Inverse Solution/solution inverses/solution_0.npy")
    m = pick_elec_in_solution(inverse_solution, indc)
    m_scalar = convert_matrix_to_scalar(m)
    print(m_scalar.T.shape)
