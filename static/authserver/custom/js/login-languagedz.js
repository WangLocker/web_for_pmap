(function () {
    var language = navigator.language;
    var value = getCookie("org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE");
    if (window.location.hash) {
        var url = window.location.href;
        url = url.substr(0,url.indexOf("#")) + encodeURIComponent(window.location.hash);
        window.location.href = url;
    }
    if (typeof(value) == "undefined" ){
        if (language.indexOf("en") != -1){
            setCookie("org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE","en");
            $("#languages span").text('中文');
            $(".language_en").show();
            $(".jqmdl").text('Remember me');
            $(".zhdlyhm").attr("placeholder","user name");
            $(".zhdlmm").attr("placeholder","Password");
            $(".dtdlsjh").attr("placeholder","Phone number");
            $(".register_acc").attr("placeholder","you will use this as the account to login");
            $(".register_pwd").attr("placeholder","set your password");
            $(".register_conf_pwd").attr("placeholder","confirm your password");
            $(".register_email").attr("placeholder","provide your email for dynamic code login");
            $(".register_gender").attr("placeholder","more information can enable us to provide better service");
            $(".register_cv").attr("placeholder","more information can enable us to provide better service");

        }else {
            setCookie("org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE","zh_CN");
            $("#languages span").text('English');
            $(".language_zh").show();
        }
        var protocol = window.location.protocol;
        if (protocol == 'https:') {
            window.location.reload();
        }else if (secure == 'false'){
            window.location.reload();
        }
    }else if (value == "en" || value == "en_US"){
        //document.getElementById("language").value = "en";
        $("#languages span").text('中文');
        $(".language_en").show();
        $(".jqmdl").text('Remember me');
        $(".zhdlyhm").attr("placeholder","User name");
        $(".zhdlmm").attr("placeholder","Password");
        $(".dtdlsjh").attr("placeholder","Email");
        $(".register_acc").attr("placeholder","you will use this as the account to login");
        $(".register_pwd").attr("placeholder","set your password");
        $(".register_conf_pwd").attr("placeholder","confirm your password");
        $(".register_email").attr("placeholder","provide your email for dynamic code login");
        $(".register_gender").attr("placeholder","more information can enable us to provide better service");
        $(".register_cv").attr("placeholder","more information can enable us to provide better service");
    }else if(value == "zh_CN") {
        //document.getElementById("language").value = "zh_CN";
        $("#languages span").text('English');
        $(".language_zh").show();
    }
})();
$("#languages").click(function() {
    var value = getCookie("org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE");
    if (value && value=='en') {
        setCookie("org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE","zh_CN");
    } else {
        setCookie("org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE","en");
    }
    window.location.reload();
})
function changeLanguage(){
    var value = document.getElementById("language").value;
    if (value != "en" && value != "en_US" && value != "zh_CN"){
        value = "zh_CN";
    }
    setCookie("org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE",value);
    window.location.reload();
}

function setCookie(_3a,_3b){
    var secure = window.location.protocol;
    if (secure == 'https:') {
        document.cookie=_3a+"="+escape(_3b)+";path=/"+";secure;expires="+(new Date(2099,12,31)).toGMTString();
    }else {
        document.cookie=_3a+"="+escape(_3b)+";path=/"+";expires="+(new Date(2099,12,31)).toGMTString();
    }
}

function getCookie(cookie_name) {
    var allcookies = document.cookie;
    var cookie_pos = allcookies.indexOf(cookie_name);
    if (cookie_pos != -1) {
        cookie_pos += cookie_name.length + 1;
        var cookie_end = allcookies.indexOf(";", cookie_pos);
        if (cookie_end == -1) {
            cookie_end = allcookies.length;
        }
        var value = unescape(allcookies.substring(cookie_pos, cookie_end));
    }
    return value;
}
