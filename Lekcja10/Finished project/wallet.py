import time
import ecdsa
import base64
import requests
from msvcrt import getch


def wallet():
    response = None
    while response not in ["1", "2", "3"]:
        response = input("""What do you want to do?
        1. Generate new wallet
        2. Send coins to another wallet
        3. Check transactions\n""")
    if response == "1":
        # Generate new wallet
        print("""=========================================\n
IMPORTANT: save this credentials or you won't be able to recover your wallet\n
=========================================\n""")
        generate_ecdsa_keys()
    elif response == "2":
        print("=========================================\n")
        addr_from = input("From: introduce your wallet address (public key)\n")
        private_key = input("Introduce your private key\n")
        addr_to = input("To: introduce destination wallet address\n")
        amount = input("Amount: number stating how much do you want to send\n")
        print("=========================================\n\n")
        print("Is everything correct?\n")
        print("From: {0}\nPrivate Key: {1}\nTo: {2}\nAmount: {3}\n".format(addr_from, private_key, addr_to, amount))
        response = input("y/n\n")
        if response.lower() == "y":
            send_transaction(addr_from, private_key, addr_to, amount)
    else:  # Will always occur when response == 3.
        check_transactions()


def send_transaction(addr_from, private_key, addr_to, amount):

    # Example
    # private_key="2bbab56c794a8da47c66f2897a9effaae78719f9053f6afafd4a344b86d33410"
    # amount="500"
	# addr_from="Qsmj8Qglv2Nrl56Nn9OG5IRhXMloT8zQMBfyMs46J++FNSyhPTjfZBUfS80XReG8TflM4XD0dmvFWH/PuBVOCA=="
	# addr_to="Qsmj8Qglv2Nrl56Nn9OG5IRhXMloT8zQMBfyMs46J++FNSyhPTjfZBUfS80XReG8TflM4XD0dmvFWH/PuBVOCA=="


    if len(private_key) == 64:
        signature, message = sign_ecdsa_msg(private_key)
        url = 'http://localhost:5000/txion'
        payload = {"from": addr_from,
                   "to": addr_to,
                   "amount": amount,
                   "signature": signature.decode(),
                   "message": message}
        headers = {"Content-Type": "application/json"}

        res = requests.post(url, json=payload, headers=headers)
        print(res.text)
    else:
        print("Wrong address or key length! Verify and try again.")




def check_transactions():
    res = requests.get('http://localhost:5000/blocks')
    print(res.text)


def generate_ecdsa_keys():
    sign_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
    private_key = sign_key.to_string().hex()
    verif_key = sign_key.get_verifying_key()
    public_key = verif_key.to_string().hex()
    public_key = base64.b64encode(bytes.fromhex(public_key))

    filename = input(str("Write the name of your new address: ")) + ".txt"
    with open(filename, "w") as f:
        f.write("""=========================================
=========================================
Private key
{0}
=========================================
Wallet address | Public key
{1}
=========================================
=========================================\n""".format(private_key, public_key.decode()))

    print("Your new address and private key are now in the file {0}".format(filename))



def sign_ecdsa_msg(private_key):
    # Get timestamp, round it, make it into a string and encode it to bytes
    message = str(round(time.time()))
    bmessage = message.encode()
    sign_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
    signature = base64.b64encode(sign_key.sign(bmessage))
    return signature, message


if __name__ == '__main__':
    print("""       =========================================\n
                     BLOCKCHAIN SYSTEM\n
       =========================================\n\n\n""")

    while True:
        print("Press ENTER to continue...")
        key = ord(getch())
        if key == 27:  # ESC
            break
        elif key == 13:  # Enter
            wallet()
