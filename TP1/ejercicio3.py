import re

def validar_mail():
  with open('TP1\mail.txt') as archivo:
      mail_data = archivo.readlines()

  for line in mail_data:
      patron_mail = '[a-zA-Z0-9-_]+@[a-zA-Z0-9]+.[a-zA-Z]{2,4}(.[a-zA-Z]{2,3})?'
      if re.search(patron_mail, line) is None:
          print("{} no es un mail.".format(line.strip()))
      else:
          print("{} es un mail.".format(line.strip()))

def validad_url():
  with open('TP1\\url.txt') as archivo:
      url_data = archivo.readlines()
    
  for line in url_data:
    patron_url = '(?:https?:\/\/)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\/|\?[a-zA-Z0-9.-=&]+)?'
    if re.search(patron_url, line) is None:
        print("{} no es un URL.".format(line.strip()))
    else:
        print("{} es un URL.".format(line.strip()))
        
def validad_ip():
  with open('TP1\IPV4.txt') as archivo:
      ip_data = archivo.readlines()
  for line in ip_data:
    patron_ip = '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    if re.search(patron_ip, line) is None:
        print("{} no es un IP.".format(line.strip()))
    else:
        print("{} es un IP.".format(line.strip()))

validar_mail()
validad_url()
validad_ip()