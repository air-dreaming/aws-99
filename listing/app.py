# app.py - tornado main entry

import tornado.httpserver
import tornado.ioloop
import tornado.web

from api import list
# config: port definition
port = 8882

# main for testing
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello 99!")


# routes
def make_app():
    return tornado.web.Application([
        (r"/",  MainHandler),
        (r"/api/listingcreate/", list.ListingCreateHandler),
        (r"/api/listingupdate/", list.ListingUpdateHandler),
        (r"/api/listingdelete/", list.ListingDeleteHandler),
        (r"/api/listingbypostalcode/", list.ListingByPostalCodeHandler),
        (r"/api/listingpriceupdate/", list.ListingPriceUpdateHandler),
        (r"/api/listingall/", list.ListingAllHandler),
        ])

# 
def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(port)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
