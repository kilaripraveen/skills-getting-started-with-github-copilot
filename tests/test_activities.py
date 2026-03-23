"""
Tests for GET /activities endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""


class TestGetActivities:
    """Test suite for fetching activities"""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        Test that GET /activities returns all 9 activities
        
        Arrange: Activities are pre-populated via fixture
        Act: Make GET request to /activities
        Assert: Response is 200 and contains 9 activities
        """
        # Arrange (done by fixture)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert "Chess Club" in data

    def test_get_activities_contains_required_fields(self, client, reset_activities):
        """
        Test that each activity has all required fields
        
        Arrange: Activities are pre-populated
        Act: Fetch activities and inspect Chess Club
        Assert: Chess Club has all required fields
        """
        # Arrange (done by fixture)
        
        # Act
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]
        
        # Assert
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club

    def test_get_activities_participants_are_correct(self, client, reset_activities):
        """
        Test that initial participants are correctly returned
        
        Arrange: Chess Club has 2 initial participants
        Act: Fetch activities
        Assert: Chess Club participants match expected list
        """
        # Arrange (done by fixture)
        
        # Act
        response = client.get("/activities")
        data = response.json()
        participants = data["Chess Club"]["participants"]
        
        # Assert
        assert len(participants) == 2
        assert "michael@mergington.edu" in participants
        assert "daniel@mergington.edu" in participants

    def test_get_activities_max_participants_correct(self, client, reset_activities):
        """
        Test that max_participants value is correct
        
        Arrange: Chess Club has max_participants of 12
        Act: Fetch activities
        Assert: max_participants is 12
        """
        # Arrange (done by fixture)
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert data["Chess Club"]["max_participants"] == 12
