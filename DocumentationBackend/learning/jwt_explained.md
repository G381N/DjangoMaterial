# 🔐 JWT Authentication — Fully Explained

> **Back to:** [Learning Index](../learning_django.md) · [Main README](../../README.md)

---

## What is JWT?

**JWT** (JSON Web Token) is a way to prove **"I am logged in"** without the server storing any session data. Instead of sessions (like cookies), the server gives the client a **signed token** that the client sends with every request.

**Key idea:** The server doesn't remember who's logged in. The token itself contains the proof.

---

## Structure of a JWT

Every JWT has **3 parts**, separated by dots:

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjgifQ.sKm3X9z...
│                      │                          │
│       HEADER         │        PAYLOAD            │   SIGNATURE
```

| Part | Contains | Example |
|------|----------|---------|
| **Header** | Algorithm + token type | `{"alg": "HS256", "typ": "JWT"}` |
| **Payload** | User data (claims) | `{"user_id": "68abc...", "exp": 1707000000}` |
| **Signature** | Proof the token wasn't tampered with | `HMAC-SHA256(header + payload, SECRET_KEY)` |

The **signature** is the security layer — only the server knows the `SECRET_KEY`, so only the server can create valid tokens. If anyone changes the payload, the signature won't match and the token is rejected.

---

## Two Types of Tokens

Our project uses **two tokens** that work together:

### Access Token (short-lived: 30 minutes)

```
Purpose: Proves "I am logged in" on every API request
Lifetime: 30 minutes (from settings.py: ACCESS_TOKEN_LIFETIME)
Sent as:  Authorization: Bearer <access_token>
```

This is the token you send with **every protected API call** (get projects, create tasks, etc.). It expires quickly so that even if it's stolen, the damage window is small.

### Refresh Token (long-lived: 7 days)

```
Purpose: Gets you a NEW access token when the old one expires
Lifetime: 7 days (from settings.py: REFRESH_TOKEN_LIFETIME)
Sent to:  POST /api/auth/token/refresh/
```

This token is stored securely on the client side. When the access token expires, the frontend uses the refresh token to get a **new access token** without requiring the user to log in again.

### Why Two Tokens?

```
Without refresh tokens:
  Access token expires → User must log in again every 30 minutes 😠

With refresh tokens:
  Access token expires → Frontend silently gets a new one → User stays logged in for 7 days 😊
```

| Token | Lifetime | Risk if stolen | Sent with every request? |
|-------|----------|---------------|------------------------|
| Access | 30 min | Attacker has 30 min access | ✅ Yes |
| Refresh | 7 days | Attacker can generate new access tokens | ❌ Only to `/token/refresh/` |

This is why the access token is short-lived — it limits the damage if intercepted.

---

## The Complete JWT Lifecycle

Here's the **full flow** from register to token expiry to refresh:

```
┌─────────────┐                                    ┌──────────────┐
│   Frontend   │                                    │   Backend     │
└──────┬──────┘                                    └──────┬───────┘
       │                                                   │
  ① REGISTER or LOGIN                                     │
       │  POST /api/auth/register/                         │
       │  {"username", "email", "password"}  ──────────▶   │
       │                                                   │
       │    ◀──────────────────────────────────────────────│
       │  {user, access: "eyJ...", refresh: "eyJ..."}      │
       │                                                   │
  ② STORE TOKENS                                          │
       │  localStorage.setItem("access", token)            │
       │  localStorage.setItem("refresh", token)           │
       │                                                   │
  ③ MAKE API CALLS (access token valid)                   │
       │  GET /api/projects/                               │
       │  Authorization: Bearer <access_token>  ──────▶    │
       │                                                   │
       │    ◀──────────────────────────────────────────────│
       │  {results: [...projects]}                         │
       │                                                   │
  ④ ACCESS TOKEN EXPIRES (after 30 min)                   │
       │  GET /api/projects/                               │
       │  Authorization: Bearer <expired_token>  ──────▶   │
       │                                                   │
       │    ◀──────────────────────────────────────────────│
       │  401 Unauthorized                                 │
       │                                                   │
  ⑤ REFRESH THE TOKEN                                     │
       │  POST /api/auth/token/refresh/                    │
       │  {"refresh": "<refresh_token>"}  ──────────────▶  │
       │                                                   │
       │    ◀──────────────────────────────────────────────│
       │  {"access": "eyJ... (NEW)"}                       │
       │                                                   │
  ⑥ RETRY with new access token                           │
       │  GET /api/projects/                               │
       │  Authorization: Bearer <new_access>  ──────────▶  │
       │                                                   │
       │    ◀──────────────────────────────────────────────│
       │  {results: [...projects]}  ✅                      │
       │                                                   │
  ⑦ REFRESH TOKEN EXPIRES (after 7 days)                  │
       │  POST /api/auth/token/refresh/                    │
       │  {"refresh": "<expired_refresh>"}  ────────────▶  │
       │                                                   │
       │    ◀──────────────────────────────────────────────│
       │  401 Invalid or expired refresh token             │
       │                                                   │
  ⑧ USER MUST LOG IN AGAIN                                │
       │  Redirect to login page                           │
```

---

## Our API Endpoints

### All Auth Endpoints

| Endpoint | Method | Auth? | Purpose |
|----------|--------|-------|---------|
| `/api/auth/register/` | POST | ❌ No | Create account, get tokens |
| `/api/auth/login/` | POST | ❌ No | Log in, get tokens |
| `/api/auth/token/refresh/` | POST | ❌ No | Get new access token |
| `/api/auth/token/verify/` | POST | ❌ No | Check if token is valid |
| `/api/auth/me/` | GET | ✅ Yes | Get current user profile |

---

### `POST /api/auth/token/refresh/`

**When to call:** When an API call returns `401 Unauthorized`, your access token has expired.

**Request:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response (200):**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...(NEW)",
    "message": "Token refreshed successfully ..."
}
```

**Error Response (401) — Refresh token also expired:**
```json
{
    "detail": "Invalid or expired refresh token",
    "error": "Token is invalid or expired"
}
```

> When the refresh endpoint returns 401, **the user must log in again**. Both tokens have expired.

---

### `POST /api/auth/token/verify/`

**When to call:** Before making API calls, to check if a stored token is still valid.

**Request:**
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Valid (200):**
```json
{
    "valid": true,
    "message": "Token is valid"
}
```

**Invalid (401):**
```json
{
    "valid": false,
    "detail": "Token is invalid or expired"
}
```

---

### `GET /api/auth/me/`

**When to call:** When the frontend needs to display the logged-in user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
    "user": {
        "id": "68abc123...",
        "username": "john",
        "email": "john@email.com",
        "created_at": "2026-02-11T12:00:00Z"
    }
}
```

---

## How It Works in Our Code

### Token Generation (Login/Register)

In `auth_handler/views.py`:

```python
from rest_framework_simplejwt.tokens import RefreshToken

# After user is verified...
refresh = RefreshToken.for_user(user)

return Response({
    "access": str(refresh.access_token),   # Short-lived (30 min)
    "refresh": str(refresh),                # Long-lived (7 days)
})
```

`RefreshToken.for_user(user)` creates a refresh token containing:
```json
{
    "user_id": "68abc123...",    // from str(user.id)
    "exp": 1707600000,           // expiry timestamp
    "iat": 1707000000,           // issued-at timestamp
    "jti": "unique-token-id",    // prevents reuse
    "token_type": "refresh"
}
```

`.access_token` generates an access token from the same user data, with a shorter expiry.

### Token Refresh (views.py)

```python
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class TokenRefreshAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        refresh_token = request.data.get("refresh")

        try:
            refresh = RefreshToken(refresh_token)       # Verify the refresh token
            new_access = str(refresh.access_token)      # Generate new access token
        except TokenError:
            return Response({"detail": "Invalid or expired"}, status=401)

        return Response({"access": new_access})
```

**What happens inside:**
1. `RefreshToken(refresh_token)` — Decodes the token, verifies the signature against `SECRET_KEY`, checks expiry
2. `.access_token` — Creates a new access token with the same `user_id` and a new 30-minute expiry
3. If the refresh token is expired or tampered → `TokenError` is raised → 401

### Token Verification on Protected Endpoints

In `auth_handler/backends.py`:

```python
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth_handler.models import User

class MongoJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")
        user = User.objects(id=user_id).first()
        if user is None:
            raise AuthenticationFailed("User not found")
        return user
```

**Every protected request goes through this flow:**
```
Request arrives with "Authorization: Bearer <token>"
  ↓
JWTAuthentication.authenticate() ← (SimpleJWT built-in)
  ↓
Decodes the token, verifies signature + expiry
  ↓
Calls our get_user(validated_token) ← (Our custom override)
  ↓
Extracts user_id from token payload
  ↓
Queries MongoDB: User.objects(id=user_id).first()
  ↓
Returns the User object → becomes request.user
```

**Why custom?** SimpleJWT's default does `User.objects.get(id=user_id)` (Django ORM). MongoEngine needs `User.objects(id=user_id).first()`.

---

## Settings That Control JWT

In `settings.py`:

```python
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'auth_handler.backends.MongoJWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

| Setting | Value | What it means |
|---------|-------|---------------|
| `ACCESS_TOKEN_LIFETIME` | 30 minutes | Access token expires 30 min after creation |
| `REFRESH_TOKEN_LIFETIME` | 7 days | Refresh token expires 7 days after creation |
| `AUTH_HEADER_TYPES` | `Bearer` | Clients must send `Authorization: Bearer <token>` |

---

## Frontend Implementation Pattern

Here's how a frontend should handle the token lifecycle:

```javascript
// After login — store both tokens
function handleLogin(response) {
    localStorage.setItem('access', response.access);
    localStorage.setItem('refresh', response.refresh);
}

// Make API calls with the access token
async function apiCall(url, options = {}) {
    let access = localStorage.getItem('access');

    let response = await fetch(url, {
        ...options,
        headers: {
            ...options.headers,
            'Authorization': `Bearer ${access}`,
            'Content-Type': 'application/json',
        },
    });

    // If 401 → try refreshing the token
    if (response.status === 401) {
        const newAccess = await refreshAccessToken();
        if (newAccess) {
            // Retry the original request with the new token
            response = await fetch(url, {
                ...options,
                headers: {
                    ...options.headers,
                    'Authorization': `Bearer ${newAccess}`,
                    'Content-Type': 'application/json',
                },
            });
        } else {
            // Refresh failed → redirect to login
            window.location.href = '/login';
        }
    }

    return response;
}

// Refresh the access token using the refresh token
async function refreshAccessToken() {
    const refresh = localStorage.getItem('refresh');
    if (!refresh) return null;

    const response = await fetch('/api/auth/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh }),
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access', data.access);
        return data.access;
    }

    // Refresh token expired → clear everything, user must log in again
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    return null;
}
```

---

## Security Considerations

| Concern | Our Approach |
|---------|-------------|
| **Token Storage** | `localStorage` is simple but vulnerable to XSS. For higher security, use `httpOnly` cookies |
| **Short Access Lifetime** | 30 minutes limits damage from stolen access tokens |
| **Signature Verification** | Every token is verified against `SECRET_KEY` — can't be forged |
| **HTTPS** | Always use HTTPS in production — tokens are in plain text in HTTP headers |
| **Passwords** | Never stored in tokens — only `user_id` is in the payload |

---

## 🔗 Navigation

← **[Back to Learning Index](../learning_django.md)** · ← **[Back to Main README](../../README.md)**

**Related:** [Auth Module Implementation](../my_project/steps_auth_module.md) · [Custom Authentication Backend](../my_project/steps_auth_module.md#44-custom-jwt-backend-backendspy)
