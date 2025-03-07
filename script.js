document.getElementById("generate-btn").addEventListener("click", async () => {
    const goal = document.getElementById("goal").value;
    const errorElement = document.getElementById("error");
    const planTextElement = document.getElementById("plan-text");
  
    // Clear previous results
    errorElement.textContent = "";
    planTextElement.textContent = "";
  
    if (!goal) {
      errorElement.textContent = "Please enter a study goal.";
      return;
    }
  
    // Disable the button to prevent multiple clicks
    const generateBtn = document.getElementById("generate-btn");
    generateBtn.disabled = true;
    generateBtn.textContent = "Generating...";
  
    try {
      // Send a POST request to the backend
      const response = await fetch("http://localhost:5000/generate-plan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ goal }),
      });
  
      if (!response.ok) {
        throw new Error("Failed to generate study plan.");
      }
  
      const data = await response.json();
      planTextElement.textContent = data.study_plan;
    } catch (error) {
      console.error("Error:", error);
      errorElement.textContent = "Failed to generate study plan. Please try again.";
    } finally {
      // Re-enable the button
      generateBtn.disabled = false;
      generateBtn.textContent = "Generate Study Plan";
    }
  });