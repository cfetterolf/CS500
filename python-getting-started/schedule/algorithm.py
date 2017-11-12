from munkres import Munkres, print_matrix
from schedule.db import get_alg_members, get_alg_leader_groups, get_alg_time_blocks


hungarian_input_dict = {}

"""
Converts a member object and leader object to a square matrix that can
be used in a Hungarian algorithm
input: member, time block and leader group dictionaries
    (key, value pairings for each)
output: dictionary containing:
            lg_map           leader group id ~ index mapping (ROW in hung alg)
            tb_map           time block id ~ index mapping (COL in hung alg)
            ct_matrix        ct_matrix[tb_i][lg_j]
                             = # of members that match with both tb_i & lg_j
                             run hungarian alg on this
            mem_id_matrix
                             mirrors ct_matrix
                             ct_matrix[tb_i][lg_j]
                             = list of members that match with both tb_i & lg_j
"""
def convertToSquareMatrix(members, time_blocks, leader_groups):

    # Create our TB (time block) id ~ index mapping
    # for running hungarian algorithm on 2D array (COL)
    # e.g. tb_map = [tb_ID1, tb_ID3, tbID2]
    tb_map = makeIdMap(time_blocks)

    # Create out leader group id ~ index mapping
    # for running hungarian algorithm on 2D array (ROW)
    # e.g. lg_map = [lg_ID2, lg_ID1, lg_ID3]
    lg_map = makeIdMap(leader_groups)

    # Create our counting matrix to fill in: [tb][lg]
    # ct_matrix[tb_i][lg_j] = # of members that match with both tb_i & lg_j
    ct_martix = [[0 for x in range(len(tb_map))] for y in range(len(lg_map))]

    # Create our member id matrix (duplicate of counting) to keep track of members we add
    mem_id_matrix = [[[] for x in range(len(tb_map))] for y in range(len(lg_map))]

    # fills the ct_matrix & mem_id_matrix
    # according to tb_map and lg_map
    for tb_id in tb_map:
        tb_obj = time_blocks[int(tb_id)]
        for mem_id in tb_obj["members_available"]:
            mem_obj = members[int(mem_id)]
            for leader_id in mem_obj["leader_preferences"]:
                if leader_id in tb_obj["leaders_available"]:
                    #print("time_id: "+str(tb_id)+"\nmem_id: "+str(mem_id)+"\nleader_id: "+str(leader_id)+"\n")
                    tb_index = tb_map.index(tb_id)
                    lg_index = lg_map.index(leader_id)

                    # Increment count matrix by 1
                    ct_martix[tb_index][lg_index]+=1

                    # Append member ID to member id matrix at same index
                    mem_id_matrix[tb_index][lg_index].append(mem_id)

    return {"mem_id_matrix": mem_id_matrix,
            "ct_martix": ct_martix,
            "tb_map": tb_map,
            "lg_map": lg_map
            }

def makeIdMap(id_dict):
    id_map = [0]*len(id_dict)
    i = 0
    for key in id_dict:
        id_map[i] = key
        i+=1
    return id_map

def invert(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = matrix[i][j] * -1



#######################################################
"""
    Runs the algorithm.  Returns a dict with two key/values:
        indexes: list of index tuples, telling which [tb][lg] slot was selected
        tb_map: list of tb ids for reference by indexes
        lg_map: list of lg ids for reference by indexes
        member_matrix: matrix of member lists, corresponding to selected indexes
"""
def run():
    hungarian_input_dict = convertToSquareMatrix(get_alg_members(), get_alg_time_blocks(), get_alg_leader_groups())
    count_matrix = hungarian_input_dict["ct_martix"]
    m = Munkres()
    invert(count_matrix)
    #return hungarian_input_dict
    indexes = m.compute(count_matrix)
    ret_dict = {
        'indexes': indexes,
        'member_matrix': hungarian_input_dict["mem_id_matrix"],
        'tb_map': hungarian_input_dict["tb_map"],
        'lg_map': hungarian_input_dict["lg_map"]
    }
    return ret_dict
