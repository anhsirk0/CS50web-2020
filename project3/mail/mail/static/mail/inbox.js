document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-submit').addEventListener('click', send_mail);
}

function send_mail() {
    const recipients = document.querySelector('#compose-recipients').value ;
    const subject = document.querySelector('#compose-subject').value ;
    const body = document.querySelector('#compose-body').value ;

       fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result

    });
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails => {
    // Print emails

    document.querySelector('#emails-view').innerHTML = '';
    if (emails.length == 0){
      document.querySelector('#emails-view').innerHTML = '<h1>Inbox is Empty</h1>'
    } else {
    for(i=0; i<emails.length;i++){

        const html = `
        <a id="btn-email" onclick="load_email(${emails[i].id})">
        <ul>
            <li id="sender"><strong>${emails[i].sender}</strong></li>
            <li id="subject">${emails[i].subject}</li>
            <li id="timestamp">${emails[i].timestamp}</li>
        </ul>
        </a>
        `;
        const div = document.createElement('div');
          if (emails[i].read){
          div.style.background = "grey";
          } else {
          div.style.background = "white";
          }
        div.innerHTML = html;
        div.className = "email";

        document.querySelector('#emails-view').append(div);
    }
    // ... do something else with emails ...
 }
 });
}

function load_email(id) {
    document.querySelector('#emails-view').style.display = 'block';
    fetch('/emails/'+id)
    .then(response => response.json())
    .then(email => {
      // Print email
    var b;

    var s = email.body;
    var p = /wrote: ".*?"/i;
    var res = s.match(p);
    if (res != null){
      s = s.slice(res.index+res[0].length).trimStart();
    }
    if (email.archived == true){
      b = `<button class="btn btn-warning" onclick="archive(${email.id}, false)">Unarchive</button>`;
    } else {
      b = `<button class="btn btn-danger" onclick="archive(${email.id}, true)">Archive</button>`;
    }

    const html = `
    <p><strong>From : </strong> ${email.sender}</p>
    <p><strong>To : </strong> ${email.recipients}</p>
    <p><strong>Subject : </strong> ${email.subject}</p>
    <p><strong>Time : </strong> ${email.timestamp}</p>
    <hr>
    <h3>${email.body}</h3>
    <hr>
    <button class="btn btn-primary"
      onclick="reply('${email.sender}','${email.subject}','${s}','${email.timestamp}')">
    Reply</button>
    `
    +b;

    const div = document.createElement('div');
      div.innerHTML = html;
      div.className = "view-email";

      document.querySelector('#emails-view').innerHTML = html;
    //

});
  fetch('/emails/'+id , {
  method: 'PUT',
  body: JSON.stringify({
      read: true
  }),
  });
  }


function reply(sender,subject, body,time) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#compose-recipients').value = sender;

  const msg = `On ${time}, ${sender} wrote: "${body}"`
  document.querySelector('#compose-body').value = msg;
  if (subject.slice(0,4) == "RE: "){
  document.querySelector('#compose-subject').value = subject;
  } else {
  document.querySelector('#compose-subject').value = "RE: "+subject;
  }
  // body...
  document.querySelector('#compose-submit').addEventListener('click', send_mail);


}

function archive(id, value) {
  // body...
  fetch('/emails/'+id , {
    method: 'PUT',
    body: JSON.stringify({
        archived: value
    }),
  });


  if (value == false){
      alert("Email Unarchived");
  } else {
      alert("Email Archived");
  }
  load_mailbox('inbox');
}
