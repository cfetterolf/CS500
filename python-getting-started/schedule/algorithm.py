from munkres import Munkres, print_matrix
from schedule.db import get_alg_members, get_alg_leader_groups, get_alg_time_blocks
from django.conf import settings
import math


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
# def convertToSquareMatrix(members, time_blocks, leader_groups):
#
#     # Create our TB (time block) id ~ index mapping
#     # for running hungarian algorithm on 2D array (COL)
#     # e.g. tb_map = [tb_ID1, tb_ID3, tbID2]
#     tb_map = makeIdMap(time_blocks)
#
#     # Create out leader group id ~ index mapping
#     # for running hungarian algorithm on 2D array (ROW)
#     # e.g. lg_map = [lg_ID2, lg_ID1, lg_ID3]
#     lg_map = makeIdMap(leader_groups)
#
#     # Create our counting matrix to fill in: [tb][lg]
#     # ct_matrix[tb_i][lg_j] = # of members that match with both tb_i & lg_j
#     ct_martix = [[0 for x in range(len(tb_map))] for y in range(len(lg_map))]
#
#     # Create our member id matrix (duplicate of counting) to keep track of members we add
#     mem_id_matrix = [[[] for x in range(len(tb_map))] for y in range(len(lg_map))]
#
#     # fills the ct_matrix & mem_id_matrix
#     # according to tb_map and lg_map
#     for tb_id in tb_map:
#         tb_obj = time_blocks[int(tb_id)]
#         for mem_id in tb_obj["members_available"]:
#             mem_obj = members[int(mem_id)]
#             for leader_id in mem_obj["leader_preferences"]:
#                 if leader_id in tb_obj["leaders_available"]:
#                     #print("time_id: "+str(tb_id)+"\nmem_id: "+str(mem_id)+"\nleader_id: "+str(leader_id)+"\n")
#                     tb_index = tb_map.index(tb_id)
#                     lg_index = lg_map.index(leader_id)
#
#                     # Increment count matrix by 1
#                     ct_martix[tb_index][lg_index]+=1
#
#                     # Append member ID to member id matrix at same index
#                     mem_id_matrix[tb_index][lg_index].append(mem_id)
#
#     return {"mem_id_matrix": mem_id_matrix,
#             "ct_martix": ct_martix,
#             "tb_map": tb_map,
#             "lg_map": lg_map
#             }



"""
Converts a member object and leader object to a square matrix that can
be used in a Hungarian algorithm
input: member, time block and leader group dictionaries
    (key, value pairings for each)
    sched_type:
        'n_leaders'     doesn't take leader tb preference into account
        'y_leaders'     take leader tb preference into account
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
def convertToSquareMatrix(members, time_blocks, leader_groups, sched_type):

    # SET VARS
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
    # sets to -10000 to check for init variable errors
    ct_matrix = [[-10000 for x in range(len(tb_map))] for y in range(len(lg_map))]

    #
    leader_avail = [(tb,lg) for tb in time_blocks for lg in
        time_blocks[tb]["leaders_available"]]
    # print('leader avail: ' + str(leader_avail))
    for tb_index in range(len(tb_map)):
        for lg_index in range(len(lg_map)):
            # if (lg_index > 0):
            #     return {'tb_map': tb_map,
            #             "lg_map": lg_map,
            #             'leader_avail': leader_avail,
            #             'bool': ((tb_map[tb_index],lg_map[lg_index]) in leader_avail)}
            if (tb_map[tb_index],str(lg_map[lg_index])) in leader_avail:
                ct_matrix[tb_index][lg_index] = 0
            else:
                ct_matrix[tb_index][lg_index] = -1000

                # use below if want to match w/o leader pref, only mem pref
                # might be useful for alt sched (--> change leader pref)
                # ct_matrix[tb_index][lg_index] = 0

    # Create our member id matrix (duplicate of counting) to keep track of members we add
    mem_id_matrix = [[[] for x in range(len(tb_map))] for y in range(len(lg_map))]


    # FILL TABLE
    # fills the ct_matrix & mem_id_matrix
    # according to tb_map and lg_map

    # Title
    # print('tb \tm \tlg \tadd to ct_matrix?')                      # SCHARPRINT

    # iterates through the indiv tb's, gets the corresponding tb object (tb_obj)
    for tb_id in tb_map:
        tb_obj = time_blocks[int(tb_id)]        # tb_obj = corresponding tb information (start, end etc)
        # print('tb_id: ' + str(tb_id) + ', mems avail: ' +
        #     str(tb_obj["members_available"]))

        # for each tb, iterates through each member available at that tb
        # gets the corresponding member object (incl first, last name, email etc)
        for mem_id in tb_obj["members_available"]:
            mem_obj = members[int(mem_id)]

            # print('\t mem_id: ' + str(mem_id) + ', leader pref: ' +
            #     str(mem_obj["leader_preferences"]))

            # for each tb + member combo,
            # finds the leaders preferred by that member
            # if that leader is avail at that time block
            for leader_id in mem_obj["leader_preferences"]:
                # convert tb,lg id --> indices
                tb_index = tb_map.index(int(tb_id))
                lg_index = lg_map.index(int(leader_id))

                # printer help function to show work of
                # this function i.e. preprocessing step for hung alg
                # print(str(tb_id) + '\t' + str(mem_id) +         # SCHARPRINT
                #     '\t' + str(leader_id) + '\t'),

                # print('\t \t leader_id: ' + str(leader_id) + ', '),
                if str(leader_id) in tb_obj["leaders_available"]:
                    # print('! ')                                 # SCHARPRINT

                    # Increment count matrix by 1
                    ct_matrix[tb_index][lg_index]+=1
                    # Append member ID to member id matrix at same index
                    mem_id_matrix[tb_index][lg_index].append(int(mem_id))

                # if lg not avail at tb, sets to -inf
                # so hung alg will never pick tb-lg
                # else:                                             # SCHARPRINT
                    # print('')                                     # SCHARPRINT

    # print(ct_matrix)
    return {"mem_id_matrix": mem_id_matrix,
            "ct_matrix": ct_matrix,
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
    hungarian_input_dict = convertToSquareMatrix(get_alg_members(settings.GID), get_alg_time_blocks(settings.GID), get_alg_leader_groups(settings.GID), "y_leaders")
    #return {'final_dict': hungarian_input_dict}
    count_matrix = hungarian_input_dict["ct_matrix"]
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
