import requests
import json
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

winnerCount = 0

def saveWallet(wallet):
    with open(__location__+"/winners.txt", "a") as f:
        f.write(wallet+"\n")
        print("Saved wallet: "+str(wallet))
        f.close()

def checkWallet(wallet):
    global winnerCount
    response = requests.get("https://api.maximalists.io/eligible/"+str(wallet))
    if response.status_code == 200:
        responseJson = json.loads(response.content)
        whiteListStatus = responseJson['whitelisted']
        if whiteListStatus == True:
            winnerCount += 1
            print("Found whitelisted Wallet: "+str(wallet))
            saveWallet(wallet)
        else:
            pass
    elif response.status_code == 400:
        pass
    else:
        print("Error checking wallet: "+str(response.status_code))

with open(__location__+"/wallets.txt", "r") as f:
    walletLines = f.readlines()
    walletCount = len(walletLines)
    print("Checking "+str(walletCount)+" wallets..")
    for wallet in walletLines:
        wallet = wallet.strip("\n")
        try:
            checkWallet(str(wallet))
        except Exception as e:
            print("Error checking wallet: "+str(e))
    print(str(winnerCount)+"/"+str(walletCount)+" Wallets Whitelisted.")