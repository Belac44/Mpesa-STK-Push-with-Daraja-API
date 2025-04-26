import requests
import base64
import os
from datetime import datetime

class MpesaSTK:

    def __init__(self):
        """
        
        Make sure to set the following environment variable in an .env file or in your environment
        or directly in the code before running the script i.e
        self.consumer_key = "your_consumer_key"
        self.consumer_secret = "your_consumer_secret" etc.

        """
        self.consumer_key = os.getenv("MPESA_CONSUMER_KEY") 
        self.consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
        self.passkey = os.getenv("MPESA_PASSKEY")
        self.shortcode = 174379 # Replace with your shortcode
 

    def get_mpesa_access_token(self):
        api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials' # Replace with production URL for live environment
        base64_encoded_string = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode('utf-8'))
        auth_token = f"Basic {base64_encoded_string.decode('utf-8')}"
        response = requests.request("GET", api_URL, headers={'Authorization': auth_token})
        return response.json().get('access_token')


    def stk_push(self, phone_number=None, amount="1",  account_reference=None, transaction_description=None):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        encode_data = f"{self.shortcode}{self.passkey}{timestamp}"
        password = base64.b64encode(encode_data.encode('utf-8')).decode('utf-8')
        access_token = self.get_mpesa_access_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" # Replace with production URL for live environment
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp, 
            "TransactionType": "CustomerPayBillOnline",
            "Amount":  amount,
            "PartyA": phone_number,
            "PartyB":self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://mydomain.com/path", 
            "AccountReference": account_reference,
            "TransactionDesc": transaction_description
        }
        response = requests.post(api_url, json=payload, headers=headers)
        
        
        return response.json()


if __name__ == "__main__":

    mpesa = MpesaSTK()
    # Example usage
    # Make sure to replace the phone number with a valid one in the format "2547XXXXXXXX"

    response = mpesa.stk_push(phone_number="", amount="1", payment_id="123456", account_reference="Test123", transaction_description="Payment for goods")

    print("STK Push Response:", response)