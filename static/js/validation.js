function validate_email(str_email) {
    let reg_email = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/
    return reg_email.test(str_email);
}

function validate_password(str_password) {
    let reg_password = /^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^a-zA-Z0-9]).{8,32}$/
    return reg_password.test(str_password);
}

function pass_validation(parent_div, next_span) {
    parent_div.attr("class", "form-group has-success");
    next_span.text("");
}

function not_pass_valication(parent_div, next_span, msg) {
    parent_div.attr("class", "form-group has-error");
    next_span.css({"color": "#ff0011", "font-size": "12px"});
    next_span.text(msg);
}

$("#email").blur(function() {
    let email = $(this).val();
    let email_div = $(this).parent("div");
    let email_span = $(this).next("span");
    let msg;
    if (validate_email(email)) {
        $.get("/user/check_email", {email: email}, function (data) {
            if (data.exists === 1) {
                msg = "The email is already in use.";
                not_pass_valication(email_div, email_span, msg);
            } else {
                pass_validation(email_div, email_span);
            }
        })
    } else {
        msg = "The email format is incorrect."
        not_pass_valication(email_div, email_span, msg);
    }
})

$("#password").blur(function() {
    let password = $(this).val();
    let password_div = $(this).parent("div");
    let password_span = $(this).next("span");
    if (validate_password(password)) {
        pass_validation(password_div, password_span);
    } else {
        msg = "The password must contain upper and lower case letters, digits and special character, 8-32 in length.";
        not_pass_valication(password_div, password_span, msg);
    }
})

$("#cfmpassword").blur(function() {
    let password = $("#password").val();
    let cfmpassword = $(this).val();
    let password_div = $(this).parent("div");
    let password_span = $(this).next("span");
    let msg;
    if (cfmpassword !== "" && password === cfmpassword) {
        pass_validation(password_div, password_span);
    } else {
        msg = "The password does not match.";
        not_pass_valication(password_div, password_span, msg);
    }
})