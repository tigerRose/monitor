
//动态绑定下拉框项  
function addItems() {  
    $.ajax({  
        url: "get_item",
        type: "post",  
        dataType: "json",  
        contentType: "application/json",  
        traditional: true,  
        success: function (data) {  
            var jsonObj =data;
            var optionstring = "";  
            for (var j = 0; j < jsonObj.length; j++) {  
                console.log(j);
                console.log(jsonObj[j].id);
                optionstring += "<option value=\"" + jsonObj[j].id + "\" >" + jsonObj[j].name + "</option>";  
            }  
            $("#select").append("<option value='请选择'>请选择...</option> "+optionstring);  
        },  
        error: function (msg) {  
            alert("出错了！");  
        }  
    });            
};  

$().ready(function(){
    //////发送请求 请求数据 放到页面
    $(".create_project .button").on("click",function () {
        var device_id = $("#select").val()
        $.ajax({
            url:"/create_project",
            type:"GET",
            dataType:"json",
            data:{"device_id":device_id},
            success:function (data) {
                $(".create_project .button").html("点击刷新设备");
                $(".create_project .device").find("span").eq(0).html("＜");
                $(".create_project .device").find("span").eq(1).html(data.device["name"]);
                $(".create_project .device").css({"background":"#6E6E6E"});
                $(".create_project .button").on("click",function () {
                    if($(".create_project .button").html()=="点击刷新设备"){
                        $(".create_project .device").find("span").eq(0).html("＜");
                        $(".create_project .spots ul").hide();
                    }
                });
                //判断两个状态
                var n=1;
                $(".create_project .device").on("click",function () {
                    if(n == 0){
                        $(".create_project .device").find("span").eq(0).html("∨");
                        //添加测点
                        var ul = $("<ul></ul>");
                        $(".create_project .spots ul").remove();
                        $(".create_project .spots").append(ul);
                        for(var i=0;i<data.spots.length;i++){
                            var showData = data.spots[i]["name"];
                            var li = $("<li>"+showData+"</li>");
                            $(".create_project .spots ul").append(li);
                        }
                        n=1
                    }else {
                        $(".create_project .device").find("span").eq(0).html("＜");
                        $(".create_project .spots ul").hide();
                        n=0
                    }
                });
            },
            error:function (data) {
                console.log(data);
            }
        })
    });

});
