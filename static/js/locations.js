$("#environment").change(function() {
    $.get(
        "/tools/get_locations",
        {env_id: $("#environment").val()},
        function(data) {
            $("#location").empty();
            for (let i = 0; i < data.length; i++) {
                let location = data[i];
                let $option = $("<option></option>");
                $option.val(location.loc_id);
                $option.text(location.loc_full_name);
                $option.appendTo($("#location"));
            }
        }
    );
})