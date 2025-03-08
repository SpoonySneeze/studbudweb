document.getElementById("generate-btn").addEventListener("click", async () => {
  const prompt = document.getElementById("prompt").value;
  const errorElement = document.getElementById("error");
  const generatedCodeElement = document.getElementById("generated-code");

  // Clear previous results
  errorElement.textContent = "";
  generatedCodeElement.textContent = "";

  if (!prompt) {
    errorElement.textContent = "Please enter a prompt.";
    return;
  }

  // Disable the button to prevent multiple clicks
  const generateBtn = document.getElementById("generate-btn");
  generateBtn.disabled = true;
  generateBtn.textContent = "Generating...";

  try {
    // Send a POST request to the backend
    const response = await fetch("http://localhost:5000/generate-code", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: prompt, max_length: 256 }),
    });

    if (!response.ok) {
      throw new Error("Failed to generate code.");
    }

    const data = await response.json();
    generatedCodeElement.textContent = data.generated_code;
  } catch (error) {
    console.error("Error:", error);
    errorElement.textContent = "Failed to generate code. Please try again.";
  } finally {
    // Re-enable the button
    generateBtn.disabled = false;
    generateBtn.textContent = "Generate Code";
  }
});