$(function () {

    // 显示 订单详情 模态框
    $('tbody tr th a').click(function () {
        let url = $(this).attr('href');
        $('#exampleModal').on('show.bs.modal', function () {
            $(this).load(url);
            // var button = $(event.relatedTarget) // Button that triggered the modal
            // var recipient = button.data('whatever') // Extract info from data-* attributes
            // // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
            // // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
            // var modal = $(this)
            // modal.find('.modal-title').text('New message to ' + recipient)
            // modal.find('.modal-body input').val(recipient)
        });
    });

    // 管理员 点击评论 显示 图书详情 定位到该评论 模态框
    $("div.main-div").on("click", "blockquote a", function () {
        let url = $(this).data('url');
        let book_id = $(this).data("book_id");
        let comment_id = $(this).data('comment_id');
        $('#modal-comment-book').on('show.bs.modal', function () {
            $.ajax({
                type: "POST",
                url: url,
                data:{
                    book_id:book_id,
                    comment_id:comment_id
                },
                dataType:'html',
                success: function (data) {//返回数据根据结果进行相应的处理
                    $("#modal-comment-book").html(data);
                },
                error: function () {
                    alert('error');
                }
            });
        });
    });
});