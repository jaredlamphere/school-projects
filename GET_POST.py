import requests
import json
import pprint
### GET function###
def invoke_http_get(url):
    response = requests.get(url)
    print(response.status_code)
    if not response.ok:
        ##Raises that an error occured#
    
     obj = response.json()
    ##test if it is in a list as well as an object##
    if isinstance(obj, list):
        for res in obj:
            print(res['userId'])
            print(res['id'])
            print(res['title'])
            print(res['body'])
##POST Function###


##main function##
def main():
    url = "https://m7bhhfooo3.execute-api.us-east-1.amazonaws.com/my-function"
    print("HTTP GET Response:")
    print(invoke_http_get(url))

##make sure main is only used as a script##
if __name__ == '__main__':
    main()
