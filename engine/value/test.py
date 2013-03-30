from numpy import *

def dataset_extractor():
    sim_file = open('Similarities.txt')
    pre_file = open('Preferences.txt')
    fuck = open('Stmp.txt','w')

    # calcuate matrix dimensions
    preferences = []
    for line in pre_file:
        preferences.append(line)
        hi = line.replace(' ','#').replace('\n', '#')
        num = hi.replace('#','')
        fuck.write(num+'\n')
    """    
    N = len(preferences)

    # reconstruct similarity matrix 
    similarity_matrix = zeros(N*N).reshape(N,N)

    for line in sim_file:
        final = []
        line = line.replace(' ','#').replace('\n', '#')
        for item in line.split('#'):
            if item!='':
                final.append(item)
        x = int(final[0])-1
        y = int(final[1])-1
        val = float(final[2])
        similarity_matrix[x][y] = val

    for count in range(N):
        val = preferences[count]
        similarity_matrix[count][count] = val 

    return similarity_matrix
    """
dataset_extractor()
