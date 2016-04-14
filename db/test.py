# -*- coding: utf-8 -*-
import db

if __name__ =='__main__':
  data = {"user_id": 5}
  print db.get_recommand_items(data)