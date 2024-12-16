// =============== BANNER ===============
document.addEventListener("DOMContentLoaded", () => {
  new Glide(".glide", {
    type: "carousel",
    autoplay: 3000,
    animationDuration: 800,
    hoverpause: false,
    perView: 1,
  }).mount();
});

// =============== CARD ===============
document.addEventListener("DOMContentLoaded", function () {
  var masonryContainer = document.querySelector("#masonry-container");

  // Initialize Masonry
  imagesLoaded(masonryContainer, function () {
    var masonry = new Masonry(masonryContainer, {
      itemSelector: ".col-md-4",
      columnWidth: ".col-md-4",
      percentPosition: true,
      gutter: 20,
    });

    // Filter Buttons
    var filterButtons = document.querySelectorAll(".filter-btn");
    filterButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        // Update active button
        filterButtons.forEach((btn) => btn.classList.remove("active"));
        this.classList.add("active");

        var filterType = this.getAttribute("data-filter");

        // Filter items
        var items = masonryContainer.querySelectorAll(".col-md-4");
        items.forEach(function (item) {
          if (
            filterType === "all" ||
            item.getAttribute("data-type") === filterType
          ) {
            item.style.display = "block";
          } else {
            item.style.display = "none";
          }
        });

        // Re-layout Masonry
        masonry.layout();
      });
    });

    // "More" Button Functionality
    var ansButtons = document.querySelectorAll(".more-btn");
    ansButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        // Find the .additional-info div inside the same card-body
        var additionalInfo =
          this.closest(".card-body").querySelector(".additional-info");

        // Toggle visibility
        additionalInfo.style.display =
          additionalInfo.style.display === "none" ||
          additionalInfo.style.display === ""
            ? "block"
            : "none";

        // Update button text
        this.textContent =
          additionalInfo.style.display === "block" ? "Less" : "More";

        // Re-layout Masonry after expanding/collapsing
        masonry.layout();
      });
    });
  });
});
