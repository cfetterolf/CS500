from schedule.connectDB import connect_postgres
from django.conf import settings
import psycopg2

#CREATE TABLE time_block (ID bigserial primary key NOT NULL, day varchar(15) NOT NULL, start_time decimal NOT NULL, end_time decimal NOT NULL);


# connect to DB
conn = connect_postgres()
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def set_gid(body):
    new_gid = int(body.get('gid'))
    settings.GID = new_gid
    return {'new_gid': settings.GID}

def reset_gid():
    settings.GID = None
    return {'gid': settings.GID}

def get_group_info(gid):
    info = {}
    query = "SELECT * FROM group_info WHERE id=%d" % (gid)
    cursor.execute(query)
    for row in cursor:
        return {'name': row[1], 'term': row[2]}

def getUsers(gid):
    users = {}
    # get all users in our group
    query = "SELECT * FROM user_contact INNER JOIN association ON user_contact.id = association.user_id AND association.group_id = %d" % (settings.GID)
    cursor.execute(query)
    for row in cursor:
        uid = row[0] # get user id
        users[uid] = {}
        users[uid]['member'] = row[5]
        users[uid]['leader'] = row[6]
        users[uid]['first_name'] = row[1]
        users[uid]['last_name'] = row[2]
        users[uid]['email'] = row[3]
        users[uid]['leader_preferences'] = row[10]
    return users

def add_user(user, gid):
    # Add user record in user_contact
    query_str = "INSERT INTO user_contact (first_name, last_name, email) VALUES ('%s', '%s', '%s') RETURNING id;" % (user.get('first_name'), user.get('last_name'), user.get('email'))
    cursor.execute(query_str)
    uid = cursor.fetchone()[0]

    # Add user to association
    leader_preferences = user.get('preferred_leaders')
    leader_preferences_str = ','.join(leader_preferences)
    leader_preferences_str = "{"+leader_preferences_str+"}"
    query_str = "INSERT INTO association (member, leader, admin, group_id, user_id, leader_preferences) VALUES (%s, %s, false, %s, %s, '%s')" % (user.get('member'), user.get('leader'), gid, uid, leader_preferences_str)
    cursor.execute(query_str)

    # Add user to time blocks
    schedule = user.get('schedule')
    for tid in schedule:
        query_str = "SELECT * FROM availability WHERE time_id=%s AND group_id=%s;" % (tid, gid)
        cursor.execute(query_str)
        row = cursor.fetchall()[0]
        placeholder = '?'
        query = ''

        if(user.get('member')):
            members = row[3]
            members.append(str(uid))
            members_str = ','.join(members)
            members_str = "{"+members_str+"}"
            query = "UPDATE availability SET members = '%s' WHERE time_id = %s AND group_id = %s" % (members_str, tid, gid)
            cursor.execute(query, members)

        if(user.get('leader')):
            leaders = row[4]
            leaders.append(str(uid))
            leaders_str = ','.join(leaders)
            leaders_str = "{"+leaders_str+"}"
            query = "UPDATE availability SET leaders = '%s' WHERE time_id = %s AND group_id = %s" % (leaders_str, tid, gid)
            cursor.execute(query, leaders)


    return {'query': query}

def add_leaders(body):
    newLeaders = body.get('new_leaders')
    uid = body.get('uid')

    query = "SELECT * FROM association WHERE user_id=%s AND group_id=%s;" % (uid, settings.GID)
    cursor.execute(query)
    row = cursor.fetchall()[0]
    leader_pref = row[6]
    leader_pref += newLeaders
    leader_pref_str = ','.join(str(e) for e in leader_pref)
    leader_pref_str = "{"+leader_pref_str+"}"

    query = "UPDATE association SET leader_preferences = '%s' WHERE user_id = %s AND group_id = %s" % (leader_pref_str, uid, settings.GID)
    cursor.execute(query)
    return {'query': query}


def get_groups():
    cursor.execute("SELECT * FROM group_info WHERE email='%s' AND password='%s'" % (settings.EMAIL, settings.PASSWORD))
    cursor_blocks = cursor.fetchall()
    groups = {}
    for group in cursor_blocks:
        groups[group[0]] = {
            'name': group[1],
            'term': group[2],
            'email': group[3],
            'password': group[4]
        }
    return groups

def add_group(group):
    query = "INSERT INTO group_info (name, term, email, password) VALUES ('%s', '%s', '%s', '%s')" % (group.get('name'), group.get('term'), settings.EMAIL, settings.PASSWORD)
    cursor.execute(query)

    # Get newly generated gid
    cursor.execute("SELECT * FROM group_info WHERE name='%s' AND term='%s' AND email='%s';" % (group.get('name'), group.get('term'), settings.EMAIL))
    gid = cursor.fetchall()[0][0]

    for tid in group.get('time_blocks'):
        block = group.get('time_blocks')[tid]
        query = "INSERT INTO time_block (day, start_time, end_time) VALUES ('%s', %d, %d) RETURNING id" % (block['day'], block['start'], block['end'])
        cursor.execute(query)
        tid = cursor.fetchone()[0]

        query = "INSERT INTO availability (time_id, group_id, members, leaders) VALUES (%d, %d, '%s', '%s')" % (int(tid), int(gid), '{}', '{}')
        cursor.execute(query)
    return {'query': query}

def delete_group(gid):
    #delete from group_info
    query = "DELETE FROM group_info WHERE id=%d" % (gid)
    cursor.execute(query)

    #delete users from association, user_contact
    query = "DELETE FROM user_contact USING association WHERE user_contact.id = association.user_id AND association.group_id=%s" % (gid)
    cursor.execute(query)
    query = "DELETE FROM association WHERE group_id=%s" % (gid)
    cursor.execute(query)


    #delete from availability, time_block
    query = "DELETE FROM time_block USING availability WHERE time_block.id = availability.time_id AND availability.group_id=%s" % (gid)
    cursor.execute(query)
    query = "DELETE FROM availability WHERE group_id=%s" % (gid)
    cursor.execute(query)

    return {'message': 'deleted all info from group!'}

def login_account(body):
    email = body.get('email')
    password = body.get('password')
    cursor.execute("SELECT * FROM account WHERE email='%s' AND password='%s'" % (email, password))
    cursor_blocks = cursor.fetchall()

    groups = []
    for row in cursor_blocks:
        groups.append(row[0])

    if not groups:
        return {'failure': 'Invalid email/password'}
    else:
        settings.LOGGED_IN = True
        settings.EMAIL = email
        settings.PASSWORD = password
        settings.AID = groups[0]
        return {'success': 'success'}

def signup_account(body):
    email = body.get('email')
    password = body.get('password')
    cursor.execute("SELECT * FROM account WHERE email='%s' AND password='%s'" % (email, password))
    cursor_blocks = cursor.fetchall()
    groups = []
    for row in cursor_blocks:
        groups.append(row[0])

    if not groups:
        cursor.execute("INSERT INTO account (email, password) VALUES ('%s', '%s') RETURNING id" % (email, password))
        account_id = cursor.fetchone()[0]
        settings.LOGGED_IN = True
        settings.EMAIL = email
        settings.PASSWORD = password
        settings.AID = account_id
        return {'success': 'success'}
    else:
        return {'failure': 'Account already exists!'}

def getTimeBlocks(gid):
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
def get_alg_members(gid):
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
        members[uid]['leader_preferences'] = results = list(map(int, member[10]))


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
def get_alg_leader_groups(gid):
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
def get_alg_time_blocks(gid):
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
