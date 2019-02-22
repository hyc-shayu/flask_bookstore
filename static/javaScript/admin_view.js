$(function () {

    // 显示 订单详情 模态框
    $('tbody tr th').off('click', 'a').on('click', 'a', function () {
        let url = $(this).data('url');
        let book_id = $(this).data('book_id');
        let comment_id = $(this).data('comment_id');
        $('#exampleModal').off('show.bs.modal').on('show.bs.modal', function () {
            if (url) {
                if (comment_id) {
                    $.ajax({
                        type: "POST",
                        url: url,
                        data: {
                            book_id: book_id,
                            comment_id: comment_id
                        },
                        dataType: 'html',
                        success: function (data) {//返回数据根据结果进行相应的处理
                            $("#exampleModal").html(data);
                        },
                        error: function () {
                            alert('error');
                        }
                    });
                } else $(this).load(url);
            }
        });
    });

    // 管理员 点击评论|图书 显示 图书详情 定位到该评论 模态框
    $("div.main-div").off('click', '.show_modal a').on("click", ".show_modal a", function () {
        let url = $(this).data('url');
        let book_id = $(this).data("book_id");
        let comment_id = $(this).data('comment_id');
        let data = {
            book_id: book_id,
            comment_id: comment_id
        };
        //显示模态框时，请求对应路由 获取对应数据
        $('.modal-book-detail:first').off('show.bs.modal').on('show.bs.modal', function () {
            if (url)
                $.ajax({
                    type: "POST",
                    url: url,
                    data: data,
                    dataType: 'html',
                    success: function (data) {//返回数据根据结果进行相应的处理
                        $(".modal-book-detail:first").html(data);
                    },
                    error: function () {
                        alert('error');
                    }
                });
        });
        // 隐藏模态框时，刷新原来的div
        $('.modal-book-detail:first').off('hidden.bs.modal').on('hidden.bs.modal', function () {
            let url = $("div.main-div .aj .active:first").data('href');
            if (url)
                $("div.main").load(url);
        });
    });

    //管理员修改增加图书分类 - 模态框
    $("div.main").off('click', '.add_update_classify_a').on('click', '.add_update_classify_a', function () {
        let url = $(this).data('url');
        let classify_id = $(this).data("classify_id");
        let sel = $(this).data("target");
        $(sel).off('show.bs.modal').on('show.bs.modal', function () {
            $(this).find('.classify_sure_btn:first').off('click').on('click', function () {
                $.ajax({
                    type: 'POST',
                    url: url,
                    dataType: 'html',
                    success: function (callback_data) {
                        $(panel_body).html(callback_data);
                        //append_content(panel_body,books);
                    },
                    error: function () {
                        alert('发生一个错误');
                    }
                })
            });
        });
    })

    //管理员点开图书列表
    $("div.main-div").off("click", 'a.open-list').on("click", 'a.open-list', function () {
        let sel = $(this).attr('href');
        let panel_body = $(sel).find('div:first');
        let url = $(this).data('url');
        append_ajax(panel_body, url);
    });
});

//ajax请求 刷新下拉列表？
function append_ajax(panel_body, s_url, page) {
    let url = s_url;
    if (page)
        url = s_url + '_' + page;
    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'html',
        success: function (callback_data) {
            $(panel_body).html(callback_data);
            //append_content(panel_body,books);
        },
        error: function () {
            alert('发生一个错误');
        }
    })

};
