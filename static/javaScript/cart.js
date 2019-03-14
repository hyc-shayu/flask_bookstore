$(function () {
    $(".spinner-div").inputCounter({
        settings: {

            // check the valus is within the min and max values
            checkValue: true,

        }
    });

    let isSave;
    //页面关闭时调用
    // $(window).on('unload', function () {
    //     if(!isSave)
    //         storeChange();
    // });

    //页面刷新时调用
    $(window).on('beforeunload', function (event) {
        storeChange();
        isSave = true;
    });

    //购物车全选
    $("#btn_check_all").off('click').on('click', function () {
        let isCheck = false;
        for (let i = 0; i < $("input[type='checkbox']").length; i++) {
            if (!$("input[type='checkbox']").eq(i).is(':checked')) {
                isCheck = true;
                break;
            }
        }
        for (let i = 0; i < $("input[type='checkbox']").length; i++) {
            $("input[type='checkbox']").eq(i).prop('checked', isCheck);
        }
    });

    //监听数值框变化 价格变化
    $('input.input_quantity').on('input propertychange',function () {
        let price = $(this).data('price');
        let quantity = $(this).val();
        let max_q = $(this).data('max');
        if(quantity > max_q)
            quantity = max_q;
        else if(quantity <= 0)
            quantity = 1;
        $(this).parents('td:first').next().find('input:first').val(parseFloat(price*quantity).toFixed(1));
    });

    //删除按钮
    $('.a_del_cart_item').on('click',function () {
        storeChange();
    });

    //点击购买按钮
    $('#btn_buy').on('click',function () {
        storeChange();
        let item_list = new Array();
        for (let i = 0,input = $("input[type='checkbox']"); i < input.length; i++) {
            if (input.eq(i).is(':checked'))
                item_list.push(input.eq(i).parents('tr:first').data('item_id'));
        }
        let recipient_id = $('#sel_address').val();
        setTimeout(function () {
            $.ajax({
                type: 'POST',
                url: '/create_order',
                contentType: 'application/json',
                dataType: 'html',
                data: JSON.stringify({item_list: item_list, recipient_id: recipient_id}),
                success: function (data) {
                    $('div.modal-pay:first').html(data);
                }
            })
        },500)
    });

    //支付 关闭 跳转到订单
    $('#div_modal').on('click', 'button', function () {
        window.location.href='/orders';
    });

    //订单支付 提交表单
    $('#div_modal').on('click','#inp_submit',function () {
        $('#pay_form').submit();
    })
});


//保存购物车
function storeChange() {


    let items = {};
    for (let i = 0,input=$("input.input_quantity"); i < input.length; i++) {
        let item_id = input.eq(i).data('item_id');
        let quantity = input.eq(i).val();
        items[item_id] = quantity;
    }

    $.ajax({
        type: "POST",
        contentType:"application/json",
        data: JSON.stringify(items),
        url: '/save_cart'
    });
}