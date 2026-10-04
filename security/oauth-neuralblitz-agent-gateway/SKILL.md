---
name: oauth
description: OAuth 2.0 and OpenID Connect implementation
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: security
---
## What I do
- Implement OAuth 2.0 flows
- Handle OpenID Connect authentication
- Manage tokens securely
- Implement authorization grants
- Handle refresh tokens
- Validate tokens
- Implement PKCE for mobile/SPA
- Secure OAuth implementations

## When to use me
When implementing OAuth authentication or authorization.

## OAuth 2.0 Flows
```
OAuth 2.0 Grant Types:

1. Authorization Code (Web Apps)
   Client → Auth Server → User Login → Auth Code → 
   Client → Token Exchange → Access Token

2. Authorization Code + PKCE (Mobile/SPA)
   Same as above, but with code_verifier

3. Client Credentials (M2M)
   Client → Token Exchange → Access Token

4. Device Code (IoT, Smart TVs)
   Device Code Flow → User authorization on second device

5. Refresh Token
   Client → Token Refresh → New Access Token
```

## OAuth Implementation
```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta
import secrets
import hashlib


@dataclass
class OAuthConfig:
    """OAuth configuration."""
    client_id: str
    client_secret: str
    authorization_endpoint: str
    token_endpoint: str
    redirect_uri: str
    scopes: list[str]
    access_token_ttl: int = 3600  # 1 hour
    refresh_token_ttl: int = 2592000  # 30 days


class OAuthClient:
    """OAuth 2.0 client implementation."""
    
    def __init__(self, config: OAuthConfig):
        self.config = config
        self.code_store = {}  # In production, use Redis
        self.token_store = {}
    
    def generate_authorization_code(self, state: str, redirect_uri: str):
        """Generate authorization code for auth code flow."""
        code = secrets.token_urlsafe(32)
        
        self.code_store[code] = {
            'state': state,
            'redirect_uri': redirect_uri,
            'scopes': self.config.scopes,
            'created_at': datetime.utcnow(),
            'expires_in': 600,  # 10 minutes
        }
        
        return code
    
    def validate_authorization_code(
        self,
        code: str,
        redirect_uri: str
    ) -> Optional[dict]:
        """Validate and consume authorization code."""
        if code not in self.code_store:
            return None
        
        code_data = self.code_store[code]
        
        # Check expiration
        elapsed = (datetime.utcnow() - code_data['created_at']).total_seconds()
        if elapsed > code_data['expires_in']:
            del self.code_store[code]
            return None
        
        # Validate redirect URI
        if code_data['redirect_uri'] != redirect_uri:
            return None
        
        # Consume code
        del self.code_store[code]
        
        return code_data
    
    def exchange_code_for_tokens(
        self,
        code: str,
        redirect_uri: str,
        client_id: str = None,
        client_secret: str = None,
        code_verifier: str = None
    ) -> dict:
        """Exchange authorization code for tokens."""
        # Validate client
        if client_id != self.config.client_id:
            raise OAuthError("invalid_client", "Invalid client ID")
        
        # Validate client secret (if required)
        if client_secret and not self._validate_client_secret(client_secret):
            raise OAuthError("invalid_client", "Invalid client secret")
        
        # Validate code
        code_data = self.validate_authorization_code(code, redirect_uri)
        if not code_data:
            raise OAuthError("invalid_grant", "Invalid or expired code")
        
        # Validate PKCE if provided
        if code_verifier and not self._validate_pkce(code, code_verifier):
            raise OAuthError("invalid_grant", "PKCE validation failed")
        
        # Generate tokens
        access_token = self._generate_access_token()
        refresh_token = self._generate_refresh_token()
        
        # Store tokens
        self.token_store[access_token] = {
            'scopes': code_data['scopes'],
            'created_at': datetime.utcnow(),
            'expires_in': self.config.access_token_ttl,
        }
        
        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': self.config.access_token_ttl,
            'refresh_token': refresh_token,
            'scope': ' '.join(code_data['scopes']),
        }
    
    def refresh_access_token(
        self,
        refresh_token: str,
        scopes: list[str] = None
    ) -> dict:
        """Refresh access token using refresh token."""
        if refresh_token not in self.token_store:
            raise OAuthError("invalid_grant", "Invalid refresh token")
        
        token_data = self.token_store[refresh_token]
        
        # Check expiration
        elapsed = (datetime.utcnow() - token_data['created_at']).total_seconds()
        if elapsed > self.config.refresh_token_ttl:
            del self.token_store[refresh_token]
            raise OAuthError("invalid_grant", "Refresh token expired")
        
        # Validate scopes (can't request more than original)
        requested_scopes = scopes or token_data['scopes']
        for scope in requested_scopes:
            if scope not in token_data['scopes']:
                raise OAuthError("invalid_scope", "Requested scope not allowed")
        
        # Generate new tokens
        access_token = self._generate_access_token()
        new_refresh_token = self._generate_refresh_token()
        
        # Invalidate old refresh token
        del self.token_store[refresh_token]
        
        # Store new tokens
        self.token_store[access_token] = {
            'scopes': requested_scopes,
            'created_at': datetime.utcnow(),
            'expires_in': self.config.access_token_ttl,
        }
        
        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': self.config.access_token_ttl,
            'refresh_token': new_refresh_token,
            'scope': ' '.join(requested_scopes),
        }
    
    def validate_access_token(self, token: str) -> Optional[dict]:
        """Validate access token and return claims."""
        if token not in self.token_store:
            return None
        
        token_data = self.token_store[token]
        
        elapsed = (datetime.utcnow() - token_data['created_at']).total_seconds()
        if elapsed > token_data['expires_in']:
            del self.token_store[token]
            return None
        
        return token_data
    
    def _generate_access_token(self) -> str:
        """Generate secure access token."""
        return secrets.token_urlsafe(32)
    
    def _generate_refresh_token(self) -> str:
        """Generate secure refresh token."""
        return secrets.token_urlsafe(32)
    
    def _validate_client_secret(self, secret: str) -> bool:
        """Validate client secret."""
        return secrets.compare_digest(secret, self.config.client_secret)
    
    def _validate_pkce(self, code_challenge: str, code_verifier: str) -> bool:
        """Validate PKCE code verifier against challenge."""
        # In production, store code_challenge with code
        return True


class OAuthError(Exception):
    """OAuth error."""
    
    def __init__(self, error: str, error_description: str):
        self.error = error
        self.error_description = error_description
        super().__init__(f"{error}: {error_description}")
```

## PKCE Implementation
```python
import base64
import hashlib
import secrets


class PKCE:
    """PKCE helper for OAuth 2.0."""
    
    @staticmethod
    def generate_code_verifier(length: int = 43) -> str:
        """
        Generate cryptographically secure code verifier.
        
        Must be 43-128 characters, using [A-Z], [a-z], [0-9], "-", ".", "_", "~"
        """
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~'
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def generate_code_challenge(code_verifier: str) -> str:
        """
        Generate code challenge from code verifier.
        
        Uses S256 method: BASE64URL(SHA256(code_verifier))
        """
        sha256_hash = hashlib.sha256(code_verifier.encode('ascii')).digest()
        return base64.urlsafe_b64encode(sha256_hash).decode('ascii').rstrip('=')
    
    @staticmethod
    def generate_pair() -> tuple[str, str]:
        """Generate code verifier and challenge pair."""
        code_verifier = PKCE.generate_code_verifier()
        code_challenge = PKCE.generate_code_challenge(code_verifier)
        return code_verifier, code_challenge
    
    @staticmethod
    def validate_code_verifier(code_verifier: str, code_challenge: str) -> bool:
        """Verify code verifier matches challenge."""
        expected_challenge = PKCE.generate_code_challenge(code_verifier)
        return secrets.compare_digest(expected_challenge, code_challenge)


# Usage for authorization code flow with PKCE
def authorization_code_flow_with_pkce():
    # Client generates code verifier and challenge
    code_verifier, code_challenge = PKCE.generate_pair()
    
    # Store code_verifier securely (session, not localStorage)
    store_code_verifier(code_verifier)
    
    # Redirect user to authorization endpoint
    auth_url = (
        f"{auth_server}/authorize?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"scope={scopes}&"
        f"state={generate_state()}&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256"
    )
    
    # After user authorizes, receive code
    # Exchange code for tokens with code_verifier
    tokens = client.exchange_code_for_tokens(
        code=authorization_code,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier
    )
```

## Token Validation
```python
from jwt import jwt, JWTError
from jwt.algorithms import RSAAlgorithm


class TokenValidator:
    """Validate OAuth and JWT tokens."""
    
    def __init__(self, jwks_uri: str):
        self.jwks_uri = jwks_uri
        self.jwks_cache = {}
    
    def validate_token(self, token: str, audience: str) -> dict:
        """Validate JWT token."""
        try:
            # Get signing key
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get('kid')
            
            key = self._get_signing_key(kid)
            
            # Decode and validate
            claims = jwt.decode(
                token,
                key,
                algorithms=['RS256'],
                audience=audience,
                options={
                    'verify_exp': True,
                    'verify_aud': True,
                    'verify_iat': True,
                }
            )
            
            return claims
        
        except jwt.ExpiredSignatureError:
            raise TokenValidationError("Token has expired")
        except jwt.InvalidAudienceError:
            raise TokenValidationError("Invalid audience")
        except JWTError as e:
            raise TokenValidationError(f"Token validation failed: {e}")
    
    def _get_signing_key(self, kid: str) -> str:
        """Get signing key from JWKS."""
        if kid in self.jwks_cache:
            return self.jwks_cache[kid]
        
        # Fetch JWKS
        jwks = requests.get(self.jwks_uri).json()
        
        for key_data in jwks.get('keys', []):
            if key_data.get('kid') == kid:
                key = RSAAlgorithm.from_jwk(key_data)
                self.jwks_cache[kid] = key
                return key
        
        raise TokenValidationError(f"Key not found: {kid}")
```

## Best Practices
```
1. Use PKCE for all flows
   Required for mobile and SPA
   Recommended for all

2. Use short-lived access tokens
   Combine with refresh tokens

3. Validate everything
   Client ID, redirect URI, scopes, audience

4. Secure token storage
   Access tokens: memory or secure cookie
   Refresh tokens: server-side storage

5. Use state parameter
   Prevent CSRF attacks

6. Implement token binding
   Bind tokens to client

7. Log and monitor
   Track token usage

8. Rotate keys regularly
   Use JWKS for key rotation

9. Don't leak tokens in URLs
   Use POST body, not query params

10. Implement token revocation
    Support token revocation endpoint
```
