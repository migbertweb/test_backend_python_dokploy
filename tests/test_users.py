import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_create_user_duplicate_email(client):
    # El usuario ya debería existir por el test anterior si se ejecutan en orden, 
    # pero para estar seguros lo creamos aquí (o confiamos en el estado persistente de la sesión si no se limpia)
    # En este caso, cada test usa una nueva sesión de db pero el motor es el mismo para la sesión.
    await client.post(
        "/users/",
        json={"email": "duplicate@example.com", "password": "testpassword"},
    )
    response = await client.post(
        "/users/",
        json={"email": "duplicate@example.com", "password": "newpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "El email ya está registrado"
