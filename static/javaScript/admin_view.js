function showAtRight(url) {
    // $.ajax({
    //     type: "GET",
    //     url: url,
    //     dataType: "html",
    //     success: function (data) {//返回数据根据结果进行相应的处理
    //         $("#content").html(data);
    //     },
    //     error: function () {
    //         $("#content").load("获取数据失败！");
    //     }
    // });
    $('#content').load(url);
}

$(function () {

    let url,target_id;
    //传什么数据给后台
    $('tbody th a').click(function () {
        url = $(this).attr('href');
    });
    $('#exampleModal').on('show.bs.modal', function (event) {
        $(this).load(url);
        // var button = $(event.relatedTarget) // Button that triggered the modal
        // var recipient = button.data('whatever') // Extract info from data-* attributes
        // // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        // var modal = $(this)
        // modal.find('.modal-title').text('New message to ' + recipient)
        // modal.find('.modal-body input').val(recipient)
    })

    $(".userMenu").on("click", "li", function () {
        let sId = "#" + $(this).data("id");  //获取data-id的值
        window.location.hash = sId;  //设置锚点
        loadInner(sId);
    });

    function loadInner(sId) {
        let pathn, i;
        switch (sId) {
            case "#center":
                pathn = "/admin/test1/";
                i = 0;
                break;
            case "#account":
                pathn = "/admin/test/";
                i = 1;
                break;
            case "#trade":
                pathn = "/admin/test1/";
                i = 2;
                break;
            case "#info":
                pathn = "/admin/test/";
                i = 3;
                break;
            default:
                pathn = "/admin/test1/";
                i = 0;
                break;
        }
        $("#content").load(pathn); //加载相对应的内容
        //$(".userMenu li").eq(i).addClass("current").siblings().removeClass("current"); //当前列表高亮
    }

    let sId = window.location.hash;
    loadInner(sId);
})