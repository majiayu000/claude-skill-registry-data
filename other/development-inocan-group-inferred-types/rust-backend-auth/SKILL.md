---
name: rust-backend-auth
description: Implements authentication and authorization for Rust backend services using JWT, password hashing, sessions, and middleware patterns. Use when building auth systems, implementing login/logout, protecting routes, hashing passwords, or working with JWT tokens in Axum/Tower applications.
---

<objective>
Provides production-ready authentication patterns for Rust backend services. Covers JWT token creation/validation, secure password hashing with Argon2, and auth middleware that injects user context.
</objective>

<essential_principles>
1. **Password Storage**: Use Argon2id with random salts. Store the PHC string.
2. **Token Validation**: Always validate exp, iss, aud claims. Handle clock skew.
3. **Middleware Design**: Inject authenticated user via request extensions. Fail closed.
</essential_principles>

<patterns>
<pattern name="jwt_service">
**JWT Encoding and Decoding**

```rust
use jsonwebtoken::{encode, decode, Header, EncodingKey, DecodingKey, Validation, Algorithm};

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: String,
    exp: usize,
    iat: usize,
    iss: String,
}

pub struct JwtService {
    encoding_key: EncodingKey,
    decoding_key: DecodingKey,
    validation: Validation,
}

impl JwtService {
    pub fn new(secret: &[u8], issuer: &str) -> Self {
        let mut validation = Validation::new(Algorithm::HS256);
        validation.set_issuer(&[issuer]);
        validation.leeway = 60;

        Self {
            encoding_key: EncodingKey::from_secret(secret),
            decoding_key: DecodingKey::from_secret(secret),
            validation,
        }
    }

    pub fn create_token(&self, claims: &Claims) -> Result<String, AuthError> {
        encode(&Header::default(), claims, &self.encoding_key)
            .map_err(|_| AuthError::TokenCreation)
    }

    pub fn validate_token(&self, token: &str) -> Result<Claims, AuthError> {
        decode::<Claims>(token, &self.decoding_key, &self.validation)
            .map(|data| data.claims)
            .map_err(|err| match *err.kind() {
                ErrorKind::ExpiredSignature => AuthError::TokenExpired,
                _ => AuthError::InvalidToken,
            })
    }
}
```
</pattern>

<pattern name="password_hashing">
**Argon2 Password Hashing**

```rust
use argon2::{
    password_hash::{rand_core::OsRng, PasswordHash, PasswordHasher, PasswordVerifier, SaltString},
    Argon2,
};

fn hash_password(password: &str) -> Result<String, argon2::password_hash::Error> {
    let salt = SaltString::generate(&mut OsRng);
    let argon2 = Argon2::default();
    Ok(argon2.hash_password(password.as_bytes(), &salt)?.to_string())
}

fn verify_password(password: &str, hash: &str) -> bool {
    let parsed_hash = match PasswordHash::new(hash) {
        Ok(h) => h,
        Err(_) => return false,
    };
    Argon2::default().verify_password(password.as_bytes(), &parsed_hash).is_ok()
}
```
</pattern>

<pattern name="auth_middleware">
**Auth Middleware**

```rust
pub async fn auth_middleware(
    Extension(jwt_service): Extension<Arc<JwtService>>,
    mut req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let auth_header = req.headers()
        .get(header::AUTHORIZATION)
        .and_then(|h| h.to_str().ok())
        .and_then(|h| h.strip_prefix("Bearer "));

    let token = auth_header.ok_or(StatusCode::UNAUTHORIZED)?;
    let claims = jwt_service.validate_token(token).map_err(|_| StatusCode::UNAUTHORIZED)?;

    req.extensions_mut().insert(AuthenticatedUser::from(claims));
    Ok(next.run(req).await)
}
```
</pattern>
</patterns>

<security_checklist>
- [ ] Secrets from environment variables, never hardcoded
- [ ] Algorithm explicitly specified in Validation
- [ ] exp, iss, aud validated on every decode
- [ ] Argon2id for password hashing
- [ ] Generic error messages ("Invalid credentials")
- [ ] Rate limiting on auth endpoints
</security_checklist>

<success_criteria>
- [ ] Passwords hashed with Argon2id
- [ ] JWT tokens include sub, exp, iat, iss claims
- [ ] Auth middleware injects user into extensions
- [ ] Protected routes return 401 without valid token
- [ ] All secrets from environment variables
</success_criteria>
