// Web Development Courses
const webDevCourses = [
  "Web Development Fundamentals",
  "HTML5 & CSS3",
  "JavaScript Programming",
  "React.js Framework",
  "Node.js Backend Development",
  "Angular Framework",
  "Vue.js Framework",
  "PHP & MySQL",
  "Python Django",
  "Ruby on Rails",
  "MongoDB Database",
  "RESTful API Design",
  "GraphQL Implementation",
  "Web Security Principles",
  "Responsive Web Design",
  "UI/UX Design Principles",
];

// Ethiopian & International Certificates
const certificates = [
  { name: "AAU Web Development Certificate", value: 5 },
  { name: "AASTU Full Stack Developer", value: 5 },
  { name: "Haramaya University IT Certification", value: 4 },
  { name: "FreeCodeCamp Certification", value: 4 },
  { name: "Google IT Support Certificate", value: 4 },
  { name: "Meta Front-End Developer", value: 4 },
  { name: "AWS Certified Developer", value: 5 },
  { name: "Microsoft Certified: Azure Developer", value: 5 },
  { name: "Coursera Web Development Specialization", value: 3 },
  { name: "edX Web Programming", value: 3 },
  { name: "Udemy Complete Web Developer", value: 2 },
  { name: "JavaScript Algorithms Certification", value: 3 },
  { name: "Ethiopian ICT Certification", value: 4 },
];

// Course Addition Logic
document.getElementById("add-course").addEventListener("click", function () {
  const courseContainer = document.getElementById("course-container");
  const courseCount = courseContainer.children.length + 1;

  const newCourseRow = document.createElement("div");
  newCourseRow.className = "course-row mb-3";
  newCourseRow.innerHTML = `
      <div class="d-flex align-items-center gap-2 mb-2">
          <select class="form-select form-select-modern course-name">
              <option value="">Select Course</option>
              ${webDevCourses
                .map((course) => `<option value="${course}">${course}</option>`)
                .join("")}
          </select>
      </div>
      <div class="d-flex align-items-center gap-2">
          <select class="form-select form-select-modern grade">
              <option value="0-50">F</option>
              <option value="51-55">C</option>
              <option value="56-60">B</option>
              <option value="61-70">B+</option>
              <option value="71-80">A</option>
              <option value="81-90">A+</option>
              <option value="91-100">O</option>
          </select>
          <select class="form-select form-select-modern credit">
              <option value="0">0 Credits</option>
              <option value="1">1 Credit</option>
              <option value="2">2 Credits</option>
              <option value="3">3 Credits</option>
              <option value="4">4 Credits</option>
              <option value="5">5 Credits</option>
          </select>
      </div>
  `;
  courseContainer.appendChild(newCourseRow);

  // Remove empty state if it exists
  const emptyState = document.getElementById("course-empty-state");
  if (emptyState) emptyState.remove();
});

// Certificate Addition Logic
document
  .getElementById("add-certificate")
  .addEventListener("click", function () {
    const certificateContainer = document.getElementById(
      "certificate-container"
    );
    const certificateCount = certificateContainer.children.length + 1;

    if (certificateCount > 5) {
      alert("Maximum of 5 certificates allowed");
      return;
    }

    const newCertificateRow = document.createElement("div");
    newCertificateRow.className = "mb-2";
    newCertificateRow.innerHTML = `
      <div class="d-flex align-items-center gap-2">
          <select class="form-select form-select-modern certificate-category">
              <option value="">Select Certificate</option>
              ${certificates
                .map(
                  (cert) =>
                    `<option value="${cert.value}">${cert.name}</option>`
                )
                .join("")}
          </select>
      </div>
  `;
    certificateContainer.appendChild(newCertificateRow);

    // Remove empty state if it exists
    const emptyState = document.getElementById("certificate-empty-state");
    if (emptyState) emptyState.remove();
  });

// Calculate Performance Logic
document
  .getElementById("calculate")
  .addEventListener("click", async function () {
    const btn = this;
    try {
      // Show loading state
      btn.innerHTML = `<i class="fas fa-spinner loading-spinner me-2"></i> Processing...`;
      btn.disabled = true;

      // Collect course data
      const courses = [];
      document.querySelectorAll(".course-row").forEach((row) => {
        const courseName = row.querySelector(".course-name").value;
        const grade = row.querySelector(".grade").value;
        const credits = parseInt(row.querySelector(".credit").value);

        // Only add if course is selected
        if (courseName) {
          courses.push({ courseName, grade, credits });
        }
      });

      // Collect certificate data
      const certificates = [];
      document.querySelectorAll(".certificate-category").forEach((select) => {
        const value = parseFloat(select.value);
        if (value > 0) {
          certificates.push({
            name: select.options[select.selectedIndex].text,
            value: value,
          });
        }
      });

      // Validate at least one course added
      if (courses.length === 0) {
        throw new Error("Please add at least one course");
      }

      // Collect other form data
      const studentData = {
        courses: courses,
        attendance: document.getElementById("attendance-select").value,
        cgpa: document.getElementById("cgpa-select").value,
        internship: document.getElementById("Internship-select").value,
        certificates: certificates,
      };

      // Send to backend
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(studentData),
      });

      if (!response.ok)
        throw new Error(`Server error! status: ${response.status}`);

      const predictionResult = await response.json();
      displayResults(predictionResult);
    } catch (error) {
      showError(error);
    } finally {
      btn.innerHTML = `<i class="fas fa-calculator me-2"></i> Calculate My Performance`;
      btn.disabled = false;
    }
  });

// Display Results Function
function displayResults(results) {
  const container = document.getElementById("results-container");
  const performanceClass =
    results.predictedGrade >= 75
      ? "performance-high"
      : results.predictedGrade >= 50
      ? "performance-medium"
      : "performance-low";

  container.innerHTML = `
      <div class="result-badge ${performanceClass} mb-3">
          ${results.performanceCategory}
      </div>
      <div class="glass-card p-4">
          <h3 class="h5 fw-semibold mb-3 text-center">Prediction Details</h3>
          <div class="row g-3">
              <div class="col-md-4">
                  <div class="text-center p-3 bg-light rounded">
                      <div class="text-muted small">Predicted Grade</div>
                      <div class="h4 fw-bold">${results.predictedGrade}%</div>
                  </div>
              </div>
              <div class="col-md-4">
                  <div class="text-center p-3 bg-light rounded">
                      <div class="text-muted small">Performance Level</div>
                      <div class="h4 fw-bold text-${
                        performanceClass.includes("high")
                          ? "success"
                          : performanceClass.includes("medium")
                          ? "warning"
                          : "danger"
                      }">
                          ${results.performanceCategory}
                      </div>
                  </div>
              </div>
              <div class="col-md-4">
                  <div class="text-center p-3 bg-light rounded">
                      <div class="text-muted small">Risk Level</div>
                      <div class="h4 fw-bold text-${
                        results.riskLevel === "High" ? "danger" : "warning"
                      }">
                          ${results.riskLevel}
                      </div>
                  </div>
              </div>
              <div class="col-md-12 mt-4">
                  <div class="recommendation p-3 rounded bg-yellow text-dark">
                      <h4><i class="fas fa-lightbulb me-2"></i>Recommendations</h4>
                      <ul class="mt-2">
                          ${results.recommendations
                            .map((r) => `<li>${r}</li>`)
                            .join("")}
                      </ul>
                  </div>
              </div>
          </div>
      </div>
  `;
}

// Error Handling Function
function showError(error) {
  const container = document.getElementById("results-container");
  container.innerHTML = `
      <div class="alert alert-danger">
          <h4 class="alert-heading">Error!</h4>
          <p>${error.message}</p>
          <hr>
          <p class="mb-0">Please check your inputs and try again</p>
      </div>
  `;
}

// Add empty state messages
document.addEventListener("DOMContentLoaded", function () {
  const courseContainer = document.getElementById("course-container");
  const certContainer = document.getElementById("certificate-container");

  // Add empty state for courses
  courseContainer.innerHTML = `
      <div id="course-empty-state" class="empty-state">
          <i class="fas fa-book-open"></i>
          <h5>No Courses Added</h5>
          <p>Click the "Add Course" button to get started</p>
      </div>
  `;

  // Add empty state for certificates
  certContainer.innerHTML = `
      <div id="certificate-empty-state" class="empty-state">
          <i class="fas fa-certificate"></i>
          <h5>No Certificates Added</h5>
          <p>Click the "+" button to add certificates</p>
      </div>
  `;
});
