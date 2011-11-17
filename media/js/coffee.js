
  $(document).ready(function() {
    console.log('heare');
    $.getJSON('/chose', function(data) {
      console.log('dsad');
      console.log('before i get full data', data);
      return $('body').append('<img src="' + data['photo'] + '">');
    });
    return console.log('fine working');
  });
