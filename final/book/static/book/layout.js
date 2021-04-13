document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.sidenav');
    M.Sidenav.init(elems, {});
    var elems = document.querySelectorAll('.dropdown-trigger');
    M.Dropdown.init(elems, {
        "hover": true,
        "alignment": 'bottom',
        "coverTrigger": false,
        "constrainWidth": false,
    });
    var elm = document.querySelector('.dropdown-trigger-2');
    M.Dropdown.init(elm, {
        "hover": true,
        "alignment": 'bottom',
        "coverTrigger": false,
        "constrainWidth": false,
        "closeOnClick": false
    });
    var elm = document.querySelector('.dropdown-trigger-3');

    M.Dropdown.init(elm, {
        "hover": true,
        "alignment": 'bottom',
        "coverTrigger": false,
        "constrainWidth": false,
        "closeOnClick": false
    });

    // Autocomplete
    const ac = document.querySelectorAll(".autocomplete");
    var instances = M.Autocomplete.init(ac, {});


    fetch('/cities')
        .then(response => response.json())
        .then(result => {
            for (i = 0; i < instances.length; i++) {
                instances[i].updateData(result);
            }
        });
});

function toTop() {
    window.scroll({
        top: 0,
        left: 0,
        behavior: 'smooth'
    });
}

window.onscroll = function (ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 20) {
        // you're at the bottom of the page
        document.querySelector(".scale-out").classList.add("scale-in");
    } else {
        document.querySelector(".scale-out").classList.remove("scale-in");
    }
};