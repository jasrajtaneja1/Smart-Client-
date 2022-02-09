

import socket, ssl, re, time, os, sys, select, threading, argparse
from urllib.parse import urlparse



def main():
   #checking if valid arguments given
   argument_length = len(sys.argv)
   if(argument_length != 2):
      print("invalid entry")
      sys.exit()


   #parsing url from user 
   url = sys.argv[1]
   print("website: ", url)

   
   
   #checking if url supports http2
   new_location_string = ""
   http2_boolean = False
   context = ssl.create_default_context()
   context.set_alpn_protocols(['h2'])
   conn = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=url)

   try:
      conn.connect((url,443))
   except socket.error:
      print("socket error 0")
      

   string_ifhttp2 = conn.selected_alpn_protocol()

   if string_ifhttp2 == "h2":
       http2_boolean =  True

       

   if http2_boolean == False:
       print("1. Supports http2: no")
   if http2_boolean == True:
       print("1. Supports http2: yes")

   result_new = ""
    #creating a socket and connecting to the url 

   #creating a socket for the first request, and sending a request, getting redirect location of request
   try:
      s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((url, 80))
      request = "GET / HTTP/1.1\r\nHost: "+ url + "\r\n\r\n"
      s.sendall(request.encode())
      result = s.recv(10000)
      result_new = result.decode()
      #print(result_new)

      match = re.search(r"Location: (.*)", result_new)
      new_location_string = urlparse(match.group(1))
      new_location1 = new_location_string.netloc
      path1 = new_location_string.path

      match = re.search(r"Location: (.*)", result_new)
      new_location_string = urlparse(match.group(1))
      new_location1 = new_location_string.netloc
      path1 = new_location_string.path
      
   except socket.error:
      print("socket error1")
   
   
  
  #getting port for the first request 
   if(new_location_string):
      if("https") in new_location_string:
         new_port = 443
         
   else:
      new_port = 80
         
   #print(new_port)
   
  

   
  
   num_redirects = 5
   final_result = ""
   i = 0

   
   #checking if url contains a path, if so , getting path
   path1 = ""
   password_protected = False
   starting_path = ""
   if '/' in url:
      match5 = re.search(".*?(/.*)",url)
      starting_path = match5.group(1)
      #print(starting_path)
   

   #loop for redirects
   while(i<5):

      i = i+1
         
      if new_port == 443:
         try:
            s1 =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s1 = ssl.wrap_socket(s1)   

         except socket.error:
            print("socket error3")

      if new_port == 80:
         try:
            s1 =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s1 = ssl.wrap_socket(s1)   
         except socket.error:
            print("socket error3")
      try:
         host_ip = socket.gethostbyname(url)

      except socket.gaierror:
         print("socket error")

      try:
         s1.connect((host_ip, new_port))

      except socket.gaierror:
         print("socket error")

      location1 = new_location1

      if starting_path == "":
         request1 = "GET / HTTP/1.1\r\nHost: "+ location1 + "\r\n\r\n"
      else:
         request1 = "GET " + starting_path + "HTTP/1.1\r\nHost: "+ location1 + "\r\n\r\n"


         
      s1.sendall(request1.encode())
      result1 = s1.recv(10000)
      result_new1 = result1.decode()

      match1 = re.search(r"Location: (.*?)",result_new1)
    
            
      new_location_string = urlparse(match.group(1))
      new_location1 = new_location_string.netloc
      starting_path = new_location_string.path
      

      if(  ("200" ) in result_new1 ):
         final_result = result_new1
         break

      if(  ("401" ) in result_new1 ):
         final_result = result_new1
         password_protected = True

         break
      
         

      s1.close()

   #print(final_result)
   



   #get the cookies
   cookie = []
   
   
   lines = final_result.split('\n')
   for line in lines:
      if 'Set-Cookie:' in line:
         cookie.append(line)
   #print(cookie)



   if cookie:
      print("2. List of Cookies: ")

      domain_name = ""
      expiry = ""
      Domain_name = ""
      Expiry = ""

   for each_cookie in cookie:
      
      match = re.search("Set-Cookie:(.*?)=", each_cookie)
      name = match.group(1)
      
      if 'expires' in each_cookie:
         match1 = re.search("expires=(.*?);",each_cookie)
         expiry = match1.group(1)
      else: 

         expiry = ""

      if 'Expires' in each_cookie:
         match1 = re.search("Expires=(.*?);",each_cookie)
         Expiry = match1.group(1)
      else: 
         Expiry = ""
        
      
      
      if 'domain=' in each_cookie:
         match2 = re.search("domain=(.*?);", each_cookie)
         domain_name = match2.group(1)
      else:
         domain_name = ""
       
      if 'Domain=' in each_cookie:
         match3 = re.search("Domain=(.*?);", each_cookie)
         Domain_name = match3.group(1)
      else:
         Domain_name = ""
      
      if domain_name:
         string_domain = "domain name: " + domain_name
      else:
         string_domain = ""
      if Domain_name:
         string_Domain = "domain name: " + Domain_name
      else: 
         string_Domain = ""
      if expiry:
         string_expiry = "expires time: " + expiry + ";"
      else: 
         string_expiry = ""
      if Expiry:
         string_Expiry = "expires time: " + Expiry + ";"
      else: 
         string_Expiry = ""
   
      print("cookie name:" + name + ",", string_expiry, string_Expiry, string_domain , string_Domain)
   if password_protected == True:
      print("3. Password-protected: yes")
   if password_protected == False:
      print("3. Password-protected: no")
   
      

      
      
         
if __name__ == "__main__":

   main()
