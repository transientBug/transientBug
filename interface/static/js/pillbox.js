// Generated by CoffeeScript 1.5.0
(function() {
  var $;

  $ = jQuery;

  $.fn.extend({
    pillbox: function(options) {
      var opts, self;
      self = $.fn.pillbox;
      opts = $.extend({}, self.default_options, options);
      return $(this).each(function(i, el) {
        return self.init(el, opts);
      });
    }
  });

  $.extend($.fn.pillbox, {
    default_options: {
      placeholder: ''
    },
    init: function(_el, opts) {
      var el, self;
      self = this;
      self._tags = {};
      el = $(_el);
      self._init_val = el.val();
      el.hide();
      el.after("<div class=\"pillbox\"><input type=\"text\" placeholder=\"" + opts.placeholder + "\"/></div>");
      el = $(el.next(".pillbox"));
      self._el = el;
      return self.build();
    },
    build: function() {
      var input_keypress, re_label, remove_this, self, tag, _i, _len, _ref;
      self = this;
      re_label = function() {
        var status, tag, tags, text, val_string, _ref;
        text = "";
        tags = [];
        self._el.find("span.label").remove();
        _ref = self._tags;
        for (tag in _ref) {
          status = _ref[tag];
          if (status && tag) {
            self._el.prepend(" <span class=\"label label-theme\">" + tag + " <i data-role=\"remove\" class=\"fa fa-times\"></i></span> ");
            tags.push(tag);
          }
        }
        val_string = tags.join(",");
        return self._el.prev().val(val_string);
      };
      input_keypress = function(e) {
        var input, key, last, tag;
        switch (e.keyCode) {
          case 13:
            e.preventDefault();
            tag = self._el.find('input').last().val().trim();
            self._tags[tag] = true;
            self._el.find("input").val("");
            return self.refresh();
          case 8:
          case 46:
            input = self._el.find("input").last();
            if (self.getCaretPosition(input[0]) === 0) {
              e.preventDefault();
              last = self._el.find("span.label").last();
              if (last != null) {
                key = last.text().trim();
                self._tags[key] = false;
                return self.refresh();
              }
            }
        }
      };
      remove_this = function() {
        var key;
        key = $(this).parent().text().trim();
        self._tags[key] = false;
        return $(this).parent().remove();
      };
      _ref = self._init_val.split(",");
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        tag = _ref[_i];
        self._tags[tag.trim()] = true;
        self.refresh();
      }
      self._el.on("keydown", input_keypress);
      self._el.on("click", 'i[data-role="remove"]', remove_this);
      return self._el.click(function() {
        return self._el.find("input").last().focus();
      });
    },
    refresh: function() {
      var self, status, tag, tags, text, val_string, _ref;
      self = this;
      text = "";
      tags = [];
      self._el.find("span.label").remove();
      _ref = self._tags;
      for (tag in _ref) {
        status = _ref[tag];
        if (status && tag) {
          self._el.prepend(" <span class=\"label label-theme\">" + tag + " <i data-role=\"remove\" class=\"fa fa-times\"></i></span> ");
          tags.push(tag);
        }
      }
      val_string = tags.join(",");
      return self._el.prev().val(val_string);
    },
    remove: function(item) {
      var self;
      self = this;
      if (item in self._tags) {
        self._tags[item] = false;
        return self.refresh();
      }
    },
    add: function(item) {
      var self;
      self = this;
      self._tags[item] = true;
      return self.refresh();
    },
    empty: function() {
      this._tags = {};
      return this.refresh();
    },
    getCaretPosition: function(oField) {
      var iCaretPos, oSel;
      iCaretPos = 0;
      if (document.selection) {
        oField.focus();
        oSel = document.selection.createRange();
        oSel.moveStart('character', -oField.value.length);
        iCaretPos = oSel.text.length;
      } else if (oField.selectionStart || oField.selectionStart === '0') {
        iCaretPos = oField.selectionStart;
      }
      return iCaretPos;
    }
  });

}).call(this);