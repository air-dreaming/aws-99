# api.py - logic process for user api service

import time, json
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado_mysql import err
from tornado_mysql.constants import ER
from db import db


def getListingTypeName(listingType):
    if listingType == 1:
        return "rent"
    elif listingType == 2:
        return "sale"
    else:
        return None

def getListingStatusName(listingStatus):
    if listingStatus == 1:
        return "active"
    elif listingStatus == 2:
        return "closed"
    elif listingStatus == 3:
        return "deleted"
    else:
        return None


class BaseListingHandler(tornado.web.RequestHandler):
    jsonBody = None

    # user data struct
    id = 0
    user = 0
    price = 0.0
    listingType = 0
    postalCode = ""
    status = 0

    # pre procee the incoming data
    def prepare(self):
        try:
            dataBody = self.request.body
            self.jsonBody = json.loads(dataBody)
            print(self.jsonBody)
            if "id" in self.jsonBody:
                self.id = long(self.jsonBody["id"])
            if "user" in self.jsonBody:
                self.user = long(self.jsonBody["user"])
            if "price" in self.jsonBody:
                self.price = float(self.jsonBody["price"])
            if "listingType" in self.jsonBody:
                self.listingType = int(self.jsonBody["listingType"])
            if "postalCode" in self.jsonBody:
                self.postalCode = self.jsonBody["postalCode"].strip()
            if "status" in self.jsonBody:
                self.status = int(self.jsonBody["status"])
        except:
            pass

    # error process - return json wrap
    def make_badrequest(self):
        self.make_reserror_json(400, "bad request")

    def make_notfound(self):
        self.make_reserror_json(404, "not found")


    def make_internalerror(self): 
        self.make_reserror_json(500, "intenral error")


    def make_reserror_json(self, code, message):
        self.set_status(code)
        self.write ({
            "status":"fail",
            "error":{"code":code, "message":message}
        })

    @gen.coroutine
    def verifyUserId(self, id):
       
        # def handleRequest(response):
        #     if response.error:
        #         print "Error:", response.error
        #     else:
        #         print response.body
        #     tornado.ioloop.IOLoop.instance().stop()
        try:
            postData = {"id": id}
            jsonData = json.dumps(postData)
            response = yield AsyncHTTPClient().fetch("http://172.31.23.200:8881/api/userexist/", method='POST', headers=None, body=jsonData)
        except:
            raise gen.Return(False)
        raise gen.Return(response.code == 200)

# user create handler
class ListingCreateHandler(BaseListingHandler):
    # post process
    @gen.coroutine
    def post(self):
        # data validation
        if self.user == 0 or self.price <= 0.0 or len(self.postalCode) == 0 or getListingTypeName(self.listingType) == None or getListingStatusName(self.status) == None:
            self.make_badrequest()
        else:
            verified = yield self.verifyUserId(self.user)
            if not verified:
                self.make_notfound()
            else:
                try:
                    sqlString = "INSERT INTO `table_listing` (`user`, `price`, `listing_type`, `postal_code`, `status`) VALUES (%s, %s, %s, %s, %s)"
                    cur = yield db.connPool().execute(sqlString, (
                        str(self.user), str(self.price), getListingTypeName(self.listingType), self.postalCode, getListingStatusName(self.status),) )
                    id = cur.lastrowid
                    self.write({
                            "status":"success",
                            "data":{"code":200, "listing": {"id": id, "user": self.user, "price": str(self.price), "listingType": self.listingType,
                                "postalCode": self.postalCode, "status": self.status}}
                        }
                    )
                except Exception as e:
                    print (e)
                    self.make_internalerror()


# update listing info by id - just sample to update all
class ListingUpdateHandler(BaseListingHandler):
    @gen.coroutine
    def post(self):
        if self.id == 0 or self.price <= 0 or len(self.postalCode) == 0 or getListingTypeName(self.listingType) == None or getListingStatusName(self.status) == None:
            self.make_badrequest()
        else:
            verified = self.verifyUserId(self.user)
            if not verified:
                self.make_notfound()
            else:
                try:
                    sqlString = "UPDATE `table_listing` SET `user`=%s,`price`=%s, `listing_type`=%s, `postal_code`=%s, `status`=%s WHERE `id`=%s"
                    cur = yield db.connPool().execute(sqlString, (str(self.user), str(self.price), getListingTypeName(self.listingType), self.postalCode, getListingStatusName(self.status), str(self.id),))
                    affectedRows = cur.rowcount
                    if affectedRows == 0:
                        self.make_badrequest()
                    else:
                        self.write({
                            "status": "sucess",
                            "data": {"code": 200, "message":""}
                        })
                except Exception as e:
                    print (e)
                    self.make_internalerror()

class ListingPriceUpdateHandler(BaseListingHandler):
    @gen.coroutine
    def post(self):
        if self.id == 0 or self.user == 0 or self.price <= 0:
            self.make_badrequest()
        else:
            verified = self.verifyUserId(self.user)
            if not verified:
                self.make_notfound()
            else:
                try:
                    sqlString = "UPDATE `table_listing` SET `price`=%s WHERE `id`=%s"
                    cur = yield db.connPool().execute(sqlString, (str(self.price), str(self.id),))
                    affectedRows = cur.rowcount
                    print(affectedRows)
                    if affectedRows == 0:
                        self.make_badrequest()
                    else:
                        self.write({
                            "status": "sucess",
                            "data": {"code": 200, "message":""}
                        })
                except Exception as e:
                    print (e)
                    self.make_internalerror()

# delete user info by  id
class ListingDeleteHandler(BaseListingHandler):
    @gen.coroutine
    def post(self):
        if self.id == 0:
            self.make_badrequest()
        else:
            verified = self.verifyUserId(self.user)
            if not verified:
                self.make_notfound()
            else:
                try:
                    sqlString = "DELETE FROM `table_listing` WHERE `id`=%s"
                    cur = yield db.connPool().execute(sqlString, (str(self.id),))
                    affected_rows = cur.rowcount
                    if affected_rows == 0:
                        self.make_reserror_json(400, "id not exist")
                    else:
                        self.write({
                            "status": "sucess",
                            "data": {"code": 200, "message":""}
                        })
                except Exception as e:
                    print(e)
                    self.make_internalerror()

# get user info by user id
class ListingAllHandler(BaseListingHandler):
    @gen.coroutine
    def get(self):
        try:
            sqlString = "SELECT l.`id`, u.`name`, `price`, `listing_type`,  `postal_code`, `status` FROM `table_listing` l JOIN `table_user` u ON (l.`user`=u.`id`)"
            cur = yield db.connPool().execute(sqlString)
            result = cur.fetchall()
            objectList = []
            for row in result:
                objectList.append(row)
            objects = json.dumps(objectList)
            self.write({
                "status": "sucess",
                "data": {"code": 200, "message":"", "listings": objects}
            })
        except Exception as e:
            print(e)
            self.make_internalerror()

class ListingByPostalCodeHandler(BaseListingHandler):
    @gen.coroutine
    def post(self):
        if not ("postalCodeList" in self.jsonBody) or len(self.jsonBody["postalCodeList"]) == 0:
            self.make_badrequest()
        else:
            try:
                sqlString = "SELECT `id`, `user`, `price`, `listing_type`,  `postal_code`, `status` FROM `table_listing`"
                filterString = ""
                objectList = []
                if "postalCodeList" in self.jsonBody:
                    for item in self.jsonBody["postalCodeList"]:
                        filterString += item + ","
                    filterString = filterString[:len(filterString) -1]
                    filterString = " WHERE `postal_code` in (" + filterString + ")"
                
                sqlString += filterString
                print(sqlString)

                cur = yield db.connPool().execute(sqlString)
                result = cur.fetchall()
                for row in result:
                    objectList.append(row)
                objects = json.dumps(objectList)
                self.write({
                    "status": "sucess",
                    "data": {"code": 200, "message":"", "listings": objects}
                })
            except Exception as e:
                print(e)
                self.make_internalerror()
       
