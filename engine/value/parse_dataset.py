from numpy import *

def dataset_extractor():
    sim_file = open('Similarities.txt')
    pre_file = open('Preferences.txt')

    # calcuate matrix dimensions
    preferences = []
    for line in pre_file:
        preferences.append(line)
    
    N = len(preferences)

    # reconstruct similarity matrix 
    similarity_matrix = zeros(N*N).reshape(N,N)

    for line in sim_file:
        final = []
        line = line.replace(' ','#').replace('\n', '#').replace('\t','#')
        tmp = line.split('#')
        ftmp = [tmp[0], tmp[1], tmp[3]]
        for item in ftmp:
            
            if item!='':
                final.append(item)
        try:
            x = int(final[0])
            y = int(final[1])
            val = float(final[2])
            similarity_matrix[x][y] = val
            print x,y
        except:
            pass

    for count in range(N):
        val = preferences[count]
        similarity_matrix[count][count] = val 

    return similarity_matrix

dataset_extractor()
