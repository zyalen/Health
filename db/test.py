from db_execute import db_execute

def get(data):
  a = {}
  a["a"] = each_result[0]
  a["b"] = each_result[1]
  return a

if __name__ =='__main__':
  sql = "select * from a"
  alist = []
  a = {}
  sql_result = db_execute.execute_fetchall(sql)
  for each_result in sql_result:
    a = get(each_result)
    alist.append(a)
    print alist