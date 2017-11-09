from schedule.connectDB import connect_postgres
import psycopg2

#CREATE TABLE time_block (ID bigserial primary key NOT NULL, day varchar(15) NOT NULL, start_time decimal NOT NULL, end_time decimal NOT NULL);

users = {}
gid = 1

#def get_data():
    #pull all data


def getUsers():
    # connect to DB
    conn = connect_postgres()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # get all users in our group
    cursor.execute("SELECT * FROM association WHERE group_id="+str(gid))
    cursor_blocks = cursor.fetchall()
    for row in cursor_blocks:
        uid = row[5] # get user id, use to pull all info
        users[uid] = {}
        users[uid]['member'] = row[1]
        users[uid]['leader'] = row[2]
        cursor.execute("SELECT * FROM user_contact WHERE id="+str(uid))
        for contact_row in cursor.fetchall():
            users[uid]['first_name'] = contact_row[1]
            users[uid]['last_name'] = contact_row[2]
            users[uid]['email'] = contact_row[3]

    # users = {
    #   '001': {
    #     'first_name': "Chris",
    #     'last_name': "Fetterolf",
    #     'email': "chris.fetterolf@gmail.com",
    #     'member': True,
    #     'leader': False,
    #     'schedule': ['100', '103', '104'],
    #   },
    #   '002': {
    #     'first_name': "Andrea",
    #     'last_name': "Narciso",
    #     'email': "anarciso@middlebury.edu",
    #     'member': True,
    #     'leader': True,
    #     'schedule': ['101', '102', '104', '106'],
    #   }
    # }
    return users




def getTimeBlocks():
    # pull the info from the database
    conn = connect_postgres()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM time_block")
    cursor_blocks = cursor.fetchall()

    time_blocks = {}
    for row in cursor_blocks:
        time_blocks[row[0]] = {
            'day': row[1],
            'start': row[2],
            'end': row[3]
        }
    return time_blocks


#####################################################################
#######                  Algorithm Methods                    #######
#####################################################################

"""
returns the composite members object for algoritm
"""
def get_alg_members():
    # Pull this members object from DB
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
    return members


"""
returns composite leader_groups object for algoritm
"""
def get_alg_leader_groups():
    # Pull this leader_groups object from DB
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
    return leader_groups


"""
returns composite time_block object for algoritm
"""
def get_alg_time_blocks():
    # Pull this time_blocks object from DB
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
    return time_blocks
