(function() {
  /*
      Img Resizer plugin, used to resize a picture, with given dimensions.
      Input parameters:
        width => width to resize
        height => height to resize
        img => img url to resize
      Use:
         $('.element').imgresizer()
         $('.element') - element in which resized photo will be inserted
      Author:
         Grisha
      Date:
         23.09.2011
  */  (function($) {
    return $.fn.imgresizer = function(params) {
      var applyScale, div, imageShape, mainShape, _height, _img, _width;
      params = $.extend({
        width: false,
        height: false,
        img: false
      }, params);
      _width = params.width;
      _height = params.height;
      _img = params.img;
      div = this;
      div.css({
        'width': _width,
        'height': _height,
        'overflow': 'hidden'
      });
      applyScale = function(scale, dim, image) {
        var margin, new_height, new_width;
        if (dim === 'w') {
          new_height = _width / scale;
          margin = (_height - new_height) / 2;
          return image.attr({
            'width': _width,
            'height': new_height
          });
        } else {
          new_width = _height * scale;
          margin = (_width - new_width) / 2;
          return image.attr({
            'width': new_width,
            'height': _height
          }).css({
            'margin-left': margin
          });
        }
      };


      mainShape = function(dim, image) {
        var scale;
        scale = image.width() / image.height();
        return applyScale(scale, dim, image);
      };
      imageShape = function() {
        var img;
        img = $('<img src="' + _img + '" />').load(function() {
          var img_height, img_width, module_h, module_w;
          img_width = $(this).width();
          img_height = $(this).height();
          module_w = img_width / _width;
          module_h = img_height / _height;
          if (module_w > module_h) {
            return mainShape('h', $(this));
          } else if (module_w < module_h) {
            return mainShape('w', $(this));
          } else if (module_w === module_h) {
            if (_width > _height) {
              return mainShape('h', $(this));
            } else if (_width < _height) {
              return mainShape('w', $(this));
            } else if (_width === _height) {
              return mainShape('w', $(this));
            }
          }
        });
        return div.html(img);
      };
      if (params.img) {
        return div.each(function() {
          return imageShape();
        });
      }
    };
  })(jQuery);
}).call(this);