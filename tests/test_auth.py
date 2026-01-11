import pytest

@pytest.mark.asyncio
async def test_login_success(client):
    # Crear usuario primero
    await client.post(
        "/users/",
        json={"email": "auth@example.com", "password": "authpassword"},
    )
    
    # Intentar login
    response = await client.post(
        "/token",
        data={"username": "auth@example.com", "password": "authpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_json_success(client):
    email = "json@example.com"
    password = "jsonpassword"
    await client.post("/users/", json={"email": email, "password": password})
    
    response = await client.post(
        "/token",
        json={"username": email, "password": password}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    response = await client.post(
        "/token",
        data={"username": "wrong@example.com", "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Nombre de usuario o contraseña incorrectos"

@pytest.mark.asyncio
async def test_login_missing_fields(client):
    response = await client.post(
        "/token",
        data={"username": "onlyuser"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    # FastAPI devolverá 422 si falta un campo requerido en el form
    assert response.status_code == 422
