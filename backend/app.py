from flask import Flask, request, jsonify
from web3 import Web3
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider(os.getenv('GANACHE_RPC_URL', 'http://127.0.0.1:7545')))

# Load contract ABI and address
with open('contracts/ComplaintPlatform.json') as f:
    contract_data = json.load(f)

if 'networks' not in contract_data or '5777' not in contract_data['networks']:
    raise ValueError("Contract address for Ganache network not found.")

contract_address = contract_data['networks']['5777']['address']  # Ganache network ID
abi = contract_data['abi']

contract = w3.eth.contract(address=contract_address, abi=abi)

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    encrypted_data = request.json.get('encrypted_data')
    account = w3.eth.accounts[0]  # Use the first account from Ganache

    try:
        tx_hash = contract.functions.submitComplaint(encrypted_data).transact({'from': account})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({"status": "Complaint submitted successfully!", "transaction_hash": tx_hash.hex()})
    except Exception as e:
        return jsonify({"status": "Error submitting complaint", "error": str(e)}), 400

@app.route('/get_complaint/<int:complaint_id>', methods=['GET'])
def get_complaint(complaint_id):
    try:
        encrypted_data, status = contract.functions.getComplaint(complaint_id).call()
        return jsonify({
            "encrypted_data": encrypted_data,
            "status": status
        })
    except Exception as e:
        return jsonify({"status": "Error retrieving complaint", "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
