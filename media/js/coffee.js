(function() {
  var Loader;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  Loader = (function() {

    function Loader() {
      this.renderChose = __bind(this.renderChose, this);
    }

    Loader.prototype.apply = function() {
      return $.getJSON('/chose', this.renderChose);
    };

    Loader.prototype.renderChose = function(data) {
      var div, img, li, parent, user, _i, _len, _results;
      var _this = this;
      parent = $('#photo_chose');
      parent.empty();
      _results = [];
      for (_i = 0, _len = data.length; _i < _len; _i++) {
        user = data[_i];
        li = $('<li></li>');
        div = $('<div></div>');
        img = $('<img width="247" src="' + user.photo_big + '" />');
        li.append(div.append(img));
        li.data('uid', user.uid);
        li.click(function(event) {
          return _this.choseUser(event);
        });
        parent.append(li);
        _results.push(console.log(user.uid));
      }
      return _results;
    };

    Loader.prototype.choseUser = function(event) {
      var uid;
      uid = $(event.currentTarget).data('uid');
      $.get('/chose/' + uid);
      return this.apply();
    };

    return Loader;

  })();

  window.loader = new Loader();

  $(document).ready(function() {
    return loader.apply();
  });

}).call(this);
