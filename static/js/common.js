;
//定义全局ajax配置
(function(){
    $.ajaxSetup({
        complete: function(xhr, status){
            if(xhr.responseJSON && xhr.responseJSON.code!=0){
                alert(xhr.responseJSON.msg)
            }
        },
        dataFilter: function(data){//在过滤器里对返回的数据进行处理，如果
            if(data && JSON.parse(data).code!=0){
                alert(JSON.parse(data).msg)
                return data.msg;
            }
            return data;
        },
       
        beforeSend: function(xhr){
            var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    })
    
})()