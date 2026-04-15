"""
auth.py — JWT verification via auth-service.

Instead of re-implementing JWT verification, we delegate to the existing
auth-service /auth/verify endpoint. This keeps the secret in one place
and makes the chatbot a proper microservice citizen.
"""

import os
import httpx
from fastapi import Header, HTTPException, status

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:5001")


async def get_current_user(authorization: str = Header(...)):
    """
    FastAPI dependency that validates the Bearer token by calling auth-service.

    Returns the decoded JWT payload dict: {"userId": "...", "email": "..."}
    Raises HTTP 401 on any failure.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must start with 'Bearer '",
        )

    token = authorization.split(" ", 1)[1]

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{AUTH_SERVICE_URL}/auth/verify",
                json={"token": token},
            )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not reach auth-service: {exc}",
        )

    if resp.status_code != 200 or not resp.json().get("valid"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return resp.json()["decoded"]
