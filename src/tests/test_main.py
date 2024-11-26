def test_read_task(client):
    response = client.get("/")
    assert response.status_code == 404

def test_read_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
