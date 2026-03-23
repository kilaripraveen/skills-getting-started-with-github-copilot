"""
Tests for POST /activities/{activity_name}/signup endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""


class TestSignupForActivity:
    """Test suite for signup functionality"""

    def test_signup_successful(self, client, reset_activities):
        """
        Test that a student can successfully sign up for an activity
        
        Arrange: New email to sign up with
        Act: POST signup request
        Assert: Response is 200 and contains success message
        """
        # Arrange
        activity = "Chess Club"
        email = "newstudent@example.com"
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert email in data["message"]

    def test_signup_adds_participant(self, client, reset_activities):
        """
        Test that signup actually adds the participant to the activity
        
        Arrange: New email and initial activity state
        Act: Sign up and fetch activities
        Assert: New participant appears in the activity list
        """
        # Arrange
        activity = "Chess Club"
        email = "newstudent@example.com"
        
        # Act
        client.post(f"/activities/{activity}/signup?email={email}")
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert email in data[activity]["participants"]
        assert len(data[activity]["participants"]) == 3  # Was 2, now 3

    def test_signup_duplicate_email_rejected(self, client, reset_activities):
        """
        Test that signing up twice with same email is rejected
        
        Arrange: Sign up once successfully
        Act: Attempt to sign up again with same email
        Assert: Response is 400 and contains error message
        """
        # Arrange
        activity = "Chess Club"
        email = "duplicate@example.com"
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_nonexistent_activity_fails(self, client, reset_activities):
        """
        Test that signing up for a non-existent activity fails
        
        Arrange: Non-existent activity name
        Act: POST signup request for non-existent activity
        Assert: Response is 404
        """
        # Arrange
        activity = "NonExistent Activity"
        email = "test@example.com"
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_signup_existing_participant_still_fails(self, client, reset_activities):
        """
        Test that existing participants cannot sign up again
        
        Arrange: michael@mergington.edu is already in Chess Club
        Act: Attempt to sign up michael@mergington.edu again
        Assert: Response is 400 with duplicate error
        """
        # Arrange
        activity = "Chess Club"
        existing_participant = "michael@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={existing_participant}")
        
        # Assert
        assert response.status_code == 400
