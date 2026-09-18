window.onload=function(){

let xhr=new XMLHttpRequest()
    xhr.open("GET","http://localhost:8001/picture",false)

   xhr.withCredentials=true
   xhr.send()
let profile=document.getElementById("profile")
if (xhr.status==200){
    let response=xhr.responseText
response=JSON.parse(response)    
 profile.src="http://localhost:8001/uploads/"+response
    }
    else if(xhr.status==401){
     
        xhr.open("GET","http://localhost:8001/refresh",false)
        xhr.withCredentials=true
        xhr.send()
window.location.reload()
}
else{
    alert("else")
}


show_post()
}


const add_btn=document.getElementById("pic")
if (add_btn==null){
    alert("null")
}
add_btn.addEventListener("change",function(){
    alert("req reaches at js")
    let formdata=new FormData()
    let pic=document.getElementById("pic").files[0]
    formdata.append("pic",pic)

    let xhr=new XMLHttpRequest()
    xhr.withCredentials=true
    xhr.open("POST","http://localhost:8001/post",false)
    xhr.send(formdata)
    

})


function show_post(){
    let xhr=new XMLHttpRequest()
    xhr.open("GET","http://localhost:8001/show_post",false)
    xhr.withCredentials=true
    xhr.send()
   
    let div=document.getElementById("show_post")
    if(xhr.status==200){
        let response=xhr.response
    response=JSON.parse(response)
        let str=""
     for(let i of response){

     str+=`<img src="data:${i["image_type"]};base64,${i["image_url"]}"></img>`
     }
     div.innerHTML=str
    }
    else{
        alert(response)
        alert('h')
    }
}

let profile=document.getElementById("profile")

profile.addEventListener("click",function(){
    window.location.assign("user.html")
})