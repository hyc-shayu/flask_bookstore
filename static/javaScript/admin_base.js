$(function () {
    // let sId = window.location.hash;
    // if (sId != '') {
    //     sId = sId.substr(1);
    //     loadInner(sId);
    // }

    //动态生成的标签没有回调函数，用原来的父标签来获取点击事件
    $("div.main-div").on("click", ".aj a", function () {
        let id = $(this).data('id');
        //alert(id);
        window.location.hash = '#' + id;
        loadInner(id);
    });



    function loadInner(id) {
        let url;
        if (id != '') {
            url = $("a[data-id*='" + id + "']").data('href');
        }
        if (url) {
            $("div.main").load(url);
            alert(url);
            //$("div.main").trigger("create");
        }
    }
});

// let sId = window.location.hash;
// if (sId != '') {
//     sId = sId.substr(1);
// }