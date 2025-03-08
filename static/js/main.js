function fetchPrograms() {
  // Gather filter values
  const fee = document.getElementById("filter-fee").value;
  const country = document.getElementById("filter-country").value;
  const field = document.getElementById("filter-field").value;
  const university = document.getElementById("filter-university").value;

  let url = `/api/programs?fee=${fee}&country=${country}&field=${field}&university=${university}`;
  fetch(url)
    .then((response) => response.json())
    .then((programs) => {
      const container = document.getElementById("programs-list");
      container.innerHTML = "";
      programs.forEach((program) => {
        // Create program card elements dynamically
        let card = document.createElement("div");
        card.className = "col-md-4 mb-3";
        card.innerHTML = `
            <div class="card h-100">
              <div class="card-body">
                <h5>${program.name}</h5>
                <p><strong>University:</strong> ${program.university}</p>
                <p><strong>Field:</strong> ${program.field}</p>
                <p><strong>Country:</strong> ${program.country}</p>
                <a href="/programs/${program.id}" class="btn btn-outline-primary">View Details</a>
              </div>
            </div>`;
        container.appendChild(card);
      });
    });
}
