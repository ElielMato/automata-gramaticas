import re



def validad_mail():
  with open('mail.txt') as archivo:
      mail_data = archivo.readlines()

  for line in mail_data:
      patron_mail = '[a-zA-Z0-9-_]+@[a-zA-Z0-9]+.[a-zA-Z]{2,4}(.[a-zA-Z]{2,3})?'
      if re.search(patron_mail, line) is None:
          return line + " no es un mail."
      else:
          return line + " es un mail."

def validad_url(url):
  patron_url =  '(?:https?:\/\/)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\/|\?[a-zA-Z0-9.-=&]+)?'
  return re.search(patron_url, url)

def validad_ip(ip):
  patron_ip = '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
  return re.search(patron_ip, ip)

print(validad_mail())

# for line in text_data:
#   if re.search(mail, line) is None:
#     print(line + " no es un mail.")
#   else:
#     print(line + " es un mail.")

#   if re.search(url, line) is None:
#     print(line + " no es un URL.")
#   else:
#     print(line + " es un URL.")

#   if re.search(ip, line) is None:
#     print(line + " no es un IP.")
#   else:
#     print(line + " es un IP.")

    
