"use strict";

$(document).ready(function(){
    if ($(`#nav_${document.title.toLowerCase().replace(/\s/g, "_")}`)) {
    $(`#nav_${document.title.toLowerCase().replace(/\s/g, "_")}`).addClass("active");
    };
});