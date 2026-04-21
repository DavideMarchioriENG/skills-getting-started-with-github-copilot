from urllib.parse import quote


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_name = quote(activity_name, safe="")
    existing_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_name}/signup",
        params={"email": existing_email},
    )
    updated_activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {existing_email} from {activity_name}"
    assert existing_email not in updated_activities[activity_name]["participants"]


def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange
    encoded_name = quote("Unknown Activity", safe="")
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_not_found_for_non_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_name = quote(activity_name, safe="")
    non_participant_email = "not.signed@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_name}/signup",
        params={"email": non_participant_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"
