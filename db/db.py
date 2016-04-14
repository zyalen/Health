#!/usr/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import random
import string
import hashlib
import numpy

from db_execute import db_execute
from util import GB
from util import get_recommand


'''
add a new account to database.
@params a dict data:
        includes account and password.
@return -1 indicates params are not complete. Or account is not unique that leads to database fails.
        other number indicates success and the number is the id of the new account.
'''
def add_account(data):
  print data
  if GB.ACCOUNT not in data or GB.PASSWORD not in data:
    return -1

  salt = ''.join(random.sample(string.ascii_letters, 8))
  sha1_encode = hashlib.sha1()
  sha1_encode.update(str(data[GB.PASSWORD])+salt)
  password = sha1_encode.hexdigest()

  sql_account = "insert into account (account, password, salt) values (%d, '%s', '%s')"
  sql_user = "insert into user (id, nickname, phone) values (%d, '%s', %d)"
  try:
    insert_id = db_execute.insert(sql_account%(data[GB.ACCOUNT], password, salt))
    db_execute.insert(sql_user%(insert_id, str(data[GB.ACCOUNT]), data[GB.ACCOUNT]))
    return insert_id
  except Exception, e:
    print e
    return -1

'''
modify user's information.
@params a dict data:
        options include user's name, nickname, gender, age, phone
        gender: 0 male, 1 female
@return True if successfully modify
        False modification fails.
'''

def update_user(data):
  print data
  if GB.ID not in data:
    return False
  result = True

  sql = ""
  if GB.NAME in data:
    sql = "update user set name = '%s' where id = %d"
    try:
      data[GB.NAME] = data[GB.NAME]
      db_execute.execute(sql % (data[GB.NAME], data[GB.ID]))
      result &= True
    except:
      result &= False
      return result

  if GB.NICKNAME in data:
    print data[GB.NICKNAME]
    sql = "update user set nickname = '%s' where id = %d"
    try:
      db_execute.execute(sql % (data[GB.NICKNAME], data[GB.ID]))
      result &= True
    except:
      result &= False
      return result

  if GB.GENDER in data:
    sql = "update user set gender = %d where id = %d"
    try:
      db_execute.execute(sql % (data[GB.GENDER], data[GB.ID]))
      result &= True
    except:
      result &= False
      return result

    if GB.AGE in data:
      sql = "update user set age = %d where id = %d"
      try:
        db_execute.execute(sql % (data[GB.AGE], data[GB.ID]))
        result &= True
      except:
        result &= False
        return result

    if GB.PHONE in data:
      sql = "update user set phone = %d where id = %d"
      try:
        db_execute.execute(sql % (data[GB.PHONE], data[GB.ID]))
        result &= True
      except:
        result &= False
        return result

  return result

'''
get salt of an account.
@params include user's account.
@return salt of an account.
        None if account not exists or database query error.
'''

def get_salt(data):
  if GB.ACCOUNT not in data:
    return None
  sql = "select salt from account where account = '%s'"
  try:
    res = db_execute.execute_fetchone(sql % (data[GB.ACCOUNT]))
    if res is None:
      return None
    else:
      return res[0]
  except:
    return None

'''
validate whether password is correct.
@params includes user's account and password.
                      password need to be sha1 encode.
@return user's id if password is correct.
         -1 otherwise.
'''
def validate_password(data):
  if GB.ACCOUNT not in data or GB.PASSWORD not in data or GB.SALT not in data:
    return -1
  sql = "select id, password from account where account = '%s' and salt = '%s'"
  user_id = -1
  password = None
  try:
    res = db_execute.execute_fetchone(sql%(data[GB.ACCOUNT], data[GB.SALT]))
    if res is not None:
      user_id = res[0]
      password = res[1]
  except:
    pass
  finally:
    if password is None or data[GB.PASSWORD] is None:
      return -1
    elif password == data[GB.PASSWORD]:
      return user_id
    else:
      return -1


'''
modify user's password to a new one, but not modify its salt value.
@params include user's account. 
                      new password that encode with salt by sha1.
@return true if successfully modify.
           false otherwise.
'''
def modify_password(data):
  if GB.ACCOUNT not in data or GB.PASSWORD not in data:
    return False
  sql = "update account set password = '%s' where account = '%s'"
  try:
    n = db_execute.execute(sql%(data[GB.PASSWORD], data[GB.ACCOUNT]))
    if n > 0:
      return True
    else:
      return False
  except:
      return False
  
'''
get user's information, which includes user's name, nickname, gender ...... .
@params include user's id
        option user's phone
@return a json includes user's concrete information.
           None if params error or database query error.
'''
def get_user_information(data):
  if GB.ID not in data:
    if GB.PHONE not in data:
      return None
    else:
      sql = "select * from user where phone = %d"%data[GB.PHONE]
  else:
    sql = "select * from user where id = %d"%data[GB.ID]
  try:
    res = db_execute.execute_fetchone(sql)
    if res is None:
      return None
    else:
      user = {}
      user[GB.ID] = res[0]
      user[GB.NAME] = res[1]
      user[GB.NICKNAME] = res[2]
      user[GB.GENDER] = res[3]
      user[GB.AGE] = res[4]
      user[GB.PHONE] = res[5]
      return user
  except:
    return None

'''
add a health report by user.
@params includes user's id 
       other option params includes heart_rate, step_num, ...
@return health_id if successfully launches.
        -1 if fails.
'''
def add_health(data):
  if GB.ID not in data:
    return -1
  sql = "insert into health (user_id) values (%d)"
  try:
    health_id = db_execute.insert(sql%data[GB.ID])
    if health_id > 0:
      data[GB.HEALTH_ID] = health_id
      if not update_health(data):
        return -1
    return health_id
  except:
    return -1

'''
modify information of a health report.
@params  includes health_id, which is id of the health to be modified.
          option params includes: heart_rate, step_num, ...
@return True if successfully modifies.
        False otherwise.
'''

def update_health(data):
  result = True
  if GB.HEALTH_ID not in data:
    return False
  sql = ""
  if GB.HEART_RATE in data:
    sql = "update health set heart_rate = %d where id = %d"
    try:
      db_execute.execute(sql % (data[GB.HEART_RATE], data[GB.HEALTH_ID]))
      result &= True
    except:
      result &= False
  if GB.STEP_NUM in data:
    sql = "update health set step_num = %d where id = %d"
    try:
      db_execute.execute(sql % (data[GB.STEP_NUM], data[GB.HEALTH_ID]))
      result &= True
    except:
      result &= False
  if GB.BLOOD_PRESSURE in data:
    sql = "update health set blood_pressure = %d where id = %d"
    try:
      db_execute.execute(sql % (data[GB.BLOOD_PRESSURE], data[GB.HEALTH_ID]))
      result &= True
    except:
      result &= False
  if GB.VISION in data:
    sql = "update health set vision = %f where id = %d"
    try:
      db_execute.execute(sql % (data[GB.VISION], data[GB.HEALTH_ID]))
      result &= True
    except:
      result &= False
  return result


'''
remove a health report by user.
@params includes user's id.
                 health's id, which represents the health report to be removed.
@return True if successfully removes, or remover is not the launcher, actually nothing happens.
        False if fails.
'''
def remove_health(data):
  if GB.ID not in data or GB.HEALTH_ID not in data:
    return False
  sql = "delete from health where id = %d and user_id = %d"
  try:
    db_execute.execute(sql%(data[GB.HEALTH_ID], data[GB.ID]))
    return True
  except:
    return False

'''
get information of a health report.
@params includes id of the health report to get.
@return concrete information of the health report:
        user_id, heart_rate, step_num, blood_pressure, vision, time.
        None indicates fail query.
'''
def get_health_information(data):
  if GB.HEALTH_ID not in data:
    return None
  health_info = None
  sql = "select * from health where id = %d"
  try:
    sql_result = db_execute.execute_fetchone(sql%data[GB.HEALTH_ID])
    if sql_result is not None:
      health_info = {}
      health_info[GB.HEALTH_ID] = sql_result[0]
      health_info[GB.USER_ID] = sql_result[1]
      health_info[GB.HEART_RATE] = sql_result[2]
      health_info[GB.STEP_NUM] = sql_result[3]
      health_info[GB.BLOOD_PRESSURE] = sql_result[4]
      health_info[GB.VISION] = str(sql_result[5])
      health_info[GB.TIME] = str(sql_result[6])
  except:
    pass
  finally:
    return health_info

'''
get a list of health reports.
@param includes user_id
@return a list of information of health reports of the user
'''
def get_health_list(data):
  health_list = []
  health_report = {}
  if GB.USER_ID not in data:
    return health_list
  sql = "select id from health where user_id = %d order by health.time DESC"%data[GB.USER_ID]
  sql_result = db_execute.execute_fetchall(sql)
  for each_result in sql_result:
    for each_id in each_result:
      health_report[GB.HEALTH_ID] = each_id
      health_report = get_health_information(health_report)
      if health_report is not None:
        health_list.append(health_report)
  return health_list

'''
get information of item
@param item's id
@return information of item
'''
def get_items_information(data):
  if GB.ITEM_ID not in data:
    return None
  sql = "select * from items where id = %d"%data[GB.ITEM_ID]
  item_info = None
  try:
    sql_result = db_execute.execute_fetchone(sql)
    if sql_result is not None:
      item_info = {}
      item_info[GB.ITEM_ID] = sql_result[0]
      item_info[GB.ITEM_NAME] = sql_result[1]
      item_info[GB.PRICE] = sql_result[2]
      item_info[GB.REPRESENTATION] = sql_result[3]
  except:
    pass
  finally:
    return item_info


'''
get a list of items
@param
@return a list of items
'''
def get_items_list(data):
  sql = "select id from items order by id"
  item_list = []
  item_info = {}
  try:
    sql_result = db_execute.execute_fetchall(sql)
    for each_result in sql_result:
      for each_id in each_result:
        item_info[GB.ITEM_ID] = each_id
        item_info = get_items_information(item_info)
        if item_info is not None:
          item_list.append(item_info)
  except Exception, e:
    print e
    pass
  finally:
    return item_list


'''
get a list of suit items
@param user_id, user's id
@return a list of items' id
'''
def get_suit_items(data):
  itmes = []
  if GB.USER_ID not in data:
    return itmes
  sql = "select * from health where health.user_id = %d"%data[GB.USER_ID]
  sql_result = db_execute.execute_fetchall(sql)
  if sql_result is None:
    return itmes
  sum = 0
  n = 0
  for each_result in sql_result:
    heart_rate = each_result[2]
    sum += heart_rate
    n+=1
  heart_rate = sum/n

  item_sql = "select id from items"
  if heart_rate > 100:
    item_sql += " where high_heart_rate = 1"
  elif heart_rate < 60:
    item_sql += " where low_heart_rate = 1"
  item_result = db_execute.execute_fetchall(item_sql)
  for each_result in item_result:
    for each_id in each_result:
      if each_id is not None:
        itmes.append(each_id)
  return itmes

'''
get recommand items
@param user_id, user's id
@return a list of recommand items
'''
def get_recommand_items(data):
  if GB.USER_ID not in data:
    return None
  items = get_suit_items(data)
  users = []
  sql = "select id from account"
  sql_result = db_execute.execute_fetchall(sql)
  for each_result in sql_result:
    for each_id in each_result:
      users.append(each_id)

  R = [[] for i in range(len(users))]
  for i in range(len(users)):
    for j in range(len(items)):
      R[i].append(0)

  reviews_sql = "select * from reviews"
  reviews_result = db_execute.execute_fetchall(reviews_sql)
  for each_result in reviews_result:
    if each_result[1] in users and each_result[2] in items:
      i = users.index(each_result[1])
      j = items.index(each_result[2])
      R[i][j] = each_result[3]

  R = get_recommand.get_recommand(R)

  raw = users.index(data[GB.USER_ID])
  items_index = numpy.argsort(R)[:, ::-1]
  items_id = []
  for i in items_index[raw]:
    items_id.append(items[i])
  suit_items_id = items_id[0:4]

  suit_items = []
  item_data = {}
  for items_id in suit_items_id:
    item_data[GB.ITEM_ID] = items_id
    item_data = get_items_information(item_data)
    suit_items.append(item_data)
  return suit_items

# test
def add_items():
  sql = "insert into items(item_name, price, high_heart_rate, low_heart_rate) VALUES ('%s', %d, %d, %d)"
  item_name = "item_name_"
  for i in range(1, 50):
    sql_result = db_execute.insert(sql%(item_name+str(i), random.randint(10,200), i%2, 1-i%2))

def add_reviews():
  sql = "insert into reviews(user_id, item_id, customer_reviews) VALUES (%d, %d, %d)"
  for i in range(1, 50):
    sql_result = db_execute.insert(sql%((random.randint(5,7)), i, random.randint(1, 5)))