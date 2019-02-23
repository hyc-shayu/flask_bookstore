
$(function () {
    //动态生成的标签没有回调函数，用原来的父标签来获取点击事件
    //局部刷新 侧边列表
    $("div.main-div").off('click',".aj a").on("click", ".aj a", function () {
        $(this).parent().siblings().children().removeClass("active");
        $(this).addClass('active');
        let url = $(this).data('href');
        if(url)
            $("div.main").load(url);
        $('html ,body').animate({scrollTop: 0}, 500);

    });

    //url 目标div

    // 图书管理 图书列表 点击分页事件
    $("div.main-div").off('click','ul.pagination a').on('click',"ul.pagination a",function () {
       let url = $(this).data('url');
       $(this).parents("div.pagination-fill-div:first").load(url);
    });


});

