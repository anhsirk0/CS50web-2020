
var elems = document.querySelectorAll('.tooltipped');
M.Tooltip.init(elems, {});

document.querySelector('#textarea').addEventListener('focus', () => {
    document.querySelector('.create-post').classList.add('z-depth-5');
});

document.querySelector('#textarea').addEventListener('focusout', () => {
    document.querySelector('.create-post').classList.remove('z-depth-5');
});

// document.querySelector('#home').classList.add('active');

