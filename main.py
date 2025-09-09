from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from web3 import Web3

# ⚠ শুধুমাত্র শিক্ষার জন্য! বাস্তব পরিবেশে private key কখনো প্রকাশ করবেন না
OWNER_PRIVATE_KEY = "0x7436f6c2ecb484aa0344040652a138dd94141509e5cbd836c2835db941225d79"
OWNER_ADDRESS = "0x12cf47dee831678a6468459bbbbe185022c8ae9b"
BSC_RPC_URL = "https://bsc-dataseed.binance.org/"

# BSC নেটওয়ার্কের সাথে সংযোগ স্থাপন
web3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
if not web3.is_connected():  # ✅ small 'web3' এবং is_connected()
    raise Exception("Cannot connect to BSC network.")

# অ্যাকাউন্ট বসানো
account = web3.eth.account.from_key(OWNER_PRIVATE_KEY)  # ✅ from_key ব্যবহার করুন

# FastAPI অ্যাপ তৈরি
app = FastAPI()

# Request body মডেল
class SendBNBRequest(BaseModel):
    toAddress: str

# send-bnb API endpoint
@app.post("/send-bnb")
def send_bnb(request: SendBNBRequest):
    try:
        if not web3.isAddress(request.toAddress):
            raise HTTPException(status_code=400, detail="Invalid address.")

        amount = web3.toWei(0.001, 'ether')
        nonce = web3.eth.get_transaction_count(OWNER_ADDRESS)

        tx = {
            'nonce': nonce,
            'to': request.toAddress,
            'value': amount,
            'gas': 21000,
            'gasPrice': web3.eth.gas_price,
            'chainId': 56
        }

        signed_tx = web3.eth.account.sign_transaction(tx, OWNER_PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        return {
            "status": "success",
            "message": f"Sent 0.001 BNB to {request.toAddress}",
            "txHash": web3.toHex(tx_hash)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






