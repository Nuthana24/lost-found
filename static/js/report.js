function toggleForm(type) {
  const lostForm = document.getElementById("lostForm");
  const foundForm = document.getElementById("foundForm");
  const lostBtn = document.getElementById("lostBtn");
  const foundBtn = document.getElementById("foundBtn");

  if (type === "lost") {
    lostForm.classList.add("active");
    foundForm.classList.remove("active");
    lostBtn.classList.add("active");
    foundBtn.classList.remove("active");
  } else {
    foundForm.classList.add("active");
    lostForm.classList.remove("active");
    foundBtn.classList.add("active");
    lostBtn.classList.remove("active");
  }
}

// Image Preview and Drag/Drop Upload Logic
const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const dragDropArea = document.getElementById("dragDropArea");
const dragDropText = document.getElementById("dragDropText");

// Function to validate image type
function isValidImage(file) {
  return file && file.type.startsWith("image/");
}

dragDropArea.addEventListener("click", () => imageInput.click());

imageInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file && isValidImage(file)) {
    const reader = new FileReader();
    reader.onload = () => {
      imagePreview.src = reader.result;
      imagePreview.classList.remove("hidden");
      dragDropText.textContent = "Image Uploaded";
    };
    reader.readAsDataURL(file);
  } else {
    dragDropText.textContent = "Please upload a valid image";
  }
});

dragDropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dragDropArea.classList.add("dragover");
});

dragDropArea.addEventListener("dragleave", () => {
  dragDropArea.classList.remove("dragover");
});

dragDropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  const file = e.dataTransfer.files[0];
  if (file && isValidImage(file)) {
    const reader = new FileReader();
    reader.onload = () => {
      imagePreview.src = reader.result;
      imagePreview.classList.remove("hidden");
      dragDropText.textContent = "Image Uploaded";
    };
    reader.readAsDataURL(file);
  } else {
    dragDropText.textContent = "Please upload a valid image";
  }
});

// Form validation with Parsley and custom submit messages with SweetAlert2
$("#lostFormSubmit")
  .parsley()
  .on("form:submit", function () {
    Swal.fire({
      icon: "success",
      title: "Success!",
      text: "Your Lost Item report has been submitted successfully.",
      confirmButtonText: "OK",
    }).then(() => {
      // Clear the form after success
      document.getElementById("lostFormSubmit").reset();
      imagePreview.classList.add("hidden");
      dragDropText.textContent = "Drag & Drop to Upload or Browse";
    });

    return false; // Prevent form submission
  });

$("#foundFormSubmit")
  .parsley()
  .on("form:submit", function () {
    Swal.fire({
      icon: "success",
      title: "Success!",
      text: "Your Found Item report has been submitted successfully.",
      confirmButtonText: "OK",
    }).then(() => {
      // Clear the form after success
      document.getElementById("foundFormSubmit").reset();
      imagePreview.classList.add("hidden");
      dragDropText.textContent = "Drag & Drop to Upload or Browse";
    });

    return false; // Prevent form submission
  });
