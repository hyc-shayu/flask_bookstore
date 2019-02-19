$(function () {
    $("li a").click(function () {
        let url = $(this).data('href');
        $("div.main").load(url);
    });

});
