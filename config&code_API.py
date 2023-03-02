import requests

def invoke_my_function(url):
    response = requests.get(url)
    print(response.status_code)

def main():
    
    url = "https://m7bhhfooo3.execute-api.us-east-1.amazonaws.com/my-function"
    print("HTTP GET Response:")
    print(invoke_my_function(url))

if __name__ == '__main__':
    main()
