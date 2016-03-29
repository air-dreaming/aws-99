# api.py - logic process for user api service

import tornado.web
from tornado import gen
import time, json
from db import db
from tornado_mysql import err
from tornado_mysql.constants import ER

class BaseUserHandler(tornado.web.RequestHandler):
    jsonBody = None

    # user data struct
    id = 0
    name = ''
    address = ''

    # pre procee the incoming data
    def prepare(self):
        try:
            dataBody = self.request.body
            self.jsonBody = json.loads(dataBody)
            if "name" in self.jsonBody:
                self.name = self.jsonBody["name"].strip()
            if "id" in self.jsonBody:
                self.id = int(self.jsonBody["id"])
            if "address" in self.jsonBody:
                self.address = self.jsonBody["address"]
        except:
            self.make_badrequest()

    # error process - return json wrap
    def make_badrequest(self):
        self.make_reserror_json(400, "bad request")

    def make_notfound(self):
        self.make_reserror_json(404, "not found")


    def make_internalerror(self): 
        self.make_reserror_json(500, "intenral error")

    def make_reserror_json(self, code, message):
        self.set_status(code)
        self.write( {
            "status":"fail",
            "error":{"code":code, "message":message}
        })

# user create handler
class UserCreateHandler(BaseUserHandler):

    # post process
    @gen.coroutine
    def post(self):
        # data validation
        # {"name": "string", "address":"string"}
        if len(self.name) == 0: 
            self.make_badrequest()
        else:
            try:
                sqlString = "INSERT INTO `table_user` (`name`, `address`) VALUES (%s, %s)"
                cur = yield db.connPool().execute(sqlString, (self.name, self.address))
                user_id = cur.lastrowid
                self.write({
                        "status":"success",
                        "data":{"code":200, "user": {"id": user_id, "name": self.name, "address": self.address}}
                    }
                )
            except err.IntegrityError as e:
                if e.code == ER.DUP_ENTRY:
                    self.make.make_reserror_json(400, "user exist already!")
                else: 
                    raise e
            except:
                self.make_internalerror()
                raise

# user exist by id or name
class UserExistHandler(BaseUserHandler):
    @gen.coroutine
    def post(self):
        if self.id != 0:
            try:
                sqlString = "SELECT 1 FROM `table_user` WHERE `id`=%s"
                cur = yield db.connPool().execute(sqlString, (self.id,))
                result = cur.fetchone()
                if result == None: 
                    self.make_reserror_json(400, "user not exist")
                else:
                    self.write({
                        "status": "success",
                        "data":{"code":200, "message": "user exist"}
                        })
            except Exception as e:
                self.make_internalerror()
        elif len(self.name) > 0:
            try:
                sqlString = "SELECT 1 FROM `table_user` WHERE `name`=%s"
                cur = yield db.connPool().execute(sqlString, (self.name,))
                result = cur.fetchone()
                if result == None: 
                    self.make_reserror_json(400, "user not exist")
                else:
                    self.write({
                        "status": "success",
                        "data":{"code":200, "message": "user exist"}
                        })
            except Exception as e:
                print(e)
                self.make_internalerror()
        else:
            self.make_badrequest()

# get user info by user id
class UserInfoHandler(BaseUserHandler):
    @gen.coroutine
    def post(self):
        if self.id != 0:
            try:
                sqlString = "SELECT `name`, `address` FROM `table_user` WHERE `id`=%s"
                cur = yield db.connPool().execute(sqlString, (str(self.id),))
                result = cur.fetchone()
                if result == None: 
                    self.make_reserror_json(400, "user not exist")
                else:
                    self.write({
                        "status": "sucess",
                        "data": {"code": 200, "message":"", "user": {"id":self.id, "name":result[0], "address": result[1]} }
                    })
            except Exception as e:
                print(e)
                self.make_internalerror()
        elif len(self.name) > 0:
            try:
                sqlString = "SELECT `id`, `name`, `address` FROM `table_user` WHERE `name`=%s"
                cur = yield db.connPool().execute(sqlString, (self.name,))
                result = cur.fetchone()
                if result == None: 
                    self.make_reserror_json(400, "user not exist")
                else:
                    self.write({
                        "status": "sucess",
                        "data": {"code": 200, "message":"", "user": {"id":result[0], "name":result[1], "address": result[2]} }
                    })
            except Exception as e:
                print(e)
                self.make_internalerror()
        else:
            self.make_badrequest()

# update user info by user id
class UserUpdateHandler(BaseUserHandler):
    @gen.coroutine
    def post(self):
        if self.id == 0:
            self.make_badrequest()
        else:
            try:
                sqlString = "UPDATE `table_user` SET `name`=%s,`address`=%s WHERE `id`=%s"
                cur = yield db.connPool().execute(sqlString, (self.name, self.address, str(self.id),))
                self.write({
                    "status": "sucess",
                    "data": {"code": 200, "message":""}
                })
            except Exception as e:
                print (e)
                self.make_internalerror()

# delete user info by user id
class UserDeleteHandler(BaseUserHandler):
    @gen.coroutine
    def post(self):
        if self.id == 0:
            self.make_badrequest()
        else:
            try:
                sqlString = "DELETE FROM `table_user` WHERE `id`=%s"
                cur = yield db.connPool().execute(sqlString, (str(self.id),))
                affected_rows = cur.rowcount
                if affected_rows == 0:
                    self.make_reserror_json(400, "user not exist")
                else:
                    self.write({
                        "status": "sucess",
                        "data": {"code": 200, "message":""}
                    })
            except Exception as e:
                print(e)
                self.make_internalerror()