window.onload=function(){
let profile=document.getElementById("user_post")
alert("recieved")
    let xhr=new XMLHttpRequest()
    xhr.open("GET","http://localhost:8001/user_post",false)
    xhr.withCredentials=true
    xhr.send()
   if (xhr.status==200){
    let response=xhr.response
    response=JSON.parse(response)
    let str=""
    for(let row of response){
      str+=`<img src="data:${row["image_type"]};base64,${row["image_url"]}"></img>`
    }
    profile.innerHTML=str
    
   }

}