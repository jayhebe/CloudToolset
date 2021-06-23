$("#environment").change(function() {
    $.get(
        "/tools/get_tenant_id",
        {env_id: $("#environment").val()},
        function(data) {
            console.log(data);
            $("#tenant_id").empty();
            for (var i = 0; i < data.length; i++) {
                let tenant_id = data[i];
                let $option = $("<option></option>");
                $option.val(tenant_id.tenant_id);
                $option.text(tenant_id.tenant_id);
                $option.appendTo($("#tenant_id"));
            }
        }
    );
})