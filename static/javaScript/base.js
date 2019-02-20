$(function () {
    //激活<li>标签
    $("li.nav-active").each(function () {
        if($(this).find("a")[0]==window.location.href)
        $(this).addClass("active");
    })
})
