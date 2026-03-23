// Test message to verify script is loading
console.log("APP.JS LOADED - Testing if JavaScript is executing");

document.addEventListener("DOMContentLoaded", () => {
  console.log("DOMContentLoaded event fired");
  
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      console.log("Fetching activities...");
      const response = await fetch(`/activities?t=${Date.now()}`);
      const activities = await response.json();
      console.log("Activities fetched, count:", Object.keys(activities).length);

      // Clear activities list
      activitiesList.innerHTML = "";

      // Remove all dropdown options except placeholder
      const options = activitySelect.querySelectorAll("option");
      options.forEach(option => {
        if (option.value !== "") {
          option.remove();
        }
      });

      // Populate activities
      Object.entries(activities).forEach(([name, details]) => {
        // Create activity card
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;
        
        // Create participants list with delete buttons
        let participantsList = "";
        if (details.participants.length > 0) {
          participantsList = details.participants
            .map(p => `<li><span>${p}</span><button class="delete-btn" title="Remove participant" data-activity="${name}" data-email="${p}">✕</button></li>`)
            .join('');
        } else {
          participantsList = '<li class="no-participants">No participants yet</li>';
        }

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="participants-section">
            <strong>Participants:</strong>
            <ul class="participants-list">
              ${participantsList}
            </ul>
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add click handlers for delete buttons
        const deleteButtons = activityCard.querySelectorAll(".delete-btn");
        deleteButtons.forEach(btn => {
          btn.addEventListener("click", async (e) => {
            e.preventDefault();
            const activityName = btn.getAttribute("data-activity");
            const email = btn.getAttribute("data-email");
            await removeParticipant(activityName, email);
          });
        });

        // Add option to dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
      console.log("Activities populated successfully");
    } catch (error) {
      console.error("Error fetching activities:", error);
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
    }
  }

  // Function to remove a participant
  async function removeParticipant(activityName, email) {
    try {
      console.log(`Removing ${email} from ${activityName}...`);
      const response = await fetch(
        `/activities/${encodeURIComponent(activityName)}/participants/${encodeURIComponent(email)}`,
        { method: "DELETE" }
      );

      const result = await response.json();
      console.log("Remove response:", result);

      if (response.ok) {
        console.log("Participant removed successfully! Refreshing activities...");
        // Refresh the activities list
        setTimeout(() => {
          fetchActivities();
        }, 100);
      } else {
        alert(result.detail || "Failed to remove participant");
      }
    } catch (error) {
      console.error("Error removing participant:", error);
      alert("Failed to remove participant. Please try again.");
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    console.log("Form submitted");

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    console.log(`Attempting to sign up ${email} for ${activity}`);

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        { method: "POST" }
      );

      const result = await response.json();
      console.log("Signup response:", result);

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        messageDiv.classList.remove("hidden");
        signupForm.reset();
        
        console.log("Signup successful! Refreshing activities in 100ms...");
        
        // Refresh the activities list
        setTimeout(() => {
          console.log("Now calling fetchActivities()");
          fetchActivities();
        }, 100);

        // Hide message after 5 seconds
        setTimeout(() => {
          messageDiv.classList.add("hidden");
        }, 5000);
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
        messageDiv.classList.remove("hidden");
      }
    } catch (error) {
      console.error("Error signing up:", error);
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
    }
  });

  // Initialize the app
  console.log("Calling initial fetchActivities()");
  fetchActivities();
});
