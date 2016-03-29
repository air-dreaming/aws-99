Preparation:

1. install python 2.7
2. install tornado
3. install Tornado_MySQL

[database config]
config database in file db/db.conf

Run:
[cmd - user service]: python /path/app.py --port=8881
[cmd - listing servie]: python /path/listing/app.py --port=8882

Deployment:
AWS: [user service ip]: 54.238.162.121
     [user serive port]: 8881
     [listing service ip]: 54.238.188.204
     [listing service port]: 8882

self deployment need change the user service ip to correct user service ip in line 94 of list.py

 
user rest api:

1. user create
    [url]: http://domain:port/api/usercreate/
    [json]: {"name":"string", "address":"string"}
    [result]: {"status": "success", "data": {"code": 200, "user": {"address": "address", "id": 18, "name": "name"}}}
    [cmd]: curl -H "Content-Type: application/json" -X POST -d '{"name":"name","address":"address"}' http://domain:port/api/usercreate/

 2. user info by id or by name
    [url]: http://domain:port/api/userinfo/
    [json]: {"id":id} / {"name":"name"}
    [result]: {"status": "success", "data": {"code": 200, "message":""}
    [cmd]: curl -H "Content-Type: application/json" -X POST -d '{"id":20}' http://domain:port/api/userinfo/

3. update user info by id
    [url]: http://domain:port/api/userupdate/
    [json]: {"id":id, "address":"string"}
    [result]: {"status": "success", "data": {"code": 200, "message":""}
    [cmd]: curl -H "Content-Type: application/json" -X POST -d '{"id":20, "address":"string"}' http://domain:port/api/userupdate/


4. delete user by id
    [url]: http://domain:port/api/userdelete/
    [json]: {"id":id}
    [result]: {"status": "success", "data": {"code": 200, "message":""}
    [cmd]: curl -H "Content-Type: application/json" -X POST -d '{"id":20}' http://domain:port/api/userdelete/


listing rest api:

1. listing create
    [url]: http://domain:port/api/listcreate/
    [json]: {"user": 1, "price": 110, "listingType": 2, "postalCode": "123456", "status": 1}
    [result]: {"status": "success", "data": {"code": 200, "listing": {"status": 1, "listingType": 2, "price": "110.0", "user": 1, "postalCode": "123456", "id": 14}}}
    [cmd]: curl -H "Content-Type: application/json" -X POST -d '[json]' [url]

2. delete listing
    [url]: http://domain:port/api/listingdelete/
    [json]: {"id":14}
    [result]: {"status": "success", "data": {"code": 200, "message":""}
    [cmd]: curl -H "Content-Type: application/json" -X POST -d '[json]' [url]

3. listing by index postalcode
    [url]: http://domain:port/api/listingpriceupdate/
    [json]: {"postalCode":""}
    [result]: {"status": "success", "data": {"code": 200, listings":[{},{}]}
    [cmd]: curl -H "Content-Type: application/json" -X POST -d '[json]' [url]

2. listing price update
    [url]: http://domain:port/api/listingpriceupdate/
    [json]: {"id":14, "user": 1, "price": 1100}
    [result]: {"status": "success", "data": {"code": 200, "message":""}
    [cmd]: curl -H "Content-Type: application/json" -X POST -d '[json]' [url]

4. listing all
    [url]: http://domain:port/api/listingall/
    [result]: {"status": "success", "data": {"code": 200, "listings":[{},{}]}
    [cmd]: curl [url]
