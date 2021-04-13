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

    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems, {});

    document.querySelectorAll('#like-btn').forEach(elm => {
        elm.addEventListener('click', el => {
            lc = elm.parentElement.parentElement.querySelector('.like-count');
            e = elm.querySelector('.like-icon');
            if (e.innerText == 'favorite_border') {
                lc.innerText = parseInt(lc.innerText) + 1;
                e.innerText = 'favorite_fill';
                M.toast({ html: 'Post liked', displayLength: 6000, classes: 'white-text' });
            } else {
                e.innerText = 'favorite_border';
                lc.innerText = parseInt(lc.innerText) - 1;
                M.toast({ html: 'Post unliked', displayLength: 6000, classes: 'white-text' });
            }
            fetch('/like', {
                method: 'POST',
                body: JSON.stringify({
                    id: elm.dataset.id
                })
            });
        });
    });

    document.querySelector('.edit-post').addEventListener('click', elm => {
        el = document.querySelector('.edit-text');
        l = document.querySelector('#post-' + el.id.toString());
        el.value = l.innerText
    })

    document.querySelector('#submit-edit').addEventListener('click', elm => {
        el = document.querySelector('.edit-text');
        l = document.querySelector('#post-' + el.id.toString());
        const newText = el.value;
        l.innerText = newText;
        M.toast({ html: 'Post updated', displayLength: 6000, classes: 'white-text' });

        fetch('/edit_post', {
            method: 'POST',
            body: JSON.stringify({
                text: newText,
                id: el.id
            })
        });
    });

});
