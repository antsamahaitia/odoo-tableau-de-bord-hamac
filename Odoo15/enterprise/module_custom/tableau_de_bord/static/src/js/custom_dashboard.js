odoo.define('tableau_de_bord.custom_dashboard', function (require) {
    "use strict";

    console.log("Custom dashboard JS loaded!");

    // Example: Add a click event to dashboard cards
    $('.dashboard-card').on('click', function () {
        console.log("Dashboard card clicked!");
    });
});