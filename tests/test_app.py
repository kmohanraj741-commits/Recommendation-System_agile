import app as application


def test_home_page_displays_recommendations():
    client = application.app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Recommendation Show List" in response.data
    assert b"Inception" in response.data


def test_health_endpoint():
    client = application.app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"