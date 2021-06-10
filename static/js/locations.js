$("#environment").change(function() {
    $.get(
        "/azure/get_locations",
        {env_id: $("#environment").val()},
        function(data) {
            console.log(data);
            $("#location").empty();
            for (var i = 0; i < data.length; i++) {
                let location = data[i];
                let $option = $("<option></option>");
                $option.val(location.loc_id);
                $option.text(location.loc_full_name);
                $option.appendTo($("#location"));
            }
        }
    );
})