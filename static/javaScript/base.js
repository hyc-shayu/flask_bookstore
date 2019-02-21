$(function () {
    //激活<li>标签
    $("li.nav-active").each(function () {
        if ($(this).find("a")[0] == window.location.href)
            $(this).addClass("active");
    });

    // 模态框分页 图书详情
    $("div.main-div").off('click', '.ajPage a').on("click", ".ajPage a", function () {
        let url = $(this).data('href');
        let book_id = $(".modal-dialog:first").data('book_id');
        let page = $(this).data('page');
        if (url)
            $.ajax({
                type: "POST",
                url: url,
                data: {book_id: book_id,page:page},
                dataType: 'html',
                success: function (data) {//返回数据根据结果进行相应的处理
                    $(".modal-book-detail:first").html(data);
                    $('.modal-book-detail:first').animate({scrollTop: 0}, 500);
                },
                error: function () {
                    alert('error');
                }
            })
    });

    //回复评论
    $("body").off('click', '.book_detail_dialog #submit_btn').on('click','.book_detail_dialog #submit_btn',function () {
        let url = $(this).data('url');
        let content = $("#comment_content").val();
        let target_id = $(this).data('to_user_id');
        let book_id = $(".book_detail_dialog").data('book_id');
        if(url)
            $.ajax({
                type: 'POST',
                url:url,
                data:{
                    content:content,
                    target_id:target_id,
                    book_id:book_id
                },
                success:function(){
                    let url_refresh = $(".book_detail_dialog:first").data("first_page");
                    $.post(url_refresh,{book_id:book_id},function (data) {
                        $(".modal-book-detail:first").html(data);
                        $('.modal-book-detail:first').animate({scrollTop: 0}, 500);
                    })
                },
                error:function () {
                    alert('发生一个错误');
                }
            })
    });


});
//设置回复目标id
function setTarget(target_user_id,target_user_username) {
    $("#submit_btn").data('to_user_id', target_user_id);
    $("#comment_content").attr('placeholder', '回复 '+target_user_username);
    $('.modal-book-detail:first').animate({scrollTop: $('#comment_content').offset().top}, 500);
}