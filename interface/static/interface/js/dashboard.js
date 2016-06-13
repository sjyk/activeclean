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

      if (data['headers'].length < 5)
        $('#col-scroll').hide();


      var table = "<table class=\"pure-table pure-table-striped\">";

      table = table + "<thead><tr>";
      for (var i = 0, len = data['headers'].length; i < len; i++)
      { 
        if (i < 5)
          table = table + "<th class=\"head-col-"+i+"\"><a href=\"#\" onclick=\"editAttr("+i+");\">"+i+"</a></th>"
        else
          table = table + "<th class=\"head-col-"+i+"\" style=\"display:none;\"><a href=\"#\" onclick=\"editAttr("+i+");\">"+i+"</a></th>"
      }

      table = table + "</tr></thead><tbody>";

      for (var i = 0, len = data['result'].length; i < len; i++) {
        
        table = table + "<tr>";
        for (var j = 0, len2 = data['result'][i].length; j < len2; j++)
           {
              //!hard coded fix
              if (j < 5)
                table = table + "<td class=\"data-col-"+j+"\">"+data['result'][i][j]+"</td>";
              else
                table = table + "<td class=\"data-col-"+j+"\" style=\"display:none;\">"+data['result'][i][j]+"</td>";

           }  

  			table = table + "</tr>";
		}

      $('.extract-data').html(table+"</tbody></table>")
    }
  });
  window.cur_col = 0;
}

//fix
function scroll() {
   for (var j = window.cur_col, len2 = window.cur_col+5; j < len2; j++)
   {
       $(".data-col-"+j).hide();
       $(".head-col-"+j).hide();
   }
   for (var j = window.cur_col+5, len2 = window.cur_col+10; j < len2; j++)
   {
      $(".data-col-"+j).show();
      $(".head-col-"+j).show();
   }
   window.cur_col = window.cur_col + 5;
}

//fix
function editAttr(j) {
   $('.col-editor').show()
   $('#attrname').val(j)
}
