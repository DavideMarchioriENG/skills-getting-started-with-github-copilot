from urllib.parse import quote


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_name = quote(activity_name, safe="")
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_name}/signup",
        params={"email": new_email},
    )
    updated_activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in updated_activities[activity_name]["participants"]


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    encoded_name = quote("Unknown Activity", safe="")
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_bad_request_for_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_name = quote(activity_name, safe="")
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
