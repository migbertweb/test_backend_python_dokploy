import pytest

async def get_token(client, email, password):
    response = await client.post(
        "/token",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_create_task(client):
    # Crear usuario y obtener token
    email = "task@example.com"
    password = "taskpassword"
    await client.post("/users/", json={"email": email, "password": password})
    token = await get_token(client, email, password)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert "id" in data

@pytest.mark.asyncio
async def test_read_tasks(client):
    email = "read@example.com"
    password = "readpassword"
    await client.post("/users/", json={"email": email, "password": password})
    token = await get_token(client, email, password)
    
    headers = {"Authorization": f"Bearer {token}"}
    # Crear una tarea
    await client.post("/tasks/", json={"title": "Task 1"}, headers=headers)
    
    response = await client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1

@pytest.mark.asyncio
async def test_update_task(client):
    email = "update@example.com"
    password = "updatepassword"
    await client.post("/users/", json={"email": email, "password": password})
    token = await get_token(client, email, password)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Crear
    create_resp = await client.post("/tasks/", json={"title": "Old Title"}, headers=headers)
    task_id = create_resp.json()["id"]
    
    # Actualizar
    update_resp = await client.put(f"/tasks/{task_id}", json={"title": "New Title", "completed": True}, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "New Title"
    assert update_resp.json()["completed"] is True

@pytest.mark.asyncio
async def test_delete_task(client):
    email = "delete@example.com"
    password = "deletepassword"
    await client.post("/users/", json={"email": email, "password": password})
    token = await get_token(client, email, password)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Crear
    create_resp = await client.post("/tasks/", json={"title": "To delete"}, headers=headers)
    task_id = create_resp.json()["id"]
    
    # Eliminar
    delete_resp = await client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {"ok": True}
    
    # Verificar que no existe
    get_resp = await client.get(f"/tasks/{task_id}", headers=headers)
    assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_unauthorized_access(client):
    response = await client.get("/tasks/")
    assert response.status_code == 401
