from schedule.connectDB import connect_postgres
import psycopg2

#CREATE TABLE time_block (ID bigserial primary key NOT NULL, day varchar(15) NOT NULL, start_time decimal NOT NULL, end_time decimal NOT NULL);

users = {}
gid = 1

# connect to DB
conn = connect_postgres()
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#def get_data():
    #pull all data


def getUsers():

    # get all users in our group
    cursor.execute("SELECT * FROM user_contact INNER JOIN association ON user_contact.id = association.user_id AND association.group_id="+str(gid))
    cursor_blocks = cursor.fetchall()
    for row in cursor_blocks:
        uid = row[0] # get user id
        users[uid] = {}
        users[uid]['member'] = row[5]
        users[uid]['leader'] = row[6]
        users[uid]['first_name'] = row[1]
        users[uid]['last_name'] = row[2]
        users[uid]['email'] = row[3]


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

def add_user(user):
    # Add user record in user_contact
    query_str = "INSERT INTO user_contact (first_name, last_name, email) VALUES ('%s', '%s', '%s');" % (user.get('first_name'), user.get('last_name'), user.get('email'))
    cursor.execute(query_str)

    # Get newly generated id
    cursor.execute("SELECT * FROM user_contact WHERE first_name='%s' AND last_name='%s';" % (user.get('first_name'), user.get('last_name')))
    uid = cursor.fetchall()[0][0]

    # Add user to association
    query_str = "INSERT INTO association (member, leader, admin, group_id, user_id, leader_preferences) VALUES (%s, %s, false, %s, %s, '%s')" % (user.get('member'), user.get('leader'), gid, uid, {1,2})
    cursor.execute(query_str)
    return {'query': query_str}

def getTimeBlocks():
    # pull the info from the database
    cursor.execute("SELECT * FROM time_block INNER JOIN availability ON time_block.id = availability.time_id AND availability.group_id="+str(gid))
    cursor_blocks = cursor.fetchall()

    time_blocks = {}
    for time_block in cursor_blocks:
        time_blocks[time_block[0]] = {
            'day': time_block[1],
            'start': time_block[2],
            'end': time_block[3]
        }
    return time_blocks


#####################################################################
#######                  Algorithm Methods                    #######
#####################################################################

"""
returns the composite members object for algoritm
"""
def get_alg_members():
    members = {}
    # get all users in our group
    cursor.execute("SELECT * FROM user_contact INNER JOIN association ON user_contact.id = association.user_id AND association.member = true AND association.group_id="+str(gid))
    cursor_blocks = cursor.fetchall()
    for member in cursor_blocks:
        uid = member[0] # get user id
        members[uid] = {}
        members[uid]['first_name'] = member[1]
        members[uid]['last_name'] = member[2]
        members[uid]['email'] = member[3]
        members[uid]['leader_preferences'] = member[10]


    # members = {
    #     0: { # ID of member (association.id)
    #         "first_name": "Chris",
    #         "last_name": "Fetterolf",
    #         "email": "chris@gmail",
    #         "leader_preferences": [10, 11], # IDs of preferred leader groups
    #     },
    #     1: {
    #         "first_name": "Andrea",
    #         "last_name": "Narciso",
    #         "email": "chris@gmail",
    #         "leader_preferences": [12], # IDs of preferred leader groups
    #     },
    #     2: {
    #         "first_name": "Joe",
    #         "last_name": "Antonioli",
    #         "email": "chris@gmail",
    #         "leader_preferences": [10], # IDs of preferred leader groups
    #     },
    # }
    return members


"""
returns composite leader_groups object for algoritm
"""
def get_alg_leader_groups():
    leader_groups = {}

    # Pull this leader_groups object from DB
    cursor.execute("SELECT * FROM association WHERE leader = true AND group_id="+str(gid))
    cursor_blocks = cursor.fetchall()
    for leader in cursor_blocks:
        id = leader[5]
        leader_groups[id] = {}
        leader_groups[id]['leaders'] = [id]

    # leader_groups = {
    #     10: {
    #         "leaders": [1] # Andrea
    #     },
    #     11: {
    #         "leaders": [2] # Joe
    #     },
    #     12: {
    #         "leaders": [3, 4] # Two other people
    #     }
    # }
    return leader_groups


"""
returns composite time_block object for algoritm
"""
def get_alg_time_blocks():
    time_blocks = {}

    # DB: JOIN availability and time_block like i did above
    cursor.execute("SELECT * FROM time_block INNER JOIN availability ON time_block.id = availability.time_id AND availability.group_id="+str(gid))
    cursor_blocks = cursor.fetchall()
    for time_block in cursor_blocks:
        id = time_block[0]
        time_blocks[id] = {}
        time_blocks[id]['day'] = time_block[1]
        time_blocks[id]['start'] = time_block[2]
        time_blocks[id]['end'] = time_block[3]
        time_blocks[id]['members_available'] = time_block[7]
        time_blocks[id]['leaders_available'] = time_block[8]

    return time_blocks

    # time_blocks = {
    #     7: { # ID for the time block
    #         "day": "Monday",
    #         "start": 14,
    #         "end": 18,
    #         "members_available": [0, 1, 2], # IDs of members available
    #         "leaders_available": [11, 12],    # IDs of leaders available
    #     },
    #     8: {
    #         "day": "Sunday",
    #         "start": 12,
    #         "end": 14,
    #         "members_available": [0, 2],
    #         "leaders_available": [12],
    #     },
    #     9: {
    #         "day": "Thursday",
    #         "start": 10,
    #         "end": 12,
    #         "members_available": [1],
    #         "leaders_available": [10, 12],
    #     }
    # }
