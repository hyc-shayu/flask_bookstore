$(function () {
    //删除图片
    $('.carousel-del').off('click').on('click',function () {
        let url = $(this).data('url');
        $.ajax({
            url:url,
            type:'POST'
        })
    });

    //上移
    $('.move-up').off('click').on('click', function () {
        let parent = $(this).parent('tr:first');
        let parent_pre = parent.prev();
        if (parent_pre){
            let old_sort = parent.data('sort');
            parent.data('sort',parent_pre.data('sort'));
            parent_pre.data('sort',old_sort);
            
        }
    });

    //保存按钮
    $('#save-sort').on('click', function () {
        let carousel = {};
        let url = $(this).data('url');
        $('.opt-carousel-td').each(function () {
            let c_id = $(this).data('id');
            let sort = $(this).data('sort');
            carousel[c_id] = sort;
        });

        $.ajax({
            url:url,
            contentType:"application/json",
            data: JSON.stringify({carousel:carousel}),
            error:function () {
                alert('发生一个错误');
            }
        });
    });
});