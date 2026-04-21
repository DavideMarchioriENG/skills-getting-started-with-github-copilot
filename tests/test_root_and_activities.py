def test_root_redirects_to_static_index(client):
    # Arrange
    root_path = "/"

    # Act
    response = client.get(root_path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert payload

    sample_activity = payload["Chess Club"]
    assert "description" in sample_activity
    assert "schedule" in sample_activity
    assert "max_participants" in sample_activity
    assert "participants" in sample_activity
    assert isinstance(sample_activity["participants"], list)
