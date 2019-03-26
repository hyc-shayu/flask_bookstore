$(function () {
    $('div.left:first').remove();
    $('div.main:first').css('width', '100%');

    //点击去付款
    $('#btn_to_pay').on('click', function () {
        let order_id = $(this).data('id');
        $.ajax({
            type: 'POST',
            url: '/to_pay',
            contentType: 'application/json',
            dataType: 'html',
            data: JSON.stringify({order_id:order_id}),
            success: function (data) {
                $('div.modal-pay:first').html(data);
            }
        })
    })

    //订单支付 提交表单
    $('#div_modal').on('click','#inp_submit',function () {
        $('#pay_form').submit();
    })
})