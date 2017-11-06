from munkres import Munkres, print_matrix

"""
----------------------------------------------
        DUMMY VARIABLES - TRIAL 1
----------------------------------------------
"""
members_t1 = {
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

leader_groups_t1 = {
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

time_blocks_t1 = {
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
----------------------------------------------
        DUMMY VARIABLES - TRIAL 2
----------------------------------------------
"""
members_t2 = {
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
    3: {
        "first_name": "Bob",
        "last_name": "Bobby",
        "email": "chris@gmail",
        "leader_preferences": [10], # IDs of preferred leader groups
    },
    4: {
        "first_name": "Jane",
        "last_name": "Ratched",
        "email": "chris@gmail",
        "leader_preferences": [11], # IDs of preferred leader groups
    },
}

leader_groups_t2 = {
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

time_blocks_t2 = {
    7: { # ID for the time block
        "day": "Monday",
        "start": 14,
        "end": 18,
        "members_available": [0, 1, 2, 3, 4], # IDs of members available
        "leaders_available": [10, 11, 12],    # IDs of leaders available
    },
    8: {
        "day": "Sunday",
        "start": 12,
        "end": 14,
        "members_available": [0, 2, 3, 4],
        "leaders_available": [12, 11],
    },
    9: {
        "day": "Thursday",
        "start": 10,
        "end": 12,
        "members_available": [1, 2, 4],
        "leaders_available": [10],
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

def invert(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = matrix[i][j] * -1

"""
Helper Function: PRINT
    prints the input of the "convertToSquareMatrix" function
    i.e. members, time_blocks, leader_groups
"""
def printConvertSqMtrxInput(members, time_blocks, leader_groups):

    # # MEMBER
    # # Title
    # print '{:10}'.format('mem id'),
    # print '{:10}'.format('f name'),
    # print '{:15}'.format('tb pref'),
    # print '{:16}'.format('lg pref: [user id]'),
    # print
    # # Set Vars: Check Hung Alg Output is in Pref
    # tb_pref_check = []
    # lg_pref_check = []
    #
    # # Entries
    # for mem in members:
    #     print '{:10}'.format(str(mem)),
    #     # print '{:6}'.format(tb_id),
    #     print '{:10}'.format(members[mem]["first_name"]),
    #
    #     # prints tb pref
    #     for tb_id in time_blocks:
    #         if mem in time_blocks[tb_id]["members_available"]:
    #             print str(tb_id) + ',',
    #             tb_pref_check.append(tb_id)
    #     print '{:9}'.format(''),
    #
    #     # prints tb hung alg output
    #
    #
    #     # prints lg pref: [user id]
    #     same_line = False
    #     for lg_id in members[mem]["leader_preferences"]:
    #         lg_pref_check.append(lg_id)
    #         if same_line == True:
    #             print '{:37}'.format(''),
    #         print '{:8}'.format(str(lg_id) + ': '),
    #         print '{:8}'.format(str(leader_groups[lg_id]["leaders"])),
    #         print
    #         same_line = True
    #
    #     # prints lg hung alg output
    #
    # print

    # LEADER GROUP
    # Title
    print '{:10}'.format('lg id'),
    print '{:20}'.format('user id'),
    print
    # Entries
    for lg in leader_groups:
        print '{:10}'.format(str(lg)),
        print '{:20}'.format(str(leader_groups[lg]["leaders"])),
        print
    print

    # TB
    # Title
    print '{:10}'.format('tb id'),
    print '{:15}'.format('time'),
    print '{:15}'.format('mem ids avail'),
    print '{:15}'.format('lg ids avail'),
    print
    # Entries
    for tb in time_blocks:
        print '{:10}'.format(str(tb)),
        print '{:15}'.format(str(time_blocks[tb]["day"]) + ': ' +
                             str(time_blocks[tb]["start"]) + '-' +
                             str(time_blocks[tb]["end"])),
        print '{:15}'.format(str(time_blocks[tb]["members_available"])),
        print '{:15}'.format(str(time_blocks[tb]["leaders_available"])),
        print
    print
        #print '{:10}'.format('tb id: ' + str(tb)),

        # print members.["first_name"]
        # # + ' ' + mem_id["last_name"]
        # print 'lead pref: ' + mem_id["leader_preferences"],
        # for lg_id in mem_id["leader_preferences"]:
        #     print leader_groups["lg_id"]


<<<<<<< HEAD
def checkMem(members, time_blocks, leader_groups,
             matchedIndices, hung_input_dict):

    # SET VARIABLES
    lg_map = hung_input_dict["lg_map"]
    tb_map = hung_input_dict["tb_map"]

    # Matched TB-LG (by Hung Alg) by ID
    matched_ID = []
    for tb,lg in matchedIndices:
        matched_ID.append((tb_map[tb],lg_map[lg]))

    # print('Matched TB-LG id\'s: ')
    # print(str(matched_tb_lg) + '\n')

    # MEMBER
    # Title
    print 'mem id'.center(10),
    print 'f name'.center(10),
    print 'tb pref'.center(10),
    # print 'lg pref: [user id]'.center(20),
    print 'lg pref'.ljust(20),
    print 'matched TB-LG'.center(15),
    print


    # Entries
    for mem in members:
        # Set Vars: Check Hung Alg Output is in Pref
        tb_pref_check = []
        lg_pref_check = []

        # PRINT: MEM ID
        print str(mem).center(10),
        print str(members[mem]["first_name"]).center(10),

        # prints tb pref
        for tb_id in time_blocks:
            if mem in time_blocks[tb_id]["members_available"]:
                # print str(tb_id) + ',',
                tb_pref_check.append(tb_id)
        print str(tb_pref_check).center(10),

        # prints lg pref: [user id]
        # same_line = False
        for lg_id in members[mem]["leader_preferences"]:
            lg_pref_check.append(lg_id)
            # PRINTS LG PREF
            # print '{:8}'.format(str(lg_id) + ': '),
            # print '{:8}'.format(str(leader_groups[lg_id]["leaders"])),
            # print
            # same_line = True
        print str(lg_pref_check).ljust(20),

        # print(str(tb_pref_check) + ', ' + str(lg_pref_check))

        # prints matched TB-LG for mem
        matched_combo = []
        for tb,lg in matched_ID:
            # CONT WORKING HEREEEEEE
            print(str(tb) + ', ' + str(lg) + ':'),
            if (tb in tb_pref_check) & (lg in lg_pref_check):
                print("!"),
                matched_combo.append((tb,lg))
            else:
                print("."),
            # print(str(matched_combo)),
            # print('. '),
        print str(matched_combo).center(15),
        print
    print


=======
"""
Helper Function: PRINTS:
    column titles = time block IDs
    row titles = leader group IDs
    1st matrix: number of matching members
    2nd matrix: array of IDs of matching members
>>>>>>> 184abd6741fda6c8efb05811a74f45a4913ea2da
"""
    Helper Print Function: lg x tb matrix

    val_type options:
        'num'            number of matched mems
        'name_array'     Array of Names of Matching Members
        'id_array'       Array of ID's of Matching Members
"""
def print1Matrix(matchedIndices, hung_input_dict, members, val_type):
    # Set Variables
    ct_matrix = hung_input_dict["ct_martix"]
    mem_id_matrix = hung_input_dict["mem_id_matrix"]
    lg_map = hung_input_dict["lg_map"]
    tb_map = hung_input_dict["tb_map"]
    matrix_len = len(ct_matrix);
    col_size = matrix_len * 5;

    # -----------

    # Print: Column Titles : Leader Group IDs
    for lg_id in lg_map:
        print str(lg_id).center(col_size),
    print
    print ''.center(col_size, '-') * (matrix_len+1)

    temp_tb_index = 0;          # goes through the row (tb)
    temp_lg_index = 0;          # goes through the col (lg)

    for temp_tb_index in range(matrix_len):
        # print('temp_tb_index: ' + str(temp_tb_index))
        for temp_lg_index in range(matrix_len):
            # print(str(temp_tb_index) + ', ' + str(temp_lg_index)),

            # printVal PT1: print val in 2D array depending on chosen val_type:
            if val_type == 'num':
                printVal = ct_matrix[temp_tb_index][temp_lg_index]
            elif val_type == 'name_array':
                temp_mem_list = []
                for user_id in mem_id_matrix[temp_tb_index][temp_lg_index]:
                    temp_mem_list.append(members[user_id]["first_name"])
                printVal = temp_mem_list
            elif val_type == 'id_array':
                printVal = mem_id_matrix[temp_tb_index][temp_lg_index]

            # printVal PT2: adds ! if tb,lg are chosen by alg
            if (temp_tb_index, temp_lg_index) in matchedIndices:
                # printVal = '!' + str(ct_matrix[temp_tb_index][temp_lg_index]) + '!'
                printVal = '!' + str(printVal) + '!'
            # else:
                # printVal = str(ct_matrix[temp_tb_index][temp_lg_index])

            print(str(printVal).center(col_size)),
            temp_lg_index += 1

        # print: row titles
        print '   |  ',
        print tb_map[temp_tb_index],

        temp_tb_index += 1
        print
    print('\n')



def printHungAlgOutput(matchedIndices, hung_input_dict, members, time_blocks, leader_groups):
    # Output of Pre-processing Step
    # fr hung_input_dict
    ct_matrix = hung_input_dict["ct_martix"]
    mem_id_matrix = hung_input_dict["mem_id_matrix"]
    lg_map = hung_input_dict["lg_map"]
    tb_map = hung_input_dict["tb_map"]
    # print(ct_matrix)

    print('Matched TB-LG Indices: ')
    print(matchedIndices)

    matched_tb_lg = []
    for tb,lg in matchedIndices:
        matched_tb_lg.append((tb_map[tb],lg_map[lg]))

    print('Matched TB-LG id\'s: ')
    print(str(matched_tb_lg) + '\n')

    # Prints the member info: tb pref, lg pref and hung alg output
    checkMem(members, time_blocks, leader_groups,
                 matchedIndices, hung_input_dict)

    # PRINTS 3 HELPER MATRICES (hung alg: input + matched output)
    print("Matrix: Number of Matching Members ")
    print1Matrix(matchedIndices, hung_input_dict, members, 'num')
    print("Matrix: Array of Names of Matching Members ")
    print1Matrix(matchedIndices, hung_input_dict, members, 'name_array')
    # print("Matrix: Array of ID's of Matching Members ")
    # print1Matrix(matchedIndices, hung_input_dict, members, 'id_array')





def runFullandPrint(members, time_blocks, leader_groups):
    """
    Runs the pre-processing step and the hungarian algorithm
    Also prints helper print functions in terminal
    """

    # PRE-PROCESSING STEP (prep for hung alg)
    hungarian_input_dict = convertToSquareMatrix(members, time_blocks, leader_groups)
    matrix = hungarian_input_dict["ct_martix"]
    member_matrix = hungarian_input_dict["mem_id_matrix"]
    # note: matrix == ct_matrix (key) in hungarian_input_dict output

    # Helper Print Functions: Hungarian Alg 2D Array Input
    # printConvertSqMtrxInput(members, time_blocks, leader_groups)

    # RUN HUNG ALG W MATRIX (possible negate)
    invert(matrix)
    m = Munkres()
    indexes = m.compute(matrix)    # indexes = indices of the max weight rows and cols
    # print(indexes)
    invert(matrix)
    # print_matrix(matrix_t1, msg='Highest cost through this matrix:')
    total = 0
    for row, column in indexes:
        value = member_matrix[row][column]
        total += len(value)
    #     print('\nTime block %d, Leader Group %d matches members:' % (row, column))
    #     print(value)
    # print('Total members matched: %d' % total)

    printHungAlgOutput(indexes, hungarian_input_dict, members, time_blocks, leader_groups)

    print('---------------------------------------------------------\n \n \n')

#######################################################

def main():

    # DUMMY 1 ---------
    print("TRIAL: DUMMY VALUES 1 \n")
    runFullandPrint(members_t1, time_blocks_t1, leader_groups_t1)

    # DUMMY 2 ---------
    # print("TRIAL: DUMMY VALUES 2 \n")
    # runFullandPrint(members_t2, time_blocks_t2, leader_groups_t2)


main()
