
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

function add_device_button() {
    var device_id = $("#select").val();
    if (device_id == null)
        return
    var device_name = $("#select").find("option:selected").text();
    console.log(device_id+device_name);
    var old = $("#add_device_list").val();
    console.log(old);
    $("#add_device_list").val(old+device_id+device_name+";");
}

function new_project_button() {
    var project_name = $("#project_name").val();
    var devices_name = $("#add_device_list").val();
    console.log(project_name);
    console.log(devices_name);
    $.ajax({
        url:"/new_project",
        type:"get",
        dataType:"json",
        data:{"project_name":project_name, "devices_name":devices_name},
        success:function (data) {
            console.log("new project success, redirect index.html");
            $.ajax({
                url:"/",
                type:"get",
                dataType:"json",
                data:{"is_exists_project":true}
            })
            
        },
        error:function (data) {
            console.log(data);
        }
    })
}

//function displayTab() {
//    console.log($(this));
//  $(this).tab('show');
//}

//$('#myTab a').click(function () {
//  //e.preventDefault();
//  $(this).tab('show');
//})

$(function () {
    $('#myTab a:last').tab('show');
})

function start() {
    $.ajax({
        url:"/start",
        type:"GET",
    })
}

function end() {
    $.ajax({
        url:"/end",
        type:"GET",
    })
}

function reloadView() {
    $.ajax({
        url:"/reload",
        type:"POST",
        async:true,
        success:function(data) {
            /* data example:
             * {'project_name': u'Slina', 'devices': [{'id': u'001', 'spots': [{'ratio': u'0.1', 'name': u'A\u76f8\u7535\u538b', 'command': u'03', 'id': 2, 'unit': u'V', 'cmd_param': u'0000'}, {'ratio': u'1', 'name': u'\u5f00\u5173\u673a\u72b6\u6001', 'command': u'03', 'id': 3, 'unit': '-', 'cmd_param': u'0001'}], 'name': u'\u4f0a\u987fUPS 5000'}]}
             */
            var devices = data['devices'];
            var records = ['value', 'status'];
            for (i=0; i<devices.length; i++){
                var device = devices[i];
                var spots = device['spots'];
                for (j=0; j<spots.length; j++){
                    var spot = spots[j];
                    for (n=0; n<records.length; n++){
                        var record = records[n];
                        var id = device['id']+"_"+spot['id']+"_"+record;
                        $("#"+id).text(spot[record]);
                    }
                }
            }
        },
        error: function (XMLHttpRequest, txtStatus, errorThrown)
        {
            // alert(XMLHttpRequest + "<br>" + txtStatus + "<br>" + errorThrown);
            clearInterval(int_var);
        }
    });
}

var int_var = setInterval("reloadView()", 5000);

$().ready(function(){

    //////发送请求 请求数据 放到页面
    $(".create_project .button").on("click",function () {
        var device_id = $("#select").val();
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
