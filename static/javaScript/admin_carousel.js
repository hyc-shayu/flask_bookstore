$(function () {
    //删除图片
    $('.carousel-del').off('click').on('click',function () {
        let url = $(this).data('url');
        $.ajax({
            url:url,
            type:'POST',
            success:function () {
                window.location.reload();
            }
        })
    });

    //获取目标元素位置
    function getXAndY(obj) {
        //获取元素在body中的绝对位置
        var x = obj.offset().left;
        var y = obj.offset().top;
        return {x: x, y: y};
    }

    //移动tr
    function move_tr(tr1,tr2,move_direction){
        if(move_direction == 'up'){
            tr1.insertBefore(tr2);
        }
        else
            tr1.insertAfter(tr2);
    }

    //上移
    $('.move-up').off('click').on('click', function () {
        let parent = $(this).parents('tr:first');
        let parent_pre = parent.prev();
        if (parent_pre.length>0){
            let old_sort = parent.data('sort');
            parent.data('sort',parent_pre.data('sort'));
            parent_pre.data('sort',old_sort);
            move_tr(parent,parent_pre,'up');
        }
    });
    //下移
    $('.move-down').off('click').on('click', function () {
        let parent = $(this).parents('tr:first');
        let parent_next = parent.next();
        if (parent_next.length>0){
            let old_sort = parent.data('sort');
            parent.data('sort',parent_next.data('sort'));
            parent_next.data('sort',old_sort);
            move_tr(parent,parent_next,'down');
        }
    });

    //保存按钮
    $('#save-sort').on('click', function () {
        let crs = {};
        let url = $(this).data('url');
        $('.opt-carousel-td').each(function () {
            let c_id = $(this).data('id');
            let sort = $(this).data('sort');
            crs[c_id] = sort;
        });

        $.ajax({
            type:"POST",
            url:url,
            contentType:"application/json",
            data: JSON.stringify({crs:crs}),
            success:function () {
                window.location.reload();
            }
        });
    });
});