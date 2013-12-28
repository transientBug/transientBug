// Generated by CoffeeScript 1.5.0
(function() {

  $(function() {
    $("#add_group").click(function(e) {
      e.preventDefault();
      return $("#groups").append("<div class=\"input-group\">\n  <input type=\"text\" class=\"form-control input-sm\" name=\"groups\" placeholder=\"Group...\" />\n  <span class=\"input-group-btn\">\n    <button class=\"btn btn-default btn-sm\"><i class=\"fa fa-times\"></i></button>\n  </span>\n</div>\n<br>");
    });
    return $("#groups").on("click", "button", function(e) {
      var yn, _ref;
      e.preventDefault();
      if ((_ref = $(this).parents("div.input-group").find("input").val()) === "root" || _ref === "admin") {
        yn = confirm("Are you sure you want to remove this group? Doing so could be dangerous");
        if (yn) {
          $(this).parents("div.input-group").next().remove();
          return $(this).parents("div.input-group").remove();
        }
      } else {
        $(this).parents("div.input-group").next().remove();
        return $(this).parents("div.input-group").remove();
      }
    });
  });

}).call(this);