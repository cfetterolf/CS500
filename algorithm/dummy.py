"""
------------------------------
        DUMMY VARIABLES
------------------------------
"""
members = {
    0: { # ID of member (association.id)
        "first_name": "Chris",
        "last_name": "Fetterolf",
        "email": "chris@gmail",
        "leader_preferences": [10, 11], # IDs of preferred leader groups
    },
    1: {
        "first_name": "Andrea",
        "last_name": "Narciso",
        "email": "chris@gmail",
        "leader_preferences": [12], # IDs of preferred leader groups
    },
    2: {
        "first_name": "Joe",
        "last_name": "Antonioli",
        "email": "chris@gmail",
        "leader_preferences": [10], # IDs of preferred leader groups
    },
}

leader_groups = {
    10: {
        "leaders": [1] # Andrea
    },
    11: {
        "leaders": [2] # Joe
    },
    12: {
        "leaders": [3, 4] # Two other people
    }
}

time_blocks = {
    7: { # ID for the time block
        "day": "Monday",
        "start": 14,
        "end": 18,
        "members_available": [0, 1, 2], # IDs of members available
        "leaders_available": [11, 12],    # IDs of leaders available
    },
    8: {
        "day": "Sunday",
        "start": 12,
        "end": 14,
        "members_available": [0, 2],
        "leaders_available": [12],
    },
    9: {
        "day": "Thursday",
        "start": 10,
        "end": 12,
        "members_available": [1],
        "leaders_available": [10, 12],
    }
}

"""
----------------------------------
    DATA STRUCTURES TO FILL IN
----------------------------------
"""

hungarian_input_dict = {}


"""
Converts a member object and leader object to a square matrix that can
be used in a Hungarian algorithm
"""
def convertToSquareMatrix(members, time_blocks):
    # Create our TB id map
    tb_map = makeIdMap(time_blocks)

    # Create out leader group id map
    lg_map = makeIdMap(leader_groups)

    # Create our counting matrix to fill in: [tb][lg]
    ct_martix = [[0 for x in range(len(tb_map))] for y in range(len(lg_map))]

    # Create our member id matrix (duplicate of counting) to keep track of members we add
    mem_id_matrix = [[[] for x in range(len(tb_map))] for y in range(len(lg_map))]

    for tb_id in tb_map:
        tb_obj = time_blocks[tb_id]
        for mem_id in tb_obj["members_available"]:
            mem_obj = members[mem_id]
            for leader_id in mem_obj["leader_preferences"]:
                if leader_id in tb_obj["leaders_available"]:
                    #print("time_id: "+str(tb_id)+"\nmem_id: "+str(mem_id)+"\nleader_id: "+str(leader_id)+"\n")
                    tb_index = tb_map.index(tb_id)
                    lg_index = lg_map.index(leader_id)

                    # Increment count matrix by 1
                    ct_martix[tb_index][lg_index]+=1

                    # Append member ID to member id matrix at same index
                    mem_id_matrix[tb_index][lg_index].append(mem_id)

    # print("tb_map:")
    # print(tb_map)
    # print("lg_map:")
    # print(lg_map)
    # print("Count Matrix:")
    # print(ct_martix)
    # print("ID Matrix:")
    # print(mem_id_matrix)

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

#######################################################

def main():
    hungarian_input_dict = convertToSquareMatrix(members, time_blocks)
    matrix = hungarian_input_dict["ct_martix"]
    #from here, run hungarian algorithm with matrix (possible negate)
    

main()
