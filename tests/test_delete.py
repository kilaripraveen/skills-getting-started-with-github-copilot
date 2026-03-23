"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""


class TestRemoveParticipant:
    """Test suite for participant removal functionality"""

    def test_remove_participant_successful(self, client, reset_activities):
        """
        Test that a participant can be successfully removed
        
        Arrange: Add a new participant to an activity
        Act: DELETE request to remove the participant
        Assert: Response is 200 and contains success message
        """
        # Arrange
        activity = "Chess Club"
        email = "removal@example.com"
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Removed" in data["message"]
        assert email in data["message"]

    def test_remove_participant_removes_from_list(self, client, reset_activities):
        """
        Test that removal actually removes participant from activity list
        
        Arrange: Add a new participant
        Act: Remove the participant and fetch activities
        Assert: Participant no longer in the activity
        """
        # Arrange
        activity = "Chess Club"
        email = "removal@example.com"
        client.post(f"/activities/{activity}/signup?email={email}")
        initial_count = len(client.get("/activities").json()[activity]["participants"])
        
        # Act
        client.delete(f"/activities/{activity}/participants/{email}")
        response = client.get("/activities")
        
        # Assert
        final_data = response.json()
        assert email not in final_data[activity]["participants"]
        assert len(final_data[activity]["participants"]) == initial_count - 1

    def test_remove_nonexistent_participant_fails(self, client, reset_activities):
        """
        Test that removing a non-existent participant fails
        
        Arrange: Non-existent email
        Act: DELETE request for non-existent participant
        Assert: Response is 404
        """
        # Arrange
        activity = "Chess Club"
        email = "nonexistent@example.com"
        
        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_remove_from_nonexistent_activity_fails(self, client, reset_activities):
        """
        Test that removing from a non-existent activity fails
        
        Arrange: Non-existent activity name
        Act: DELETE request for non-existent activity
        Assert: Response is 404
        """
        # Arrange
        activity = "NonExistent Activity"
        email = "test@example.com"
        
        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")
        
        # Assert
        assert response.status_code == 404

    def test_remove_existing_participant(self, client, reset_activities):
        """
        Test that we can remove an initially existing participant
        
        Arrange: michael@mergington.edu is in Chess Club initially
        Act: DELETE request to remove michael@mergington.edu
        Assert: Response is 200 and participant is gone
        """
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")
        activities_response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = activities_response.json()
        assert email not in data[activity]["participants"]
