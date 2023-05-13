

import smtplib
smtp_server = 'smtp.qq.com'
smtp_port = 465
smtp_username = '1057857414@qq.com'
smtp_password = 'vyaetryyodzhbcgf'

try:
    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(smtp_username, smtp_password)
    print("SMTP connection successful")
except Exception as e:
    print("SMTP connection failed:", e)


