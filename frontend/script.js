// =========================================
// SIDEBAR MOBILE TOGGLE
// =========================================

const menuBtn = document.querySelector(".menu-btn");
const sidebar = document.querySelector(".sidebar");

if (menuBtn) {

    menuBtn.addEventListener("click", () => {

        sidebar.classList.toggle("open");

    });

}


// =========================================
// SIDEBAR NAVIGATION
// =========================================

const navItems = document.querySelectorAll(".nav-item");

navItems.forEach(item => {

    item.addEventListener("click", function () {

        navItems.forEach(nav => {
            nav.classList.remove("active");
        });

        if (!this.classList.contains("logout")) {
            this.classList.add("active");
        }

    });

});


// =========================================
// GLOBAL SEARCH
// =========================================

const searchInput =
    document.querySelector(".global-search input");

if (searchInput) {

    searchInput.addEventListener("input", function () {

        console.log(
            "Searching:",
            this.value
        );

    });

}


// =========================================
// KEYBOARD SHORTCUT
// CMD + K / CTRL + K
// =========================================

document.addEventListener("keydown", function (event) {

    if (
        (event.metaKey || event.ctrlKey) &&
        event.key.toLowerCase() === "k"
    ) {

        event.preventDefault();

        if (searchInput) {

            searchInput.focus();

        }

    }

});