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

    //点击添加到购物车
    $('body').off('click', '.a_add_to_cart').on('click', '.a_add_to_cart', function () {
        let origin_href = $(this).prop('href');
        let scrollPos;
        if (typeof window.pageYOffset != 'undefined') {
            scrollPos = window.pageYOffset;
        } else if (typeof document.compatMode != 'undefined' &&
            document.compatMode != 'BackCompat') {
            scrollPos = document.documentElement.scrollTop;
        } else if (typeof document.body != 'undefined') {
            scrollPos = document.body.scrollTop;
        }
        $(this).prop('href', origin_href + '&scrollPos='+scrollPos);
    });

    // 管理员 点击评论|图书 显示 图书详情 定位到该评论 模态框
    $("body:first").off('click', '.show_modal a').on("click", ".show_modal a", function () {
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
                        if(data)
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
            if (url && url.indexOf('book')==-1)
                $("div.main").load(url);
        });
    });

    //管理员修改增加删除图书分类 删除图书 按钮 - 模态框
    $("div.main").off('click', '.opt_classify_del_book_a').on('click', '.opt_classify_del_book_a', function () {
        let url = $(this).data('url');
        let sel = $(this).data("target");
        $(sel).off('show.bs.modal').on('show.bs.modal', function () {
            $(this).find('.classify_sure_btn:first').off('click').on('click', function () {
                let name = $(sel).find('#message-text').val();
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {name: name},
                    success: function () {
                        reflash_main_div();
                    },
                    error: function () {
                        alert('发生一个错误');
                    }
                })
            });
        });
    });

    //管理员修改添加图书 模态框
    $("div.main").off('click', '.opt_book_a').on('click', '.opt_book_a', function () {
        let url = $(this).data('url');
        let book_id = $(this).data('book_id');
        let sel = $(this).data('target');
        $(sel).off('show.bs.modal').on('show.bs.modal', function () {
            $.ajax({
                async: false,
                type: "POST",
                url: url,
                data: {book_id: book_id},
                dataType: 'html',
                success: function (data) {
                    $(sel).html(data);
                },
                error: function () {
                    alert('发生一个错误');
                }
            })
            $(this).find('.book_sure_btn:first').off('click').on('click', function () {

                $(sel).find('form:first').submit();

                /*let book_classify_id = $(sel).find('select:first').val();
                let book_name = $(sel).find('#book-name').val();
                let quantity = $(sel).find('#book-quantity').val();
                let price = $(sel).find('#book-price').val();
                let author = $(sel).find('#book-author').val();
                let publish_time = $(sel).find('#book-publish_time').val();
                let press = $(sel).find('#book-press').val();
                let sales_volume = $(sel).find('#book-sales_volume').val();
                let introduction = $(sel).find('#book-introduction').val();
                let image = $(sel).find('#book-image').val();
                $.ajax({
                    type: "POST",
                    url: url,
                    contentType:'application/json',
                    data: JSON.stringify({book_classify_id: book_classify_id, book_name: book_name, quantity: quantity,
                        price: price, author:author, publish_time:publish_time, press:press, sales_volume:sales_volume,
                        introduction:introduction, image:image}),
                    success: function () {
                        reflash_main_div();
                    }
                })*/
            })
        });
    });

    //管理员点开图书列表
    $("div.main-div").off("click", 'a.open-list').on("click", 'a.open-list', function () {
        let sel = $(this).attr('href');
        let panel_body = $(sel).find('div:first');
        let url = $(this).data('url');
        append_ajax(panel_body, url);
    });

    //管理员修改订单信息
    $("#alter_input").off('click').on('click',function () {
        let fieldset = $('#fieldset_recipient');
        if(fieldset.attr('disabled'))
            fieldset.removeAttr('disabled');
        else
            fieldset.attr('disabled', true);
    });
});

//刷新div.main
function reflash_main_div() {
    let url = $('div.left .aj .active:first').data('href');
    if (url)
        $('div.main').load(url);
    else
        window.location.reload();
}

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
