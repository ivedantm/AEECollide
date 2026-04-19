import os
import time
import requests
from threading import Lock
from dotenv import load_dotenv

load_dotenv()

class ErcotAuth:
    """
    Handles OAuth2 Bearer token acquisition for the ERCOT MIS API.
    Uses the ROPC flow as per ERCOT Public API documentation.
    """
    _instance = None
    _lock = Lock()

    def __init__(self):
        self.username = os.getenv("ERCOT_USERNAME")
        self.password = os.getenv("ERCOT_PASSWORD")
        self.subscription_key = os.getenv("ERCOT_SUBSCRIPTION_KEY")
        
        self.token = None
        self.expiry = 0
        
        # ERCOT B2C OAuth2 Endpoint
        self.token_url = "https://ercotb2c.b2clogin.com/ercotb2c.onmicrosoft.com/B2C_1_PUBAPI-ROPC-FLOW/oauth2/v2.0/token"
        self.client_id = "77c73229-3a3d-4956-a36c-2f3b79ce459d" # Public API Client ID
        self.scope = f"https://ercotb2c.onmicrosoft.com/pubapi/API.Read openid offline_access"

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance

    def get_token(self):
        """Returns a valid Bearer token, refreshing if necessary."""
        if self.token and time.time() < self.expiry - 60:
            return self.token
        
        with self._lock:
            # Check again inside lock
            if self.token and time.time() < self.expiry - 60:
                return self.token
            
            return self._refresh_token()

    def _refresh_token(self):
        if not self.username or not self.password:
            print("⚠️ ERCOT_USERNAME or ERCOT_PASSWORD missing. Cannot fetch token.")
            return None

        print(f"📡 Requesting new ERCOT Bearer token for {self.username}...")
        
        payload = {
            "grant_type": "password",
            "client_id": self.client_id,
            "scope": self.scope,
            "username": self.username,
            "password": self.password,
            "response_type": "token id_token"
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.post(self.token_url, data=payload, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            self.token = data.get("access_token")
            # Set expiry to now + expires_in (usually 3600s)
            self.expiry = time.time() + int(data.get("expires_in", 3600))
            
            print("✅ ERCOT Token acquired successfully.")
            return self.token
        except Exception as e:
            print(f"❌ Failed to fetch ERCOT token: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"   Response: {e.response.text}")
            return None

    def get_auth_headers(self):
        """Returns headers including Subscription Key and Bearer Token."""
        token = self.get_token()
        if not token:
            # Fallback to just subscription key if OAuth fails (might work for some public reports)
            return {
                "Ocp-Apim-Subscription-Key": self.subscription_key
            }
        
        return {
            "Authorization": f"Bearer {token}",
            "Ocp-Apim-Subscription-Key": self.subscription_key
        }

# Singleton instance
ercot_auth = ErcotAuth.get_instance()
