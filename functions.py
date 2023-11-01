import mysql.connector
from mysql.connector import Error
import pandas as pd
import config

import creds 

async def get_current_roles():
    mydb = mysql.connector.connect(
                                host = creds.forum_role_mysql(0),
                                user = creds.forum_role_mysql(1),
                                password = creds.forum_role_mysql(2),
                                database = creds.forum_role_mysql(3)
                            )
    mycursor = mydb.cursor()
    
    _query = "SELECT member_id, member_group_id, token_identifier from sql_forums_ghost.discord_id_forum_id"

    mycursor = mydb.cursor()
    _err = None
    result = None
    checker = True
    df_maps = None
    while checker:
        try:
            with mycursor as cursor:
                cursor.execute(_query)
                result = cursor.fetchall()
            checker = False

        except Error as e:
            _err = e
            print("Error :{}".format(e))
            break

        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()

            if not checker:
                break
    
    if len(result) > 0:
        df_maps = pd.DataFrame(result, columns =['forum_id', 'forum_role_id','discord_id'])


    if _err is None:
        return df_maps
    else:
        return _err

async def get_user_ids():
    mydb = mysql.connector.connect(
                                host = creds.forum_role_mysql(0),
                                user = creds.forum_role_mysql(1),
                                password = creds.forum_role_mysql(2),
                                database = creds.forum_role_mysql(3)
                            )
    mycursor = mydb.cursor()
    
    _query = "SELECT token_member, token_identifier from sql_forums_ghost.core_login_links"

    mycursor = mydb.cursor()
    _err = None
    result = None
    checker = True
    df_maps = None
    while checker:
        try:
            with mycursor as cursor:
                cursor.execute(_query)
                result = cursor.fetchall()
            checker = False

        except Error as e:
            _err = e
            print("Error :{}".format(e))
            break

        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()

            if not checker:
                break
    
    if len(result) > 0:
        df_maps = pd.DataFrame(result, columns =['user_id', 'discord_id'])


    if _err is None:
        return df_maps
    else:
        return _err


async def update_forum_roles(id,role):
    mydb = mysql.connector.connect(
                                host = creds.forum_role_mysql(0),
                                user = creds.forum_role_mysql(1),
                                password = creds.forum_role_mysql(2),
                                database = creds.forum_role_mysql(3)
                            )
    update_query = "UPDATE sql_forums_ghost.core_members SET member_group_id = '{}' WHERE member_id = {}".format(config.forum_roles[role],id)
    
    mycursor = mydb.cursor()
    # result = None
    try:
        with mycursor as cursor:
            cursor.execute(update_query)
            mydb.commit()
            result = cursor.rowcount

    except Error as err:
        print(" Cust_func insert_map_noti error : {}".format(err))

    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()

