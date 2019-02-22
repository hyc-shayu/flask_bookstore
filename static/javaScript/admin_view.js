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
            // var button = $(event.relatedTarget) // Button that triggered the modal
            // var recipient = button.data('whatever') // Extract info from data-* attributes
            // // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
            // // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
            // var modal = $(this)
            // modal.find('.modal-title').text('New message to ' + recipient)
            // modal.find('.modal-body input').val(recipient)
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

    //管理员点开图书列表
    $("div.main-div").one("click", 'a.open-list' ,function () {
        let sel = $(this).attr('href');
        let panel_body = $(sel).find('div:first');
        let url = $(this).data('url');
        append_ajax(panel_body,url)
    });
});

//ajax请求
function append_ajax(panel_body, s_url,page) {
    let url = s_url;
    if(page)
        url = s_url+'_'+page;
    $.ajax({
        type:'POST',
        url:url,
        dataType:'html',
        success:function (callback_data) {
            $(panel_body).html(callback_data);
            //append_content(panel_body,books);
        },
        error:function () {
            alert('发生一个错误');
        }
    })

};

//添加内容
function append_content(panel_body,json_data) {
    let obj = JSON.parse(json_data);
    let books = obj.paginate;
    $(panel_body).append()

}

//添加分页
function add_paginate(obj, currentPage, totalPages, url) {
    $(obj).append()
    $(obj).bootstrapPaginator({
        currentPage: currentPage,//当前的请求页面。
        totalPages: totalPages,//一共多少页。
        size: "normal",//应该是页眉的大小。
        bootstrapMajorVersion: 3,//bootstrap的版本要求。
        alignment: "right",
        numberOfPages: 5,//一页列出多少数据。
        itemTexts: function (type, page, current) {//如下的代码是将页眉显示的中文显示我们自定义的中文。
            switch (type) {
                case "first":
                    return "首页";
                case "prev":
                    return "上一页";
                case "next":
                    return "下一页";
                case "last":
                    return "末页";
                case "page":
                    return page;
            }
        },
        onPageClicked: function (event, originalEvent, type, page) {//给每个页眉绑定一个事件，其实就是ajax请求，其中page变量为当前点击的页上的数字。
            $.ajax({
                url: '/task_list_page/',
                type: 'POST',
                data: {'page': page, 'count': 12},
                dataType: 'JSON',
                success: function (callback) {
                    $('tbody').empty();
                    var page_count = callback.page_count;
                    var page_cont = callback.page_content;
                    $('tbody').append(page_cont);
                    $('#last_page').text(page_count)
                }
            })
        }
    });
}