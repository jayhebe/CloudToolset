$("#copy").click(function() {
    $("#random_password").select()
    document.execCommand("Copy");

    let $copied = $("#copy")
    $copied.text("Copied")
})