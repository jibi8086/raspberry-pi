import smtplib
try:
	fromaddr = 'smarthealth911@gmail.com'
	toaddrs  = 'jibin8086@gmail.com'
	msg = 'raspberry pi test mail'
	username = 'smarthealth911@gmail.com'
	password = 'smartadmin'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()
except:
   print("sending faild")
