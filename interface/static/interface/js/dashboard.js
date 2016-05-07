function loadFile() {
    var filename = $('input[type=file]')[0].files[0].name
    console.log($('input[type=file]')[0].files[0].name);

   $.ajax({
    // The URL for the request
    url: "load",
 
    // The data to send (will be converted to a query string)
    data: {
        name: filename
    },
 
    // Whether this is a POST or GET request
    type: "GET",
 
    // The type of data we expect back
    dataType : "json",
    success:function(data) {
      $('.load-start').fadeOut();
      $('.extract-start').fadeIn();

      var table = "<table class=\"pure-table pure-table-striped\">";
      table = table + "<thead><tr><th>Sample Data</th></tr></thead><tbody>";

      for (var i = 0, len = data['result'].length; i < len; i++) {
  			table = table + "<tr><td style=\"max-width:800px;\">" + data['result'][i] + "</td></tr>";
		}

      $('.extract-data').html(table+"</tbody></table>")
    }
  });
}


