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
    $(".userMenu").on("click", "li", function(){
        let sId = "#" + $(this).data("id");  //获取data-id的值
        window.location.hash = sId;  //设置锚点
        alert(sId);
        loadInner(sId);
    });
    function loadInner(sId){
        let pathn, i;
        switch(sId){
            case "#center": pathn = "/admin/test1"; i = 0; break;
　　　　　　　case "#account": pathn = "/admin/test"; i = 1; break;
            case "#trade": pathn = "/admin/test1"; i = 2; break;
            case "#info": pathn = "/admin/test"; i = 3; break;
　　　　　　  default: pathn = "/admin/test1"; i = 0; break;
        }
        $("#content").load(pathn); //加载相对应的内容
        //$(".userMenu li").eq(i).addClass("current").siblings().removeClass("current"); //当前列表高亮
    }
    let sId = window.location.hash;
    loadInner(sId);
    alert(sId);
})