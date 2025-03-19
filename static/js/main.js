// Function to fetch programs based on current filter input values
function fetchPrograms() {
  // Retrieve filter values, if the input exists (fallback to empty string)
  const feeInput = document.getElementById("filter-fee");
  const countryInput = document.getElementById("filter-country");
  const fieldInput = document.getElementById("filter-field");
  const universityInput = document.getElementById("filter-university");

  const fee = feeInput ? feeInput.value : "";
  const country = countryInput ? countryInput.value : "";
  const field = fieldInput ? fieldInput.value : "";
  const university = universityInput ? universityInput.value : "";

  // Build the API URL with query parameters 
  const url = `/api/programs?fee=${encodeURIComponent(fee)}&country=${encodeURIComponent(country)}&field=${encodeURIComponent(field)}&university=${encodeURIComponent(university)}`;

  fetch(url)
    .then(response => response.json())
    .then(programs => {
      const container = document.getElementById("programs-list");
      if (container) {
        container.innerHTML = "";
        programs.forEach(program => {
          // Create a card for each program
          const card = document.createElement("div");
          card.className = "col-md-4 mb-3";
          card.innerHTML = `
            <div class="card h-100">
            <div class="card-header text-center" style="background-color:rgba(247, 248, 248, 0.95)" >
              <h5>${program.name}</h5>
              </div> 
              <div class="card-body">  
                <p><strong>University:</strong> ${program.university}</p>
                <p><strong>Field:</strong> ${program.field}</p>
                <p><strong>Country:</strong> ${program.country}</p>
                <a href="/programs/${program.id}" class="btn btn-outline-primary">View Details</a>
              </div>
            </div>`;
          container.appendChild(card);
        });
      }
    })
    .catch(error => {
      console.error("Error fetching programs:", error);
    });
}

// On DOMContentLoaded, fetch the initial list of programs
document.addEventListener("DOMContentLoaded", function () {
  fetchPrograms();

  // Attach input event listeners to filter inputs (if they exist) to update the program list in real time
  const filterIds = ["filter-fee", "filter-country", "filter-field", "filter-university"];
  filterIds.forEach(id => {
    const input = document.getElementById(id);
    if (input) {
      input.addEventListener("input", fetchPrograms);
    }
  });
});
