#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode

from util import utils
from util import GB
from db import db

class Get_Item_List_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    items = db.get_items_list(params)
    resp = {}
    resp[GB.STATUS] = GB.OK
    resp[GB.ITEM_LIST] = items

    self.write(json_encode(resp))