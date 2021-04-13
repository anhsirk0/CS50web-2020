// document.querySelector('#profile').classList.add('active');

var elems = document.querySelectorAll('.fixed-action-btn');
var instances = M.FloatingActionButton.init(elems, {});

var elems = document.querySelectorAll('.tooltipped');
M.Tooltip.init(elems, {});

document.querySelector(".follow").addEventListener('click', elm => {
    el = document.querySelector(".follow-icon");
    dt = document.querySelector(".tooltipped");
    f = dt.dataset.tooltip.split(" ")[0];
    const user = dt.dataset.tooltip.split(" ")[1];
    if (el.innerText == "add") {
        el.innerText = "remove";
        dt.dataset.tooltip = "Unfollow " + user;
        count = parseInt(document.querySelector('.follower-count').innerText.split(' ')[0]);
        document.querySelector('.follower-count').innerText = (count + 1).toString() + ' Followers';
        M.toast({ html: 'Following ' + user, displayLength: 6000, classes: 'white-text' });
    }

    else {
        el.innerText = "add"
        dt.dataset.tooltip = "Follow " + user;
        M.toast({ html: 'Unfollowed ' + user, displayLength: 6000, classes: 'white-text' });
        count = parseInt(document.querySelector('.follower-count').innerText.split(' ')[0]);
        document.querySelector('.follower-count').innerText = (count - 1).toString() + ' Followers';
    }

    var username = document.querySelector("#username").innerText;
    fetch('/follow', {
        method: 'POST',
        body: JSON.stringify({
            username: username
        })
    });
});
